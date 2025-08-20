The `Gatherer` interface, introduced in Java 22, provides a new way to implement custom intermediate operations in streams. Unlike `Stream::map` or `Stream::flatMap` which operate on elements individually or in immediate relation, a `Gatherer` can maintain an *internal state* that evolves as elements are processed. This allows for more complex aggregate operations that result in a stream.

A `Gatherer` is composed of several functional interfaces:

1.  **`initializer()`**: A `Supplier<S>` that creates the initial internal state `S`.
2.  **`integrator()`**: A `Gatherer.Integrator<S, T, R>` that incorporates a new input element `T` into the state `S`. This can optionally produce output elements `R` directly.
3.  **`combiner()`**: A `BinaryOperator<S>` for parallel streams, merging two states `S` into one.
4.  **`finisher()`**: A `Function<S, Stream<R>>` that transforms the final state `S` into the resulting stream of elements `R`.

This document focuses on the `finisher()` component.

---

## `Gatherer.Finisher`

The `finisher()` method in a `Gatherer` is responsible for taking the *final accumulated state* and transforming it into the output `Stream` of elements.

### Purpose

The primary purpose of the `finisher` is to:

1.  **Process the Final State:** After all input elements have been processed by the `integrator` (and `combiner` in parallel streams), the internal state `S` holds the accumulated information. The `finisher` is the last opportunity to do any final computations or transformations on this state.
2.  **Produce the Output Stream:** The `finisher` must return a `Stream<R>`, where `R` is the type of elements that will be emitted downstream from the `Gatherer`. This means a single state object can produce zero, one, or many output elements.
3.  **Derive Results:** Often, the internal state `S` is not the desired output itself, but rather contains the raw data from which the final results `R` need to be derived.

### Method Signature

The `finisher` is defined as a `Function<S, Stream<R>>`:

```java
Function<S, Stream<R>> finisher()
```

*   `S`: The type of the internal state.
*   `R`: The type of elements produced by the `Gatherer` (and consumed by the subsequent stream operations).

### When is it Called?

The `finisher()` is called **once** per stream pipeline (or once per sub-stream in a parallel pipeline, with results then combined) *after* all input elements have been processed by the `integrator` (and merged by the `combiner` if applicable). It's the final stage of the `Gatherer`'s internal logic before its results are passed to the next operation in the stream.

### Why is it Needed?

*   **Aggregation and Transformation:** When a `Gatherer` needs to perform an aggregate operation (like summing all numbers, collecting all unique items, or finding patterns across elements), the internal state accumulates the necessary data. The `finisher` then performs the final aggregation or transformation to produce the meaningful output.
*   **Context-Dependent Output:** Sometimes, the output elements depend on the *entire context* of the input stream, not just individual elements. For example, if you want to output each number divided by the total sum of all numbers, the `finisher` would calculate the total sum from the accumulated state (all numbers) and then map each number to its proportion.
*   **Generating Multiple Outputs from One State:** A single accumulated state might need to be "unpacked" into multiple output elements. For instance, if the state is a `List<ProcessedItem>`, the `finisher` can convert this list into a `Stream<ProcessedItem>`.
*   **Handling Incomplete Batches:** In batch processing, the `finisher` can handle any remaining elements in an incomplete final batch.

### Key Characteristics

*   **Terminal for the `Gatherer`'s Internal Logic:** It marks the end of the `Gatherer`'s state management.
*   **Produces a Stream:** Crucially, it returns a `Stream`, allowing for a 1-to-N transformation from the single final state object.
*   **Optional for `Gatherer.Integrator.of(...)`:** If you use the `Gatherer.Integrator.of(BiFunction<S, T, S> accumulator, Consumer<R> downstream)` overload for the `integrator`, the `finisher` might not be strictly necessary if all outputs are emitted during integration. However, if the output depends on the *entire* stream being processed, or requires final processing of the state, the `finisher` is essential. For the simpler `Gatherer.of(initializer, integrator, finisher)` constructor, the `finisher` is always required to convert the state into the output stream.

---

## Examples

Let's illustrate `finisher` with two examples.

### Example 1: `LastElementGatherer` (Finding the Last Element)

This `Gatherer` will process all elements but only emit the very last one.

**Problem:** From a stream of integers, get only the last integer.

**Gatherer Components:**

*   **State (`S`):** `Optional<Integer>` to hold the last seen element. `Optional` is good for representing zero or one element.
*   **Initializer:** `() -> Optional.empty()` - Start with no element.
*   **Integrator:** `(state, element) -> Optional.of(element)` - For each element, update the state to hold the current element. This effectively keeps track of the "last" element seen so far.
*   **Finisher:** `(state) -> state.stream()` - After all elements are processed, the `state` will contain the very last element. This `finisher` converts the `Optional` state into a `Stream` of zero or one element.

```java
import java.util.Optional;
import java.util.List;
import java.util.stream.Gatherer;
import java.util.stream.Stream;

public class LastElementGathererExample {

    public static void main(String[] args) {
        // Define the Gatherer
        Gatherer<Integer, Optional<Integer>, Integer> lastElementGatherer = Gatherer.of(
            Optional::empty, // initializer: start with an empty Optional
            (state, element) -> Optional.of(element), // integrator: update state with the current element
            (state) -> state.stream() // finisher: convert the final Optional state into a stream
        );

        // --- Example 1.1: With elements ---
        List<Integer> numbers1 = List.of(10, 20, 30, 40, 50);
        System.out.println("Input 1: " + numbers1);

        List<Integer> result1 = numbers1.stream()
                                        .gather(lastElementGatherer)
                                        .toList();
        System.out.println("Output 1 (Last Element): " + result1);
        // Expected Output: [50]

        System.out.println("\n---");

        // --- Example 1.2: Empty stream ---
        List<Integer> numbers2 = List.of();
        System.out.println("Input 2: " + numbers2);

        List<Integer> result2 = numbers2.stream()
                                        .gather(lastElementGatherer)
                                        .toList();
        System.out.println("Output 2 (Last Element): " + result2);
        // Expected Output: []
    }
}
```

