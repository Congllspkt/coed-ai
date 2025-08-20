# Introduction to Java Streams Pipeline

Java Streams, introduced in Java 8, provide a powerful and declarative way to process collections of data. They allow you to perform complex data manipulations in a concise, readable, and often more efficient manner, especially when dealing with large datasets or parallel processing.

## What is a Stream?

At its core, a Java Stream is a sequence of elements that supports various aggregate operations. Think of it not as a data structure itself (like a `List` or `Map`), but rather as a *flow of data* that you can process.

**Key Characteristics of Streams:**

1.  **Not a Data Structure:** A stream doesn't store data; it operates on a source (like a `Collection`, an array, or an I/O channel) and produces a result.
2.  **Functional in Nature:** Stream operations are typically functional, meaning they don't modify the source data. Instead, they produce new streams or a final result. This promotes immutability and fewer side effects.
3.  **Lazy Evaluation:** Intermediate operations are "lazy." They are not executed until a terminal operation is invoked. This allows for optimizations, as operations can be short-circuited if the final result can be determined early.
4.  **Cannot Be Reused:** Once a terminal operation is performed on a stream, the stream is "consumed" and cannot be used again. If you need to re-process the data, you must create a new stream from the source.

## The Stream Pipeline Structure

A Stream Pipeline consists of three main components:

1.  **Source:**
    *   The origin of the elements in the stream.
    *   Examples: `Collection.stream()`, `Arrays.stream()`, `Stream.of()`, `Files.lines()`, `IntStream.range()`.

2.  **Zero or More Intermediate Operations:**
    *   These operations transform the stream into another stream.
    *   They are "lazy" and don't process the elements until a terminal operation is called.
    *   Examples: `filter()`, `map()`, `flatMap()`, `distinct()`, `sorted()`, `limit()`, `skip()`.
    *   Each intermediate operation returns a `Stream` (or a specialized primitive stream like `IntStream`), allowing multiple intermediate operations to be chained together.

3.  **Exactly One Terminal Operation:**
    *   These operations produce a non-stream result (e.g., a `List`, a `Map`, a single value, or `void`).
    *   They are "eager" and trigger the execution of all preceding intermediate operations.
    *   Once a terminal operation is performed, the stream is consumed and cannot be used again.
    *   Examples: `forEach()`, `collect()`, `reduce()`, `count()`, `min()`, `max()`, `anyMatch()`, `allMatch()`, `noneMatch()`, `findFirst()`, `findAny()`.

**Visual Representation:**

```
[Source]  -->  [Intermediate Op 1]  -->  [Intermediate Op 2]  -->  ...  -->  [Terminal Op]  -->  [Result]
(e.g., List)     (e.g., filter)           (e.g., map)                             (e.g., collect)    (e.g., new List)
```

---

## Getting a Stream (Stream Sources)

Before you can build a pipeline, you need a stream to start with.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;

public class StreamSources {
    public static void main(String[] args) {
        // 1. From a Collection (e.g., List)
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
        Stream<String> streamFromList = names.stream();
        System.out.println("Stream from List elements (via forEach):");
        streamFromList.forEach(System.out::print); // Output: AliceBobCharlie
        System.out.println("\n---");

        // 2. From an Array
        String[] colors = {"Red", "Green", "Blue"};
        Stream<String> streamFromArray = Arrays.stream(colors);
        System.out.println("Stream from Array elements (via forEach):");
        streamFromArray.forEach(System.out::print); // Output: RedGreenBlue
        System.out.println("\n---");

        // 3. From individual elements using Stream.of()
        Stream<Integer> streamFromElements = Stream.of(1, 2, 3, 4, 5);
        System.out.println("Stream from elements (via forEach):");
        streamFromElements.forEach(System.out::print); // Output: 12345
        System.out.println("\n---");
        
        // Note: Streams are consumed after a terminal operation.
        // The following line would throw an IllegalStateException:
        // streamFromElements.count(); 
    }
}
```

---

## Intermediate Operations (Examples)

Intermediate operations transform the stream. They are lazy and return a new `Stream`.

### 1. `filter(Predicate<? super T> predicate)`

Selects elements that match a given condition.

**Example:** Filtering even numbers.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class FilterExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        System.out.println("Input: " + numbers); // Input: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        List<Integer> evenNumbers = numbers.stream()
                                            .filter(n -> n % 2 == 0) // Keep only even numbers
                                            .collect(Collectors.toList()); // Collect into a new List

        System.out.println("Output (Even Numbers): " + evenNumbers); // Output: [2, 4, 6, 8, 10]
    }
}
```

