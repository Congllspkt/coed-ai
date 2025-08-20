The Java Stream API, introduced in Java 8, revolutionized how we process collections of data. It provides a powerful and declarative way to perform operations like filtering, mapping, and reducing. However, certain common patterns, especially those involving stateful, intermediate aggregations or "windowing" operations, were not easily expressed using the existing `map`, `filter`, or even `reduce`/`collect` operations.

This is where **Stream Gatherers**, introduced as a preview feature in **Java 22** and officially released in **Java 24**, come into play. They fill a crucial gap, providing a new intermediate stream operation that allows for highly flexible and stateful transformations of stream elements.

---

# Introduction to Stream Gatherers API (Java 24)

## 1. The Problem Before Gatherers

Before Gatherers, stream operations were primarily categorized as:

*   **Intermediate Operations (Stateless):** Like `map()`, `filter()`, `distinct()`, `sorted()`. These operate on individual elements or a small, local context without maintaining a significant state across multiple elements. They produce another stream.
*   **Terminal Operations (Stateful):** Like `collect()`, `reduce()`, `forEach()`. These consume the stream, performing a final aggregation or action. They produce a result or a side effect, not another stream.

This distinction left a gap for scenarios where you needed:
*   **Stateful intermediate operations:** Operations that remember previous elements or maintain some aggregate state *as the stream flows*, and *still produce another stream*.
*   **Windowing operations:** Grouping elements into fixed-size or sliding "windows" for processing, without terminating the stream.
*   **Pairwise processing:** Operating on adjacent elements.
*   **Scanning/Folding:** Computing running aggregates similar to a `reduce` but emitting intermediate results as a new stream.

For these, developers often had to resort to:
*   Breaking the stream chain, converting to a list, and then processing manually.
*   Using complex `reduce` operations that accumulate state in a `List` and then flatten it, which could be inefficient or non-idiomatic.
*   Leveraging external libraries.

## 2. What is a `Gatherer`?

A `Gatherer<T, A, R>` is a new type of **intermediate stream operation** that takes elements of type `T` from an upstream stream, maintains an internal mutable state of type `A`, processes elements, and emits elements of type `R` to a downstream stream.

It's essentially a highly flexible, stateful, and potentially parallelizable transformer. It bridges the gap between the stateless `map`/`filter` and the terminal `collect` operations.

You use it via the new `Stream.gather(Gatherer)` method.

## 3. How a `Gatherer` Works (The Lifecycle)

A `Gatherer` is defined by four main components, similar to a `Collector` but designed for intermediate processing:

1.  **`initializer()`: `Supplier<A>`**
    *   Provides the initial mutable state `A` for the gathering operation. This state will accumulate information as elements are processed.
    *   Called once for each gathering task (or once if not parallel).

2.  **`integrator()`: `BiConsumer<A, T>` or `Gatherer.Integrator<A, T, R>`**
    *   This is the core logic. It takes the current accumulated state `A` and the current input element `T` from the upstream stream.
    *   It updates the state `A` based on the input element.
    *   Crucially, unlike a `Collector`, an `integrator` can also **emit zero, one, or multiple elements of type `R`** to the downstream stream. This is what makes it an *intermediate* operation.

3.  **`combiner()`: `BinaryOperator<A>`**
    *   Used in parallel streams. If the stream is processed in parallel, multiple independent states (`A`) might be created. The `combiner` defines how to merge two partial states into one.
    *   If not provided, the gatherer implies it cannot be efficiently parallelized (or that its state does not need combining, which is rare for meaningful state).

4.  **`finisher()`: `Function<A, R>` or `Gatherer.Finisher<A, R>`**
    *   This optional function is called once at the end of the gathering operation for a given state `A`.
    *   It takes the final accumulated state `A` and performs any necessary transformation or cleanup before emitting final elements of type `R` to the downstream stream. For example, if the state is a partial buffer, the finisher might emit the remaining elements.

### Analogy: A Production Line Worker

Imagine a worker on a production line (the stream).

