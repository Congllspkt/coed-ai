# Java Streams: A Detailed Guide

Java 8 introduced Streams, a powerful addition to the Java Collections Framework. Streams provide a declarative and functional way to process sequences of elements. They are not data structures themselves but rather a way to perform operations on data sources like collections, arrays, or I/O channels.

## Key Concepts of Java Streams

1.  **Source:** Streams are created from a source, such as `List`, `Set`, `Map` (via `entrySet()`), arrays, `Stream.of()`, `IntStream.range()`, etc.
2.  **Immutability:** Stream operations do not modify the original data source. Instead, they produce a new stream or a result.
3.  **Lazy Evaluation:** Intermediate operations are "lazy." They are only executed when a terminal operation is invoked. This allows for optimizations like short-circuiting.
4.  **Pipelining:** Stream operations can be chained together to form a pipeline.
5.  **Intermediate Operations:** These operations return another `Stream`, allowing for method chaining. They transform the stream (e.g., `filter`, `map`, `sorted`).
6.  **Terminal Operations:** These operations produce a non-stream result (e.g., a collection, a primitive value, a side effect) and terminate the stream pipeline. A stream can only be consumed once.

---

## Common Stream Operations

Let's dive into the most frequently used stream operations: `filter`, `map`, `reduce`, and `collect`, along with others for context.

### 1. Intermediate Operation: `filter()`

The `filter()` operation is used to select elements from a stream that match a given `Predicate` (a functional interface that takes an argument and returns a boolean).

*   **Purpose:** To create a new stream containing only elements that satisfy a specific condition.
*   **Signature:** `Stream<T> filter(Predicate<? super T> predicate)`

**Example:** Filtering even numbers from a list.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class FilterExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // Filter out even numbers
        List<Integer> evenNumbers = numbers.stream()
                                            .filter(n -> n % 2 == 0) // Lambda expression as Predicate
                                            .collect(Collectors.toList());

        System.out.println("Original numbers: " + numbers);
        System.out.println("Even numbers: " + evenNumbers); // Output: [2, 4, 6, 8, 10]

        List<String> names = Arrays.asList("Alice", "Bob", "Anna", "Charlie", "Alex");
        List<String> namesStartingWithA = names.stream()
                                                .filter(name -> name.startsWith("A"))
                                                .collect(Collectors.toList());

        System.out.println("Names starting with 'A': " + namesStartingWithA); // Output: [Alice, Anna, Alex]
    }
}
```

### 2. Intermediate Operation: `map()`

The `map()` operation transforms each element of a stream into a new element using a `Function` (a functional interface that takes an argument and returns a result).

*   **Purpose:** To apply a transformation to each element, producing a stream of new elements.
*   **Signature:** `Stream<R> map(Function<? super T, ? extends R> mapper)`

**Example:** Squaring numbers, converting objects to strings.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class MapExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

        // Square each number
        List<Integer> squaredNumbers = numbers.stream()
                                            .map(n -> n * n) // Lambda expression as Function
                                            .collect(Collectors.toList());

        System.out.println("Original numbers: " + numbers);
        System.out.println("Squared numbers: " + squaredNumbers); // Output: [1, 4, 9, 16, 25]

        List<String> words = Arrays.asList("hello", "world", "java");
        List<Integer> wordLengths = words.stream()
                                        .map(String::length) // Method reference as Function
                                        .collect(Collectors.toList());

        System.out.println("Words: " + words);
        System.out.println("Word lengths: " + wordLengths); // Output: [5, 5, 4]
    }
}
```

### (Bonus) Intermediate Operation: `flatMap()`

While `map` transforms one element into one new element, `flatMap` transforms one element into *zero, one, or many* new elements, and then *flattens* the resulting streams into a single stream. It's useful when you have a stream of collections, and you want to process all elements across all collections.

*   **Purpose:** To transform each element into a stream of elements, and then flatten all these streams into a single stream.
*   **Signature:** `Stream<R> flatMap(Function<? super T, ? extends Stream<? extends R>> mapper)`

