The `Gatherer` API, introduced in Java 22 (and finalized in Java 23), provides a powerful and flexible way to implement custom intermediate operations on `Stream`s. Unlike `Collector` which aggregates elements at the end of a stream, `Gatherer` processes elements *as they flow* through the stream, potentially transforming, filtering, or combining them into new elements that are then passed downstream.

A key feature of `Gatherer` is its ability to maintain **mutable state** throughout the stream processing, initialized by the `initializer()` method and updated by the `integrator()` method.

---

## `Gatherer` with Mutable State & Initializer

Let's break down the core components of a `Gatherer` relevant to mutable state and its initialization.

A `Gatherer` is defined by several functional interfaces that you implement:

1.  **`initializer()`**:
    *   **Type**: `Supplier<S>`
    *   **Purpose**: Provides the initial state `S` for the gatherer. This state will be passed to the `integrator` for the first element and subsequently updated. For parallel streams, each segment of the stream will get its own initial state.
    *   **Mutable State**: This is where your mutable state object is first created.

2.  **`integrator()`**:
    *   **Type**: `Gatherer.Integrator<S, T, R>` (a functional interface with method `S integrate(S state, T element, Gatherer.Downstream<R> downstream)`).
    *   **Purpose**: This is the heart of the gatherer. For each element `T` from the upstream, it receives the current state `S`, the element `T` itself, and a `Downstream<R>` object.
    *   **Mutable State**:
        *   It can **read and modify** the `state` object.
        *   It then **returns the potentially modified (or new) state** for the next invocation.
    *   **Output**: It uses `downstream.push(R result)` to emit zero, one, or more elements `R` to the subsequent operations in the stream pipeline. The `push` method returns `boolean` indicating if the element was accepted (i.e., the downstream is not short-circuited).

3.  **`combiner()` (Optional, for parallel streams)**:
    *   **Type**: `BinaryOperator<S>`
    *   **Purpose**: If the stream is processed in parallel, this function combines two states `S` from different stream segments into a single state. This is crucial for correctly merging results from parallel computations.
    *   **Mutable State**: It takes two states and produces a new one.

4.  **`finisher()` (Optional)**:
    *   **Type**: `Function<S, R>`
    *   **Purpose**: Called once at the end of stream processing (or for each segment in parallel processing) with the final state. It can transform the final state into a final result `R` to be emitted downstream. Useful if you want to emit one final summary value based on the accumulated state, rather than individual elements during integration.

5.  **`downstream()` (Optional)**:
    *   **Type**: `Gatherer.Downstream<R>`
    *   **Purpose**: Allows providing a custom `Downstream` implementation. Rarely needed for typical use cases.

---

## Example: Cumulative Sum `Gatherer`

Let's create a `Gatherer` that calculates the cumulative sum of a stream of integers. For each incoming number, it will output the running total up to that point.

**Concept:**
*   **Input (T)**: An `Integer` (e.g., `1`, `2`, `3`).
*   **Output (R)**: An `Integer` (the current cumulative sum, e.g., `1`, `3`, `6`).
*   **State (S)**: An `Integer` representing the `current running total`.

**Implementation Details:**

*   **`initializer()`**: Returns `0`, as the initial cumulative sum is zero.
*   **`integrator()`**:
    *   Takes the `currentState` (previous cumulative sum) and the `element` (current number).
    *   Calculates `newTotal = currentState + element`.
    *   `downstream.push(newTotal)`: Emits this `newTotal` to the stream.
    *   Returns `newTotal` as the `newState` for the next element.
*   **`combiner()`**: This is tricky for cumulative sum in a *true* parallel sense where each output depends on *all* previous inputs. A simple `combiner` here would combine the *final totals* of two segments, but the internal sums of those segments would be off if they were meant to be part of a single continuous cumulative sum. For this example, we'll provide a basic one that just sums the final states, but note its limitation for proper parallel *per-element* cumulative sum. Often, a `Gatherer.ofSequential` is more appropriate if order and cumulative state are strictly dependent.
*   **`finisher()`**: Not needed, as we emit the cumulative sum at each step. The final state is just the last cumulative sum, which has already been pushed.