*   **`initializer`**: The worker gets their initial empty toolbox (the initial state).
*   **`integrator`**: For each incoming product (input element), the worker takes it, uses their tools (updates state), and then decides what to send down the line next (emits 0-N output elements). Maybe they combine it with something from their toolbox, or store it in their toolbox for later.
*   **`combiner`**: If there are multiple workers on parallel lines, this defines how their toolboxes (states) are merged when their lines converge.
*   **`finisher`**: Once all products have passed, the worker might perform a final task with whatever is left in their toolbox (final state) and send those last results down the line.

## 4. Creating a Custom `Gatherer`

You can create custom `Gatherer` instances using the static factory methods on the `Gatherer` interface, primarily `Gatherer.of(...)`.

Let's create a custom `Gatherer` that buffers elements into lists of a fixed size. This is similar to `Gatherers.windowFixed()`, but we'll implement it manually to understand the components.

**Scenario:** Buffer stream elements into lists of a specific size. If the stream doesn't end cleanly, the last partial buffer is also emitted.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.function.BiConsumer;
import java.util.function.Function;
import java.util.function.Supplier;
import java.util.stream.Gatherer;
import java.util.stream.Stream;

public class CustomGathererExample {

    /**
     * A custom Gatherer that buffers elements into lists of a fixed size.
     * Emits the last partial buffer if the stream doesn't divide evenly.
     *
     * @param <T> The type of elements in the stream.
     * @param batchSize The desired size of each buffer.
     * @return A Gatherer that transforms a stream of T into a stream of List<T>.
     */
    public static <T> Gatherer<T, List<T>, List<T>> bufferElements(int batchSize) {
        if (batchSize <= 0) {
            throw new IllegalArgumentException("Batch size must be positive");
        }

        // 1. Initializer: Provides the initial state (an empty mutable list for the current buffer)
        Supplier<List<T>> initializer = ArrayList::new;

        // 2. Integrator: Processes each incoming element
        Gatherer.Integrator<List<T>, T, List<T>> integrator = (state, element, downstream) -> {
            state.add(element); // Add element to the current buffer (state)
            if (state.size() == batchSize) {
                downstream.push(state); // If buffer is full, emit it
                return new ArrayList<>(); // Reset state for the next buffer
            }
            return state; // Keep current state, not yet full
        };

        // 3. Combiner: How to combine two partial states in parallel processing (simple for this example)
        // For buffering, parallel combination is tricky. For simplicity, we'll assume sequential or a
        // basic combiner that appends, which might not be ideal for all parallel buffering scenarios.
        // A more robust parallel buffer would need careful thought about boundary elements.
        // For this example, we'll use one that works if elements are distributed and then combined.
        Function<List<T>, List<T>> finisher = state -> {
            if (!state.isEmpty()) {
                // If there are remaining elements in the buffer when the stream ends,
                // emit the partial buffer.
                return state;
            }
            return null; // Don't emit anything if the buffer is empty
        };

        return Gatherer.of(initializer, integrator, finisher, Gatherer.Combiner.of((left, right) -> {
            // This combiner is simplistic. For true parallel buffering, you'd need
            // more complex logic to handle where batches split.
            // For now, it just appends the right buffer to the left.
            left.addAll(right);
            return left;
        }));
    }