**Example:** Combining lists of strings into a single list of strings.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class FlatMapExample {
    public static void main(String[] args) {
        List<List<String>> listOfLists = Arrays.asList(
            Arrays.asList("apple", "banana"),
            Arrays.asList("orange", "grape", "kiwi"),
            Arrays.asList("mango")
        );

        // Flatten the list of lists into a single list of strings
        List<String> allFruits = listOfLists.stream()
                                            .flatMap(List::stream) // Each list is mapped to a stream, then flattened
                                            .collect(Collectors.toList());

        System.out.println("List of Lists: " + listOfLists);
        System.out.println("All fruits (flattened): " + allFruits);
        // Output: [apple, banana, orange, grape, kiwi, mango]

        List<String> sentences = Arrays.asList("Hello world", "Java streams are great", "Functional programming");
        List<String> allWords = sentences.stream()
                                        .flatMap(sentence -> Arrays.stream(sentence.split(" ")))
                                        .collect(Collectors.toList());

        System.out.println("Sentences: " + sentences);
        System.out.println("All words: " + allWords);
        // Output: [Hello, world, Java, streams, are, great, Functional, programming]
    }
}
```

### 3. Terminal Operation: `reduce()`

The `reduce()` operation is a powerful terminal operation that applies a binary operator to each element in the stream to combine them into a single summary result. It's often used for summing, finding min/max, or concatenating.

There are three overloaded versions of `reduce()`:

#### a) `Optional<T> reduce(BinaryOperator<T> accumulator)`

*   **Purpose:** Performs a reduction on the elements of this stream, using an associative accumulation function, and returns an `Optional` describing the result.
*   **Parameters:**
    *   `accumulator`: A `BinaryOperator` that combines two elements into one.
*   **Return:** An `Optional` because the stream might be empty, in which case there's no single result.

**Example:** Summing numbers (without an initial value).

```java
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

public class ReduceExample1 {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

        // Sum the numbers
        Optional<Integer> sum = numbers.stream()
                                        .reduce((a, b) -> a + b); // (accumulator)

        sum.ifPresent(s -> System.out.println("Sum of numbers: " + s)); // Output: 15

        List<String> words = Arrays.asList("Java", "is", "fun");
        Optional<String> combined = words.stream()
                                            .reduce((s1, s2) -> s1 + " " + s2); // Concatenate strings

        combined.ifPresent(c -> System.out.println("Combined words: " + c)); // Output: Java is fun

        List<Integer> emptyList = Arrays.asList();
        Optional<Integer> emptySum = emptyList.stream().reduce((a, b) -> a + b);
        System.out.println("Sum of empty list: " + emptySum); // Output: Optional.empty
    }
}
```

#### b) `T reduce(T identity, BinaryOperator<T> accumulator)`

*   **Purpose:** Performs a reduction on the elements of this stream, using the provided `identity` value and an associative `accumulator` function.
*   **Parameters:**
    *   `identity`: The initial value of the reduction. It's also the default result if the stream is empty.
    *   `accumulator`: A `BinaryOperator` that combines the current accumulated result with the next element.
*   **Return:** The reduced value (not an `Optional`, as `identity` provides a default).

**Example:** Summing numbers (with an initial value), safely handling empty streams.

```java
import java.util.Arrays;
import java.util.List;

public class ReduceExample2 {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

        // Sum the numbers with initial identity 0
        int sum = numbers.stream()
                        .reduce(0, (a, b) -> a + b); // 0 (identity), (accumulator)

        System.out.println("Sum of numbers (with identity): " + sum); // Output: 15

        List<Integer> emptyList = Arrays.asList();
        int emptyListSum = emptyList.stream()
                                    .reduce(0, (a, b) -> a + b);
        System.out.println("Sum of empty list (with identity): " + emptyListSum); // Output: 0

        List<String> words = Arrays.asList("Java", "Streams", "are", "powerful");
        String sentence = words.stream()
                                .reduce("", (s1, s2) -> s1 + (s1.isEmpty() ? "" : " ") + s2); // Identity is empty string

        System.out.println("Sentence: " + sentence); // Output: Java Streams are powerful
    }
}
```

#### c) `U reduce(U identity, BiFunction<U, ? super T, U> accumulator, BinaryOperator<U> combiner)`

*   **Purpose:** Performs a reduction on the elements of this stream, using an `identity`, a `BiFunction` `accumulator`, and a `BinaryOperator` `combiner`. This version is specifically designed for parallel streams where the accumulation function might return a different type than the input elements, and intermediate results need to be combined.
*   **Parameters:**
    *   `identity`: The initial value for the accumulation.
    *   `accumulator`: A `BiFunction` that incorporates a stream element into a partial result.
    *   `combiner`: A `BinaryOperator` that combines two partial results. This is crucial for parallel processing. It must be able to combine the results of two different `accumulator` operations.
*   **Return:** The reduced value.

**Example:** Summing numbers and printing intermediate steps (more complex, often for parallel processing or type transformation).

```java
import java.util.Arrays;
import java.util.List;

public class ReduceExample3 {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