**Input:**
```
Input 1: [10, 20, 30, 40, 50]
Input 2: []
```

**Output:**
```
Output 1 (Last Element): [50]

---
Input 2: []
Output 2 (Last Element): []
```

**Explanation:**
For `Input 1`, the `integrator` continuously updates the `Optional` state.
*   After `10`: `Optional[10]`
*   After `20`: `Optional[20]`
*   ...
*   After `50`: `Optional[50]`

When all elements are processed, the `finisher` `(state) -> state.stream()` is called with `Optional[50]`. `Optional.stream()` returns a stream containing `50`. If the input stream was empty (`Input 2`), the `state` would remain `Optional.empty()`, and `Optional.empty().stream()` would produce an empty stream.

---

### Example 2: `RelativeProportionGatherer` (Calculating Proportions)

This `Gatherer` will take a stream of numbers and output each number divided by the total sum of all numbers in the stream. This requires knowing the total sum *before* processing individual numbers for output, making it a perfect use case for `finisher`.

**Problem:** Given a stream of integers, output a stream of doubles where each double is the original integer divided by the total sum of all integers in the input stream.

**Gatherer Components:**

*   **State (`S`):** `List<Integer>` to store all the input numbers temporarily.
*   **Initializer:** `() -> new ArrayList<>()` - Start with an empty list.
*   **Integrator:** `(list, element) -> { list.add(element); return list; }` - Add each incoming element to the list.
*   **Finisher:** `(list) -> { ... }` - This is where the magic happens:
    1.  Calculate the `totalSum` from the `list`.
    2.  If `totalSum` is zero, return an empty stream to prevent division by zero.
    3.  Otherwise, convert the `list` into a stream and map each element `n` to `n / totalSum`.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Gatherer;
import java.util.stream.Stream;

public class RelativeProportionGathererExample {

    public static void main(String[] args) {
        // Define the Gatherer
        Gatherer<Integer, List<Integer>, Double> relativeProportionGatherer = Gatherer.of(
            ArrayList::new, // initializer: start with an empty list to store all numbers
            (list, element) -> { // integrator: add each element to the list
                list.add(element);
                return list;
            },
            (list) -> { // finisher: called once after all elements are processed
                double totalSum = list.stream().mapToDouble(Integer::doubleValue).sum();

                // Handle case where total sum is zero to avoid division by zero
                if (totalSum == 0) {
                    return Stream.empty();
                }

                // Map each number in the list to its proportion
                return list.stream()
                           .map(n -> n / totalSum);
            }
        );

        // --- Example 2.1: Positive numbers ---
        List<Integer> numbers1 = List.of(1, 2, 3, 4); // Sum = 10
        System.out.println("Input 1: " + numbers1);

        List<Double> result1 = numbers1.stream()
                                       .gather(relativeProportionGatherer)
                                       .toList();
        System.out.println("Output 1 (Proportions): " + result1);
        // Expected Output: [0.1, 0.2, 0.3, 0.4]

        System.out.println("\n---");

        // --- Example 2.2: Numbers summing to zero ---
        List<Integer> numbers2 = List.of(1, -1, 5, -5); // Sum = 0
        System.out.println("Input 2: " + numbers2);

        List<Double> result2 = numbers2.stream()
                                       .gather(relativeProportionGatherer)
                                       .toList();
        System.out.println("Output 2 (Proportions): " + result2);
        // Expected Output: []

        System.out.println("\n---");

        // --- Example 2.3: Empty stream ---
        List<Integer> numbers3 = List.of(); // Sum = 0
        System.out.println("Input 3: " + numbers3);

        List<Double> result3 = numbers3.stream()
                                       .gather(relativeProportionGatherer)
                                       .toList();
        System.out.println("Output 3 (Proportions): " + result3);
        // Expected Output: []
    }
}
```

**Input:**
```
Input 1: [1, 2, 3, 4]
Input 2: [1, -1, 5, -5]
Input 3: []
```

**Output:**
```
Output 1 (Proportions): [0.1, 0.2, 0.3, 0.4]

---
Input 2: [1, -1, 5, -5]
Output 2 (Proportions): []

---
Input 3: []
Output 3 (Proportions): []
```

**Explanation:**

For `Input 1`, the `integrator` adds `1, 2, 3, 4` to the `ArrayList` state. So, the final `state` (list) will be `[1, 2, 3, 4]`.
When the `finisher` is called with this list:
1.  `totalSum` is calculated as `1 + 2 + 3 + 4 = 10.0`.
2.  The `finisher` then streams `[1, 2, 3, 4]` and maps each element:
    *   `1 / 10.0 = 0.1`
    *   `2 / 10.0 = 0.2`
    *   `3 / 10.0 = 0.3`
    *   `4 / 10.0 = 0.4`
The resulting `Stream<Double>` `[0.1, 0.2, 0.3, 0.4]` is then passed downstream.

For `Input 2` and `Input 3`, the `totalSum` becomes `0.0`. The `finisher`'s conditional check `if (totalSum == 0)` correctly handles this by returning `Stream.empty()`, preventing division-by-zero errors and producing an empty output.

---

In summary, the `Gatherer.Finisher` is a powerful component that enables `Gatherer`s to perform final, aggregate computations on the accumulated internal state, producing a new stream of results that are often dependent on the entire context of the processed elements.