### 2. `map(Function<? super T, ? extends R> mapper)`

Transforms each element into a new element by applying a function.

**Example:** Converting strings to uppercase.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class MapExample {
    public static void main(String[] args) {
        List<String> words = Arrays.asList("hello", "world", "java", "streams");

        System.out.println("Input: " + words); // Input: [hello, world, java, streams]

        List<String> upperCaseWords = words.stream()
                                            .map(String::toUpperCase) // Transform each word to uppercase
                                            .collect(Collectors.toList());

        System.out.println("Output (Uppercase Words): " + upperCaseWords); // Output: [HELLO, WORLD, JAVA, STREAMS]
    }
}
```

### 3. `flatMap(Function<? super T, ? extends Stream<? extends R>> mapper)`

Transforms each element into a stream of other elements, and then flattens these streams into a single stream. Useful when you have a stream of collections (or similar structures) and want to process all inner elements as a single stream.

**Example:** Flattening a list of lists of words into a single list of words.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class FlatMapExample {
    public static void main(String[] args) {
        List<List<String>> sentences = Arrays.asList(
            Arrays.asList("Java", "is", "awesome"),
            Arrays.asList("Stream", "API", "is", "powerful")
        );

        System.out.println("Input: " + sentences); // Input: [[Java, is, awesome], [Stream, API, is, powerful]]

        List<String> allWords = sentences.stream()
                                          .flatMap(List::stream) // Flatten each List<String> into a Stream<String>
                                          .collect(Collectors.toList());

        System.out.println("Output (All Words): " + allWords); // Output: [Java, is, awesome, Stream, API, is, powerful]
    }
}
```

### 4. `distinct()`

Returns a stream consisting of the distinct elements (according to `equals()`) of this stream.

**Example:** Removing duplicate numbers.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class DistinctExample {
    public static void main(String[] args) {
        List<Integer> numbersWithDuplicates = Arrays.asList(1, 2, 2, 3, 1, 4, 5, 4, 6);

        System.out.println("Input: " + numbersWithDuplicates); // Input: [1, 2, 2, 3, 1, 4, 5, 4, 6]

        List<Integer> distinctNumbers = numbersWithDuplicates.stream()
                                                             .distinct() // Remove duplicates
                                                             .collect(Collectors.toList());

        System.out.println("Output (Distinct Numbers): " + distinctNumbers); // Output: [1, 2, 3, 4, 5, 6]
    }
}
```

### 5. `sorted()` / `sorted(Comparator<? super T> comparator)`

Returns a stream consisting of the elements of this stream, sorted according to natural order or a custom `Comparator`.

**Example:** Sorting strings alphabetically and by length.

```java
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class SortedExample {
    public static void main(String[] args) {
        List<String> fruits = Arrays.asList("Banana", "Apple", "Orange", "Kiwi", "Grape");

        System.out.println("Input: " + fruits); // Input: [Banana, Apple, Orange, Kiwi, Grape]

        // Natural order sorting
        List<String> sortedNaturally = fruits.stream()
                                              .sorted() // Sorts alphabetically (natural order for String)
                                              .collect(Collectors.toList());
        System.out.println("Output (Sorted Naturally): " + sortedNaturally); // Output: [Apple, Banana, Grape, Kiwi, Orange]

        // Custom comparator sorting (by length)
        List<String> sortedByLength = fruits.stream()
                                             .sorted(Comparator.comparingInt(String::length)) // Sorts by string length
                                             .collect(Collectors.toList());
        System.out.println("Output (Sorted by Length): " + sortedByLength); // Output: [Kiwi, Apple, Grape, Banana, Orange]
    }
}
```

### 6. `limit(long maxSize)`

Returns a stream consisting of the elements of this stream, truncated to be no longer than `maxSize` in length.

**Example:** Taking the first 3 elements.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class LimitExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        System.out.println("Input: " + numbers); // Input: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        List<Integer> firstThree = numbers.stream()
                                           .limit(3) // Take only the first 3 elements
                                           .collect(Collectors.toList());

        System.out.println("Output (First 3): " + firstThree); // Output: [1, 2, 3]
    }
}
```

### 7. `skip(long n)`

Returns a stream consisting of the remaining elements of this stream after discarding the first `n` elements.