    public static void main(String[] args) {
        // Example 1: Evenly divisible stream
        System.out.println("--- Evenly Divisible Stream (Batch Size 3) ---");
        List<Integer> numbers1 = List.of(1, 2, 3, 4, 5, 6);
        System.out.println("Input: " + numbers1);

        List<List<Integer>> result1 = numbers1.stream()
                .gather(bufferElements(3))
                .toList();

        System.out.println("Output: " + result1);
        // Expected Output: [[1, 2, 3], [4, 5, 6]]

        // Example 2: Stream with a partial last batch
        System.out.println("\n--- Partial Last Batch (Batch Size 3) ---");
        List<Integer> numbers2 = List.of(10, 20, 30, 40, 50);
        System.out.println("Input: " + numbers2);

        List<List<Integer>> result2 = numbers2.stream()
                .gather(bufferElements(3))
                .toList();

        System.out.println("Output: " + result2);
        // Expected Output: [[10, 20, 30], [40, 50]]

        // Example 3: Empty stream
        System.out.println("\n--- Empty Stream (Batch Size 2) ---");
        List<Integer> numbers3 = List.of();
        System.out.println("Input: " + numbers3);

        List<List<Integer>> result3 = numbers3.stream()
                .gather(bufferElements(2))
                .toList();

        System.out.println("Output: " + result3);
        // Expected Output: []

        // Example 4: Single element stream, batch size > 1
        System.out.println("\n--- Single Element Stream (Batch Size 5) ---");
        List<Integer> numbers4 = List.of(99);
        System.out.println("Input: " + numbers4);

        List<List<Integer>> result4 = numbers4.stream()
                .gather(bufferElements(5))
                .toList();

        System.out.println("Output: " + result4);
        // Expected Output: [[99]]
    }
}
```

**Output:**

```
--- Evenly Divisible Stream (Batch Size 3) ---
Input: [1, 2, 3, 4, 5, 6]
Output: [[1, 2, 3], [4, 5, 6]]

--- Partial Last Batch (Batch Size 3) ---
Input: [10, 20, 30, 40, 50]
Output: [[10, 20, 30], [40, 50]]

--- Empty Stream (Batch Size 2) ---
Input: []
Output: []

--- Single Element Stream (Batch Size 5) ---
Input: [99]
Output: [[99]]
```

**Explanation of the Custom `bufferElements` Gatherer:**

*   **`initializer`**: `ArrayList::new` provides an empty `List<T>` as the initial buffer.
*   **`integrator`**:
    *   `state.add(element)`: Adds the current stream element to the buffer.
    *   `if (state.size() == batchSize)`: Checks if the buffer is full.
    *   `downstream.push(state)`: If full, the complete buffer (`state`) is emitted to the downstream stream.
    *   `return new ArrayList<>()`: A *new* empty list is returned as the next state, effectively "resetting" the buffer for the next batch. If `state` was modified and returned, it would continue accumulating indefinitely.
    *   `return state`: If not full, the current (partially filled) `state` is returned to continue accumulating.
*   **`finisher`**:
    *   `if (!state.isEmpty())`: After all elements from the upstream have been processed, this checks if there are any remaining elements in the last buffer (i.e., the stream ended before a full batch was formed).
    *   `return state`: If there are, this partial buffer is emitted.
    *   `return null`: If the buffer is empty (meaning all elements formed full batches or the stream was empty), nothing is emitted.
*   **`combiner`**: The provided `Combiner.of((left, right) -> { left.addAll(right); return left; })` is a placeholder. For `bufferElements`, a truly robust parallel combiner would be very complex, requiring careful handling of stream boundaries and batch alignment. This simple one just appends, which might not maintain batch integrity if batches are split across different threads in a complex way. For `Gatherers` with simple, append-only state (like a running sum), a combiner is more straightforward.

## 5. Built-in `Gatherers`

Java 24 provides several useful pre-built `Gatherers` in the `java.util.stream.Gatherers` class:

### 5.1 `Gatherers.scan()` / `Gatherers.scanConcurrent()`

Applies an accumulator function to elements and returns a stream of intermediate results, effectively a "running aggregate" or "prefix sum".

```java
import java.util.List;
import java.util.stream.Gatherers;
import java.util.stream.Stream;

