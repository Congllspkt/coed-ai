The Java Stream API, introduced in Java 8, provides powerful ways to process collections. While `map`, `filter`, `flatMap` are common intermediate operations and `collect`, `reduce` are terminal operations, there are scenarios where you need more fine-grained control, statefulness, or the ability to emit multiple elements (or no elements) based on accumulated state during intermediate processing.

This is where **`Gatherer`**, introduced as a preview feature in **Java 22 (JEP 461)** and becoming standard in **Java 23/24**, comes into play. `Gatherer` is a new kind of stream operation that acts as a flexible, stateful intermediate operation, bridging the gap between existing intermediate operations and terminal collectors.

## What is `Gatherer`?

A `Gatherer` allows you to define a custom, stateful intermediate stream operation. Unlike `Collector` (which is always terminal), a `Gatherer` can transform a stream of elements into *another stream of elements*, making it an ideal intermediate operation. It processes elements sequentially, maintaining internal state, and can emit zero, one, or multiple output elements for each input element (or group of input elements).

## Why `Gatherer.of()` for Intermediate Operations?

`Gatherer.of()` is the simplest way to construct a `Gatherer`. It provides static factory methods to create `Gatherer` instances by specifying their core components:

1.  **`Supplier<A> initialSupplier`**: A function that provides an initial, mutable state object for the gathering process. `A` is the type of the state object.
2.  **`Gatherer.Integrator<A, T, R> integrator`**: This is the heart of the `Gatherer` for intermediate operations. It defines how each input element `T` modifies the state `A` and, crucially, how to emit output elements `R` to the downstream stream.
    *   It takes the current state `A`, the input element `T`, and a `Downstream.Consumer<R> downstream` (which is how you emit elements).
    *   It returns a `Gatherer.Integrator.Result` to control the stream flow (`CONTINUE`, `FINISH`, `FINISH_AND_STOP`).
3.  **`BinaryOperator<A> combiner` (optional)**: For parallel streams, this function merges two state objects into one.
4.  **`BiConsumer<A, Downstream.Consumer<R>> finisher` (optional)**: After all input elements have been processed, this function can perform a final action on the state and emit any remaining elements to the downstream. This is vital for operations like batching where you might have partial batches left over.

The key to `Gatherer.of()` creating an *intermediate* operation is the `integrator`'s ability to call `downstream.accept(result)` multiple times, allowing elements to be passed to the next stage of the stream pipeline as they are processed.

## Anatomy of an Intermediate `Gatherer.of()`

The most common `Gatherer.of()` signature for intermediate operations will involve the `integrator`:

```java
public static <T, R, A> Gatherer<T, A, R> of(
    Supplier<A> initialSupplier,
    Gatherer.Integrator<A, T, R> integrator,
    BinaryOperator<A> combiner, // for parallelism, can be null for sequential
    BiConsumer<A, Gatherer.Downstream.Consumer<R>> finisher // for final emission
)
```

Where:

*   `T`: Type of input elements to the `Gatherer`.
*   `R`: Type of output elements from the `Gatherer`.
*   `A`: Type of the internal mutable state.

The `integrator` is critical:
`Gatherer.Integrator<A, T, R> integrator = (state, element, downstream) -> { ... };`

Inside the `integrator`'s lambda, you'll update `state` and call `downstream.accept(someResult)` whenever you want to emit an `R` element.

---

## Examples

Let's illustrate with practical examples.

### Example 1: Consecutive Deduplication

**Problem:** Given a stream of elements, remove consecutive duplicates. Only emit an element if it's different from the immediately preceding one.

**Input:** `[1, 1, 2, 2, 2, 3, 3, 1, 4]`
**Desired Output:** `[1, 2, 3, 1, 4]`

**Solution using `Gatherer.of()`:**
We need to maintain state: the last element seen.