**Example:** Skipping the first 5 elements.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class SkipExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        System.out.println("Input: " + numbers); // Input: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        List<Integer> remainingNumbers = numbers.stream()
                                                 .skip(5) // Skip the first 5 elements
                                                 .collect(Collectors.toList());

        System.out.println("Output (After skipping 5): " + remainingNumbers); // Output: [6, 7, 8, 9, 10]
    }
}
```

---

## Terminal Operations (Examples)

Terminal operations consume the stream and produce a final result. The stream cannot be used again after a terminal operation.

### 1. `forEach(Consumer<? super T> action)`

Performs an action for each element in the stream. No return value (`void`). Often used for side effects like printing.

**Example:** Printing each element.

```java
import java.util.Arrays;
import java.util.List;

public class ForEachExample {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

        System.out.println("Input: " + names); // Input: [Alice, Bob, Charlie]

        System.out.print("Output (Printed elements): ");
        names.stream().forEach(name -> System.out.print(name + " ")); // Output: Alice Bob Charlie
        System.out.println();
    }
}
```

### 2. `collect(Collector<? super T, A, R> collector)`

Accumulates the elements into a mutable result container (e.g., a `List`, `Set`, `Map`). This is one of the most common terminal operations.

**Example:** Collecting elements into a `List`.

```java
import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.Map;
import java.util.stream.Collectors;

public class CollectExample {
    public static void main(String[] args) {
        List<String> words = Arrays.asList("apple", "banana", "orange", "apple");

        System.out.println("Input: " + words); // Input: [apple, banana, orange, apple]

        // Collect to List
        List<String> wordList = words.stream()
                                     .collect(Collectors.toList());
        System.out.println("Output (Collected to List): " + wordList); // Output: [apple, banana, orange, apple]

        // Collect to Set (removes duplicates)
        Set<String> wordSet = words.stream()
                                   .collect(Collectors.toSet());
        System.out.println("Output (Collected to Set): " + wordSet); // Output: [orange, apple, banana] (order not guaranteed)

        // Collect to Map (e.g., word -> length)
        Map<String, Integer> wordLengthMap = words.stream()
                                                  .distinct() // Ensure unique keys for the map
                                                  .collect(Collectors.toMap(
                                                      word -> word,       // Key mapper
                                                      String::length      // Value mapper
                                                  ));
        System.out.println("Output (Collected to Map): " + wordLengthMap); // Output: {orange=6, apple=5, banana=6}
    }
}
```

### 3. `reduce(T identity, BinaryOperator<T> accumulator)`

Combines the elements of the stream into a single result.

**Example:** Summing numbers.

```java
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

public class ReduceExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

        System.out.println("Input: " + numbers); // Input: [1, 2, 3, 4, 5]

        // Summing using reduce with an identity (initial value)
        int sum = numbers.stream()
                         .reduce(0, (a, b) -> a + b); // identity = 0, accumulator = (sum, element) -> sum + element
        System.out.println("Output (Sum using reduce with identity): " + sum); // Output: 15

        // Multiplying using reduce without an identity (returns Optional)
        Optional<Integer> product = numbers.stream()
                                           .reduce((a, b) -> a * b); // (element1, element2) -> element1 * element2
        System.out.println("Output (Product using reduce without identity): " + product.orElse(1)); // Output: 120 (1*2*3*4*5)
    }
}
```

### 4. `count()`

Returns the number of elements in the stream as a `long`.

**Example:** Counting elements.

```java
import java.util.Arrays;
import java.util.List;

public class CountExample {
    public static void main(String[] args) {
        List<String> items = Arrays.asList("A", "B", "C", "D");

        System.out.println("Input: " + items); // Input: [A, B, C, D]

        long count = items.stream().count();
        System.out.println("Output (Count): " + count); // Output: 4
    }
}
```

### 5. `min(Comparator<? super T> comparator)` / `max(Comparator<? super T> comparator)`

Returns an `Optional` containing the minimum/maximum element of this stream according to the provided `Comparator`.

**Example:** Finding the minimum and maximum number.

```java
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;

public class MinMaxExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(5, 1, 8, 2, 7, 3);

        System.out.println("Input: " + numbers); // Input: [5, 1, 8, 2, 7, 3]

        Optional<Integer> min = numbers.stream().min(Comparator.naturalOrder());
        Optional<Integer> max = numbers.stream().max(Comparator.naturalOrder());

        System.out.println("Output (Minimum): " + min.orElse(0)); // Output: 1
        System.out.println("Output (Maximum): " + max.orElse(0)); // Output: 8
    }
}
```

### 6. `anyMatch(Predicate<? super T> predicate)` / `allMatch(Predicate<? super T> predicate)` / `noneMatch(Predicate<? super T> predicate)`

Returns a `boolean` indicating whether any, all, or none of the elements match the given predicate. These are short-circuiting operations (they may not process all elements).

**Example:** Checking conditions.

```java
import java.util.Arrays;
import java.util.List;