public class ScanGathererExample {
    public static void main(String[] args) {
        System.out.println("--- Gatherers.scan() ---");

        // Example 1: Running sum
        List<Integer> numbers = List.of(1, 2, 3, 4, 5);
        System.out.println("Input: " + numbers);

        List<Integer> runningSums = numbers.stream()
                .gather(Gatherers.scan(() -> 0, (sum, element) -> sum + element))
                .toList();

        System.out.println("Output: " + runningSums);
        // Expected Output: [1, 3, 6, 10, 15]

        // Example 2: Running concatenation of strings
        List<String> words = List.of("Java", "is", "awesome");
        System.out.println("Input: " + words);

        List<String> concatenatedWords = words.stream()
                .gather(Gatherers.scan(() -> "", (acc, word) -> acc.isEmpty() ? word : acc + " " + word))
                .toList();

        System.out.println("Output: " + concatenatedWords);
        // Expected Output: ["Java", "Java is", "Java is awesome"]
    }
}
```

**Output:**

```
--- Gatherers.scan() ---
Input: [1, 2, 3, 4, 5]
Output: [1, 3, 6, 10, 15]
Input: [Java, is, awesome]
Output: [Java, Java is, Java is awesome]
```

### 5.2 `Gatherers.windowFixed()`

Partitions the stream into fixed-size lists (windows). The last window might be smaller if the stream length is not a multiple of the window size.

```java
import java.util.List;
import java.util.stream.Gatherers;
import java.util.stream.Stream;

public class WindowFixedGathererExample {
    public static void main(String[] args) {
        System.out.println("--- Gatherers.windowFixed() ---");

        // Example 1: Fixed size windows
        List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7);
        System.out.println("Input: " + numbers);

        List<List<Integer>> fixedWindows = numbers.stream()
                .gather(Gatherers.windowFixed(3))
                .toList();

        System.out.println("Output: " + fixedWindows);
        // Expected Output: [[1, 2, 3], [4, 5, 6], [7]]

        // Example 2: Exactly divisible
        List<String> items = List.of("A", "B", "C", "D");
        System.out.println("Input: " + items);

        List<List<String>> fixedStringWindows = items.stream()
                .gather(Gatherers.windowFixed(2))
                .toList();

        System.out.println("Output: " + fixedStringWindows);
        // Expected Output: [[A, B], [C, D]]
    }
}
```

**Output:**

```
--- Gatherers.windowFixed() ---
Input: [1, 2, 3, 4, 5, 6, 7]
Output: [[1, 2, 3], [4, 5, 6], [7]]
Input: [A, B, C, D]
Output: [[A, B], [C, D]]
```

### 5.3 `Gatherers.windowSliding()`

Creates overlapping windows of a specified size, moving by a defined step.

```java
import java.util.List;
import java.util.stream.Gatherers;
import java.util.stream.Stream;

