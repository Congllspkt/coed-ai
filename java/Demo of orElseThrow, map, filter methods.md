This document provides a detailed explanation and examples for `orElseThrow`, `map`, and `filter` methods in Java, primarily focusing on their use with `java.util.Optional` and `java.util.stream.Stream` API introduced in Java 8.

## Java Stream and Optional APIs: An Introduction

Before diving into the methods, let's briefly understand the context:

*   **`java.util.Optional`**: A container object which may or may not contain a non-null value. It's used to avoid `NullPointerException`s and to make it explicit when a value might be absent.
*   **`java.util.stream.Stream`**: A sequence of elements supporting sequential and parallel aggregate operations. It allows for functional-style operations on collections, arrays, and other data sources.

These APIs promote a more functional, declarative, and often more concise way of writing Java code.

---

## 1. `orElseThrow()` Method

### Purpose
The `orElseThrow()` method of the `Optional` class is used to retrieve the value contained within an `Optional` instance if it's present. If the `Optional` is empty (contains no value), it throws an exception provided by the given `Supplier`.

### Signature
```java
public <X extends Throwable> T orElseThrow(Supplier<? extends X> exceptionSupplier)
```
*   `T`: The type of the value held by the `Optional`.
*   `X`: The type of the exception to be thrown.
*   `exceptionSupplier`: A `Supplier` that produces the exception to be thrown if the `Optional` is empty.

### Description
This method is a powerful way to ensure that if a value is expected, its absence is handled by immediately throwing a meaningful exception. It's often preferred over `get()` (which throws `NoSuchElementException` if empty) because you can specify *what* exception to throw and include a custom message.

### Example 1: Value is Present (Success Case)

```java
import java.util.Optional;
import java.util.List;
import java.util.Arrays;

class User {
    private int id;
    private String name;

    public User(int id, String name) {
        this.id = id;
        this.name = name;
    }

    public int getId() { return id; }
    public String getName() { return name; }

    @Override
    public String toString() {
        return "User{id=" + id + ", name='" + name + "'}";
    }

    public static Optional<User> findUserById(List<User> users, int id) {
        return users.stream()
                    .filter(user -> user.getId() == id)
                    .findFirst(); // Returns an Optional<User>
    }

    public static void main(String[] args) {
        List<User> users = Arrays.asList(
            new User(1, "Alice"),
            new User(2, "Bob"),
            new User(3, "Charlie")
        );

        // --- Success Case ---
        int userIdToFind = 2;
        System.out.println("Attempting to find user with ID: " + userIdToFind);
        try {
            User foundUser = findUserById(users, userIdToFind)
                                .orElseThrow(() -> new IllegalArgumentException("User with ID " + userIdToFind + " not found!"));
            System.out.println("Successfully found user: " + foundUser);
        } catch (IllegalArgumentException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
```

**Input:**
A list of `User` objects and a request to find a user with ID `2`.

**Output:**
```
Attempting to find user with ID: 2
Successfully found user: User{id=2, name='Bob'}
```

**Explanation:**
The `findUserById` method returns an `Optional<User>`. Since a user with ID `2` exists, the `orElseThrow()` method successfully retrieves the `User` object and prints it.

### Example 2: Value is Absent (Failure Case)

```java
import java.util.Optional;
import java.util.List;
import java.util.Arrays;

// User class and findUserById method are the same as in Example 1

class UserDemo { // Renamed class to avoid conflict if run with previous example
    private int id;
    private String name;

    public UserDemo(int id, String name) {
        this.id = id;
        this.name = name;
    }

    public int getId() { return id; }
    public String getName() { return name; }

    @Override
    public String toString() {
        return "User{id=" + id + ", name='" + name + "'}";
    }

    public static Optional<UserDemo> findUserById(List<UserDemo> users, int id) {
        return users.stream()
                    .filter(user -> user.getId() == id)
                    .findFirst(); // Returns an Optional<User>
    }

    public static void main(String[] args) {
        List<UserDemo> users = Arrays.asList(
            new UserDemo(1, "Alice"),
            new UserDemo(2, "Bob"),
            new UserDemo(3, "Charlie")
        );

        // --- Failure Case ---
        int userIdToFind = 99; // This ID does not exist
        System.out.println("\nAttempting to find user with ID: " + userIdToFind);
        try {
            UserDemo foundUser = findUserById(users, userIdToFind)
                                .orElseThrow(() -> new IllegalArgumentException("User with ID " + userIdToFind + " not found!"));
            System.out.println("Successfully found user: " + foundUser);
        } catch (IllegalArgumentException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
```

