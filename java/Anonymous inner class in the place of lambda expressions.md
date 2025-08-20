Java, since version 8, introduced lambda expressions as a more concise and readable way to represent instances of functional interfaces, often replacing the need for anonymous inner classes in many scenarios.

Let's dive into the details, comparing anonymous inner classes with lambda expressions.

---

# Anonymous Inner Class vs. Lambda Expressions in Java

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Anonymous Inner Classes (Pre-Java 8 Style)](#2-anonymous-inner-classes-pre-java-8-style)
    *   Definition
    *   Syntax
    *   Characteristics
    *   Example
3.  [Lambda Expressions (Java 8+ Style)](#3-lambda-expressions-java-8-style)
    *   Definition
    *   Syntax
    *   Characteristics
    *   Example
4.  [The Connection: Functional Interfaces](#4-the-connection-functional-interfaces)
5.  [Key Differences and When to Use Which](#5-key-differences-and-when-to-use-which)
    *   Conciseness & Readability
    *   `this` Keyword Behavior
    *   Scope
    *   Compilation
    *   Applicability
6.  [Practical Example: Sorting a List (Side-by-Side)](#6-practical-example-sorting-a-list-side-by-side)
    *   Problem Statement
    *   Anonymous Inner Class Approach
    *   Lambda Expression Approach
7.  [Conclusion](#7-conclusion)

---

## 1. Introduction

Before Java 8, if you needed to implement an interface or extend a class on the fly, typically for a one-time use and without defining a separate, named class, you'd use an **Anonymous Inner Class**.

With Java 8, **Lambda Expressions** were introduced, primarily to simplify the syntax for implementing "functional interfaces" (interfaces with a single abstract method). This change significantly reduced boilerplate code and improved code readability, especially in scenarios like event handling, callbacks, and working with the Streams API.

## 2. Anonymous Inner Classes (Pre-Java 8 Style)

### Definition
An anonymous inner class is a class that has no name and whose object is created and declared at the same time. It is typically used when you need to create an object of an interface or an abstract class, or even a concrete class, for a single, one-off use.

### Syntax
Anonymous inner classes are declared using the `new` operator, followed by the name of the interface or class to implement/extend, immediately followed by curly braces `{}` containing the implementation.

```java
new InterfaceOrAbstractClass() {
    // Implementation of abstract methods
    // Can also override concrete methods
    // Can have its own fields and methods (private to this instance)
};
```

### Characteristics
*   **Verbosity:** They often require more lines of code due to the boilerplate.
*   **`this` Keyword:** Inside an anonymous inner class, `this` refers to the instance of the anonymous class itself.
*   **Capabilities:** Can implement any interface (even those with multiple abstract methods) or extend any class (abstract or concrete). Can have fields, constructors (though implicitly defined), and multiple methods.
*   **Compilation:** Compiles into a separate `.class` file, typically named `EnclosingClass$1.class` (if it's the first anonymous class in `EnclosingClass`), `EnclosingClass$2.class`, etc.

### Example: Implementing `Runnable` using Anonymous Inner Class

**File: `AnonymousRunnableExample.java`**

```java
public class AnonymousRunnableExample {

    public static void main(String[] args) {
        System.out.println("--- Anonymous Inner Class Example ---");

        // 1. Using Anonymous Inner Class to implement Runnable
        Runnable myRunnable = new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 3; i++) {
                    System.out.println("Anonymous Runnable running: " + i);
                    try {
                        Thread.sleep(100); // Simulate some work
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        System.err.println("Thread interrupted!");
                    }
                }
            }
        };

        // Create and start a new Thread with the Runnable
        Thread thread1 = new Thread(myRunnable);
        thread1.start();

        System.out.println("Main thread continues...");
        // Ensure main thread waits a bit for the other thread to run
        try {
            thread1.join(); // Wait for thread1 to complete
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Main thread interrupted!");
        }

        System.out.println("--- Anonymous Inner Class Example End ---");
    }
}
```

**Compilation and Execution:**

```bash
javac AnonymousRunnableExample.java
java AnonymousRunnableExample
```

**Expected Output (may vary slightly due to thread scheduling):**

```
--- Anonymous Inner Class Example ---
Main thread continues...
Anonymous Runnable running: 0
Anonymous Runnable running: 1
Anonymous Runnable running: 2
--- Anonymous Inner Class Example End ---
```

**Explanation:**
Here, `new Runnable() { ... }` creates an instance of an anonymous class that implements the `Runnable` interface. We provide the concrete implementation for its single abstract method, `run()`, directly within the curly braces.

## 3. Lambda Expressions (Java 8+ Style)

### Definition
A lambda expression is a short block of code which takes parameters and returns a value. Lambda expressions are similar to methods, but they do not need a name, and they can be implemented right in the body of a method. They provide a clear and concise way to represent an instance of a functional interface.

### Syntax
The basic syntax of a lambda expression is:

```java
(parameters) -> expression
```
or
```java
(parameters) -> { statements; }
```

*   `parameters`: Zero or more parameters.
*   `->`: The arrow token, which links the parameters to the body of the lambda.
*   `expression` / `{ statements; }`: The body of the lambda expression. If it's a single expression, the result of the expression is returned. If it's a block of statements, you must explicitly use a `return` statement if a value needs to be returned.

### Characteristics
*   **Conciseness:** Significantly reduces boilerplate code, especially for single-method interfaces.
*   **`this` Keyword:** Inside a lambda expression, `this` refers to the instance of the *enclosing class* (the class where the lambda is defined), not the lambda itself.
*   **Capabilities:** Can *only* be used to implement functional interfaces (interfaces with exactly one abstract method). Cannot have fields or additional methods.
*   **Compilation:** Lambdas are compiled differently, often using Java's `invokedynamic` instruction, which allows for more efficient and flexible runtime linking compared to generating new `.class` files for each anonymous inner class.

### Example: Implementing `Runnable` using Lambda Expression

**File: `LambdaRunnableExample.java`**

```java
public class LambdaRunnableExample {

    public static void main(String[] args) {
        System.out.println("--- Lambda Expression Example ---");

        // 1. Using Lambda Expression to implement Runnable
        // Runnable is a functional interface with a single abstract method: void run();
        Runnable myRunnable = () -> {
            for (int i = 0; i < 3; i++) {
                System.out.println("Lambda Runnable running: " + i);
                try {
                    Thread.sleep(100); // Simulate some work
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    System.err.println("Thread interrupted!");
                }
            }
        };

        // Create and start a new Thread with the Runnable
        Thread thread1 = new Thread(myRunnable);
        thread1.start();

        System.out.println("Main thread continues...");
        // Ensure main thread waits a bit for the other thread to run
        try {
            thread1.join(); // Wait for thread1 to complete
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Main thread interrupted!");
        }

        System.out.println("--- Lambda Expression Example End ---");
    }
}
```

**Compilation and Execution:**

```bash
javac LambdaRunnableExample.java
java LambdaRunnableExample
```

**Expected Output (may vary slightly due to thread scheduling):**

```
--- Lambda Expression Example ---
Main thread continues...
Lambda Runnable running: 0
Lambda Runnable running: 1
Lambda Runnable running: 2
--- Lambda Expression Example End ---
```

**Explanation:**
Here, `() -> { ... }` is a lambda expression. Since `Runnable` has a `void run()` method that takes no arguments, the lambda takes no arguments (`()`) and executes the block of code `{ ... }`. This is much more compact than the anonymous inner class version.

## 4. The Connection: Functional Interfaces

Lambda expressions can *only* be used to implement **functional interfaces**. A functional interface is an interface that has exactly **one abstract method**.

Many existing interfaces in the Java API were retrofitted to be functional interfaces (e.g., `Runnable`, `Callable`, `Comparator`, `ActionListener`). You can also define your own functional interfaces using the `@FunctionalInterface` annotation (which is optional but highly recommended to ensure it remains a functional interface).

**Example of a custom functional interface:**

```java
@FunctionalInterface
interface MyFunctionalInterface {
    void doSomething(String message);
    // You cannot add another abstract method here if you want it to remain a functional interface
    // default void doSomethingElse() { ... } // Default methods are allowed
    // static void utilityMethod() { ... } // Static methods are allowed
}
```

## 5. Key Differences and When to Use Which

| Feature               | Anonymous Inner Class                               | Lambda Expression                                             |
| :-------------------- | :-------------------------------------------------- | :------------------------------------------------------------ |
| **Conciseness**       | Verbose, requires more boilerplate code.            | Concise, less boilerplate, more readable for simple cases.    |
| **`this` Keyword**    | Refers to the instance of the anonymous class itself. | Refers to the instance of the *enclosing class*.              |
| **Scope**             | Can shadow variables from the enclosing scope.      | Cannot shadow variables from the enclosing scope; they are implicitly `final` or effectively `final`. |
| **Applicability**     | Can implement **any** interface (single or multiple abstract methods) or extend **any** class (abstract or concrete). Can have fields and multiple methods. | Can *only* implement **functional interfaces** (interfaces with exactly one abstract method). Cannot have fields or additional methods. |
| **Compilation**       | Compiles to a separate `.class` file (e.g., `MyClass$1.class`). | Compiles using `invokedynamic` bytecodes, often without generating a separate `.class` file. Optimized by the JVM. |
| **Use Cases**         | Complex scenarios, overriding multiple methods, adding state, pre-Java 8. | Simple callbacks, event handlers, Streams API, functional programming paradigms. |

## 6. Practical Example: Sorting a List (Side-by-Side)

Let's illustrate with a common scenario: sorting a list of strings using a custom `Comparator`.

### Problem Statement
Sort a list of names in reverse alphabetical order.

### Anonymous Inner Class Approach

**File: `SortWithAnonymousClass.java`**

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class SortWithAnonymousClass {

    public static void main(String[] args) {
        System.out.println("--- Sorting with Anonymous Inner Class ---");

        List<String> names = new ArrayList<>();
        names.add("Charlie");
        names.add("Alice");
        names.add("Bob");
        names.add("David");

        System.out.println("Original list: " + names);

        // Sort the list using an anonymous inner class for Comparator
        // Comparator is a functional interface (has one abstract method: compare)
        Collections.sort(names, new Comparator<String>() {
            @Override
            public int compare(String s1, String s2) {
                // For reverse alphabetical order
                return s2.compareTo(s1);
            }
        });

        System.out.println("Sorted list (Anonymous Class): " + names);
        System.out.println("--- End Sorting with Anonymous Inner Class ---");
    }
}
```

**Compilation and Execution:**

```bash
javac SortWithAnonymousClass.java
java SortWithAnonymousClass
```

**Expected Output:**

```
--- Sorting with Anonymous Inner Class ---
Original list: [Charlie, Alice, Bob, David]
Sorted list (Anonymous Class): [David, Charlie, Bob, Alice]
--- End Sorting with Anonymous Inner Class ---
```

### Lambda Expression Approach

**File: `SortWithLambda.java`**

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class SortWithLambda {

    public static void main(String[] args) {
        System.out.println("--- Sorting with Lambda Expression ---");

        List<String> names = new ArrayList<>();
        names.add("Charlie");
        names.add("Alice");
        names.add("Bob");
        names.add("David");

        System.out.println("Original list: " + names);

        // Sort the list using a lambda expression
        // Comparator is a functional interface
        Collections.sort(names, (s1, s2) -> s2.compareTo(s1));

        System.out.println("Sorted list (Lambda Expression): " + names);
        System.out.println("--- End Sorting with Lambda Expression ---");
    }
}
```

**Compilation and Execution:**

```bash
javac SortWithLambda.java
java SortWithLambda
```

**Expected Output:**

```
--- Sorting with Lambda Expression ---
Original list: [Charlie, Alice, Bob, David]
Sorted list (Lambda Expression): [David, Charlie, Bob, Alice]
--- End Sorting with Lambda Expression ---
```

**Comparison:**
As you can see, the lambda expression `(s1, s2) -> s2.compareTo(s1)` achieves the exact same result as the anonymous inner class, but in a much more compact and readable form. The compiler understands that this lambda expression provides the implementation for the single abstract method `compare(String s1, String s2)` of the `Comparator` interface.

## 7. Conclusion

Lambda expressions are a powerful addition to Java 8+, significantly reducing boilerplate and improving the readability of code that deals with functional interfaces. They are the preferred choice for implementing functional interfaces over anonymous inner classes due to their conciseness and better alignment with functional programming paradigms.

However, anonymous inner classes still have their place when you need to:
*   Implement an interface with **multiple abstract methods**.
*   Extend a concrete class and override some of its methods.
*   Add state (fields) or multiple helper methods within the anonymous implementation.

For simple, single-method callbacks and functional programming constructs, lambdas are the clear winner.