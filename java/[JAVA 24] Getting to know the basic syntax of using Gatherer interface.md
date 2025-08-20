The `Gatherer` interface, introduced in **Java 22**, is a powerful addition to the Stream API. It offers a flexible mechanism for stateful, intermediate stream operations, allowing you to transform a stream of elements into another stream by maintaining internal state and potentially emitting zero, one, or multiple elements for each input element.

While `Collectors` are designed to reduce a stream to a single, final result (like a `List`, `Map`, or sum), `Gatherer` is for transforming streams *into other streams* in a more dynamic way than simple `map`, `filter`, or `flatMap`.

## What is `Gatherer`?

A `Gatherer<T, S, R>` is an interface that represents a stateful intermediate operation on a stream:
*   `T`: The type of elements in the **input stream**.
*   `S`: The type of the **internal state** that the gatherer maintains.
*   `R`: The type of elements in the **output stream**.

It operates by taking elements from an upstream `Stream<T>`, processing them with an internal `state` of type `S`, and pushing elements of type `R` to a `Downstream` consumer.

## Key Components and Methods

A `Gatherer` is defined by several functional components, which are typically provided as lambda expressions or method references when using its static factory methods:

1.  ### `initializer()`: `Supplier<S>` (Optional)
    *   Provides the initial state `S` for the gatherer.
    *   Executed once per stream pipeline execution.
    *   If not provided, the gatherer implicitly has no initial state, or a `Void` state for stateless operations.

2.  ### `integrator()`: `(S state, T element, Gatherer.Downstream<? super R> downstream) -> boolean`
    *   **The core processing logic.** This function is called for each element `T` from the input stream.
    *   `state`: The current internal state of type `S`.
    *   `element`: The current input element from the stream of type `T`.
    *   `downstream`: An instance of `Gatherer.Downstream`, which is used to *emit* elements of type `R` to the output stream. You call `downstream.push(element)` to send elements.
    *   Returns `boolean`:
        *   `true`: Indicates that the gatherer should continue processing subsequent elements from the input stream.
        *   `false`: Indicates that the gatherer wants to stop processing the stream (short-circuiting).

3.  ### `combiner()`: `(S state1, S state2) -> S` (Optional)
    *   Used when the stream pipeline is executed in parallel.
    *   Defines how to combine two partial states (`S`) from different parallel execution branches into a single state. If parallel processing is not supported or desired for your gatherer, you don't need to provide this.

4.  ### `finisher()`: `(S state, Gatherer.Downstream<? super R> downstream) -> void` (Optional)
    *   Called once after all input elements have been processed.
    *   Allows the gatherer to emit any final elements based on its accumulated `state`.
    *   Useful for emitting summary results, flushing buffered elements, or handling elements that couldn't form a full "window" at the end of the stream.

### The `Gatherer.Downstream` Interface

This inner interface is crucial for `Gatherer` as it's the mechanism through which your gatherer produces elements for the subsequent operations in the stream pipeline. It has a single method:

*   `void push(R element)`: Sends an element `R` to the downstream of the stream pipeline.

## Creating `Gatherer` Instances

The easiest way to create `Gatherer` instances is by using its static factory methods:

*   `Gatherer.of(integrator)`: For simple stateless transformations.
*   `Gatherer.of(initializer, integrator)`: For basic stateful transformations.
*   `Gatherer.of(initializer, integrator, finisher)`: For stateful transformations with a finalization step.
*   `Gatherer.of(initializer, integrator, combiner, finisher)`: The most complete method for fully custom stateful and parallel-aware gatherers.

There's also `Gatherer.Group.group(...)` for specific grouping scenarios, similar to `Collectors.groupingBy` but with more flexibility in how groups are processed and emitted.

## Practical Examples

Let's illustrate the `Gatherer` syntax and its capabilities with some examples.

### Example 1: Simple One-to-One Transformation (Stateless, Map-like)

This gatherer simply adds 1 to each integer, demonstrating the simplest form using only an `integrator`.

**Scenario:** Transform `[1, 2, 3]` to `[2, 3, 4]`.

**Code:**

```java
import java.util.List;
import java.util.stream.Stream;
import java.util.stream.Gatherer;

public class BasicGathererExample {

    public static void main(String[] args) {
        // Define a simple Gatherer that adds 1 to each element
        // <Integer (input), Void (state, because stateless), Integer (output)>
        Gatherer<Integer, ?, Integer> addOneGatherer = Gatherer.of(
            // Integrator: (state, element, downstream) -> boolean
            (state, element, downstream) -> {
                // For each element, push element + 1 to the downstream
                downstream.push(element + 1);
                return true; // Continue processing the stream
            }
        );

        System.out.println("--- Example 1: Simple One-to-One Transformation ---");
        List<Integer> numbers = List.of(1, 2, 3);
        System.out.println("Input: " + numbers);

        List<Integer> transformedNumbers = numbers.stream()
                                                  .gather(addOneGatherer) // Apply the gatherer
                                                  .toList(); // Collect to a list

        System.out.println("Output: " + transformedNumbers);
        System.out.println();
    }
}
```

