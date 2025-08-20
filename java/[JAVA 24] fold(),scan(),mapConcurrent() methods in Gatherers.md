`java.util.stream.Gatherers` is a powerful new addition to the Java Stream API, introduced as a preview feature in **JDK 22** and standardized in **JDK 23**. It provides a new type of intermediate stream operation called a "gatherer," which can transform elements from an upstream `Stream` into a downstream `Stream`, potentially changing the number of elements and performing stateful operations.

Unlike traditional intermediate operations (`map`, `filter`, `sorted`), gatherers are more flexible. They can:
*   Produce a different number of output elements for a given number of input elements (e.g., combining multiple inputs into one output, or expanding one input into multiple outputs).
*   Maintain internal state to process elements.

To use `Gatherers`, you invoke the `stream.gather()` method, passing an instance of a `Gatherer`.

Let's dive into `fold()`, `scan()`, and `mapConcurrent()`.

---

## 1. `Gatherers.fold()`

### Method Signature
```java
public static <T, R> Gatherer<T, ?, R> fold(Supplier<R> initial, BiFunction<R, ? super T, R> accumulator)
```

### Explanation
`Gatherers.fold()` is conceptually similar to `Stream.reduce()` or `Collectors.reducing()`, but it operates as an *intermediate* stream operation. It takes all elements from the upstream stream and "folds" them into a *single* result element. The resulting stream will therefore contain only one element (the final accumulated result).

*   **`initial` (Supplier<R>):** A `Supplier` that provides the initial value for the accumulation. This is the starting point for your reduction.
*   **`accumulator` (BiFunction<R, ? super T, R>):** A `BiFunction` that takes the current accumulated value (`R`) and the next element from the input stream (`T`), and returns a new accumulated value (`R`).

**Key Characteristics:**
*   **Single Output:** Regardless of how many elements are in the input stream, `fold()` will always produce exactly one element in the output stream, which is the final accumulated value.
*   **Stateful:** It maintains an internal state (the accumulated value) throughout its operation.
*   **Terminal-like Intermediate:** While it's an intermediate operation, its behavior of reducing the entire stream into one element makes it feel like a terminal operation that just happens to return a `Stream` with one element.

### When to Use
Use `fold()` when you want to aggregate all elements of a stream into a single summary value, and you want this aggregation to be part of an intermediate pipeline step rather than a terminal `collect()` operation. For example, summing all numbers, concatenating all strings, or collecting all elements into a single list.

### Example: Collecting all elements into a single List

#### Java Code
```java
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Gatherers;
import java.util.stream.Collectors;

public class FoldExample {
    public static void main(String[] args) {
        List<Integer> numbers = List.of(1, 2, 3, 4, 5);

        System.out.println("Original numbers: " + numbers);

        // Using Gatherers.fold to collect all numbers into a single list
        List<List<Integer>> foldedResult = numbers.stream()
            .gather(Gatherers.fold(
                () -> new ArrayList<>(), // Initial value: an empty ArrayList
                (list, item) -> {       // Accumulator: add the current item to the list
                    list.add(item);
                    return list; // Return the modified list
                }
            ))
            .collect(Collectors.toList()); // Collect the single resulting list

        System.out.println("Folded Result (List of lists): " + foldedResult);
        System.out.println("Single folded list: " + foldedResult.get(0));

        // Another common use case: Summing all numbers
        Integer sum = numbers.stream()
            .gather(Gatherers.fold(
                () -> 0, // Initial value: 0
                (currentSum, item) -> currentSum + item // Accumulator: add item to current sum
            ))
            .findFirst() // Get the single element from the stream
            .orElse(0);

        System.out.println("Folded Sum: " + sum);
    }
}
```

#### Input
`List.of(1, 2, 3, 4, 5)`

#### Output
```
Original numbers: [1, 2, 3, 4, 5]
Folded Result (List of lists): [[1, 2, 3, 4, 5]]
Single folded list: [1, 2, 3, 4, 5]
Folded Sum: 15
```

---

## 2. `Gatherers.scan()`