public class WindowSlidingGathererExample {
    public static void main(String[] args) {
        System.out.println("--- Gatherers.windowSliding() ---");

        // Example 1: Sliding window size 3, step 1
        List<Integer> numbers = List.of(1, 2, 3, 4, 5);
        System.out.println("Input: " + numbers);

        List<List<Integer>> slidingWindows = numbers.stream()
                .gather(Gatherers.windowSliding(3, 1))
                .toList();

        System.out.println("Output: " + slidingWindows);
        // Expected Output: [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

        // Example 2: Sliding window size 2, step 2 (non-overlapping, same as windowFixed)
        List<Character> chars = List.of('A', 'B', 'C', 'D', 'E');
        System.out.println("Input: " + chars);

        List<List<Character>> nonOverlappingWindows = chars.stream()
                .gather(Gatherers.windowSliding(2, 2))
                .toList();

        System.out.println("Output: " + nonOverlappingWindows);
        // Expected Output: [[A, B], [C, D], [E]]
    }
}
```

**Output:**

```
--- Gatherers.windowSliding() ---
Input: [1, 2, 3, 4, 5]
Output: [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
Input: [A, B, C, D, E]
Output: [[A, B], [C, D], [E]]
```

### 5.4 `Gatherers.pairwise()`

Transforms a stream of elements into a stream of pairs of adjacent elements.

```java
import java.util.List;
import java.util.stream.Gatherers;
import java.util.stream.Stream;

public class PairwiseGathererExample {
    public static void main(String[] args) {
        System.out.println("--- Gatherers.pairwise() ---");

        List<String> elements = List.of("apple", "banana", "cherry", "date");
        System.out.println("Input: " + elements);

        List<List<String>> pairs = elements.stream()
                .gather(Gatherers.pairwise())
                .toList();

        System.out.println("Output: " + pairs);
        // Expected Output: [[apple, banana], [banana, cherry], [cherry, date]]

        List<Integer> singleElement = List.of(100);
        System.out.println("Input: " + singleElement);
        List<List<Integer>> singlePair = singleElement.stream()
                .gather(Gatherers.pairwise())
                .toList();
        System.out.println("Output: " + singlePair);
        // Expected Output: []
    }
}
```

**Output:**

```
--- Gatherers.pairwise() ---
Input: [apple, banana, cherry, date]
Output: [[apple, banana], [banana, cherry], [cherry, date]]
Input: [100]
Output: []
```

### 5.5 `Gatherers.fold()` / `Gatherers.foldConcurrent()`

Similar to `scan()`, but the accumulator emits only the *final* accumulated value when the stream terminates. It's like a `reduce` operation that returns a single result, but specifically as a `Gatherer` which could theoretically be followed by other stream operations (though typically it's the last).

```java
import java.util.List;
import java.util.stream.Gatherers;
import java.util.stream.Stream;

public class FoldGathererExample {
    public static void main(String[] args) {
        System.out.println("--- Gatherers.fold() ---");

        // Example: Summing all elements, emitting only the final sum
        List<Integer> numbers = List.of(1, 2, 3, 4, 5);
        System.out.println("Input: " + numbers);

        List<Integer> totalSum = numbers.stream()
                .gather(Gatherers.fold(() -> 0, (sum, element) -> sum + element))
                .toList();

        System.out.println("Output: " + totalSum);
        // Expected Output: [15] (contrast with scan which would be [1,3,6,10,15])

        // Example: Concatenating all words
        List<String> words = List.of("Hello", "World", "!");
        System.out.println("Input: " + words);

        List<String> finalString = words.stream()
                .gather(Gatherers.fold(() -> "", (acc, word) -> acc.isEmpty() ? word : acc + " " + word))
                .toList();

        System.out.println("Output: " + finalString);
        // Expected Output: ["Hello World !"]
    }
}
```

**Output:**

```
--- Gatherers.fold() ---
Input: [1, 2, 3, 4, 5]
Output: [15]
Input: [Hello, World, !]
Output: [Hello World !]
```

## 6. Advantages and Use Cases

*   **Enhanced Expressiveness:** Gatherers allow for complex, stateful intermediate operations to be expressed declaratively within the Stream API, making the code more readable and maintainable.
*   **True Intermediate Stateful Operations:** They fill the gap between stateless `map`/`filter` and terminal `collect`, enabling operations like windowing, scanning, and custom buffering without breaking the stream pipeline.
*   **Cleaner Code:** Avoids the need for complex `reduce` operations that return intermediate collections or the need to convert streams to lists for mid-pipeline processing.
*   **Improved Performance (Potentially):** By keeping operations within the stream pipeline, the JVM's stream optimizations (like short-circuiting and fusion) can still apply, potentially leading to more efficient execution compared to breaking the pipeline.
*   **Parallelism Support:** With proper `combiner` implementations, custom and built-in gatherers can leverage parallel streams for improved performance on multi-core systems.

**When to use Gatherers:**
*   You need to group or batch elements into windows (fixed, sliding).
*   You need to compute running aggregates (like `scan`).
*   You need to process adjacent elements (like `pairwise`).
*   You have a custom stateful transformation that needs to emit zero, one, or multiple elements for each input element, and you want to keep the operation within the stream pipeline.
*   When `map` is too simple (stateless, one-to-one) and `collect` is too late (terminal).

## 7. Conclusion

Stream Gatherers in Java 24 are a powerful addition to the Stream API, providing a flexible and expressive way to handle stateful, intermediate transformations. They allow developers to write cleaner, more efficient, and more idiomatic stream pipelines for common data processing patterns that were previously awkward to implement. As you adopt Java 24 and beyond, integrating Gatherers into your toolkit will undoubtedly enhance your ability to leverage the full potential of the Stream API.