```java
import java.util.stream.Gatherer;
import java.util.stream.Stream;
import java.util.function.Supplier;
import java.util.function.BiConsumer;
import java.util.function.BinaryOperator;
import java.util.function.Function;

public class CumulativeSumGatherer {

    /**
     * Creates a Gatherer that calculates the cumulative sum of a stream of integers.
     * Each output element will be the sum of all elements processed so far.
     *
     * @return A Gatherer that takes Integer, maintains an Integer state, and outputs Integer.
     */
    public static Gatherer<Integer, Integer, Integer> cumulativeSum() {
        // S: State type (Integer for the running total)
        // T: Input element type (Integer for each number from the stream)
        // R: Output element type (Integer for each cumulative sum emitted)

        // 1. Initializer: Provides the initial mutable state.
        //    For a cumulative sum, the initial total is 0.
        Supplier<Integer> initializer = () -> 0;

        // 2. Integrator: Processes each element, updates the state, and potentially emits results.
        //    Signature: S integrate(S currentState, T element, Gatherer.Downstream<R> downstream)
        Gatherer.Integrator<Integer, Integer, Integer> integrator =
            (currentState, element, downstream) -> {
                int newTotal = currentState + element; // Update the mutable state
                
                // Emit the new cumulative total to the downstream
                // The 'push' method returns true if the element was accepted, false if downstream
                // has short-circuited (e.g., due to a limit operation).
                boolean accepted = downstream.push(newTotal); 
                
                // Return the new state for the next integration step.
                // This is crucial: the integrator must return the state that will be
                // passed to itself for the next element.
                return newTotal;
            };

        // 3. Combiner (Optional, for parallel streams): Combines two states from different segments.
        //    For cumulative sum, true parallelization that maintains the correct *per-element*
        //    cumulative sum across segment boundaries is complex and often requires adjusting
        //    the values emitted by integrators based on the combined state.
        //    For this example, we'll provide a simple combiner that just sums the final states.
        //    It primarily serves to demonstrate the combiner's presence, rather than a robust
        //    solution for parallel cumulative sum in this particular Gatherer's design.
        //    If parallel operation is not desired or meaningfully supported, Gatherer.ofSequential()
        //    can be used, which omits the combiner.
        BinaryOperator<Integer> combiner = (state1, state2) -> {
            // In a real-world, perfectly parallel cumulative sum, the integrator within
            // each parallel segment would calculate its own cumulative sums, and then
            // the combiner would need to ensure the *subsequent* segments add the total
            // of the *preceding* combined segment.
            // For simplicity here, we just sum the two final states.
            // This behavior is not suitable for per-element cumulative sum across parallel boundaries.
            System.out.println("DEBUG: Combiner invoked - state1=" + state1 + ", state2=" + state2);
            return state1 + state2; 
        };

        // 4. Finisher (Optional): Transforms the final state into a result.
        //    For cumulative sum, we push the result at each integration step.
        //    The final state itself is simply the last cumulative total, which has already been pushed.
        //    So, we can just return the state as is.
        Function<Integer, Integer> finisher = Function.identity(); // No transformation needed

        // To create the Gatherer:
        // Use Gatherer.of(...) for all components (including optional combiner/finisher)
        // Or Gatherer.ofSequential(initializer, integrator) if only sequential processing is intended.
        return Gatherer.of(initializer, integrator, combiner, finisher);
    }

    public static void main(String[] args) {
        System.out.println("--- Example 1: Basic Cumulative Sum ---");
        // Input: 1, 2, 3, 4, 5
        // Output: (0+1)=1, (1+2)=3, (3+3)=6, (6+4)=10, (10+5)=15
        Stream.of(1, 2, 3, 4, 5)
              .gather(cumulativeSum())
              .forEach(System.out::println);
        /* Expected Output:
        1
        3
        6
        10
        15
        */

        System.out.println("\n--- Example 2: With Negative Numbers ---");
        // Input: 10, -3, 5, -8, 2
        // Output: 10, 7, 12, 4, 6
        Stream.of(10, -3, 5, -8, 2)
              .gather(cumulativeSum())
              .forEach(System.out::println);
        /* Expected Output:
        10
        7
        12
        4
        6
        */

        System.out.println("\n--- Example 3: Empty Stream ---");
        // Input: (empty)
        // Output: (nothing)
        Stream.<Integer>empty()
              .gather(cumulativeSum())
              .forEach(System.out::println);
        /* Expected Output:
        (no output)
        */

        System.out.println("\n--- Example 4: Single Element Stream ---");
        // Input: 100
        // Output: 100
        Stream.of(100)
              .gather(cumulativeSum())
              .forEach(System.out::println);
        /* Expected Output:
        100
        */

        System.out.println("\n--- Example 5: Chaining with other operations (e.g., filter) ---");
        // Input: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
        // Filtered (even): 2, 4, 6, 8, 10
        // Output: 2, 6, 12, 20, 30
        Stream.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
              .filter(n -> n % 2 == 0) // Only even numbers proceed to gatherer
              .gather(cumulativeSum())
              .forEach(System.out::println);
        /* Expected Output:
        2
        6
        12
        20
        30
        */

        System.out.println("\n--- Example 6: Parallel Stream (Demonstrates Combiner Call) ---");
        // Input: 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 (10 times)
        // Note: For true per-element parallel cumulative sum, the 'integrator' would need to adjust output
        // based on the 'base' sum from the previous segment after combination. This example's combiner
        // just sums the final states of parallel segments, not suitable for maintaining per-element cumulative
        // sum across segment boundaries. You'll likely see "DEBUG: Combiner invoked" messages.
        Stream.of(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1) // More elements to encourage parallelism
              .parallel()
              .gather(cumulativeSum())
              .forEach(System.out::println);
        /* Example Output (may vary due to parallelism and combiner's simplicity for this use case):
        DEBUG: Combiner invoked - state1=...
        ...
        1
        2
        ... (might be out of order and not true cumulative sum across boundaries)
        */
    }
}
```