**Input:**
A list of `User` objects and a request to find a user with ID `99`.

**Output:**
```
Attempting to find user with ID: 99
Error: User with ID 99 not found!
```

**Explanation:**
The `findUserById` method returns an `empty Optional` because no user with ID `99` exists. Consequently, `orElseThrow()` invokes the provided `Supplier` which creates and throws an `IllegalArgumentException`. The `catch` block then handles this exception, printing the custom error message.

---

## 2. `map()` Method

### Purpose
The `map()` method is a **transformation** operation. It applies a function to each element in a stream (or the value in an `Optional`) and returns a new stream (or `Optional`) containing the results of that function. It does *not* modify the original stream or `Optional`.

### Signature
#### For `Stream`:
```java
<R> Stream<R> map(Function<? super T, ? extends R> mapper)
```
*   `T`: The type of elements in the input stream.
*   `R`: The type of elements in the output stream.
*   `mapper`: A `Function` that takes an element of type `T` and returns an element of type `R`.

#### For `Optional`:
```java
public <U> Optional<U> map(Function<? super T, ? extends U> mapper)
```
*   `T`: The type of the value held by the input `Optional`.
*   `U`: The type of the value held by the output `Optional`.
*   `mapper`: A `Function` that takes the value of type `T` and returns an element of type `U`. If the `Optional` is empty, the `mapper` is not applied, and an empty `Optional` is returned.

### Description
`map()` is essential for converting elements from one form to another. Think of it as a projection or a translation step in your data pipeline.

### Example 1: `Stream.map()` - Transforming Strings

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamMapDemo {
    public static void main(String[] args) {
        List<String> words = Arrays.asList("apple", "banana", "cherry", "date");

        System.out.println("Original words: " + words);

        // Map: Transform each word to its uppercase version
        List<String> upperCaseWords = words.stream()
                                           .map(String::toUpperCase) // Method reference for s -> s.toUpperCase()
                                           .collect(Collectors.toList());

        System.out.println("Uppercase words: " + upperCaseWords);

        // Map: Transform each word to its length
        List<Integer> wordLengths = words.stream()
                                         .map(String::length) // Method reference for s -> s.length()
                                         .collect(Collectors.toList());

        System.out.println("Word lengths: " + wordLengths);
    }
}
```

**Input:**
A `List` of `String` objects: `["apple", "banana", "cherry", "date"]`

**Output:**
```
Original words: [apple, banana, cherry, date]
Uppercase words: [APPLE, BANANA, CHERRY, DATE]
Word lengths: [5, 6, 6, 4]
```

**Explanation:**
The first `map` operation takes each `String` and applies `toUpperCase()`, producing a new stream of uppercase strings. The second `map` operation takes each `String` and applies `length()`, producing a new stream of integers representing the lengths. `collect(Collectors.toList())` gathers the elements of the new stream into a `List`.

### Example 2: `Stream.map()` - Extracting Data from Objects

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

class Product {
    private String name;
    private double price;
    private int stock;

    public Product(String name, double price, int stock) {
        this.name = name;
        this.price = price;
        this.stock = stock;
    }

    public String getName() { return name; }
    public double getPrice() { return price; }
    public int getStock() { return stock; }

    @Override
    public String toString() {
        return "Product{name='" + name + "', price=" + price + ", stock=" + stock + '}';
    }

    public static void main(String[] args) {
        List<Product> products = Arrays.asList(
            new Product("Laptop", 1200.0, 50),
            new Product("Mouse", 25.0, 200),
            new Product("Keyboard", 75.0, 100)
        );

        System.out.println("Original products: " + products);

        // Map: Get a list of product names
        List<String> productNames = products.stream()
                                            .map(Product::getName) // p -> p.getName()
                                            .collect(Collectors.toList());
        System.out.println("Product names: " + productNames);

        // Map: Get a list of product prices (doubled)
        List<Double> doubledPrices = products.stream()
                                             .map(p -> p.getPrice() * 2)
                                             .collect(Collectors.toList());
        System.out.println("Doubled prices: " + doubledPrices);
    }
}
```

