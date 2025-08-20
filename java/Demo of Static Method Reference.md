# Demo of Static Method Reference in Java

A Static Method Reference is a concise way to refer to an existing static method as a lambda expression. It's a feature introduced in Java 8 to make code more readable and compact when the lambda expression's body simply calls an existing method.

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Prerequisites](#2-prerequisites)
3.  [Syntax](#3-syntax)
4.  [How it Works (Behind the Scenes)](#4-how-it-works-behind-the-scenes)
5.  [Key Benefits](#5-key-benefits)
6.  [Examples](#6-examples)
    *   [Example 1: Using `Consumer` for Printing](#example-1-using-consumer-for-printing)
    *   [Example 2: Using `Function` for String Transformation](#example-2-using-function-for-string-transformation)
    *   [Example 3: Using `Comparator` for Sorting](#example-3-using-comparator-for-sorting)
    *   [Example 4: Using `Predicate` for Filtering](#example-4-using-predicate-for-filtering)
7.  [When to Use Static Method References](#7-when-to-use-static-method-references)
8.  [Conclusion](#8-conclusion)

---

## 1. Introduction

In Java 8, lambda expressions provided a concise way to represent anonymous functions. Method references take this conciseness a step further. A **static method reference** is used when you want to use a static method as the implementation for the abstract method of a functional interface.

Instead of writing:
`parameter -> ClassName.staticMethod(parameter)`

You can write:
`ClassName::staticMethod`

This makes your code cleaner and more readable, especially when the lambda's sole purpose is to invoke an existing static method.

## 2. Prerequisites

To understand static method references, you should be familiar with:
*   **Lambda Expressions:** Method references are a shorthand for certain lambda expressions.
*   **Functional Interfaces:** Method references can only be used with functional interfaces (interfaces with exactly one abstract method). The signature of the referenced method must match the signature of the functional interface's abstract method.

## 3. Syntax

The syntax for a static method reference is:

`ClassName::staticMethodName`

Where:
*   `ClassName`: The name of the class where the static method is defined.
*   `staticMethodName`: The name of the static method you want to reference.

## 4. How it Works (Behind the Scenes)

When the Java compiler encounters a static method reference like `ClassName::staticMethodName`, it effectively translates it into a lambda expression. The key requirement is that the signature of `staticMethodName` must be compatible with the abstract method of the functional interface it's assigned to.

**Compatibility Rules:**
*   The number and types of parameters must match.
*   The return type must be compatible (e.g., if the functional interface method returns `void`, the static method can return anything, but its return value will be ignored; if it returns a type, the static method must return a compatible type).

## 5. Key Benefits

*   **Readability:** Makes code easier to understand by explicitly stating that an existing method is being used.
*   **Conciseness:** Reduces boilerplate code compared to a full lambda expression.
*   **Reusability:** Encourages the reuse of existing utility methods.

---

## 6. Examples

Let's look at several examples demonstrating static method references with different functional interfaces.

### Example 1: Using `Consumer` for Printing

**Scenario:** We want to print each element of a list using a static utility method.

**`MathUtils.java` (Utility Class)**

```java
public class Printer {
    public static void printMessage(String message) {
        System.out.println("Message: " + message);
    }
    
    public static void printNumber(Integer number) {
        System.out.println("Number: " + number);
    }
}
```

**`StaticMethodReferenceConsumerDemo.java` (Main Class)**

```java
import java.util.Arrays;
import java.util.List;
import java.util.function.Consumer;

public class StaticMethodReferenceConsumerDemo {

    public static void main(String[] args) {
        List<String> messages = Arrays.asList("Hello", "World", "Java", "8");
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

        System.out.println("--- Using Lambda Expression (for comparison) ---");
        // Using a lambda expression to print messages
        Consumer<String> lambdaPrinter = msg -> Printer.printMessage(msg);
        messages.forEach(lambdaPrinter);
        
        System.out.println("\n--- Using Static Method Reference ---");
        // Using a static method reference to print messages
        // Printer::printMessage is equivalent to msg -> Printer.printMessage(msg)
        Consumer<String> staticMethodRefPrinter = Printer::printMessage;
        messages.forEach(staticMethodRefPrinter);
        
        // Directly using method reference in forEach
        System.out.println("\n--- Using Static Method Reference directly in forEach ---");
        numbers.forEach(Printer::printNumber);
    }
}
```

**Input (Implicit):**
*   `messages`: ["Hello", "World", "Java", "8"]
*   `numbers`: [1, 2, 3, 4, 5]

**Output:**
```
--- Using Lambda Expression (for comparison) ---
Message: Hello
Message: World
Message: Java
Message: 8

--- Using Static Method Reference ---
Message: Hello
Message: World
Message: Java
Message: 8

--- Using Static Method Reference directly in forEach ---
Number: 1
Number: 2
Number: 3
Number: 4
Number: 5
```

**Explanation:**
The `Consumer<String>` functional interface has an abstract method `void accept(T t)`. Our static method `Printer.printMessage(String message)` matches this signature (takes a `String` and returns `void`). Therefore, `Printer::printMessage` can be used directly as a `Consumer<String>`.

---

### Example 2: Using `Function` for String Transformation

**Scenario:** We want to transform a list of strings to uppercase using a static utility method.

**`StringProcessor.java` (Utility Class)**

```java
public class StringProcessor {
    public static String toUpperCase(String input) {
        if (input == null) {
            return null;
        }
        return input.toUpperCase();
    }
}
```

**`StaticMethodReferenceFunctionDemo.java` (Main Class)**

```java
import java.util.Arrays;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;

public class StaticMethodReferenceFunctionDemo {

    public static void main(String[] args) {
        List<String> words = Arrays.asList("apple", "banana", "cherry", "date");

        System.out.println("Original words: " + words);

        System.out.println("\n--- Using Lambda Expression (for comparison) ---");
        // Using a lambda expression to convert to uppercase
        Function<String, String> lambdaTransformer = s -> StringProcessor.toUpperCase(s);
        List<String> upperCaseWordsLambda = words.stream()
                                                .map(lambdaTransformer)
                                                .collect(Collectors.toList());
        System.out.println("Uppercase (Lambda): " + upperCaseWordsLambda);

        System.out.println("\n--- Using Static Method Reference ---");
        // Using a static method reference to convert to uppercase
        // StringProcessor::toUpperCase is equivalent to s -> StringProcessor.toUpperCase(s)
        Function<String, String> staticMethodRefTransformer = StringProcessor::toUpperCase;
        List<String> upperCaseWordsMethodRef = words.stream()
                                                    .map(staticMethodRefTransformer)
                                                    .collect(Collectors.toList());
        System.out.println("Uppercase (Method Ref): " + upperCaseWordsMethodRef);
        
        System.out.println("\n--- Using Static Method Reference directly in stream.map ---");
        List<String> moreUpperCaseWords = words.stream()
                                               .map(StringProcessor::toUpperCase)
                                               .collect(Collectors.toList());
        System.out.println("More Uppercase (Direct): " + moreUpperCaseWords);
    }
}
```

**Input (Implicit):**
*   `words`: ["apple", "banana", "cherry", "date"]

**Output:**
```
Original words: [apple, banana, cherry, date]

--- Using Lambda Expression (for comparison) ---
Uppercase (Lambda): [APPLE, BANANA, CHERRY, DATE]

--- Using Static Method Reference ---
Uppercase (Method Ref): [APPLE, BANANA, CHERRY, DATE]

--- Using Static Method Reference directly in stream.map ---
More Uppercase (Direct): [APPLE, BANANA, CHERRY, DATE]
```

**Explanation:**
The `Function<T, R>` functional interface has an abstract method `R apply(T t)`. Our static method `StringProcessor.toUpperCase(String input)` matches this signature (takes a `String` and returns a `String`). Hence, `StringProcessor::toUpperCase` can be used as a `Function<String, String>`.

---

### Example 3: Using `Comparator` for Sorting

**Scenario:** We want to sort a list of integers using a custom static comparison method.

**`NumberUtils.java` (Utility Class)**

```java
public class NumberUtils {
    // A static method to compare two integers
    // Returns a negative integer, zero, or a positive integer as the first argument
    // is less than, equal to, or greater than the second.
    public static int compareIntegers(Integer a, Integer b) {
        return a.compareTo(b); // For ascending order
        // return b.compareTo(a); // For descending order
    }
}
```

**`StaticMethodReferenceComparatorDemo.java` (Main Class)**

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class StaticMethodReferenceComparatorDemo {

    public static void main(String[] args) {
        List<Integer> numbers = new ArrayList<>(Arrays.asList(5, 2, 8, 1, 9, 4));

        System.out.println("Original numbers: " + numbers);

        // Make a copy to demonstrate both approaches
        List<Integer> numbersLambda = new ArrayList<>(numbers);
        List<Integer> numbersMethodRef = new ArrayList<>(numbers);

        System.out.println("\n--- Using Lambda Expression (for comparison) ---");
        // Using a lambda expression for comparison
        Comparator<Integer> lambdaComparator = (num1, num2) -> NumberUtils.compareIntegers(num1, num2);
        Collections.sort(numbersLambda, lambdaComparator);
        System.out.println("Sorted (Lambda): " + numbersLambda);

        System.out.println("\n--- Using Static Method Reference ---");
        // Using a static method reference for comparison
        // NumberUtils::compareIntegers is equivalent to (num1, num2) -> NumberUtils.compareIntegers(num1, num2)
        Comparator<Integer> staticMethodRefComparator = NumberUtils::compareIntegers;
        Collections.sort(numbersMethodRef, staticMethodRefComparator);
        System.out.println("Sorted (Method Ref): " + numbersMethodRef);
        
        System.out.println("\n--- Using Static Method Reference directly in sort ---");
        List<Integer> moreNumbers = new ArrayList<>(Arrays.asList(7, 3, 6, 0));
        System.out.println("Original more numbers: " + moreNumbers);
        Collections.sort(moreNumbers, NumberUtils::compareIntegers);
        System.out.println("Sorted more numbers: " + moreNumbers);
    }
}
```

**Input (Implicit):**
*   `numbers`: [5, 2, 8, 1, 9, 4]
*   `moreNumbers`: [7, 3, 6, 0]

**Output:**
```
Original numbers: [5, 2, 8, 1, 9, 4]

--- Using Lambda Expression (for comparison) ---
Sorted (Lambda): [1, 2, 4, 5, 8, 9]

--- Using Static Method Reference ---
Sorted (Method Ref): [1, 2, 4, 5, 8, 9]

--- Using Static Method Reference directly in sort ---
Original more numbers: [7, 3, 6, 0]
Sorted more numbers: [0, 3, 6, 7]
```

**Explanation:**
The `Comparator<T>` functional interface has an abstract method `int compare(T o1, T o2)`. Our static method `NumberUtils.compareIntegers(Integer a, Integer b)` matches this signature (takes two `Integer`s and returns an `int`). Thus, `NumberUtils::compareIntegers` can be used as a `Comparator<Integer>`.

---

### Example 4: Using `Predicate` for Filtering

**Scenario:** We want to filter a list of integers to keep only even numbers using a static utility method.

**`MathUtils.java` (Utility Class)**

```java
public class MathUtils {
    public static boolean isEven(Integer number) {
        return number % 2 == 0;
    }
}
```

**`StaticMethodReferencePredicateDemo.java` (Main Class)**

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.function.Predicate;
import java.util.stream.Collectors;

public class StaticMethodReferencePredicateDemo {

    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        System.out.println("Original numbers: " + numbers);

        System.out.println("\n--- Using Lambda Expression (for comparison) ---");
        // Using a lambda expression to check for even numbers
        Predicate<Integer> lambdaIsEven = num -> MathUtils.isEven(num);
        List<Integer> evenNumbersLambda = numbers.stream()
                                                 .filter(lambdaIsEven)
                                                 .collect(Collectors.toList());
        System.out.println("Even numbers (Lambda): " + evenNumbersLambda);

        System.out.println("\n--- Using Static Method Reference ---");
        // Using a static method reference to check for even numbers
        // MathUtils::isEven is equivalent to num -> MathUtils.isEven(num)
        Predicate<Integer> staticMethodRefIsEven = MathUtils::isEven;
        List<Integer> evenNumbersMethodRef = numbers.stream()
                                                    .filter(staticMethodRefIsEven)
                                                    .collect(Collectors.toList());
        System.out.println("Even numbers (Method Ref): " + evenNumbersMethodRef);
        
        System.out.println("\n--- Using Static Method Reference directly in stream.filter ---");
        List<Integer> moreEvenNumbers = numbers.stream()
                                               .filter(MathUtils::isEven)
                                               .collect(Collectors.toList());
        System.out.println("More even numbers (Direct): " + moreEvenNumbers);

        // Example with removeIf
        List<Integer> mutableNumbers = new ArrayList<>(Arrays.asList(11, 12, 13, 14, 15));
        System.out.println("\nOriginal mutable numbers for removeIf: " + mutableNumbers);
        mutableNumbers.removeIf(MathUtils::isEven); // Remove even numbers
        System.out.println("Mutable numbers after removing evens: " + mutableNumbers); // Should contain only odds
    }
}
```

**Input (Implicit):**
*   `numbers`: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
*   `mutableNumbers`: [11, 12, 13, 14, 15]

**Output:**
```
Original numbers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

--- Using Lambda Expression (for comparison) ---
Even numbers (Lambda): [2, 4, 6, 8, 10]

--- Using Static Method Reference ---
Even numbers (Method Ref): [2, 4, 6, 8, 10]

--- Using Static Method Reference directly in stream.filter ---
More even numbers (Direct): [2, 4, 6, 8, 10]

Original mutable numbers for removeIf: [11, 12, 13, 14, 15]
Mutable numbers after removing evens: [11, 13, 15]
```

**Explanation:**
The `Predicate<T>` functional interface has an abstract method `boolean test(T t)`. Our static method `MathUtils.isEven(Integer number)` matches this signature (takes an `Integer` and returns a `boolean`). Thus, `MathUtils::isEven` can be used as a `Predicate<Integer>`.

---

## 7. When to Use Static Method References

*   **Existing Utility Methods:** When you already have static helper or utility methods that perform a specific operation, and you want to use them in contexts expecting a functional interface (like Stream API operations, `Collections.sort`, `List.forEach`, etc.).
*   **Clarity and Conciseness:** When the lambda expression's body is a direct call to a static method without any additional logic. It improves readability by making the intent clear.
*   **Code Reusability:** Promotes writing modular code where logic is encapsulated in methods that can be referenced.

## 8. Conclusion

Static method references are a powerful and elegant feature in Java 8 that enhance the readability and conciseness of code, especially when working with the Stream API and other functional programming constructs. They are a direct replacement for lambda expressions that simply call an existing static method, provided the method's signature matches the functional interface's abstract method. By using them, you can write cleaner, more expressive, and more maintainable Java code.