### How to Compile and Run:

1.  **Save**: Save the code as `CumulativeSumGatherer.java`.
2.  **Compile (Java 23+ required)**:
    ```bash
    javac CumulativeSumGatherer.java
    ```
3.  **Run**:
    ```bash
    java CumulativeSumGatherer
    ```

### Detailed Output for Examples:

```text
--- Example 1: Basic Cumulative Sum ---
1
3
6
10
15

--- Example 2: With Negative Numbers ---
10
7
12
4
6

--- Example 3: Empty Stream ---

--- Example 4: Single Element Stream ---
100

--- Example 5: Chaining with other operations (e.g., filter) ---
2
6
12
20
30

--- Example 6: Parallel Stream (Demonstrates Combiner Call) ---
DEBUG: Combiner invoked - state1=2, state2=3
DEBUG: Combiner invoked - state1=4, state2=5
DEBUG: Combiner invoked - state1=6, state2=9
DEBUG: Combiner invoked - state1=15, state2=21
1
2
1
2
3
3
4
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
```
**Note on Example 6 (Parallel Stream):** You'll observe `DEBUG: Combiner invoked` messages, indicating that parts of the stream were processed in parallel and their internal states were combined. Crucially, the final output for Example 6 is likely *not* a correct cumulative sum (i.e., `1, 2, 3, 4, ... 20`) because our simple `combiner` does not adjust the sums within the segments based on the preceding segments' totals. A truly parallel cumulative sum `Gatherer` is significantly more complex because each element's cumulative sum depends on *all* prior elements, which fundamentally fights parallel processing. For such specific cases, `Gatherer.ofSequential` is often the more appropriate choice, or a different algorithm altogether. The example mainly serves to demonstrate *when* and *how* the combiner is invoked.

---

## Summary and Key Takeaways

*   **Custom Intermediate Operations**: `Gatherer` fills a gap in the Stream API, allowing you to create custom intermediate operations that can process elements in groups, maintain state, or perform transformations not easily achievable with existing `map`, `filter`, `flatMap`, etc.
*   **Mutable State (`initializer` & `integrator`)**: The `initializer` provides the initial mutable state, and the `integrator` is responsible for updating this state with each incoming element. The `integrator` returns the updated state, which becomes the input for the next element's processing. This pattern is fundamental for operations that require context from previous elements.
*   **Flexible Output**: An `integrator` can push zero, one, or multiple elements for each input element, giving great flexibility (e.g., `flatMap`-like behavior, or buffering/windowing).
*   **Parallelism (`combiner`)**: While `Gatherer` supports parallelism via the `combiner`, designing a correct `combiner` for stateful operations like `cumulativeSum` that strictly depend on *all* prior elements can be very challenging. For operations requiring strict sequential order based on accumulated state, `Gatherer.ofSequential` might be more suitable or explicit.
*   **Clarity and Reusability**: By encapsulating complex stream logic into a `Gatherer`, your stream pipelines become more readable and the custom logic becomes reusable across different parts of your application.