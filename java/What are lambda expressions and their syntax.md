# Lambda Expressions in Java

Lambda expressions, introduced in Java 8, are a powerful feature that brings functional programming paradigms to Java. They provide a concise way to represent a method interface using an expression. Essentially, they are **anonymous functions** – functions without a name, but with parameters and a body, that can be passed around as an argument.

## What Problem Do They Solve?

Before Java 8, if you wanted to pass a block of code as an argument to a method, you typically had to create an **anonymous inner class**. This often led to verbose and boilerplate code, even for very simple operations.

Lambda expressions dramatically reduce this boilerplate by providing a compact syntax for implementing **functional interfaces**.

## Core Concept: Functional Interfaces

Lambda expressions can *only* be used in contexts where a **Functional Interface** is expected.

A **Functional Interface** is an interface that has **exactly one abstract method**.
It can have multiple `default` or `static` methods, but only one abstract method.

The `@FunctionalInterface` annotation (optional but recommended) is used to indicate that an interface is intended to be a functional interface. The compiler will then enforce the "single abstract method" rule.

**Examples of Built-in Functional Interfaces in `java.util.function` package:**
*   `Runnable`: `void run()` (no arguments, no return)
*   `Consumer<T>`: `void accept(T t)` (one argument, no return)
*   `Supplier<T>`: `T get()` (no arguments, returns a value)
*   `Function<T, R>`: `R apply(T t)` (one argument, returns a value)
*   `Predicate<T>`: `boolean test(T t)` (one argument, returns a boolean)
*   `Comparator<T>`: `int compare(T o1, T o2)` (two arguments, returns an int)

## Lambda Expression Syntax

The basic syntax of a lambda expression is:

```java
(parameters) -> { body }
```

Let's break down each part:

1.  **`(parameters)`**:
    *   **No parameters:** If the abstract method takes no arguments, use empty parentheses.
        ```java
        () -> System.out.println("Hello!")
        ```
    *   **One parameter:** If there's only one parameter, the parentheses are optional. The type of the parameter can also be omitted (type inference).
        ```java
        s -> System.out.println(s)             // Type of 's' inferred
        (String s) -> System.out.println(s)   // Explicit type
        ```
    *   **Multiple parameters:** If there are multiple parameters, they must be enclosed in parentheses and separated by commas. Types are optional (type inference).
        ```java
        (a, b) -> a + b                      // Types of 'a', 'b' inferred
        (int a, int b) -> a + b              // Explicit types
        ```

2.  **`->` (Arrow Operator)**:
    *   This is the lambda operator. It separates the parameters from the body.

3.  **`{ body }`**:
    *   **Single expression body:** If the body consists of a single expression, you can omit the curly braces and the `return` keyword (if a value is expected). The result of the expression is implicitly returned.
        ```java
        (a, b) -> a + b
        s -> s.length()
        ```
    *   **Block body:** If the body contains multiple statements, or if you need explicit control over what is returned, use curly braces. The `return` keyword is then required if the method expects a return value.
        ```java
        (int x, int y) -> {
            int sum = x + y;
            System.out.println("Sum is: " + sum);
            return sum;
        }
        ```

### Summary of Syntax Variations:

| Parameters | Body Type          | Syntax                                         | Example                                                  |
| :--------- | :----------------- | :--------------------------------------------- | :------------------------------------------------------- |
| None       | Single Expression  | `() -> expression`                             | `() -> "Hello"`                                          |
| None       | Block              | `() -> { statements; }`                        | `() -> { System.out.println("Hi"); }`                   |
| Single     | Single Expression  | `param -> expression` (or `(param) -> ...`)  | `name -> "Hello " + name`                                |
| Single     | Block              | `param -> { statements; }` (or `(param) -> ...`) | `num -> { int x = num * 2; return x; }`                  |
| Multiple   | Single Expression  | `(p1, p2) -> expression`                       | `(a, b) -> a + b`                                        |
| Multiple   | Block              | `(p1, p2) -> { statements; }`                  | `(s1, s2) -> { System.out.println(s1); return s2; }` |

## Detailed Examples

Let's illustrate with practical examples.

### Example 1: `Runnable` (No parameters, no return)

This shows the reduction in boilerplate compared to an anonymous inner class.

