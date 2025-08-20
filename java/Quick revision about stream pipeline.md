# Java Stream Pipeline: A Quick Revision

This revision provides a detailed overview of Java Stream Pipelines, including their core components, benefits, and practical examples with input and output.

---

## 1. What is a Stream Pipeline?

In Java 8, the **Stream API** was introduced to provide a new way to process collections of data. A **Stream Pipeline** is a sequence of operations that are performed on a stream to produce a result. It allows you to process data in a declarative, functional, and often more concise way compared to traditional loop-based iteration.

**Key Characteristics:**

*   **Source:** A stream always starts from a data source (e.g., `Collection`, `Array`, I/O channels).
*   **Intermediate Operations:** These operations transform the stream (e.g., `filter`, `map`, `sorted`). They are *lazy*, meaning they don't execute until a terminal operation is invoked. They return a new `Stream`, allowing for chaining.
*   **Terminal Operation:** This operation consumes the stream and produces a final result (e.g., `collect`, `forEach`, `reduce`). It triggers the execution of all preceding intermediate operations. A stream can only have one terminal operation.

**Analogy:** Think of an assembly line.
*   **Source:** Raw materials entering the line.
*   **Intermediate Operations:** Various machines processing, shaping, or filtering parts as they move along the line.
*   **Terminal Operation:** The final packaging machine that produces the finished product.

---

## 2. Core Components of a Stream Pipeline

### 2.1. Stream Source

A stream pipeline begins by obtaining a stream from a data source.

**Common ways to create a Stream:**

*   **From Collections:**
    ```java
    List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
    Stream<String> nameStream = names.stream(); // Sequential stream
    Stream<String> parallelNameStream = names.parallelStream(); // Parallel stream
    ```

*   **From Arrays:**
    ```java
    String[] cities = {"New York", "London", "Paris"};
    Stream<String> cityStream = Arrays.stream(cities);
    ```

*   **Using `Stream.of()`:**
    ```java
    Stream<Integer> numberStream = Stream.of(1, 2, 3, 4, 5);
    ```

*   **From Primitive Ranges (`IntStream`, `LongStream`, `DoubleStream`):**
    ```java
    IntStream intStream = IntStream.range(1, 5); // 1, 2, 3, 4 (exclusive end)
    IntStream closedIntStream = IntStream.rangeClosed(1, 5); // 1, 2, 3, 4, 5 (inclusive end)
    ```

*   **From Files (Java NIO):**
    ```java
    import java.nio.file.Files;
    import java.nio.file.Paths;
    // ...
    try (Stream<String> lineStream = Files.lines(Paths.get("data.txt"))) {
        // process lines
    } catch (IOException e) {
        e.printStackTrace();
    }
    ```

---

### 2.2. Intermediate Operations

These operations transform the stream elements without consuming the stream itself. They are *lazy* and return a new `Stream<T>`. You can chain multiple intermediate operations.

| Operation   | Description                                                               | Example (Conceptual)                                    |
| :---------- | :------------------------------------------------------------------------ | :-------------------------------------------------------- |
| `filter(Predicate<T>)` | Selects elements that match a given condition.                          | `stream.filter(n -> n % 2 == 0)` (even numbers)           |
| `map(Function<T, R>)` | Transforms each element into another type/value.                      | `stream.map(s -> s.toUpperCase())` (strings to uppercase) |
| `flatMap(Function<T, Stream<R>>)` | Transforms each element into a stream of elements and flattens them into a single stream. Useful for "un-nesting." | `stream.flatMap(list -> list.stream())` (List<List<T>> to List<T>) |
| `distinct()`| Returns a stream with unique elements (based on `equals()`).            | `stream.distinct()`                                       |
| `sorted()` / `sorted(Comparator<T>)` | Sorts the elements. Natural order or custom comparator.       | `stream.sorted()` or `stream.sorted(String::compareToIgnoreCase)` |
| `limit(long maxSize)` | Truncates the stream to at most `maxSize` elements.             | `stream.limit(5)` (first 5 elements)                      |
| `skip(long n)`| Discards the first `n` elements.                                    | `stream.skip(2)` (skip first 2 elements)                  |
| `peek(Consumer<T>)` | Performs an action on each element as it's consumed, without altering the stream. Useful for debugging. | `stream.peek(System.out::println)` (prints elements during processing) |