**Input:**
A `List` of `Product` objects.

**Output:**
```
Original products: [Product{name='Laptop', price=1200.0, stock=50}, Product{name='Mouse', price=25.0, stock=200}, Product{name='Keyboard', price=75.0, stock=100}]
Product names: [Laptop, Mouse, Keyboard]
Doubled prices: [2400.0, 50.0, 150.0]
```

**Explanation:**
The first `map` operation extracts the `name` from each `Product` object. The second `map` operation calculates a new value (doubled price) for each `Product`. In both cases, a new list with transformed data is created.

### Example 3: `Optional.map()` - Transforming Optional Values

```java
import java.util.Optional;

public class OptionalMapDemo {
    public static void main(String[] args) {
        // --- Case 1: Optional contains a value ---
        Optional<String> strNumber = Optional.of("123");
        System.out.println("Original Optional String: " + strNumber);

        Optional<Integer> intNumber = strNumber.map(Integer::parseInt);
        System.out.println("Transformed Optional Integer: " + intNumber); // Optional[123]
        System.out.println("Value if present: " + intNumber.orElse(0)); // 123

        // --- Case 2: Optional is empty ---
        Optional<String> emptyStr = Optional.empty();
        System.out.println("\nOriginal empty Optional String: " + emptyStr);

        Optional<Integer> emptyInt = emptyStr.map(Integer::parseInt);
        System.out.println("Transformed empty Optional Integer: " + emptyInt); // Optional.empty
        System.out.println("Value if present: " + emptyInt.orElse(0)); // 0
    }
}
```

**Input:**
An `Optional<String>` containing "123" and an empty `Optional<String>`.

**Output:**
```
Original Optional String: Optional[123]
Transformed Optional Integer: Optional[123]
Value if present: 123

Original empty Optional String: Optional.empty
Transformed empty Optional Integer: Optional.empty
Value if present: 0
```

**Explanation:**
If the `Optional` has a value (`"123"`), `map` applies `Integer::parseInt` to it and wraps the result (`123`) in a *new* `Optional<Integer>`. If the `Optional` is empty, `map` does nothing and simply returns an empty `Optional` of the new type. This preserves the "optionality" throughout the transformation chain.

---

## 3. `filter()` Method

### Purpose
The `filter()` method is a **selection** operation. It selects elements from a stream that match a given condition (a `Predicate`) and returns a new stream containing only those matching elements.

### Signature
#### For `Stream`:
```java
Stream<T> filter(Predicate<? super T> predicate)
```
*   `T`: The type of elements in the stream.
*   `predicate`: A `Predicate` (a functional interface with a single method `test(T t)` that returns `boolean`) that specifies the condition. Elements for which the predicate returns `true` are included.

#### For `Optional`:
```java
public Optional<T> filter(Predicate<? super T> predicate)
```
*   `T`: The type of the value held by the `Optional`.
*   `predicate`: A `Predicate` that tests the value if present. If the `Optional` contains a value AND the predicate returns `true`, then an `Optional` containing that value is returned. Otherwise, an empty `Optional` is returned.

### Description
`filter()` is used to reduce the number of elements in a stream by keeping only those that satisfy a certain criterion.