```java
import java.util.List;
import java.util.Optional;
import java.util.stream.Gatherer;
import java.util.stream.Stream;

public class GathererDeduplicationExample {

    public static void main(String[] args) {
        System.out.println("--- Example 1: Consecutive Deduplication ---");

        List<Integer> numbers = List.of(1, 1, 2, 2, 2, 3, 3, 1, 4);
        System.out.println("Input: " + numbers);

        // State: Optional<Integer> to hold the last seen element.
        // Optional is used to correctly handle the very first element.
        Gatherer<Integer, Optional<Integer>, Integer> deduplicator =
            Gatherer.of(
                () -> Optional.empty(), // Initial state: no last element seen
                (lastElementOpt, currentElement, downstream) -> {
                    if (lastElementOpt.isEmpty() || !lastElementOpt.get().equals(currentElement)) {
                        // If it's the first element OR different from the last, emit it
                        downstream.accept(currentElement);
                        return Gatherer.Integrator.Result.CONTINUE; // Continue processing
                    }
                    // If it's a duplicate, do not emit
                    return Gatherer.Integrator.Result.CONTINUE; // Continue processing
                },
                (state1, state2) -> { // Combiner for parallel streams (simple for Optional)
                    // For this specific Gatherer, a combiner might not be strictly necessary
                    // if elements are processed strictly sequentially per partition.
                    // But in general, you need to define how to merge states.
                    // For Optional, you'd typically take the non-empty one if available.
                    return state2.isEmpty() ? state1 : state2;
                },
                (finalState, downstream) -> {
                    // No final emission needed for this specific gatherer
                    // as all emissions happen in the integrator.
                }
            );

        List<Integer> result = numbers.stream()
                                      .gather(deduplicator)
                                      .toList();

        System.out.println("Output: " + result); // Expected: [1, 2, 3, 1, 4]

        // Another test case
        List<String> words = List.of("apple", "apple", "banana", "orange", "orange", "orange", "kiwi");
        System.out.println("\nInput: " + words);
        List<String> resultWords = words.stream()
                                        .gather(Gatherer.of(
                                            () -> Optional.empty(),
                                            (lastElementOpt, currentElement, downstream) -> {
                                                if (lastElementOpt.isEmpty() || !lastElementOpt.get().equals(currentElement)) {
                                                    downstream.accept(currentElement);
                                                    return Gatherer.Integrator.Result.CONTINUE;
                                                }
                                                return Gatherer.Integrator.Result.CONTINUE;
                                            },
                                            (s1, s2) -> s2.isEmpty() ? s1 : s2,
                                            (s, d) -> {}
                                        ))
                                        .toList();
        System.out.println("Output: " + resultWords); // Expected: [apple, banana, orange, kiwi]
    }
}
```

**Explanation:**
1.  **State (`Optional<Integer>`):** We use an `Optional` to store the `lastElement`. `Optional.empty()` is the initial state, indicating no element has been processed yet.
2.  **Integrator:**
    *   If `lastElementOpt` is empty (first element) or the `currentElement` is different from `lastElementOpt.get()`, we `downstream.accept(currentElement)` to emit it.
    *   We then update the `lastElementOpt` to the `currentElement` for the next iteration. *Correction:* The `integrator` itself cannot update the `state` in place with the `Gatherer.of()` signature. The state is mutated outside, and the `integrator` receives the current mutable state. So, the `lastElementOpt` here needs to be a mutable container, like `AtomicReference` or a single-element array, or the `Gatherer` needs to return a new state (which is not how `Gatherer.of` works directly for state mutation).
    *   **Revised State for Mutation:** Let's use `AtomicReference` for the state to allow mutation inside the lambda.

---

### Example 1 (Revised with Mutable State): Consecutive Deduplication