```java
// MyRunnable.java
public class MyRunnable {

    public static void main(String[] args) {

        System.out.println("--- Using Anonymous Inner Class ---");
        // Traditional way: Anonymous Inner Class
        Runnable oldSchoolRunnable = new Runnable() {
            @Override
            public void run() {
                System.out.println("Hello from an anonymous inner class!");
            }
        };
        Thread thread1 = new Thread(oldSchoolRunnable);
        thread1.start();

        System.out.println("\n--- Using Lambda Expression ---");
        // Modern way: Lambda Expression
        Runnable lambdaRunnable = () -> {
            System.out.println("Hello from a lambda expression!");
        };
        Thread thread2 = new Thread(lambdaRunnable);
        thread2.start();

        // Even more concise lambda (single expression body)
        Runnable conciseLambdaRunnable = () -> System.out.println("Hello from a concise lambda!");
        new Thread(conciseLambdaRunnable).start();
    }
}
```

**Compilation & Execution:**
```bash
javac MyRunnable.java
java MyRunnable
```

**Expected Output (order of threads may vary slightly):**
```
--- Using Anonymous Inner Class ---
Hello from an anonymous inner class!

--- Using Lambda Expression ---
Hello from a lambda expression!
Hello from a concise lambda!
```

**Explanation:**
The `Runnable` interface has a single abstract method `void run()`.
*   The anonymous inner class required `new Runnable() { ... }` with the `run()` method explicitly overridden.
*   The lambda expression `() -> { System.out.println("..."); }` provides the implementation for `run()` directly, without the need for `new Runnable()`, `override`, or the method name.

### Example 2: `Consumer<T>` (One parameter, no return)

Using a built-in functional interface `Consumer` which accepts one argument and performs an action.

```java
// MyConsumer.java
import java.util.function.Consumer;
import java.util.Arrays;
import java.util.List;

public class MyConsumer {

    public static void main(String[] args) {

        List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

        System.out.println("--- Using Lambda with Consumer ---");
        // Lambda to print each name
        Consumer<String> namePrinter = name -> System.out.println("Name: " + name);

        // Iterate and apply the consumer
        names.forEach(namePrinter);

        System.out.println("\n--- Direct Lambda in forEach ---");
        // Even more common: passing lambda directly to forEach
        names.forEach(name -> System.out.println("Directly: " + name.toUpperCase()));
    }
}
```

**Compilation & Execution:**
```bash
javac MyConsumer.java
java MyConsumer
```

**Expected Output:**
```
--- Using Lambda with Consumer ---
Name: Alice
Name: Bob
Name: Charlie

--- Direct Lambda in forEach ---
Directly: ALICE
Directly: BOB
Directly: CHARLIE
```

**Explanation:**
The `Consumer<T>` interface has one abstract method `void accept(T t)`.
*   `name -> System.out.println("Name: " + name)` implements `accept` for `String` objects. The `name` parameter corresponds to `T t`.

### Example 3: `Comparator<T>` (Multiple parameters, return value)

A classic use case for lambdas is with `Comparator` for custom sorting. `Comparator<T>` has `int compare(T o1, T o2)`.

```java
// MyComparator.java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Comparator; // Not strictly needed, but good for clarity

public class MyComparator {

    public static void main(String[] args) {
        List<String> fruits = new ArrayList<>();
        fruits.add("Apple");
        fruits.add("Banana");
        fruits.add("Kiwi");
        fruits.add("Orange");

        System.out.println("Original List: " + fruits);

        System.out.println("\n--- Sorting by String Length (Ascending) ---");
        // Lambda expression for Comparator
        // (s1, s2) are the two parameters, and s1.length() - s2.length() is the expression body
        Collections.sort(fruits, (s1, s2) -> s1.length() - s2.length());
        System.out.println("Sorted by length (Asc): " + fruits);

        System.out.println("\n--- Sorting by String Length (Descending) ---");
        // Lambda expression with explicit types and block body for a more complex comparison
        Collections.sort(fruits, (String s1, String s2) -> {
            int len1 = s1.length();
            int len2 = s2.length();
            return Integer.compare(len2, len1); // Descending order
        });
        System.out.println("Sorted by length (Desc): " + fruits);
    }
}
```

**Compilation & Execution:**
```bash
javac MyComparator.java
java MyComparator
```

**Expected Output:**
```
Original List: [Apple, Banana, Kiwi, Orange]

--- Sorting by String Length (Ascending) ---
Sorted by length (Asc): [Kiwi, Apple, Orange, Banana]

--- Sorting by String Length (Descending) ---
Sorted by length (Desc): [Banana, Orange, Apple, Kiwi]
```

