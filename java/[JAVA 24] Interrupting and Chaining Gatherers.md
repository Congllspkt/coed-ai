Java 24 introduces a powerful new intermediate stream operation called `Stream.gather()`, along with the `java.util.stream.Gatherer` interface. This feature is currently a preview feature. Gatherers allow for highly customizable, stateful intermediate operations that can process elements, maintain state, and emit zero, one, or multiple elements for each input element.

This document will delve into two key aspects of `Gatherers`: **Chaining** them together and **Interrupting** the stream processing from within a Gatherer.

---

## Table of Contents

1.  **Introduction to Gatherers (Java 24 Preview)**
2.  **Chaining Gatherers**
    *   Explanation
    *   Example: Prefix Sum followed by Filtering
    *   Code Example: `ChainingGatherers.java`
    *   Input/Output
3.  **Interrupting Gatherers**
    *   Explanation
    *   Mechanism: `Optional.empty()` from Integrator
    *   Example: Limiting Processing Based on a Condition
    *   Code Example: `InterruptingGatherer.java`
    *   Input/Output
4.  **Chaining and Interrupting Together**
    *   Explanation
    *   Example: Prefix Sum followed by Interrupt on Threshold
    *   Code Example: `ChainingAndInterrupting.java`
    *   Input/Output
5.  **How to Run Java 24 Preview Features**
6.  **Key Takeaways**

---

## 1. Introduction to Gatherers (Java 24 Preview)

A `Gatherer` is a new building block for the Stream API, designed for operations that are more complex than simple `map`, `filter`, or `reduce`, but still fit within the intermediate operation paradigm. They are stateful and can produce a varying number of output elements for a given input element or set of input elements.

The `Gatherer` interface defines several components:

*   **`initializer()`**: A `Supplier<S>` that creates the initial state `S` for the gatherer.
*   **`integrator()`**: A `Gatherer.Integrator<S, T, R>` which is a `(S state, T element, Downstream<? super R> downstream) -> S` (for non-short-circuiting) or `(S state, T element, Downstream<? super R> downstream) -> Optional<S>` (for short-circuiting). This is the core logic that processes an input `T` using the current `state S`, potentially emits `R` elements to the `downstream`, and returns the updated `state S`.
*   **`combiner()`**: An `BinaryOperator<S>` for combining states in parallel streams (optional).
*   **`finisher()`**: A `Function<S, R>` or `Gatherer.Finisher<S, R>` for processing the final state after all input elements have been processed (optional).
*   **`reducer()`**: For specialized cases of reduction (optional).

The `gather()` method on `Stream` takes a `Gatherer` instance and returns a new `Stream`.

```java
// Basic structure
public interface Gatherer<T, S, R> {
    // ... methods ...
}

// How to use
Stream<T> input = ...;
Stream<R> output = input.gather(myGatherer);
```

**Note:** As of Java 24, `Gatherer` is a preview API. You need to enable preview features to compile and run code using it.

---

## 2. Chaining Gatherers

Just like other intermediate stream operations (`map`, `filter`, `sorted`), the `Stream.gather()` method returns a new `Stream`. This means you can chain multiple `gather()` calls together, or combine `gather()` with other standard stream operations. Chaining Gatherers allows you to build complex, multi-stage, stateful transformations on a stream.

### Explanation

When you chain `gather()` calls:

```java
stream.gather(gatherer1).gather(gatherer2).gather(gatherer3)...
```

1.  `gatherer1` processes the elements from the original `stream`.
2.  The output elements produced by `gatherer1` form the input stream for `gatherer2`.
3.  The output elements produced by `gatherer2` form the input stream for `gatherer3`, and so on.

This composition allows for modular design, where each Gatherer performs a specific, stateful transformation, and their results are passed along the pipeline.

### Example: Prefix Sum followed by Filtering

Let's create two Gatherers and chain them:
1.  **`PrefixSumGatherer`**: Takes a stream of numbers and emits their running prefix sums.
    *   Input: `[1, 2, 3, 4]`
    *   Output: `[1, 3, 6, 10]`
2.  **`FilterEvenGatherer`**: Takes a stream of numbers and filters out only the even ones.
    *   Input: `[1, 3, 6, 10]`
    *   Output: `[6, 10]`

### Code Example: `ChainingGatherers.java`