### Example 1: `Stream.filter()` - Filtering Numbers

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamFilterDemo {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        System.out.println("Original numbers: " + numbers);

        // Filter: Keep only even numbers
        List<Integer> evenNumbers = numbers.stream()
                                           .filter(n -> n % 2 == 0) // Lambda expression for predicate
                                           .collect(Collectors.toList());

        System.out.println("Even numbers: " + evenNumbers);

        // Filter: Keep numbers greater than 5
        List<Integer> greaterThanFive = numbers.stream()
                                               .filter(n -> n > 5)
                                               .collect(Collectors.toList());

        System.out.println("Numbers greater than 5: " + greaterThanFive);
    }
}
```

**Input:**
A `List` of `Integer` objects: `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`

**Output:**
```
Original numbers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Even numbers: [2, 4, 6, 8, 10]
Numbers greater than 5: [6, 7, 8, 9, 10]
```

**Explanation:**
The first `filter` operation retains only numbers for which the condition `n % 2 == 0` evaluates to `true`. The second `filter` keeps numbers where `n > 5` is `true`.

### Example 2: `Stream.filter()` - Filtering Objects based on a Property

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

class Article {
    private String title;
    private String author;
    private boolean isPublished;

    public Article(String title, String author, boolean isPublished) {
        this.title = title;
        this.author = author;
        this.isPublished = isPublished;
    }

    public String getTitle() { return title; }
    public String getAuthor() { return author; }
    public boolean isPublished() { return isPublished; }

    @Override
    public String toString() {
        return "Article{title='" + title + "', author='" + author + "', isPublished=" + isPublished + '}';
    }

    public static void main(String[] args) {
        List<Article> articles = Arrays.asList(
            new Article("Java Streams Guide", "Alice", true),
            new Article("Kotlin Basics", "Bob", false),
            new Article("Spring Boot Tutorial", "Alice", true),
            new Article("Microservices Architecture", "Charlie", false)
        );

        System.out.println("Original articles:\n" + articles.stream().map(Article::getTitle).collect(Collectors.joining(", ")));

        // Filter: Get only published articles
        List<Article> publishedArticles = articles.stream()
                                                  .filter(Article::isPublished) // Method reference for a -> a.isPublished()
                                                  .collect(Collectors.toList());
        System.out.println("\nPublished articles:");
        publishedArticles.forEach(a -> System.out.println("- " + a.getTitle() + " by " + a.getAuthor()));

        // Filter: Get articles by a specific author
        String authorName = "Alice";
        List<Article> aliceArticles = articles.stream()
                                              .filter(a -> a.getAuthor().equals(authorName))
                                              .collect(Collectors.toList());
        System.out.println("\nArticles by " + authorName + ":");
        aliceArticles.forEach(a -> System.out.println("- " + a.getTitle() + " (Published: " + a.isPublished() + ")"));
    }
}
```

**Input:**
A `List` of `Article` objects with various titles, authors, and publication statuses.

**Output:**
```
Original articles:
Java Streams Guide, Kotlin Basics, Spring Boot Tutorial, Microservices Architecture

Published articles:
- Java Streams Guide by Alice
- Spring Boot Tutorial by Alice

Articles by Alice:
- Java Streams Guide (Published: true)
- Spring Boot Tutorial (Published: true)
```

**Explanation:**
The first `filter` operation keeps only `Article` objects where `isPublished()` returns `true`. The second `filter` keeps articles where the author's name matches "Alice".

### Example 3: `Optional.filter()` - Conditionally Emptying an Optional

```java
import java.util.Optional;

public class OptionalFilterDemo {
    public static void main(String[] args) {
        // --- Case 1: Optional contains a value, and predicate is true ---
        Optional<Integer> number1 = Optional.of(10);
        System.out.println("Original Optional: " + number1);

        Optional<Integer> filteredNumber1 = number1.filter(n -> n > 5);
        System.out.println("Filtered (n > 5): " + filteredNumber1); // Optional[10]

        // --- Case 2: Optional contains a value, but predicate is false ---
        Optional<Integer> number2 = Optional.of(3);
        System.out.println("\nOriginal Optional: " + number2);

        Optional<Integer> filteredNumber2 = number2.filter(n -> n > 5);
        System.out.println("Filtered (n > 5): " + filteredNumber2); // Optional.empty

        // --- Case 3: Optional is already empty ---
        Optional<Integer> emptyOptional = Optional.empty();
        System.out.println("\nOriginal empty Optional: " + emptyOptional);

        Optional<Integer> filteredEmpty = emptyOptional.filter(n -> n > 5);
        System.out.println("Filtered empty: " + filteredEmpty); // Optional.empty
    }
}
```

**Input:**
`Optional` instances with values `10`, `3`, and an empty `Optional`.

**Output:**
```
Original Optional: Optional[10]
Filtered (n > 5): Optional[10]

Original Optional: Optional[3]
Filtered (n > 5): Optional.empty

Original empty Optional: Optional.empty
Filtered empty: Optional.empty
```

**Explanation:**
`Optional.filter()` only applies the predicate if a value is present. If the predicate returns `true`, the original `Optional` is returned. If the predicate returns `false` (or the `Optional` was already empty), an `empty Optional` is returned. This is useful for adding a "conditional presence" to an `Optional` chain.

---

These three methods (`orElseThrow`, `map`, `filter`) are fundamental building blocks for working with `Optional` and `Stream` APIs, enabling more expressive, robust, and concise code in modern Java.