### Method Signature
```java
public static <T, R> Gatherer<T, ?, R> scan(Supplier<R> initial, BiFunction<R, ? super T, R> accumulator)
```

### Explanation
`Gatherers.scan()` has the exact same signature as `fold()`, but its behavior is fundamentally different. Instead of producing a single final result, `scan()` produces a stream of *intermediate accumulated results*. For each input element, it applies the accumulator and emits the current accumulated state. Think of it as a "running total" or "prefix sum" operation.

*   **`initial` (Supplier<R>):** A `Supplier` that provides the initial value for the accumulation.
*   **`accumulator` (BiFunction<R, ? super T, R>):** A `BiFunction` that takes the current accumulated value (`R`) and the next element from the input stream (`T`), and returns a new accumulated value (`R`). This new value is then emitted to the downstream stream.

**Key Characteristics:**
*   **Multiple Outputs:** For each element processed from the input stream, `scan()` produces one element in the output stream. The output stream will have the same number of elements as the input stream.
*   **Stateful:** It maintains an internal state (the accumulated value) that is updated with each element and then emitted.
*   **Running Accumulation:** Useful for tracking changes or states through a sequence of operations.

### When to Use
Use `scan()` when you need to see the result of an accumulation at each step of processing. Common use cases include calculating running sums, running averages, maintaining a list of elements processed so far, or tracking state changes in a sequence.

### Example: Calculating running sums

#### Java Code
```java
import java.util.List;
import java.util.stream.Gatherers;
import java.util.stream.Collectors;

public class ScanExample {
    public static void main(String[] args) {
        List<Integer> numbers = List.of(1, 2, 3, 4, 5);

        System.out.println("Original numbers: " + numbers);

        // Using Gatherers.scan to get a running sum
        List<Integer> runningSums = numbers.stream()
            .gather(Gatherers.scan(
                () -> 0, // Initial sum
                (currentSum, item) -> currentSum + item // Accumulator: add current item to sum
            ))
            .collect(Collectors.toList());

        System.out.println("Running Sums: " + runningSums);

        // Example: Tracking a running list of elements seen so far
        List<List<String>> runningLists = List.of("apple", "banana", "cherry").stream()
            .gather(Gatherers.scan(
                () -> new ArrayList<String>(), // Initial empty list
                (list, item) -> {
                    // Create a new list to avoid modifying previous emitted lists directly
                    // (important for immutable streams if intermediate lists are used later)
                    ArrayList<String> newList = new ArrayList<>(list);
                    newList.add(item);
                    return newList;
                }
            ))
            .collect(Collectors.toList());

        System.out.println("Running Lists: " + runningLists);
    }
}
```

#### Input
`List.of(1, 2, 3, 4, 5)` for the first example.
`List.of("apple", "banana", "cherry")` for the second example.

#### Output
```
Original numbers: [1, 2, 3, 4, 5]
Running Sums: [1, 3, 6, 10, 15]
Running Lists: [[apple], [apple, banana], [apple, banana, cherry]]
```

**Difference between `fold()` and `scan()`:**
*   `fold()`: Produces one output element (the final accumulated result) from the entire input stream.
*   `scan()`: Produces one output element for *each* input element (the accumulated result up to that point).

---

## 3. `Gatherers.mapConcurrent()`

### Method Signature
```java
public static <T, R> Gatherer<T, ?, R> mapConcurrent(int maxConcurrency, Function<T, R> mapper)
```

### Explanation
`Gatherers.mapConcurrent()` applies a mapping function to elements concurrently, similar to `Stream.parallel().map()`, but with a crucial difference: it *maintains the encounter order* of the elements. This means even if tasks complete out of order, the results will be emitted to the downstream stream in the same order as their corresponding inputs appeared in the upstream stream.

It uses an internal thread pool to execute the `mapper` function. The `maxConcurrency` parameter controls how many mapping tasks can run simultaneously.

*   **`maxConcurrency` (int):** The maximum number of concurrent tasks allowed. This limits the number of elements being processed by the `mapper` function at any given time.
*   **`mapper` (Function<T, R>):** The function to apply to each input element. This function should ideally be independent of other elements and potentially long-running (e.g., I/O operations, complex computations).