```java
// ChainingGatherers.java
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Gatherer; // Make sure to import Gatherer

public class ChainingGatherers {

    public static void main(String[] args) {
        List<Integer> numbers = List.of(1, 2, 3, 4, 5);
        System.out.println("Original numbers: " + numbers);

        // --- Gatherer 1: Calculates prefix sums ---
        // State 'S' is an Integer representing the current accumulated sum
        // Input 'T' is Integer, Output 'R' is Integer
        Gatherer<Integer, Integer, Integer> prefixSumGatherer = Gatherer.of(
            () -> 0, // Initializer: state starts at 0
            (currentSum, element, downstream) -> { // Integrator: processes each element
                int newSum = currentSum + element;
                downstream.accept(newSum); // Emit the new prefix sum
                System.out.println("  PrefixSumGatherer: Input=" + element + ", CurrentSum=" + currentSum + ", NewSum=" + newSum + ", Emitted=" + newSum);
                return newSum; // Update the state for the next element
            }
        );

        // --- Gatherer 2: Filters out odd numbers ---
        // State 'S' is Void (no state needed for this simple filter)
        // Input 'T' is Integer (from prefixSumGatherer), Output 'R' is Integer
        Gatherer<Integer, Void, Integer> filterEvenGatherer = Gatherer.of(
            Gatherer.Integrator.of((state, element, downstream) -> { // Integrator
                if (element % 2 == 0) {
                    downstream.accept(element); // Emit only if even
                    System.out.println("    FilterEvenGatherer: Input=" + element + ", Emitted=" + element + " (Even)");
                } else {
                    System.out.println("    FilterEvenGatherer: Input=" + element + ", Skipped (Odd)");
                }
                return state; // No state change
            })
        );

        // Chain the two gatherers
        List<Integer> result = numbers.stream()
            .gather(prefixSumGatherer)  // First gatherer: computes prefix sums
            .gather(filterEvenGatherer) // Second gatherer: filters even numbers from the prefix sums
            .collect(Collectors.toList());

        System.out.println("Final Result (Chained Gatherers): " + result);
    }
}
```

### Input/Output

**Input:**
`List.of(1, 2, 3, 4, 5)`

**Output:**

```
Original numbers: [1, 2, 3, 4, 5]
  PrefixSumGatherer: Input=1, CurrentSum=0, NewSum=1, Emitted=1
    FilterEvenGatherer: Input=1, Skipped (Odd)
  PrefixSumGatherer: Input=2, CurrentSum=1, NewSum=3, Emitted=3
    FilterEvenGatherer: Input=3, Skipped (Odd)
  PrefixSumGatherer: Input=3, CurrentSum=3, NewSum=6, Emitted=6
    FilterEvenGatherer: Input=6, Emitted=6 (Even)
  PrefixSumGatherer: Input=4, CurrentSum=6, NewSum=10, Emitted=10
    FilterEvenGatherer: Input=10, Emitted=10 (Even)
  PrefixSumGatherer: Input=5, CurrentSum=10, NewSum=15, Emitted=15
    FilterEvenGatherer: Input=15, Skipped (Odd)
Final Result (Chained Gatherers): [6, 10]
```

---

## 3. Interrupting Gatherers

One of the most powerful features of Gatherers is their ability to **short-circuit** or **interrupt** the stream processing. This means a Gatherer can decide, based on its internal state or an input element, that no further elements from the upstream should be processed. This is similar to how `Stream.anyMatch()` or `Stream.findFirst()` can stop a pipeline early.

### Explanation

A `Gatherer` can signal an interruption by returning `Optional.empty()` from its `integrator` function.

*   If `integrator` returns `Optional.of(newState)`: The Gatherer continues processing, and `newState` becomes the current state for the next element.
*   If `integrator` returns `Optional.empty()`:
    *   The Gatherer's state is discarded.
    *   No more upstream elements are passed to this Gatherer's `integrator`.
    *   The `finisher()` method (if present) for *this Gatherer* is called immediately.
    *   Crucially, **no further elements from the upstream source will be processed by any subsequent intermediate operations or the terminal operation.** The stream processing effectively stops at this point for all downstream operations.

This is extremely useful for implementing "take while" or "limit until condition" type operations directly within the stream pipeline.

### Example: Limiting Processing Based on a Condition (Sum Threshold)

Let's create a Gatherer that processes integers and stops as soon as the cumulative sum of processed elements exceeds a certain threshold (e.g., 10).

*   Input: `[1, 2, 3, 4, 5, 6, 7]`
*   Expected output: `[1, 2, 3, 4]` (because `1+2+3+4=10`, but `1+2+3+4+5=15`, which exceeds 10, so processing stops before 5 is processed).

### Code Example: `InterruptingGatherer.java`