        // Sum numbers using the three-argument reduce
        // Here, the type U (String) is different from T (Integer)
        String result = numbers.stream()
                                .reduce(
                                    "Start", // identity (initial value for the result type, U)
                                    (acc, num) -> { // accumulator (takes U and T, returns U)
                                        System.out.println("Accumulator: acc=" + acc + ", num=" + num);
                                        return acc + "-" + num; // Combine current accumulated string with number
                                    },
                                    (acc1, acc2) -> { // combiner (takes two U's, returns U) - for parallel streams
                                        System.out.println("Combiner: acc1=" + acc1 + ", acc2=" + acc2);
                                        return acc1 + "|" + acc2; // Combine partial results
                                    }
                                );

        System.out.println("Final Result: " + result);
        // For a sequential stream, the combiner is often not called, or called trivially.
        // For parallel stream, it's essential:
        // Output for sequential:
        // Accumulator: acc=Start, num=1
        // Accumulator: acc=Start-1, num=2
        // Accumulator: acc=Start-1-2, num=3
        // Accumulator: acc=Start-1-2-3, num=4
        // Accumulator: acc=Start-1-2-3-4, num=5
        // Final Result: Start-1-2-3-4-5

        System.out.println("\n--- Parallel Stream Example ---");
        String parallelResult = numbers.parallelStream()
                                        .reduce(
                                            "Start",
                                            (acc, num) -> {
                                                System.out.println("Parallel Accumulator: acc=" + acc + ", num=" + num + " on " + Thread.currentThread().getName());
                                                return acc + "-" + num;
                                            },
                                            (acc1, acc2) -> {
                                                System.out.println("Parallel Combiner: acc1=" + acc1 + ", acc2=" + acc2 + " on " + Thread.currentThread().getName());
                                                return acc1 + "|" + acc2;
                                            }
                                        );
        System.out.println("Final Parallel Result: " + parallelResult);
        // Output for parallel stream will vary due to thread execution order,
        // but you'll see Combiner calls:
        // Parallel Accumulator: ...
        // Parallel Combinator: ...
        // Final Parallel Result: Start-1-2|Start-3-4|Start-5 (example structure)
    }
}
```

### 4. Terminal Operation: `collect()`

The `collect()` operation is the most versatile terminal operation for transforming a stream into a collection or a single value. It uses a `Collector` interface (often via static methods in the `Collectors` utility class).

*   **Purpose:** To accumulate elements into a `Collection` (like `List`, `Set`, `Map`), a single value (like a concatenated string, sum, average), or to group elements.
*   **Signature:** `<R, A> R collect(Collector<? super T, A, R> collector)`

**Common `Collectors` methods:**

*   **`toList()`:** Collects all elements into a `List`.
*   **`toSet()`:** Collects all elements into a `Set` (removes duplicates).
*   **`toMap()`:** Collects elements into a `Map`, requiring key and value mappers.
*   **`joining()`:** Concatenates `CharSequence` elements (e.g., strings) into a single string.
*   **`counting()`:** Counts the number of elements.
*   **`summingInt/Long/Double()`:** Calculates the sum of numeric elements.
*   **`averagingInt/Long/Double()`:** Calculates the average of numeric elements.
*   **`groupingBy()`:** Groups elements by a classification function, often returning a `Map<K, List<V>>`.
*   **`partitioningBy()`:** Partitions elements into two groups based on a `Predicate` (`Map<Boolean, List<T>>`).
*   **`reducing()`:** A collector that implements the `reduce` pattern (can be an alternative to `stream.reduce()`).

**Examples:**

```java
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