**Input (simulated):**
The `List.of(1, 2, 3)` creates the input stream.

**Output:**
```
--- Example 1: Simple One-to-One Transformation ---
Input: [1, 2, 3]
Output: [2, 3, 4]
```

**Explanation:**
The `integrator` lambda receives each `element` from the input stream and immediately calls `downstream.push(element + 1)`, emitting the transformed value. Since no state is needed and there's no finalization step, this is the most basic usage. The `?` for the state type indicates an unused state (or `Void` effectively).

### Example 2: Stateful Filtering (Unique Elements)

This gatherer keeps track of elements it has already seen and only emits new, unique ones, demonstrating the use of an `initializer` to manage state.

**Scenario:** Remove duplicate numbers from `[1, 2, 2, 3, 1, 4]`, keeping only the first occurrence.

**Code:**

```java
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Gatherer;

public class StatefulGathererExample {

    public static void main(String[] args) {
        // Define a Gatherer that keeps track of seen elements to filter out duplicates
        // <Integer (input), Set<Integer> (state), Integer (output)>
        Gatherer<Integer, Set<Integer>, Integer> uniqueElementsGatherer = Gatherer.of(
            // Initializer: Supplier<Set<Integer>> - provides a new HashSet for the state
            HashSet::new,
            // Integrator: (state, element, downstream) -> boolean
            (state, element, downstream) -> {
                if (state.add(element)) { // Set.add returns true if element was new
                    downstream.push(element); // If new, push to downstream
                }
                return true; // Continue processing
            }
            // No combiner or finisher needed for this simple case
        );

        System.out.println("--- Example 2: Stateful Filtering (Unique Elements) ---");
        List<Integer> numbersWithDuplicates = List.of(1, 2, 2, 3, 1, 4);
        System.out.println("Input: " + numbersWithDuplicates);

        List<Integer> uniqueNumbers = numbersWithDuplicates.stream()
                                                           .gather(uniqueElementsGatherer)
                                                           .toList();

        System.out.println("Output: " + uniqueNumbers);
        System.out.println();
    }
}
```

**Input (simulated):**
The `List.of(1, 2, 2, 3, 1, 4)` creates the input stream.

**Output:**
```
--- Example 2: Stateful Filtering (Unique Elements) ---
Input: [1, 2, 2, 3, 1, 4]
Output: [1, 2, 3, 4]
```