```java
// InterruptingGatherer.java
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.Gatherer;

public class InterruptingGatherer {

    public static void main(String[] args) {
        List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7);
        System.out.println("Original numbers: " + numbers);

        // --- Gatherer: Stops when cumulative sum exceeds a threshold ---
        // State 'S' is an Integer representing the current cumulative sum
        // Input 'T' is Integer, Output 'R' is Integer
        Gatherer<Integer, Integer, Integer> limitSumGatherer = Gatherer.of(
            () -> 0, // Initializer: state starts at 0 (current sum)
            (currentSum, element, downstream) -> { // Integrator
                int newSum = currentSum + element;

                System.out.println("  LimitSumGatherer: Processing " + element + ". Current sum: " + currentSum + " -> new sum would be " + newSum);

                if (newSum > 10) { // Check if the sum *after* adding the current element exceeds the threshold
                    System.out.println("    >>> INTERRUPTING: Cumulative sum (" + newSum + ") exceeded 10. Stopping stream processing.");
                    // Return Optional.empty() to signal interruption
                    return Optional.empty();
                }

                downstream.accept(element); // Emit the element if not interrupted
                return Optional.of(newSum); // Update the state with the new sum
            },
            (finalSum, downstream) -> { // Finisher: will be called if not interrupted or immediately on interrupt
                System.out.println("  Finisher called. Final sum state: " + finalSum);
            }
        );

        List<Integer> result = numbers.stream()
            .gather(limitSumGatherer)
            .collect(Collectors.toList());

        System.out.println("Final Result (Interrupting Gatherer): " + result);
    }
}
```

### Input/Output

**Input:**
`List.of(1, 2, 3, 4, 5, 6, 7)`

**Output:**

```
Original numbers: [1, 2, 3, 4, 5, 6, 7]
  LimitSumGatherer: Processing 1. Current sum: 0 -> new sum would be 1
  LimitSumGatherer: Processing 2. Current sum: 1 -> new sum would be 3
  LimitSumGatherer: Processing 3. Current sum: 3 -> new sum would be 6
  LimitSumGatherer: Processing 4. Current sum: 6 -> new sum would be 10
  LimitSumGatherer: Processing 5. Current sum: 10 -> new sum would be 15
    >>> INTERRUPTING: Cumulative sum (15) exceeded 10. Stopping stream processing.
  Finisher called. Final sum state: 10
Final Result (Interrupting Gatherer): [1, 2, 3, 4]
```
Notice that `Finisher called. Final sum state: 10` indicates the state *before* the element causing the interrupt was processed. The element `5` was *not* emitted.

---

## 4. Chaining and Interrupting Together

You can combine chaining and interruption to build very sophisticated stream pipelines. An interruption in one Gatherer in a chain will stop the entire pipeline for all subsequent operations (including other Gatherers or terminal operations).

### Explanation

Consider the sequence:
`stream.gather(gathererA).gather(gathererB).gather(gathererC).collect(...)`

If `gathererB` decides to interrupt:
1.  `gathererA` processes its input and emits to `gathererB`.
2.  `gathererB` processes its input (from `gathererA`).
3.  When `gathererB`'s `integrator` returns `Optional.empty()`:
    *   No more elements are pulled from `gathererA`'s output.
    *   No more elements are pulled from the original `stream`.
    *   `gathererB`'s `finisher` is called.
    *   `gathererC` (and any subsequent operations) will not receive any more elements.
    *   The `collect()` operation will only receive elements that were emitted *before* the interruption.

### Example: Prefix Sum followed by Interrupt on Threshold

We'll re-use the `PrefixSumGatherer` and then apply a new `InterruptingGatherer` that stops when the *prefix sum itself* exceeds a threshold.

1.  **`PrefixSumGatherer`**: (Same as before) `[1, 2, 3, 4, 5]` -> `[1, 3, 6, 10, 15]`
2.  **`InterruptPrefixSumGatherer`**: Takes prefix sums and stops processing when a prefix sum exceeds 10.
    *   Input: `[1, 3, 6, 10, 15, ...]`
    *   Output: `[1, 3, 6, 10]` (stops when `15` is received)

### Code Example: `ChainingAndInterrupting.java`