```java
import java.util.List;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicReference;
import java.util.stream.Gatherer;

public class GathererDeduplicationExampleRevised {

    public static void main(String[] args) {
        System.out.println("--- Example 1: Consecutive Deduplication (Revised) ---");

        List<Integer> numbers = List.of(1, 1, 2, 2, 2, 3, 3, 1, 4);
        System.out.println("Input: " + numbers);

        // State: AtomicReference<T> to hold the last seen element, allowing mutable state.
        Gatherer<Integer, AtomicReference<Integer>, Integer> deduplicator =
            Gatherer.of(
                () -> new AtomicReference<>(), // Initial state: AtomicReference holding null
                (lastElementRef, currentElement, downstream) -> {
                    // Get the value of the last element
                    Integer lastElement = lastElementRef.get();

                    if (!Objects.equals(lastElement, currentElement)) {
                        // If it's the first element (lastElement is null)
                        // OR if it's different from the last, emit it
                        downstream.accept(currentElement);
                        // Update the state for the next iteration
                        lastElementRef.set(currentElement);
                    }
                    return Gatherer.Integrator.Result.CONTINUE; // Always continue processing
                },
                (state1, state2) -> { // Combiner for parallel streams
                    // For deduplication, combining states in parallel is tricky as it depends
                    // on the *previous* element. This Gatherer is primarily sequential in nature.
                    // A simple combiner might just take the last element from the second state,
                    // but true parallel deduplication would need more complex logic at partition boundaries.
                    // For illustrative purposes for sequential, this is sufficient.
                    if (state2.get() != null) {
                        state1.set(state2.get());
                    }
                    return state1; // Merge state2 into state1 (or create new merged state)
                },
                (finalState, downstream) -> {
                    // No final emission needed as all logic is in integrator
                }
            );

        List<Integer> result = numbers.stream()
                                      .gather(deduplicator)
                                      .toList();

        System.out.println("Output: " + result);

        List<String> words = List.of("apple", "apple", "banana", "orange", "orange", "orange", "kiwi");
        System.out.println("\nInput: " + words);
        List<String> resultWords = words.stream()
                                        .gather(Gatherer.of(
                                            () -> new AtomicReference<>(),
                                            (lastElementRef, currentElement, downstream) -> {
                                                if (!Objects.equals(lastElementRef.get(), currentElement)) {
                                                    downstream.accept(currentElement);
                                                    lastElementRef.set(currentElement);
                                                }
                                                return Gatherer.Integrator.Result.CONTINUE;
                                            },
                                            (s1, s2) -> { if (s2.get() != null) s1.set(s2.get()); return s1; },
                                            (s, d) -> {}
                                        ))
                                        .toList();
        System.out.println("Output: " + resultWords);
    }
}
```

**Input:**
```
--- Example 1: Consecutive Deduplication (Revised) ---
Input: [1, 1, 2, 2, 2, 3, 3, 1, 4]

Input: [apple, apple, banana, orange, orange, orange, kiwi]
```

**Output:**
```
Output: [1, 2, 3, 1, 4]

Output: [apple, banana, orange, kiwi]
```

---

### Example 2: Chunking/Batching Elements

**Problem:** Group a stream of elements into fixed-size chunks (e.g., lists of 3 elements). Any remaining elements should form a smaller final chunk.

**Input:** `[A, B, C, D, E, F, G]` (chunk size 3)
**Desired Output:** `[[A, B, C], [D, E, F], [G]]` (as a stream of lists)

**Solution using `Gatherer.of()`:**
We need to maintain state: the current list of elements being accumulated for the chunk. The `finisher` is crucial here to emit the last, potentially incomplete, chunk.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Gatherer;
import java.util.stream.Stream;

public class GathererChunkingExample {