**Example Snippets:**

```java
List<String> words = Arrays.asList("apple", "banana", "apricot", "grape");

// filter & map
Stream<String> processedWords = words.stream()
    .filter(s -> s.startsWith("a"))      // Intermediate: apple, apricot
    .map(String::toUpperCase);           // Intermediate: APPLE, APRICOT
// At this point, nothing has actually executed yet.
```

---

### 2.3. Terminal Operations

These operations consume the stream, trigger the execution of all lazy intermediate operations, and produce a final result. A stream can only have one terminal operation.

| Operation   | Description                                                               | Example (Result Type)                                     |
| :---------- | :------------------------------------------------------------------------ | :-------------------------------------------------------- |
| `forEach(Consumer<T>)` | Iterates over each element and performs an action. (Void return)      | `stream.forEach(System.out::println)`                     |
| `collect(Collector<T, A, R>)` | Accumulates elements into a collection or summarizes them. Most common and powerful terminal operation. | `stream.collect(Collectors.toList())` (List<T>) <br> `stream.collect(Collectors.joining(", "))` (String) |
| `reduce(BinaryOperator<T>)` / `reduce(identity, accumulator)` / `reduce(identity, accumulator, combiner)` | Combines elements into a single result using a reduction operation. | `stream.reduce(0, Integer::sum)` (Integer sum) <br> `stream.reduce("", String::concat)` (String concatenation) |
| `count()`   | Returns the number of elements in the stream. (long)                      | `stream.count()`                                          |
| `min(Comparator<T>)` / `max(Comparator<T>)` | Returns the smallest/largest element in the stream, wrapped in an `Optional`. | `stream.min(Integer::compare)` (Optional<Integer>)       |
| `anyMatch(Predicate<T>)` | Checks if any element matches the given predicate. (boolean)      | `stream.anyMatch(n -> n > 10)`                            |
| `allMatch(Predicate<T>)` | Checks if all elements match the given predicate. (boolean)       | `stream.allMatch(n -> n > 0)`                             |
| `noneMatch(Predicate<T>)` | Checks if no element matches the given predicate. (boolean)       | `stream.noneMatch(n -> n == 0)`                           |
| `findFirst()` | Returns the first element of the stream, wrapped in an `Optional`. Short-circuits. | `stream.findFirst()` (Optional<T>)                        |
| `findAny()` | Returns any element of the stream, wrapped in an `Optional`. Good for parallel streams. | `stream.findAny()` (Optional<T>)                          |
| `toArray()` | Returns an array containing the elements of this stream.                | `stream.toArray(String[]::new)` (T[])                     |

**Example Snippets:**

```java
List<String> words = Arrays.asList("apple", "banana", "apricot", "grape");

// Collect to a List
List<String> resultList = words.stream()
    .filter(s -> s.startsWith("a"))
    .map(String::toUpperCase)
    .collect(Collectors.toList()); // Terminal: Triggers execution. Result: [APPLE, APRICOT]

// Count elements
long count = words.stream()
    .filter(s -> s.length() > 5)
    .count(); // Terminal. Result: 2 (banana, apricot)

// Check for existence
boolean hasLongWord = words.stream()
    .anyMatch(s -> s.length() > 7); // Terminal. Result: true (banana, apricot)
```

---

## 3. Benefits of Stream Pipelines

*   **Concise & Readable Code:** Reduces boilerplate compared to traditional loops.
*   **Functional Style:** Promotes immutability and side-effect-free operations.
*   **Declarative:** You define *what* to do, not *how* to do it. The Stream API handles the internal iteration.
*   **Lazy Evaluation:** Operations are only executed when a terminal operation is present, which can be more efficient, especially with large datasets or infinite streams.
*   **Composability:** Intermediate operations can be easily chained to build complex data processing logic.
*   **Parallelism:** Streams can be easily made parallel using `parallelStream()`, leveraging multi-core processors without complex manual thread management.

---

## 4. Comprehensive Example: Processing Product Data

Let's imagine we have a list of `Product` objects and we want to perform several operations on them using a stream pipeline.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.Comparator;

// --- 1. Define a simple Product class ---
class Product {
    private String name;
    private double price;
    private int quantity;