**Explanation:**
The `Comparator` interface has `int compare(T o1, T o2)`.
*   `(s1, s2) -> s1.length() - s2.length()` directly implements this method, comparing string lengths.
*   The second lambda uses explicit types and a block body to demonstrate that multiple statements can be used.

### Example 4: Custom Functional Interface

You can define your own functional interfaces and implement them using lambdas.

```java
// MyCalculator.java

// 1. Define a custom Functional Interface
@FunctionalInterface
interface MathOperation {
    int operate(int a, int b);
}

public class MyCalculator {

    public static void main(String[] args) {

        System.out.println("--- Using Lambda for Addition ---");
        // Implement MathOperation using a lambda for addition
        MathOperation addition = (a, b) -> a + b;
        int sum = addition.operate(10, 5);
        System.out.println("10 + 5 = " + sum);

        System.out.println("\n--- Using Lambda for Subtraction ---");
        // Implement MathOperation using a lambda for subtraction
        MathOperation subtraction = (a, b) -> a - b;
        int difference = subtraction.operate(10, 5);
        System.out.println("10 - 5 = " + difference);

        System.out.println("\n--- Using Lambda for Multiplication (with block body) ---");
        // Implement MathOperation using a lambda for multiplication with a block body
        MathOperation multiplication = (int a, int b) -> {
            System.out.println("Multiplying " + a + " and " + b);
            return a * b;
        };
        int product = multiplication.operate(10, 5);
        System.out.println("10 * 5 = " + product);

        System.out.println("\n--- Passing Lambda Directly to a Method ---");
        // Method that takes a MathOperation and applies it
        operateAndPrint(20, 4, (a, b) -> a / b); // Division
        operateAndPrint(7, 3, (a, b) -> a % b);  // Modulo
    }

    // A helper method that takes numbers and a MathOperation
    public static void operateAndPrint(int a, int b, MathOperation operation) {
        int result = operation.operate(a, b);
        System.out.println("Operation result: " + result);
    }
}
```

**Compilation & Execution:**
```bash
javac MyCalculator.java
java MyCalculator
```

**Expected Output:**
```
--- Using Lambda for Addition ---
10 + 5 = 15

--- Using Lambda for Subtraction ---
10 - 5 = 5

--- Using Lambda for Multiplication (with block body) ---
Multiplying 10 and 5
10 * 5 = 50

--- Passing Lambda Directly to a Method ---
Operation result: 5
Operation result: 1
```

**Explanation:**
*   We defined `MathOperation` as a functional interface.
*   We then provided different lambda implementations (`(a, b) -> a + b`, `(a, b) -> a - b`, etc.) for its `operate` method.
*   This demonstrates how lambdas allow you to define and pass "behavior" (the operation logic) directly.

## Key Benefits of Lambda Expressions

1.  **Concise Code:** Significantly reduces boilerplate code, especially when dealing with anonymous inner classes for simple operations.
2.  **Readability:** For simple operations, lambdas make the code cleaner and easier to understand by focusing on the core logic.
3.  **Enables Functional Programming:** Lambdas are the cornerstone of functional programming features in Java, most notably the **Stream API** (for processing collections declaratively).
4.  **Easier Parallel Processing:** When combined with the Stream API, lambdas make it straightforward to write parallel code, leveraging multi-core processors.

## Limitations and Considerations

*   **Readability for Complex Logic:** While great for concise code, overly complex logic within a lambda can make it harder to read and debug. For complex logic, a traditional named method might be better.
*   **Debugging:** Stack traces involving lambdas can sometimes be less intuitive than those from named methods or anonymous inner classes.
*   **Variable Capture (Effectively Final):** Lambdas can access local variables from their enclosing scope, but these variables must be **effectively final** (meaning their value doesn't change after initialization). If you try to modify a local variable from within a lambda, it will result in a compile-time error. Instance and static variables are freely accessible.
*   **No State:** Lambdas are meant to be stateless; they don't have fields like classes do. If you need state, a full class might be more appropriate.

## Conclusion

Lambda expressions are a game-changer in Java, simplifying code, improving readability, and unlocking the power of functional programming. By understanding functional interfaces and the various syntax forms, developers can write more efficient, expressive, and modern Java code, especially when working with the Java Stream API and other functional constructs.