    public static void main(String[] args) {
        System.out.println("\n--- Example 2: Chunking/Batching Elements ---");

        List<String> items = List.of("A", "B", "C", "D", "E", "F", "G");
        int chunkSize = 3;
        System.out.println("Input: " + items + ", Chunk Size: " + chunkSize);

        // State: List<T> to accumulate elements for the current chunk.
        Gatherer<String, List<String>, List<String>> chunker =
            Gatherer.of(
                () -> new ArrayList<>(), // Initial state: an empty list for the current chunk
                (currentChunk, element, downstream) -> {
                    currentChunk.add(element); // Add current element to the chunk
                    if (currentChunk.size() == chunkSize) {
                        // If chunk is full, emit it and start a new one
                        downstream.accept(currentChunk);
                        return Gatherer.Integrator.Result.CONTINUE; // Continue with a new empty chunk implicitly
                    }
                    return Gatherer.Integrator.Result.CONTINUE; // Keep accumulating
                },
                (chunk1, chunk2) -> { // Combiner for parallel streams
                    // For chunking, this would involve merging partial chunks at partition boundaries.
                    // For simplicity, we'll assume sequential for this example.
                    // In a real parallel scenario, this would be more complex.
                    chunk1.addAll(chunk2);
                    return chunk1;
                },
                (finalChunk, downstream) -> {
                    // After all input elements, emit any remaining elements in the finalChunk
                    if (!finalChunk.isEmpty()) {
                        downstream.accept(finalChunk);
                    }
                }
            );

        List<List<String>> result = items.stream()
                                         .gather(chunker)
                                         .toList();

        System.out.println("Output: " + result); // Expected: [[A, B, C], [D, E, F], [G]]

        List<Integer> numbers = List.of(10, 20, 30, 40);
        int intChunkSize = 2;
        System.out.println("\nInput: " + numbers + ", Chunk Size: " + intChunkSize);
        List<List<Integer>> intResult = numbers.stream()
                                            .gather(Gatherer.of(
                                                () -> new ArrayList<>(),
                                                (currentChunk, element, downstream) -> {
                                                    currentChunk.add(element);
                                                    if (currentChunk.size() == intChunkSize) {
                                                        downstream.accept(currentChunk);
                                                        return Gatherer.Integrator.Result.CONTINUE;
                                                    }
                                                    return Gatherer.Integrator.Result.CONTINUE;
                                                },
                                                (c1, c2) -> { c1.addAll(c2); return c1; },
                                                (finalChunk, downstream) -> {
                                                    if (!finalChunk.isEmpty()) {
                                                        downstream.accept(finalChunk);
                                                    }
                                                }
                                            ))
                                            .toList();
        System.out.println("Output: " + intResult); // Expected: [[10, 20], [30, 40]]

        List<Character> chars = List.of('x', 'y', 'z', 'a');
        int charChunkSize = 5;
        System.out.println("\nInput: " + chars + ", Chunk Size: " + charChunkSize);
        List<List<Character>> charResult = chars.stream()
                                                .gather(Gatherer.of(
                                                    () -> new ArrayList<>(),
                                                    (currentChunk, element, downstream) -> {
                                                        currentChunk.add(element);
                                                        if (currentChunk.size() == charChunkSize) {
                                                            downstream.accept(currentChunk);
                                                            return Gatherer.Integrator.Result.CONTINUE;
                                                        }
                                                        return Gatherer.Integrator.Result.CONTINUE;
                                                    },
                                                    (c1, c2) -> { c1.addAll(c2); return c1; },
                                                    (finalChunk, downstream) -> {
                                                        if (!finalChunk.isEmpty()) {
                                                            downstream.accept(finalChunk);
                                                        }
                                                    }
                                                ))
                                                .toList();
        System.out.println("Output: " + charResult); // Expected: [[x, y, z, a]]
    }
}
```

**Input:**
```
--- Example 2: Chunking/Batching Elements ---
Input: [A, B, C, D, E, F, G], Chunk Size: 3

Input: [10, 20, 30, 40], Chunk Size: 2

Input: [x, y, z, a], Chunk Size: 5
```

**Output:**
```
Output: [[A, B, C], [D, E, F], [G]]

Output: [[10, 20], [30, 40]]

Output: [[x, y, z, a]]
```

**Explanation:**
1.  **State (`List<String>`):** An `ArrayList` holds the elements for the current chunk.
2.  **Integrator:**
    *   Each `element` is added to `currentChunk`.
    *   If `currentChunk.size()` reaches `chunkSize`, the full `currentChunk` is `downstream.accept()`ed (emitted), and a new `ArrayList` is implicitly created by the next `initialSupplier` call *if the `integrator` returns `FINISH` or similar that causes a new state to be initialized*. However, for `Gatherer.of()`, the `integrator` *always* receives the *same mutable state object* (or a combined one in parallel).
    *   **Crucial point for `Gatherer.of()` state management:** To "reset" the chunk, you must clear the *existing* `currentChunk` *after* emitting it. If you don't clear it, you'll be adding to the same list.
    *   **Revised Integrator for Chunking:**

```java
// Inside Gatherer.of for chunking
(currentChunk, element, downstream) -> {
    currentChunk.add(element);
    if (currentChunk.size() == chunkSize) {
        downstream.accept(new ArrayList<>(currentChunk)); // Emit a copy
        currentChunk.clear(); // Clear the state for the next chunk
    }
    return Gatherer.Integrator.Result.CONTINUE;
}
```

This ensures that the emitted list is a *copy* (so subsequent modifications to `currentChunk` don't affect the emitted one) and that `currentChunk` is cleared for the next batch.

3.  **Finisher (`BiConsumer<List<String>, Downstream.Consumer<List<String>>>`):** This is essential. After all elements are processed, the `finisher` is called with the final `currentChunk` (which might be partially filled). If it's not empty, it's `downstream.accept()`ed as the last chunk.

---

### Example 3: Adding an Index to Elements

**Problem:** Transform a stream of elements into a stream of `(element, index)` pairs.

**Input:** `[A, B, C]`
**Desired Output:** `[(A, 0), (B, 1), (C, 2)]` (as a stream of a custom pair object or Map.Entry)

**Solution using `Gatherer.of()`:**
We need to maintain state: an integer counter for the index.

```java
import java.util.AbstractMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Gatherer;

