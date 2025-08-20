# Introduction to Streams `reduce()` Method in Java

The `Stream.reduce()` method is a powerful **terminal operation** that aggregates elements of a stream into a single summary result. It's a generalization of operations like summing elements, finding the minimum or maximum, or concatenating strings.

Think of `reduce()` as "folding" a stream of elements into one. It repeatedly applies an operation to elements until a single value is produced.

## Why use `reduce()`?

*   **Generalization:** It can implement various aggregation operations like sum, product, min, max, average, and custom aggregations.
*   **Flexibility:** Unlike specific methods like `sum()` or `count()`, `reduce()` works with any type of element, not just numbers.
*   **Parallel Processing:** The third overload is specifically designed to work efficiently with parallel streams.

## Understanding the `reduce()` Overloads

There are three main overloads for the `reduce()` method, each serving slightly different purposes:

---

### 1. `Optional<T> reduce(BinaryOperator<T> accumulator)`

*   **Purpose:** Performs a reduction on the elements of the stream, returning an `Optional` describing the reduced value. If the stream is empty, an empty `Optional` is returned.
*   **Signature:** `Optional<T> reduce(BinaryOperator<T> accumulator)`
*   **Parameters:**
    *   `accumulator`: A `BinaryOperator<T>` that takes two elements of type `T` and returns a single element of type `T`. This operation is applied repeatedly to combine elements.
*   **Return Type:** `Optional<T>` (because there might be no elements to reduce, resulting in no value).

**How it works:**
1.  Takes the first two elements from the stream.
2.  Applies the `accumulator` function to them to produce an intermediate result.
3.  Takes the intermediate result and the next element from the stream.
4.  Applies the `accumulator` again.
5.  Repeats until all elements are processed.

#### Example 1: Sum of Integers (simple)

```java
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

public class ReduceExample1 {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

        // Reduce using the sum accumulator
        Optional<Integer> sumOptional = numbers.stream()
                                               .reduce(Integer::sum); // Equivalent to (a, b) -> a + b

        System.out.println("Input: " + numbers);
        System.out.println("Output (sumOptional): " + sumOptional); // Output: Optional[15]

        // Handle the Optional result
        sumOptional.ifPresent(sum -> System.out.println("Sum: " + sum)); // Output: Sum: 15

        List<Integer> emptyList = Arrays.asList();
        Optional<Integer> emptySum = emptyList.stream().reduce(Integer::sum);
        System.out.println("\nInput: " + emptyList);
        System.out.println("Output (emptySum): " + emptySum); // Output: Optional.empty
    }
}
```

#### Example 2: Finding the Longest String

```java
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

public class ReduceExample2 {
    public static void main(String[] args) {
        List<String> words = Arrays.asList("apple", "banana", "kiwi", "grapefruit");

        // Find the longest string
        Optional<String> longestWord = words.stream()
                                            .reduce((s1, s2) -> s1.length() >= s2.length() ? s1 : s2);

        System.out.println("Input: " + words);
        System.out.println("Output (longestWord): " + longestWord); // Output: Optional[grapefruit]

        longestWord.ifPresent(word -> System.out.println("Longest word: " + word)); // Output: Longest word: grapefruit
    }
}
```

---

### 2. `T reduce(T identity, BinaryOperator<T> accumulator)`

*   **Purpose:** Performs a reduction on the elements of the stream, using an initial `identity` value. This overload guarantees a result of type `T` (never `Optional`).
*   **Signature:** `T reduce(T identity, BinaryOperator<T> accumulator)`
*   **Parameters:**
    *   `identity`: An initial value that is the `identity` for the `accumulator` function. For example, `0` is the identity for addition, `1` for multiplication, an empty string for string concatenation. It's the starting point for the reduction. If the stream is empty, this `identity` value is returned.
    *   `accumulator`: A `BinaryOperator<T>` that takes two elements of type `T` (the current reduced value and the next stream element) and returns a single element of type `T`.
*   **Return Type:** `T`

**How it works:**
1.  The `identity` value is taken as the initial result.
2.  For each element in the stream, the `accumulator` function is applied with the current result and the stream element.
3.  The result of the `accumulator` becomes the new current result.
4.  This continues until all elements are processed.

#### Example 1: Sum of Integers (with identity)

```java
import java.util.Arrays;
import java.util.List;

public class ReduceExample3 {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

        // Reduce with identity (0 for sum)
        Integer sum = numbers.stream()
                             .reduce(0, Integer::sum); // 0 is the identity for addition

        System.out.println("Input: " + numbers);
        System.out.println("Output (sum): " + sum); // Output: 15

        List<Integer> emptyList = Arrays.asList();
        Integer sumOfEmpty = emptyList.stream().reduce(0, Integer::sum);
        System.out.println("\nInput: " + emptyList);
        System.out.println("Output (sumOfEmpty): " + sumOfEmpty); // Output: 0 (identity value)
    }
}
```

#### Example 2: Concatenate Strings

```java
import java.util.Arrays;
import java.util.List;

public class ReduceExample4 {
    public static void main(String[] args) {
        List<String> letters = Arrays.asList("H", "e", "l", "l", "o");

        // Concatenate strings with an empty string as identity
        String greeting = letters.stream()
                                 .reduce("", (acc, letter) -> acc + letter);

        System.out.println("Input: " + letters);
        System.out.println("Output (greeting): " + greeting); // Output: Hello

        List<String> emptyWords = Arrays.asList();
        String emptyConcat = emptyWords.stream().reduce("", (acc, word) -> acc + word);
        System.out.println("\nInput: " + emptyWords);
        System.out.println("Output (emptyConcat): '" + emptyConcat + "'"); // Output: ''
    }
}
```

---