```java
// ChainingAndInterrupting.java
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.Gatherer;

public class ChainingAndInterrupting {

    public static void main(String[] args) {
        List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7);
        System.out.println("Original numbers: " + numbers);

        // --- Gatherer 1: Calculates prefix sums ---
        Gatherer<Integer, Integer, Integer> prefixSumGatherer = Gatherer.of(
            () -> 0,
            (currentSum, element, downstream) -> {
                int newSum = currentSum + element;
                downstream.accept(newSum); // Emit the new prefix sum
                System.out.println("  PrefixSumGatherer: Input=" + element + ", NewSum=" + newSum + ", Emitted=" + newSum);
                return newSum;
            }
        );

        // --- Gatherer 2: Interrupts when the incoming prefix sum exceeds a threshold ---
        // Note: The state (Integer) is just to demonstrate its presence, it's not strictly
        //       necessary for this particular logic, as the decision is made on the 'element'.
        Gatherer<Integer, Integer, Integer> interruptOnPrefixSumGatherer = Gatherer.of(
            () -> 0, // Initializer: state starts at 0 (can be anything if not used)
            (currentState, prefixSumElement, downstream) -> { // Integrator
                System.out.println("    InterruptOnPrefixSumGatherer: Processing incoming prefix sum " + prefixSumElement);
                if (prefixSumElement > 10) { // Check the incoming prefix sum
                    System.out.println("      >>> INTERRUPTING CHAIN: Prefix sum (" + prefixSumElement + ") exceeded 10. Stopping stream.");
                    return Optional.empty(); // Signal interruption
                }
                downstream.accept(prefixSumElement); // Emit the prefix sum if not interrupted
                return Optional.of(currentState); // No state change needed for this logic
            }
        );

        // Chain the two gatherers
        List<Integer> result = numbers.stream()
            .gather(prefixSumGatherer)             // First: generates prefix sums
            .gather(interruptOnPrefixSumGatherer)  // Second: interrupts if a prefix sum is too high
            .collect(Collectors.toList());

        System.out.println("Final Result (Chained & Interrupting Gatherers): " + result);
    }
}
```

### Input/Output

**Input:**
`List.of(1, 2, 3, 4, 5, 6, 7)`

**Output:**

```
Original numbers: [1, 2, 3, 4, 5, 6, 7]
  PrefixSumGatherer: Input=1, NewSum=1, Emitted=1
    InterruptOnPrefixSumGatherer: Processing incoming prefix sum 1
  PrefixSumGatherer: Input=2, NewSum=3, Emitted=3
    InterruptOnPrefixSumGatherer: Processing incoming prefix sum 3
  PrefixSumGatherer: Input=3, NewSum=6, Emitted=6
    InterruptOnPrefixSumGatherer: Processing incoming prefix sum 6
  PrefixSumGatherer: Input=4, NewSum=10, Emitted=10
    InterruptOnPrefixSumGatherer: Processing incoming prefix sum 10
  PrefixSumGatherer: Input=5, NewSum=15, Emitted=15
    InterruptOnPrefixSumGatherer: Processing incoming prefix sum 15
      >>> INTERRUPTING CHAIN: Prefix sum (15) exceeded 10. Stopping stream.
Final Result (Chained & Interrupting Gatherers): [1, 3, 6, 10]
```
The `PrefixSumGatherer` initially computes `15` and emits it, but then the `InterruptOnPrefixSumGatherer` receives `15` and immediately signals an interruption, preventing `15` from being added to the final result list and stopping any further elements from the original `numbers` list from being processed.

---

## 5. How to Run Java 24 Preview Features

Since `Gatherer` is a preview feature, you need to enable it when compiling and running your Java code.

1.  **Save the code:** Save any of the `.java` files (e.g., `ChainingGatherers.java`).
2.  **Compile:** Use `javac` with the `--enable-preview` and `--release` flags. The release version should be at least `22` (or `23`/`24` if available, depending on your JDK version).

    ```bash
    javac --enable-preview --release 22 ChainingGatherers.java
    ```
3.  **Run:** Use `java` with the `--enable-preview` flag.

    ```bash
    java --enable-preview ChainingGatherers
    ```

---

## 6. Key Takeaways

*   **Gatherers are for Stateful Intermediate Operations:** They fill a gap in the Stream API for complex transformations that need to maintain state across elements.
*   **Chaining for Modularity:** Like other stream operations, `gather()` returns a `Stream`, allowing you to compose multiple Gatherers or other stream operations for powerful pipelines.
*   **Interruption for Short-Circuiting:** Returning `Optional.empty()` from the `integrator()` method provides a mechanism to gracefully stop stream processing early, based on a condition within the Gatherer's logic. This is crucial for "take while" or "limit until" scenarios.
*   **Impact of Interruption:** When a Gatherer interrupts, the entire stream pipeline stops. No more elements are pulled from the upstream, and no more elements are passed downstream. The `finisher()` of the interrupting Gatherer is called immediately.
*   **Preview Feature:** Remember that `Gatherer` is a preview API and may change in future Java versions. Always enable preview features when compiling and running.

Gatherers significantly enhance the flexibility and power of the Java Stream API, enabling more expressive and efficient solutions for complex data processing tasks.