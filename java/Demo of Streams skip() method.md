The `Stream.skip()` method in Java is a powerful **intermediate operation** that allows you to discard a specified number of elements from the beginning of a stream and return a new stream consisting of the remaining elements.

It's particularly useful for scenarios like pagination, skipping header rows in data, or processing elements from a certain offset.

---

## **Java Stream `skip()` Method**

### **1. Introduction**

The `skip(long n)` method returns a stream consisting of the remaining elements of this stream after discarding the first `n` elements. If this stream contains fewer than `n` elements, an empty stream is returned.

### **2. Method Signature**

```java
Stream<T> skip(long n)
```

*   **`T`**: The type of the stream elements.
*   **`n`**: The number of leading elements to skip.

### **3. How it Works**

*   **Intermediate Operation**: `skip()` is an intermediate operation, meaning it returns another `Stream` and can be chained with other stream operations. It does not perform any processing until a terminal operation is invoked.
*   **Stateful**: It's a stateful intermediate operation because it needs to keep track of how many elements it has skipped so far.
*   **Lazy Evaluation**: Like all stream operations, `skip()` is evaluated lazily. The actual skipping of elements only happens when a terminal operation (like `forEach`, `collect`, `count`, etc.) is called on the stream pipeline.
*   **Returns a New Stream**: It does not modify the original stream or its source. Instead, it returns a new `Stream` instance that represents the view after skipping elements.

### **4. Key Characteristics**

*   **Discards Elements**: Effectively removes `n` elements from the front of the stream.
*   **Non-negative `n`**: The argument `n` must be non-negative. Passing a negative value will result in an `IllegalArgumentException`.
*   **Handles Large `n`**: If `n` is greater than or equal to the total number of elements in the stream, the resulting stream will be empty.
*   **Efficiency**: For ordered streams, `skip` will typically bypass the first `n` elements without processing them unnecessarily, which can be efficient.

### **5. Parameters**

*   `n`: A `long` value representing the number of elements to skip from the beginning of the stream.

### **6. Return Value**

*   A new `Stream<T>` containing the elements remaining after skipping `n` elements.

### **7. Exceptions**

*   `IllegalArgumentException`: If `n` is negative.

---

## **Examples**

Let's look at various examples demonstrating the usage of `Stream.skip()`.

### **Example 1: Basic Usage - Skipping a Few Elements**

This example demonstrates skipping the first two elements from a stream of integers.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamSkipBasicExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        System.out.println("Input List: " + numbers);

        // Skip the first 2 elements
        List<Integer> skippedNumbers = numbers.stream()
                                            .skip(2)
                                            .collect(Collectors.toList());

        System.out.println("Output (after skipping 2): " + skippedNumbers);
    }
}
```

**Input:**
```
Input List: [1, 2, 3, 4, 5]
```

**Output:**
```
Output (after skipping 2): [3, 4, 5]
```

---

### **Example 2: Skipping More Elements Than Available**

If `n` is greater than the number of elements in the stream, `skip()` returns an empty stream.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamSkipMoreThanAvailable {
    public static void main(String[] args) {
        List<String> fruits = Arrays.asList("Apple", "Banana", "Cherry");
        System.out.println("Input List: " + fruits);

        // Try to skip 5 elements from a list of 3
        List<String> skippedFruits = fruits.stream()
                                            .skip(5)
                                            .collect(Collectors.toList());

        System.out.println("Output (after skipping 5): " + skippedFruits);
    }
}
```

**Input:**
```
Input List: [Apple, Banana, Cherry]
```

**Output:**
```
Output (after skipping 5): []
```

---

### **Example 3: Skipping Zero Elements**