### 3. `U reduce(U identity, BiFunction<U, ? super T, U> accumulator, BinaryOperator<U> combiner)`

*   **Purpose:** This is the most complex overload, used when:
    *   The type of the elements in the stream (`T`) is different from the type of the result (`U`).
    *   The stream might be processed in parallel.
*   **Signature:** `U reduce(U identity, BiFunction<U, ? super T, U> accumulator, BinaryOperator<U> combiner)`
*   **Parameters:**
    *   `identity`: An initial value of type `U` (the type of the result). It's the starting point for the reduction and the default value if the stream is empty.
    *   `accumulator`: A `BiFunction<U, ? super T, U>`. This function takes the current result of type `U` and a stream element of type `T`, and combines them to produce a new result of type `U`. It "accumulates" an element into the current partial result.
    *   `combiner`: A `BinaryOperator<U>`. This function takes two partial results of type `U` (which might come from different parallel sub-streams) and combines them into a single result of type `U`. This is crucial for parallel processing.

**How it works (Sequential):**
1.  Starts with `identity` as the initial `U` result.
2.  For each `T` element in the stream, `accumulator` is called with the current `U` result and the `T` element, producing a new `U` result.
3.  This continues until all elements are processed. The `combiner` is *not* used in sequential streams.

**How it works (Parallel):**
1.  The stream is split into multiple sub-streams.
2.  Each sub-stream processes its elements sequentially using the `identity` and `accumulator` to produce a partial result of type `U`.
3.  Once all sub-streams have their partial results, the `combiner` function is used to merge these partial results into a single final result.

#### Example: Calculating Total Price of Products

Let's say we have a `Product` class and we want to calculate the total price of all products. The stream elements are `Product` objects (`T`), but the result is a `Double` (`U`).

```java
import java.util.Arrays;
import java.util.List;

class Product {
    private String name;
    private double price;

    public Product(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public double getPrice() {
        return price;
    }

    @Override
    public String toString() {
        return "Product{" + "name='" + name + '\'' + ", price=" + price + '}';
    }
}

public class ReduceExample5 {
    public static void main(String[] args) {
        List<Product> products = Arrays.asList(
            new Product("Laptop", 1200.00),
            new Product("Mouse", 25.50),
            new Product("Keyboard", 75.00),
            new Product("Monitor", 300.00)
        );

        // Calculate total price using the 3-argument reduce
        double totalPrice = products.stream().reduce(
            0.0, // identity: initial total price (U)
            (currentTotal, product) -> currentTotal + product.getPrice(), // accumulator: (U, T) -> U
            Double::sum // combiner: (U, U) -> U (merges partial sums from parallel streams)
        );

        System.out.println("Input Products:");
        products.forEach(System.out::println);
        System.out.println("\nOutput (Total Price): " + totalPrice); // Output: 1600.5
    }
}
```

**Explanation for the 3-arg `reduce` example:**

*   **`identity` (0.0):** This is the starting value for our total price. If the list of products were empty, the result would be 0.0.
*   **`accumulator` (`(currentTotal, product) -> currentTotal + product.getPrice()`):**
    *   `currentTotal` is of type `U` (`Double`).
    *   `product` is of type `T` (`Product`).
    *   It takes the `currentTotal` (the accumulated sum so far) and adds the `product.getPrice()` to it, returning the new `currentTotal`. This happens for each product in the stream.
*   **`combiner` (`Double::sum`):**
    *   This is `(total1, total2) -> total1 + total2`.
    *   If you run this on a **parallel stream** (`products.parallelStream().reduce(...)`), the stream might be split. One thread might sum the prices of the first two products, another thread the last two. The `combiner` then takes these two partial sums and adds them together to get the final total.
    *   In a **sequential stream**, the `combiner` is **not used**, but it's still required by the method signature. It must be an operation that can correctly merge two partial results of type `U`.

---

## Common Use Cases for `reduce()`

*   **Sum/Product:** As shown in examples.
*   **Min/Max:** `numbers.stream().reduce(Integer::min)` or `numbers.stream().reduce(Integer.MAX_VALUE, Integer::min)`.
*   **Concatenation:** `strings.stream().reduce("", String::concat)`.
*   **Aggregation into a single object:** For example, combining a stream of `OrderLine` objects into a single `Order` summary object.

## Important Considerations

*   **Identity Value:** For the 2-argument and 3-argument `reduce()`, the `identity` must be truly an identity for the `accumulator` function. This means `accumulator.apply(identity, x)` should be equivalent to `x`. If not, your results will be incorrect, especially with parallel streams.
*   **Associativity:** For parallel streams to work correctly with `reduce()`, the `accumulator` function (and `combiner` in the 3-arg version) must be **associative**. This means the order of operations doesn't matter (e.g., `(a + b) + c` is the same as `a + (b + c)`). Summation is associative, string concatenation is, but some operations might not be.
*   **Immutability:** Ideally, the `accumulator` and `combiner` functions should not modify the existing `identity` or partial results. They should return new values to ensure thread safety and predictability, especially in parallel contexts.
*   **When not to use `reduce()`:**
    *   For simple numeric aggregations, built-in methods like `sum()`, `average()`, `min()`, `max()`, `count()` on `IntStream`, `LongStream`, `DoubleStream` are often more concise and efficient.
    *   If you need to produce a collection (e.g., a `List`, `Set`, `Map`), `collect()` is the appropriate terminal operation. `reduce()` is for producing a *single, scalar* result.

## Conclusion

The `Stream.reduce()` method is a fundamental and versatile tool in the Java Streams API for performing aggregation operations. By understanding its three overloads, especially the role of the `identity`, `accumulator`, and `combiner` functions, you can effectively summarize and transform data from streams into meaningful single results, both sequentially and in parallel.