public class MatchExamples {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(2, 4, 6, 8, 10);

        System.out.println("Input: " + numbers); // Input: [2, 4, 6, 8, 10]

        boolean anyEven = numbers.stream().anyMatch(n -> n % 2 == 0);
        System.out.println("Output (Any even?): " + anyEven); // Output: true

        boolean allEven = numbers.stream().allMatch(n -> n % 2 == 0);
        System.out.println("Output (All even?): " + allEven); // Output: true

        boolean noneOdd = numbers.stream().noneMatch(n -> n % 2 != 0);
        System.out.println("Output (None odd?): " + noneOdd); // Output: true
    }
}
```

### 7. `findFirst()` / `findAny()`

Returns an `Optional` describing some element of the stream, or an empty `Optional` if the stream is empty. `findFirst()` guarantees to return the first element in encounter order, while `findAny()` is less constrained and can be useful for performance in parallel streams.

**Example:** Finding an element.

```java
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

public class FindExamples {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");

        System.out.println("Input: " + names); // Input: [Alice, Bob, Charlie, David]

        Optional<String> first = names.stream().findFirst();
        System.out.println("Output (First element): " + first.orElse("None")); // Output: Alice

        Optional<String> any = names.parallelStream().findAny(); // findAny can be non-deterministic in order
        System.out.println("Output (Any element - parallel): " + any.orElse("None")); // Output: Alice (or Bob, Charlie, David depending on execution)
    }
}
```

---

## Complete Pipeline Example: Processing Names

Let's combine multiple intermediate operations with a terminal operation to build a complete pipeline.

**Scenario:** We have a list of names. We want to:
1. Filter out names shorter than 4 characters.
2. Convert the remaining names to uppercase.
3. Sort them alphabetically.
4. Collect the result into a new list.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class FullPipelineExample {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David", "Eve", "frank", "Grace");

        System.out.println("Initial Input Names: " + names);
        // Input: [Alice, Bob, Charlie, David, Eve, frank, Grace]

        List<String> processedNames = names.stream()               // 1. Source: Create a stream from the list
                                            .filter(name -> name.length() >= 4) // 2. Intermediate: Keep names with 4 or more characters
                                            .map(String::toUpperCase)           // 3. Intermediate: Convert names to uppercase
                                            .sorted()                           // 4. Intermediate: Sort names alphabetically
                                            .collect(Collectors.toList());      // 5. Terminal: Collect the final names into a new List

        System.out.println("Processed Output Names: " + processedNames);
        // Output: [ALICE, CHARLIE, DAVID, FRANK, GRACE]

        // Let's trace the flow:
        // 1. Source Stream:
        //    "Alice", "Bob", "Charlie", "David", "Eve", "frank", "Grace"

        // 2. After filter(name -> name.length() >= 4):
        //    "Alice", "Charlie", "David", "frank", "Grace" (Bob and Eve filtered out)

        // 3. After map(String::toUpperCase):
        //    "ALICE", "CHARLIE", "DAVID", "FRANK", "GRACE"

        // 4. After sorted():
        //    "ALICE", "CHARLIE", "DAVID", "FRANK", "GRACE" (Already in this order alphabetically for these names)

        // 5. After collect(Collectors.toList()):
        //    A new List containing: ["ALICE", "CHARLIE", "DAVID", "FRANK", "GRACE"]
    }
}
```

---

## Benefits of Using Streams

*   **Conciseness and Readability:** Streams allow you to write less boilerplate code and express complex operations in a more readable, declarative style.
*   **Modularity and Composability:** Operations can be chained together easily, promoting a functional programming style where transformations are applied sequentially.
*   **Parallel Processing:** Streams can be easily converted to parallel streams (`.parallelStream()`), allowing the JVM to automatically manage multi-threading for faster execution on multi-core processors, often with minimal code changes.
*   **Efficiency (Lazy Evaluation):** Due to lazy evaluation, elements are processed only when necessary, and short-circuiting operations can improve performance by stopping processing early.
*   **Immutability:** Stream operations do not modify the original data source, promoting safer and more predictable code.

## Conclusion

Java Streams provide an elegant and efficient way to process data collections. Understanding the concept of a pipeline – consisting of a source, zero or more intermediate operations, and one terminal operation – is fundamental to effectively using the Streams API. By chaining these operations, you can build powerful and expressive data processing logic that is both clean and performant.