public class CollectExample {
    public static void main(String[] args) {
        List<String> words = Arrays.asList("apple", "banana", "orange", "grape", "apple", "kiwi");

        // 1. Collect to a List
        List<String> list = words.stream()
                                .collect(Collectors.toList());
        System.out.println("Collected to List: " + list); // [apple, banana, orange, grape, apple, kiwi]

        // 2. Collect to a Set (removes duplicates)
        Set<String> set = words.stream()
                                .collect(Collectors.toSet());
        System.out.println("Collected to Set: " + set);   // [apple, banana, orange, grape, kiwi] (order may vary)

        // 3. Join strings
        String joinedString = words.stream()
                                    .collect(Collectors.joining(", "));
        System.out.println("Joined String: " + joinedString); // apple, banana, orange, grape, apple, kiwi

        // 4. Grouping by length
        Map<Integer, List<String>> groupedByLength = words.stream()
                                                        .collect(Collectors.groupingBy(String::length));
        System.out.println("Grouped by length: " + groupedByLength);
        // Output: {5=[apple, grape, apple], 6=[banana, orange], 4=[kiwi]}

        List<Person> people = Arrays.asList(
            new Person("Alice", 30, "NY"),
            new Person("Bob", 25, "NY"),
            new Person("Charlie", 35, "CA"),
            new Person("David", 30, "NY")
        );

        // 5. Grouping by city
        Map<String, List<Person>> peopleByCity = people.stream()
                                                        .collect(Collectors.groupingBy(Person::getCity));
        System.out.println("People by city: " + peopleByCity);
        // Output: {NY=[Person{name='Alice', age=30, city='NY'}, Person{name='Bob', age=25, city='NY'}, Person{name='David', age=30, city='NY'}], CA=[Person{name='Charlie', age=35, city='CA'}]}

        // 6. Partitioning by age (e.g., adult vs. not adult)
        Map<Boolean, List<Person>> partitionedByAdult = people.stream()
                                                            .collect(Collectors.partitioningBy(p -> p.getAge() >= 30));
        System.out.println("Partitioned by adult (>=30): " + partitionedByAdult);
        // Output: {false=[Person{name='Bob', age=25, city='NY'}], true=[Person{name='Alice', age=30, city='NY'}, Person{name='Charlie', age=35, city='CA'}, Person{name='David', age=30, city='NY'}]}
    }
}

class Person {
    private String name;
    private int age;
    private String city;

    public Person(String name, int age, String city) {
        this.name = name;
        this.age = age;
        this.city = city;
    }

    public String getName() { return name; }
    public int getAge() { return age; }
    public String getCity() { return city; }

    @Override
    public String toString() {
        return "Person{" +
               "name='" + name + '\'' +
               ", age=" + age +
               ", city='" + city + '\'' +
               '}';
    }
}
```

---

## Putting it All Together: A Stream Pipeline Example

Let's combine `filter`, `map`, and `collect` to solve a common problem: find the names of all adults from a list of people, sorted alphabetically, and collect them into a string.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamPipelineExample {
    public static void main(String[] args) {
        List<Person> people = Arrays.asList(
            new Person("Alice", 30, "NY"),
            new Person("Bob", 25, "NY"),
            new Person("Charlie", 35, "CA"),
            new Person("David", 22, "TX"),
            new Person("Eve", 40, "NY")
        );

        // Find names of adults (age >= 30), sort them, and join them into a comma-separated string.
        String adultNames = people.stream()
                                .filter(p -> p.getAge() >= 30) // Intermediate: Keep only adults
                                .map(Person::getName)         // Intermediate: Transform Person to their name (String)
                                .sorted()                     // Intermediate: Sort names alphabetically
                                .collect(Collectors.joining(", ")); // Terminal: Collect into a single string

        System.out.println("Adult names: " + adultNames);
        // Output: Adult names: Alice, Charlie, Eve
    }
}

// Re-using the Person class from the CollectExample
class Person {
    private String name;
    private int age;
    private String city;

    public Person(String name, int age, String city) {
        this.name = name;
        this.age = age;
        this.city = city;
    }

    public String getName() { return name; }
    public int getAge() { return age; }
    public String getCity() { return city; }

    @Override
    public String toString() {
        return "Person{" +
               "name='" + name + '\'' +
               ", age=" + age +
               ", city='" + city + '\'' +
               '}';
    }
}
```

---

## When to Use Streams

*   **Declarative Processing:** When you want to express *what* you want to do with the data, rather than *how* to do it (imperative loops).
*   **Data Transformation:** When you need to transform elements from one type to another, or filter them based on conditions.
*   **Aggregation:** When you need to sum, average, count, or find min/max values.
*   **Parallel Processing:** When you have large datasets and want to leverage multiple CPU cores easily (`.parallelStream()`).
*   **Readability & Conciseness:** For complex data processing logic, streams often lead to more readable and compact code compared to traditional loops.

## When NOT to Use Streams

*   **Simple Iteration:** For very simple iteration where a `for-each` loop is clearer and more performant (e.g., just printing each element).
*   **Side Effects:** While possible, performing side effects (modifying external state) within stream operations (especially intermediate ones) is generally discouraged as it can lead to non-deterministic behavior, especially in parallel streams. Streams are primarily for pure functions.
*   **Debugging Complex Pipelines:** Debugging multi-line stream pipelines can sometimes be trickier than debugging traditional loops.

---

## Conclusion

Java Streams provide a powerful, functional, and declarative approach to processing collections of data. By understanding intermediate operations like `filter` and `map` for transformation, and terminal operations like `reduce` and `collect` for aggregation and result generation, you can write more concise, readable, and potentially more performant Java code for data manipulation tasks. Mastering these operations is key to leveraging the full power of modern Java.