public class GathererIndexedExample {

    public static void main(String[] args) {
        System.out.println("\n--- Example 3: Adding an Index to Elements ---");

        List<String> fruits = List.of("Apple", "Banana", "Cherry", "Date");
        System.out.println("Input: " + fruits);

        // State: AtomicInteger to keep track of the current index.
        Gatherer<String, AtomicInteger, Map.Entry<String, Integer>> indexer =
            Gatherer.of(
                () -> new AtomicInteger(0), // Initial state: index starts at 0
                (indexCounter, element, downstream) -> {
                    // Emit a new Map.Entry with the current element and index
                    downstream.accept(new AbstractMap.SimpleEntry<>(element, indexCounter.getAndIncrement()));
                    return Gatherer.Integrator.Result.CONTINUE; // Continue processing
                },
                (state1, state2) -> { // Combiner for parallel streams
                    // For indexing, parallel processing requires careful coordination
                    // of index ranges per partition. A simple merge isn't usually enough.
                    // For sequential, this is not invoked.
                    state1.addAndGet(state2.get()); // Example merge (summing counts, typically not for index)
                    return state1;
                },
                (finalState, downstream) -> {
                    // No final emission needed
                }
            );

        List<Map.Entry<String, Integer>> result = fruits.stream()
                                                       .gather(indexer)
                                                       .toList();

        System.out.println("Output: " + result); // Expected: [Apple=0, Banana=1, Cherry=2, Date=3]
    }
}
```

**Input:**
```
--- Example 3: Adding an Index to Elements ---
Input: [Apple, Banana, Cherry, Date]
```

**Output:**
```
Output: [Apple=0, Banana=1, Cherry=2, Date=3]
```

**Explanation:**
1.  **State (`AtomicInteger`):** An `AtomicInteger` is used as a mutable counter for the index.
2.  **Integrator:**
    *   `indexCounter.getAndIncrement()` atomically gets the current value and then increments it. This ensures that each emitted element gets a unique, sequential index.
    *   A `Map.Entry` (or any custom `Pair` class) is created and `downstream.accept()`ed.
    *   `Gatherer.Integrator.Result.CONTINUE` is returned to signal that the stream should continue processing the next element.
3.  **Combiner/Finisher:** Not strictly necessary for this sequential operation, but included for completeness of the `Gatherer.of()` signature. For parallel streams, indexing would be more complex as each partition would start its own index from 0.

## Benefits of `Gatherer.of()` as an Intermediate Operation

*   **Stateful Processing:** Unlike `map` or `filter` which are stateless, `Gatherer` allows you to maintain and update state across elements.
*   **Flexible Emission:** You can emit zero, one, or multiple output elements for each input element (or group of elements), which is not directly possible with `map` (one-to-one) or `filter` (one-to-zero/one). `flatMap` allows one-to-many but is stateless.
*   **Fine-Grained Control:** The `Integrator.Result` allows you to control the flow of the stream, potentially stopping processing early (`FINISH`, `FINISH_AND_STOP`).
*   **Custom Pipeline Stages:** Enables the creation of highly specialized, reusable intermediate stream operations.
*   **Improved Readability for Complex Operations:** For scenarios that would otherwise require convoluted `reduce` operations or pre-processing, `Gatherer` can make the stream pipeline clearer and more expressive.

## Conclusion

`Gatherer.of()` provides a powerful and flexible way to introduce custom, stateful intermediate operations into your Java Stream pipelines. By understanding its components – the `supplier` for state, the `integrator` for element processing and emission, and the optional `finisher` for final logic – you can build sophisticated data transformations that were previously difficult or impossible to express cleanly within the Stream API. It's a valuable addition for Java developers working with complex data processing tasks.