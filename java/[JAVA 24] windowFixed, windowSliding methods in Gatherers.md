This document provides a detailed explanation of `windowFixed` and `windowSliding` methods within the `java.util.stream.Gatherers` API, introduced in Java 21 as a powerful extension to the Stream API.

---

# Gatherers: `windowFixed` and `windowSliding` Methods

## Introduction to Gatherers

`Gatherers` are a new type of intermediate operation in the Java Stream API (introduced in Java 21) that bridge the gap between simple element-wise transformations (`map`, `filter`) and terminal reductions (`collect`). They allow for stateful processing of stream elements, enabling operations like windowing, splitting, or merging elements before passing them down the stream.

Unlike `Collectors` which produce a single result from a stream, `Gatherers` consume a stream of elements and produce *another stream* of elements (or collections of elements), making them intermediate operations.

The `windowFixed` and `windowSliding` methods are powerful tools for grouping sequential elements from a stream into sub-lists (windows) based on specific sizing and movement rules.

## 1. `Gatherers.windowFixed(int windowSize)`

### Description

The `windowFixed` gatherer divides the input stream into fixed-size "windows" (lists). Each window contains a specified number of elements. When the input stream has fewer elements remaining than the `windowSize`, the last window will contain the remaining elements and will be smaller than `windowSize`.

### Method Signature

```java
public static <T> Gatherer<T, ?, List<T>> windowFixed(int windowSize)
```

-   `T`: The type of elements in the input stream.
-   `windowSize`: The desired size of each window. Must be a positive integer. An `IllegalArgumentException` is thrown if `windowSize` is less than or equal to zero.
-   Returns: A `Gatherer` that takes `T` elements and emits `List<T>` (each list representing a window).

### Behavior and Characteristics

*   **Fixed Size:** All windows (except possibly the last one) will have exactly `windowSize` elements.
*   **Non-overlapping:** Windows do not share elements. They are distinct, contiguous blocks of the stream.
*   **Last Window:** If the total number of elements in the stream is not a perfect multiple of `windowSize`, the last window will contain the remaining elements and thus will be smaller than `windowSize`.
*   **Empty Stream:** If the input stream is empty, no windows are produced.

### Use Cases

*   **Batch Processing:** Grouping items into fixed-size batches for processing (e.g., sending records to a database in chunks, processing files in fixed-size blocks).
*   **Display Pagination:** Grouping data for displaying in pages or columns.
*   **Simple Grouping:** When you need to segment a sequence into equally sized parts.

### Example: `windowFixed`

Let's process a stream of integers, grouping them into windows of 3.

```java
import java.util.List;
import java.util.stream.Gatherers;
import java.util.stream.Stream;

public class WindowFixedExample {
    public static void main(String[] args) {
        System.out.println("--- Example 1: windowSize = 3 ---");
        Stream<Integer> numbers1 = Stream.of(1, 2, 3, 4, 5, 6, 7, 8);
        System.out.println("Input Stream: 1, 2, 3, 4, 5, 6, 7, 8");

        numbers1.gather(Gatherers.windowFixed(3))
                .forEach(window -> System.out.println("Window: " + window));

        System.out.println("\n--- Example 2: windowSize = 4 (Exact fit) ---");
        Stream<String> words2 = Stream.of("alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta");
        System.out.println("Input Stream: alpha, beta, gamma, delta, epsilon, zeta, eta, theta");

        words2.gather(Gatherers.windowFixed(4))
              .forEach(window -> System.out.println("Window: " + window));

        System.out.println("\n--- Example 3: windowSize = 5 (Partial last window) ---");
        Stream<Character> chars3 = Stream.of('a', 'b', 'c', 'd', 'e', 'f', 'g');
        System.out.println("Input Stream: a, b, c, d, e, f, g");

        chars3.gather(Gatherers.windowFixed(5))
              .forEach(window -> System.out.println("Window: " + window));

        try {
            System.out.println("\n--- Example 4: Invalid windowSize (throws IllegalArgumentException) ---");
            Stream.of(1, 2, 3).gather(Gatherers.windowFixed(0));
        } catch (IllegalArgumentException e) {
            System.out.println("Caught expected exception: " + e.getMessage());
        }
    }
}
```

### Output (WindowFixedExample.java)