Skipping zero elements will result in a stream identical to the original.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamSkipZeroExample {
    public static void main(String[] args) {
        List<Double> temperatures = Arrays.asList(25.5, 26.1, 24.9, 27.0);
        System.out.println("Input List: " + temperatures);

        // Skip 0 elements
        List<Double> result = temperatures.stream()
                                            .skip(0)
                                            .collect(Collectors.toList());

        System.out.println("Output (after skipping 0): " + result);
    }
}
```

**Input:**
```
Input List: [25.5, 26.1, 24.9, 27.0]
```

**Output:**
```
Output (after skipping 0): [25.5, 26.1, 24.9, 27.0]
```

---

### **Example 4: Chaining `skip()` with `limit()` (Pagination)**

This is a common use case for `skip()`: implementing pagination. `skip()` determines the starting point, and `limit()` determines the page size.

Let's get the "second page" of data, with 3 items per page.
*   Page 1: items 1, 2, 3 (skip 0, limit 3)
*   Page 2: items 4, 5, 6 (skip 3, limit 3)
*   Page 3: items 7, 8, 9 (skip 6, limit 3)

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamSkipLimitExample {
    public static void main(String[] args) {
        List<String> names = Arrays.asList(
            "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi"
        );
        System.out.println("Input List: " + names);

        int pageSize = 3;
        int pageNumber = 2; // We want the second page (1-indexed)

        // Calculate the number of elements to skip to get to the desired page
        long skipCount = (long) (pageNumber - 1) * pageSize;

        System.out.println("\n--- Getting Page " + pageNumber + " (Page Size: " + pageSize + ") ---");
        System.out.println("Calculated skip count: " + skipCount);

        List<String> page = names.stream()
                                .skip(skipCount) // Skip elements from previous pages
                                .limit(pageSize) // Limit to the current page size
                                .collect(Collectors.toList());

        System.out.println("Output (Page " + pageNumber + "): " + page);

        // Example: Getting the first page
        System.out.println("\n--- Getting Page 1 (Page Size: " + pageSize + ") ---");
        List<String> page1 = names.stream()
                                .skip((long) (1 - 1) * pageSize)
                                .limit(pageSize)
                                .collect(Collectors.toList());
        System.out.println("Output (Page 1): " + page1);

        // Example: Getting the last page (which might be incomplete)
        System.out.println("\n--- Getting Page 3 (Page Size: " + pageSize + ") ---");
        List<String> page3 = names.stream()
                                .skip((long) (3 - 1) * pageSize)
                                .limit(pageSize)
                                .collect(Collectors.toList());
        System.out.println("Output (Page 3): " + page3);
    }
}
```

**Input:**
```
Input List: [Alice, Bob, Charlie, David, Eve, Frank, Grace, Heidi]
```

**Output:**
```
--- Getting Page 2 (Page Size: 3) ---
Calculated skip count: 3
Output (Page 2): [David, Eve, Frank]

--- Getting Page 1 (Page Size: 3) ---
Output (Page 1): [Alice, Bob, Charlie]

--- Getting Page 3 (Page Size: 3) ---
Output (Page 3): [Grace, Heidi]
```

---

### **Example 5: Handling Negative `n` (IllegalArgumentException)**

Passing a negative value to `skip()` will throw an `IllegalArgumentException`.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamSkipNegativeExample {
    public static void main(String[] args) {
        List<Integer> data = Arrays.asList(10, 20, 30);
        System.out.println("Input List: " + data);

        try {
            System.out.println("\nAttempting to skip with negative value (-1)...");
            List<Integer> result = data.stream()
                                        .skip(-1) // This will throw IllegalArgumentException
                                        .collect(Collectors.toList());
            System.out.println("Output (should not reach here): " + result);
        } catch (IllegalArgumentException e) {
            System.err.println("Caught Expected Exception: " + e.getMessage());
        }
    }
}
```

**Input:**
```
Input List: [10, 20, 30]
```

**Output:**
```
Attempting to skip with negative value (-1)...
Caught Expected Exception: skip() requires n >= 0: -1
```

---

### **Example 6: Skipping a Header Row in Data**

Imagine you're processing a list of lines from a CSV file, where the first line is a header. You can use `skip(1)` to process only the data rows.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamSkipHeaderExample {
    public static void main(String[] args) {
        List<String> csvLines = Arrays.asList(
            "ID,Name,Email",         // Header row
            "1,Alice,alice@example.com",
            "2,Bob,bob@example.com",
            "3,Charlie,charlie@example.com"
        );
        System.out.println("Input CSV Lines:\n" + String.join("\n", csvLines));

        System.out.println("\nProcessing data rows (skipping header):");
        csvLines.stream()
                .skip(1) // Skip the first line (header)
                .map(line -> line.split(",")) // Split each line by comma
                .forEach(parts -> System.out.println("  ID: " + parts[0] + ", Name: " + parts[1]));
    }
}
```

**Input:**
```
Input CSV Lines:
ID,Name,Email
1,Alice,alice@example.com
2,Bob,bob@example.com
3,Charlie,charlie@example.com
```

**Output:**
```
Processing data rows (skipping header):
  ID: 1, Name: Alice
  ID: 2, Name: Bob
  ID: 3, Name: Charlie
```

---

### **Summary**

The `Stream.skip(long n)` method is a fundamental intermediate operation for manipulating streams. It provides a clean and efficient way to:

*   **Remove leading elements** from a stream.
*   **Implement pagination logic** when combined with `limit()`.
*   **Process subsets of data** starting from a specific offset.

Remember that `skip()` is lazy and does not modify the original data source; it always returns a new `Stream` representing the filtered view.