**Key Characteristics:**
*   **Concurrency with Order Preservation:** Processes elements concurrently while ensuring the output order matches the input order. This is a significant advantage over raw `parallelStream().map()`, which does not guarantee order.
*   **Fixed Output Count:** Produces exactly one output element for each input element, just like a regular `map()` operation.
*   **Internal Buffering:** To preserve order, it might buffer completed results until earlier results are ready to be emitted. This can introduce slight latency if tasks complete significantly out of order.
*   **Resource Management:** Manages an internal thread pool, simplifying concurrent execution.

### When to Use
Use `mapConcurrent()` when you have a stream of elements, and applying a mapping function to each element is a potentially slow or blocking operation (e.g., calling an external API, performing a database lookup, complex image processing), but you still need the results in the original encounter order. It's a safer and often more performant alternative to managing your own `ExecutorService` for such scenarios within a stream pipeline.

### Example: Simulating Concurrent API Calls

#### Java Code
```java
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Gatherers;

public class MapConcurrentExample {
    // Simulate a slow API call or computation
    private static String processData(String data) {
        System.out.println(Thread.currentThread().getName() + " - Starting processing: " + data);
        try {
            // Simulate work that takes a variable amount of time
            long delay = (data.length() * 100L); // Shorter for "data1", longer for "data5"
            Thread.sleep(delay);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        System.out.println(Thread.currentThread().getName() + " - Finished processing: " + data);
        return "Processed_" + data;
    }

    public static void main(String[] args) {
        List<String> items = List.of("data1", "data2", "data3", "data4", "data5", "data6", "data7", "data8");

        System.out.println("Original items: " + items);
        System.out.println("Starting concurrent mapping with max concurrency = 3...");

        long startTime = System.currentTimeMillis();

        List<String> results = items.stream()
            .gather(Gatherers.mapConcurrent(
                3, // Max 3 concurrent tasks
                MapConcurrentExample::processData // Our simulated slow operation
            ))
            .collect(Collectors.toList());

        long endTime = System.currentTimeMillis();

        System.out.println("Finished concurrent mapping.");
        System.out.println("Results (order preserved): " + results);
        System.out.println("Time taken: " + (endTime - startTime) + " ms");
    }
}
```

#### Input
`List.of("data1", "data2", "data3", "data4", "data5", "data6", "data7", "data8")`

#### Output (Example - actual thread names and timing will vary)
You will see `Starting processing` and `Finished processing` messages interleave due to concurrency, but the final `Results` list will maintain the original order.
```
Original items: [data1, data2, data3, data4, data5, data6, data7, data8]
Starting concurrent mapping with max concurrency = 3...
pool-1-thread-1 - Starting processing: data1
pool-1-thread-2 - Starting processing: data2
pool-1-thread-3 - Starting processing: data3
pool-1-thread-1 - Finished processing: data1
pool-1-thread-4 - Starting processing: data4
pool-1-thread-2 - Finished processing: data2
pool-1-thread-5 - Starting processing: data5
pool-1-thread-3 - Finished processing: data3
pool-1-thread-6 - Starting processing: data6
pool-1-thread-4 - Finished processing: data4
pool-1-thread-7 - Starting processing: data7
pool-1-thread-5 - Finished processing: data5
pool-1-thread-8 - Starting processing: data8
pool-1-thread-6 - Finished processing: data6
pool-1-thread-7 - Finished processing: data7
pool-1-thread-8 - Finished processing: data8
Finished concurrent mapping.
Results (order preserved): [Processed_data1, Processed_data2, Processed_data3, Processed_data4, Processed_data5, Processed_data6, Processed_data7, Processed_data8]
Time taken: 1105 ms  <-- This will be roughly (8 items / 3 concurrency) * avg_delay, so approx 3 * 100ms for data1, data2, data3 + 3 * 100ms for data4, data5, data6 + 2 * 100ms for data7, data8 + some overhead. Much faster than 8 * 100ms sequentially.
```

---

These `Gatherers` methods significantly enhance the expressiveness and capability of the Java Stream API, allowing for more complex and efficient intermediate data transformations.