**Explanation:**
The `initializer` creates a new `HashSet` to serve as the `state` for each stream operation. The `integrator` attempts to add the current `element` to this `state` set. If `Set.add()` returns `true` (meaning the element was successfully added because it wasn't present before), the element is `push`ed to the `downstream`. Otherwise, it's a duplicate and is ignored.

### Example 3: One-to-Many Transformation (Pairwise Sums)

This gatherer pairs consecutive elements and emits their sum. It also demonstrates using a `finisher` to handle any leftover state.

**Scenario:** Given `[1, 2, 3, 4, 5]`, produce `[3, 7]`. The last `5` is unpaired and ignored.

**Code:**

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Gatherer;

public class PairwiseGathererExample {

    public static void main(String[] args) {
        // Define a Gatherer for pairwise sums
        // <Integer (input), Optional<Integer> (state for the first element of a pair), Integer (output)>
        Gatherer<Integer, Optional<Integer>, Integer> pairwiseSumGatherer = Gatherer.of(
            // Initializer: Start with an empty Optional (no element yet for a pair)
            Optional::empty,
            // Integrator: Process elements to form pairs
            (state, element, downstream) -> {
                if (state.isEmpty()) {
                    // This is the first element of a potential pair, store it in state
                    return Optional.of(element); // Update state to contain the element
                } else {
                    // This is the second element, completing a pair. Sum them and emit.
                    Integer first = state.get();
                    downstream.push(first + element);
                    return Optional.empty(); // Reset state, ready for the next pair
                }
            },
            // Finisher: (state, downstream) -> void
            // For this example, if there's an odd element left, we simply ignore it.
            // If we wanted to emit it, we'd add: state.ifPresent(downstream::push);
            (state, downstream) -> { /* No action needed */ }
        );

        System.out.println("--- Example 3: One-to-Many Transformation (Pairwise Sums) ---");
        List<Integer> numbers = List.of(1, 2, 3, 4, 5);
        System.out.println("Input: " + numbers);

        List<Integer> pairwiseSums = numbers.stream()
                                             .gather(pairwiseSumGatherer)
                                             .toList();

        System.out.println("Output: " + pairwiseSums);
        System.out.println();

        List<Integer> evenNumbers = List.of(10, 20, 30, 40);
        System.out.println("Input (even count): " + evenNumbers);
        List<Integer> pairwiseSumsEven = evenNumbers.stream()
                                                     .gather(pairwiseSumGatherer)
                                                     .toList();
        System.out.println("Output (even count): " + pairwiseSumsEven);
        System.out.println();
    }
}
```

**Input (simulated):**
The `List.of(1, 2, 3, 4, 5)` and `List.of(10, 20, 30, 40)` create the input streams.

**Output:**
```
--- Example 3: One-to-Many Transformation (Pairwise Sums) ---
Input: [1, 2, 3, 4, 5]
Output: [3, 7]

Input (even count): [10, 20, 30, 40]
Output (even count): [30, 70]
```

**Explanation:**
The `state` is `Optional<Integer>`, which is used to store the first element of a potential pair.
*   **`initializer`**: Starts with `Optional.empty()`.
*   **`integrator`**:
    *   If the `state` is empty, the current `element` is considered the first of a new pair, and it's stored in the state (`return Optional.of(element)`).
    *   If the `state` already contains an element, the current `element` completes the pair. Their sum is `push`ed to `downstream`, and the `state` is reset to `Optional.empty()`.
*   **`finisher`**: In this case, it's an empty lambda, meaning any leftover single element (if the input count is odd) is simply dropped.

### Example 4: Sliding Window (Averages of N Elements)

This gatherer maintains a sliding window of elements and emits the average of elements within that window. This demonstrates a more complex state (`Deque`) and conditional emission.

**Scenario:** Given `[1, 2, 3, 4, 5]` and a window size of 3, calculate the average of `[1,2,3]`, `[2,3,4]`, `[3,4,5]`.

**Code:**

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;
import java.util.stream.Gatherer;

public class SlidingWindowGathererExample {

    public static void main(String[] args) {
        final int WINDOW_SIZE = 3;

        // Define a Gatherer for sliding window average
        // <Integer (input), Deque<Integer> (state: the current window elements), Double (output: average)>
        Gatherer<Integer, Deque<Integer>, Double> slidingWindowAverageGatherer = Gatherer.of(
            // Initializer: Provide a new ArrayDeque for the window state
            ArrayDeque::new,
            // Integrator: Add element to window, calculate average if window is full
            (window, element, downstream) -> {
                window.addLast(element); // Add current element to the end of the window

                if (window.size() == WINDOW_SIZE) {
                    // Window is full, calculate average
                    double sum = window.stream().mapToDouble(Integer::doubleValue).sum();
                    downstream.push(sum / WINDOW_SIZE);
                    window.removeFirst(); // Slide the window: remove the oldest element
                }
                return true; // Continue processing
            },
            // Finisher: (window, downstream) -> void
            // No remaining calculations needed, as average is pushed when window is full.
            // If partial windows needed to be emitted, logic would go here.
            (window, downstream) -> { /* No action needed */ }
        );

        System.out.println("--- Example 4: Sliding Window (Averages of N Elements) ---");
        List<Integer> numbers = List.of(1, 2, 3, 4, 5);
        System.out.println("Input (Window Size " + WINDOW_SIZE + "): " + numbers);

        List<Double> averages = numbers.stream()
                                       .gather(slidingWindowAverageGatherer)
                                       .toList();

        System.out.println("Output: " + averages);
        System.out.println();
    }
}
```

**Input (simulated):**
The `List.of(1, 2, 3, 4, 5)` creates the input stream.

**Output:**
```
--- Example 4: Sliding Window (Averages of N Elements) ---
Input (Window Size 3): [1, 2, 3, 4, 5]
Output: [2.0, 3.0, 4.0]
```

**Explanation:**
The `state` is a `Deque<Integer>` (implemented by `ArrayDeque`) to efficiently add elements to the tail and remove from the head, simulating a sliding window.
*   **`initializer`**: Creates an empty `ArrayDeque`.
*   **`integrator`**:
    1.  Adds the current `element` to the `window` (using `addLast`).
    2.  If the `window`'s `size()` reaches `WINDOW_SIZE`, it calculates the sum of its elements and `push`es the average to `downstream`.
    3.  It then `removeFirst()` to slide the window, discarding the oldest element and making space for the next input.
*   **`finisher`**: Is empty, as we only output full windows. Any remaining elements in the `Deque` (if the stream ends before a full window can be formed) are implicitly ignored.

## When to Use `Gatherer` vs. `Collector`

*   **`Collector`**: Primarily for **reduction** operations. Use it when you want to transform an entire stream into a **single, final result** (e.g., a `List`, `Map`, `String`, a sum, or an average of all elements).
*   **`Gatherer`**: For **intermediate stateful transformations** that produce another stream. Use it when:
    *   You need to maintain state across multiple elements.
    *   You need to emit zero, one, or multiple output elements for each input element.
    *   You're implementing operations like windowing, pairing, deduplicating based on history, or any custom sequence-to-sequence transformation that goes beyond `map`/`filter`/`flatMap`.

`Gatherer` fills a crucial gap in the Stream API, enabling more complex and custom intermediate stream operations with a clear and flexible API. Remember, `Gatherer` is available from **Java 22** onwards.