```
--- Example 1: windowSize = 3 ---
Input Stream: 1, 2, 3, 4, 5, 6, 7, 8
Window: [1, 2, 3]
Window: [4, 5, 6]
Window: [7, 8]

--- Example 2: windowSize = 4 (Exact fit) ---
Input Stream: alpha, beta, gamma, delta, epsilon, zeta, eta, theta
Window: [alpha, beta, gamma, delta]
Window: [epsilon, zeta, eta, theta]

--- Example 3: windowSize = 5 (Partial last window) ---
Input Stream: a, b, c, d, e, f, g
Window: [a, b, c, d, e]
Window: [f, g]

--- Example 4: Invalid windowSize (throws IllegalArgumentException) ---
Caught expected exception: windowSize must be positive
```

---

## 2. `Gatherers.windowSliding(int windowSize, int slideSize)`

### Description

The `windowSliding` gatherer creates "sliding" windows over the input stream. Each window has a fixed `windowSize`, and subsequent windows start after a `slideSize` number of elements. This allows for overlapping windows (when `slideSize < windowSize`), non-overlapping windows (when `slideSize == windowSize`), or windows with gaps (when `slideSize > windowSize`).

### Method Signature

```java
public static <T> Gatherer<T, ?, List<T>> windowSliding(int windowSize, int slideSize)
```

-   `T`: The type of elements in the input stream.
-   `windowSize`: The desired size of each window. Must be a positive integer.
-   `slideSize`: The number of elements to advance for the next window. Must be a positive integer.
-   Returns: A `Gatherer` that takes `T` elements and emits `List<T>` (each list representing a window).
-   `IllegalArgumentException` is thrown if `windowSize` or `slideSize` is less than or equal to zero.

### Key Parameters Explained

*   **`windowSize`**: Determines how many elements are included in each generated `List`.
*   **`slideSize`**: Determines how much the "window" moves forward after emitting a list.
    *   **`slideSize < windowSize` (Overlapping Windows):** The most common use case. Elements appear in multiple adjacent windows.
    *   **`slideSize == windowSize` (Non-overlapping, like `windowFixed`):** Each window starts immediately after the previous one ends. This behaves identically to `windowFixed(windowSize)`.
    *   **`slideSize > windowSize` (Windows with Gaps):** Some elements might be skipped and not appear in any window.

### Behavior and Characteristics

*   **Fixed Window Size (mostly):** All windows will have `windowSize` elements, *unless* there aren't enough remaining elements in the stream to fill a full window, in which case the last window might be smaller.
*   **Overlapping/Gaps:** Behavior depends entirely on the relationship between `windowSize` and `slideSize`.
*   **Initial Window:** The first window starts at the beginning of the stream.
*   **Partial Last Window:** Similar to `windowFixed`, if the stream ends before a full `windowSize` can be formed for the current slide, the remaining elements will form a partial last window.
*   **Empty Stream:** If the input stream is empty, no windows are produced.

### Use Cases

*   **Moving Averages/Calculations:** Calculating a running average or sum over a specific number of data points in a time series.
*   **Signal Processing:** Analyzing data points in a continuous, shifting segment.
*   **Pattern Recognition:** Detecting sequences or patterns within a larger stream of data.
*   **Text Analysis:** Analyzing n-grams (sequences of n words/characters) in text.

### Example: `windowSliding`

Let's explore different `windowSize` and `slideSize` combinations.

```java
import java.util.List;
import java.util.stream.Gatherers;
import java.util.stream.Stream;

public class WindowSlidingExample {
    public static void main(String[] args) {
        List<Integer> data = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        System.out.println("Input Stream: " + data);

        System.out.println("\n--- Example 1: Overlapping (windowSize = 3, slideSize = 1) ---");
        // Each window slides by 1 element, heavily overlapping
        Stream.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
              .gather(Gatherers.windowSliding(3, 1))
              .forEach(window -> System.out.println("Window: " + window));

        System.out.println("\n--- Example 2: Partial Overlap (windowSize = 4, slideSize = 2) ---");
        // Each window slides by 2 elements
        Stream.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
              .gather(Gatherers.windowSliding(4, 2))
              .forEach(window -> System.out.println("Window: " + window));

        System.out.println("\n--- Example 3: Non-overlapping (windowSize = 3, slideSize = 3) ---");
        // Behaves like windowFixed(3)
        Stream.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
              .gather(Gatherers.windowSliding(3, 3))
              .forEach(window -> System.out.println("Window: " + window));

        System.out.println("\n--- Example 4: Windows with Gaps (windowSize = 2, slideSize = 4) ---");
        // Some elements are skipped between windows
        Stream.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
              .gather(Gatherers.windowSliding(2, 4))
              .forEach(window -> System.out.println("Window: " + window));

        System.out.println("\n--- Example 5: Stream smaller than windowSize (partial windows) ---");
        List<String> shortData = List.of("A", "B", "C");
        System.out.println("Input Stream: " + shortData);
        Stream.of("A", "B", "C")
              .gather(Gatherers.windowSliding(5, 1)) // windowSize 5, slide 1
              .forEach(window -> System.out.println("Window: " + window));

        try {
            System.out.println("\n--- Example 6: Invalid slideSize (throws IllegalArgumentException) ---");
            Stream.of(1, 2, 3).gather(Gatherers.windowSliding(2, 0));
        } catch (IllegalArgumentException e) {
            System.out.println("Caught expected exception: " + e.getMessage());
        }
    }
}
```