    public Product(String name, double price, int quantity) {
        this.name = name;
        this.price = price;
        this.quantity = quantity;
    }

    public String getName() { return name; }
    public double getPrice() { return price; }
    public int getQuantity() { return quantity; }

    @Override
    public String toString() {
        return "Product{" +
               "name='" + name + '\'' +
               ", price=" + price +
               ", quantity=" + quantity +
               '}';
    }
}

public class StreamPipelineExample {

    public static void main(String[] args) {

        // --- 2. Input Data (Stream Source) ---
        List<Product> products = Arrays.asList(
            new Product("Laptop", 1200.00, 5),
            new Product("Mouse", 25.00, 50),
            new Product("Keyboard", 75.00, 30),
            new Product("Monitor", 300.00, 10),
            new Product("Webcam", 50.00, 20),
            new Product("Headphones", 150.00, 15)
        );

        System.out.println("--- Original Products ---");
        products.forEach(System.out::println);
        System.out.println("\n-------------------------\n");

        // --- 3. Stream Pipeline Operations ---
        // Goal: Get the names of the top 3 most expensive products
        // (with price > $100), sorted alphabetically.

        List<String> topExpensiveProductNames = products.stream()
            // Intermediate Operation 1: Filter
            // Keep only products with price greater than $100
            .filter(p -> p.getPrice() > 100.00) // (Laptop, Monitor, Headphones)

            // Intermediate Operation 2: Sorted
            // Sort by price in descending order (most expensive first)
            .sorted(Comparator.comparing(Product::getPrice).reversed())
                                                // (Laptop, Headphones, Monitor) based on price

            // Intermediate Operation 3: Limit
            // Take only the top 3 most expensive products
            .limit(3)                           // (Laptop, Headphones, Monitor)

            // Intermediate Operation 4: Map
            // Transform Product objects into their names
            .map(Product::getName)              // (Laptop, Headphones, Monitor)

            // Intermediate Operation 5: Sorted (again)
            // Sort the names alphabetically
            .sorted()                           // (Headphones, Laptop, Monitor)

            // Terminal Operation: Collect
            // Collect the resulting names into a List<String>
            .collect(Collectors.toList());      // Triggers execution of the entire pipeline
        
        System.out.println("--- Output ---");
        System.out.println("Top 3 most expensive product names (price > $100), sorted alphabetically:");
        System.out.println(topExpensiveProductNames);

        System.out.println("\n-------------------------\n");

        // Another example: Sum of quantities for cheap products
        int totalCheapQuantity = products.stream()
            .filter(p -> p.getPrice() < 100.00) // Mouse, Keyboard, Webcam
            .mapToInt(Product::getQuantity)     // 50, 30, 20
            .sum();                             // Terminal: Sums the int stream

        System.out.println("--- Another Output ---");
        System.out.println("Total quantity of products cheaper than $100: " + totalCheapQuantity);
    }
}
```

**Input Data (Initial `products` list):**

```
Product{name='Laptop', price=1200.0, quantity=5}
Product{name='Mouse', price=25.0, quantity=50}
Product{name='Keyboard', price=75.0, quantity=30}
Product{name='Monitor', price=300.0, quantity=10}
Product{name='Webcam', price=50.0, quantity=20}
Product{name='Headphones', price=150.0, quantity=15}
```

**Output of the first pipeline (`topExpensiveProductNames`):**

```
--- Original Products ---
Product{name='Laptop', price=1200.0, quantity=5}
Product{name='Mouse', price=25.0, quantity=50}
Product{name='Keyboard', price=75.0, quantity=30}
Product{name='Monitor', price=300.0, quantity=10}
Product{name='Webcam', price=50.0, quantity=20}
Product{name='Headphones', price=150.0, quantity=15}

-------------------------

--- Output ---
Top 3 most expensive product names (price > $100), sorted alphabetically:
[Headphones, Laptop, Monitor]

-------------------------

--- Another Output ---
Total quantity of products cheaper than $100: 100
```

---

## 5. Conclusion

Java Stream Pipelines offer a powerful and elegant way to process collections of data. By understanding the distinction between stream sources, intermediate operations (lazy and chained), and terminal operations (triggering execution and producing a result), you can write more efficient, readable, and maintainable Java code for data manipulation. Embrace the functional paradigm!