### Output (WindowSlidingExample.java)

```
Input Stream: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

--- Example 1: Overlapping (windowSize = 3, slideSize = 1) ---
Window: [1, 2, 3]
Window: [2, 3, 4]
Window: [3, 4, 5]
Window: [4, 5, 6]
Window: [5, 6, 7]
Window: [6, 7, 8]
Window: [7, 8, 9]
Window: [8, 9, 10]
Window: [9, 10]    <-- Partial window
Window: [10]       <-- Partial window

--- Example 2: Partial Overlap (windowSize = 4, slideSize = 2) ---
Window: [1, 2, 3, 4]
Window: [3, 4, 5, 6]
Window: [5, 6, 7, 8]
Window: [7, 8, 9, 10]
Window: [9, 10]    <-- Partial window

--- Example 3: Non-overlapping (windowSize = 3, slideSize = 3) ---
Window: [1, 2, 3]
Window: [4, 5, 6]
Window: [7, 8, 9]
Window: [10]       <-- Partial window

--- Example 4: Windows with Gaps (windowSize = 2, slideSize = 4) ---
Window: [1, 2]
Window: [5, 6]
Window: [9, 10]

--- Example 5: Stream smaller than windowSize (partial windows) ---
Input Stream: [A, B, C]
Window: [A, B, C]

--- Example 6: Invalid slideSize (throws IllegalArgumentException) ---
Caught expected exception: slideSize must be positive
```

---

## Key Differences and When to Use Which

| Feature          | `Gatherers.windowFixed(windowSize)`                                | `Gatherers.windowSliding(windowSize, slideSize)`                         |
| :--------------- | :----------------------------------------------------------------- | :----------------------------------------------------------------------- |
| **Overlap**      | Never. Windows are completely distinct.                            | Can overlap (`slideSize < windowSize`), be contiguous (`slideSize == windowSize`), or have gaps (`slideSize > windowSize`). |
| **Window Start** | Each window starts immediately after the previous one ends.        | Each window starts `slideSize` elements after the previous one started. |
| **Complexity**   | Simpler concept, ideal for clear segmentation.                     | More flexible, but requires careful consideration of `slideSize`.        |
| **Use Cases**    | Batching, simple pagination, fixed-size data chunking.             | Moving averages, time-series analysis, N-gram generation, real-time analytics requiring overlapping views. |
| **Parameters**   | Takes only `windowSize`.                                           | Takes both `windowSize` and `slideSize`.                                |

Choose `windowFixed` when you need to process distinct, non-overlapping chunks of a stream.
Choose `windowSliding` when you need a "moving view" of your stream, allowing for overlapping analysis or specific step-through patterns.

## Important Notes

*   **Java Version:** `Gatherers` were introduced as a preview feature in Java 21 and became a standard feature in Java 22. Ensure you are using Java 21 or later.
*   **Intermediate Operation:** Remember that `gather()` is an intermediate operation. You need a terminal operation (like `forEach`, `collect`, `toList`, etc.) after it for the stream pipeline to execute.
*   **`List<T>` Output:** Both methods produce a `Stream<List<T>>`, meaning each element in the output stream is itself a `List` containing the elements of that specific window.
*   **Error Handling:** Both methods throw `IllegalArgumentException` if `windowSize` or `slideSize` (for `windowSliding`) is less than or equal to zero.