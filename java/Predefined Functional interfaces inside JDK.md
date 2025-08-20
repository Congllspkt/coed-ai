# Predefined Functional Interfaces in JDK (Java)

In Java 8, the concept of **Functional Interfaces** was introduced to enable **Lambda Expressions** and **Method References**. A functional interface is an interface that contains **exactly one abstract method**. This single abstract method is known as the "functional method" or "SAM (Single Abstract Method) method".

The `java.util.function` package was added to the JDK to provide a set of commonly used functional interfaces, saving developers from having to define their own for standard operations. These predefined interfaces are the building blocks for writing more concise, readable, and functional-style code.

Here's a detailed look at the most important predefined functional interfaces, along with examples demonstrating their usage (including inputs and outputs).

---

## Table of Contents
1.  [Core Functional Interfaces](#1-core-functional-interfaces)
    *   [1.1. Predicate&lt;T&gt;](#11-predicatet)
    *   [1.2. Consumer&lt;T&gt;](#12-consumert)
    *   [1.3. Function&lt;T, R&gt;](#13-functiont-r)
    *   [1.4. Supplier&lt;T&gt;](#14-suppliert)
    *   [1.5. UnaryOperator&lt;T&gt;](#15-unaryoperatort)
    *   [1.6. BinaryOperator&lt;T&gt;](#16-binaryoperatort)
2.  [Bi-Functional Interfaces (Two Arguments)](#2-bi-functional-interfaces-two-arguments)
    *   [2.1. BiPredicate&lt;T, U&gt;](#21-bipredicatet-u)
    *   [2.2. BiConsumer&lt;T, U&gt;](#22-biconsumert-u)
    *   [2.3. BiFunction&lt;T, U, R&gt;](#23-bifunctiont-u-r)
3.  [Primitive Functional Interfaces](#3-primitive-functional-interfaces)
    *   [Purpose](#purpose)
    *   [Examples (IntPredicate, ToIntFunction, IntConsumer)](#examples-intpredicate-tointfunction-intconsumer)
4.  [Conclusion](#conclusion)

---

## 1. Core Functional Interfaces

These are the most commonly used functional interfaces, typically dealing with one input argument.

### 1.1. Predicate&lt;T&gt;

*   **Package:** `java.util.function`
*   **Abstract Method:** `boolean test(T t)`
*   **Purpose:** Represents an operation that takes one argument and returns a boolean result. It's often used for filtering or conditional checks.
*   **Default/Static Methods:** `and(Predicate other)`, `or(Predicate other)`, `negate()`, `isEqual(Object targetRef)`

**Example:** Checking if a number is even or if a string is long enough.

```java
import java.util.function.Predicate;

public class PredicateExample {
    public static void main(String[] args) {
        // Predicate to check if an Integer is even
        Predicate<Integer> isEven = num -> num % 2 == 0;

        System.out.println("--- Predicate<Integer> Example ---");
        // Input: 4, Output: true
        System.out.println("Is 4 even? " + isEven.test(4)); 
        // Input: 7, Output: false
        System.out.println("Is 7 even? " + isEven.test(7)); 

        // Predicate to check if a String's length is greater than 5
        Predicate<String> isLongEnough = s -> s.length() > 5;

        System.out.println("\n--- Predicate<String> Example ---");
        // Input: "hello", Output: false
        System.out.println("Is 'hello' long enough? " + isLongEnough.test("hello")); 
        // Input: "wonderful", Output: true
        System.out.println("Is 'wonderful' long enough? " + isLongEnough.test("wonderful"));

        // Using default methods: and(), negate()
        Predicate<Integer> isGreaterThanTen = num -> num > 10;
        Predicate<Integer> isLessThanTwenty = num -> num < 20;

        // Predicate combining two conditions (num > 10 AND num < 20)
        Predicate<Integer> isBetweenTenAndTwenty = isGreaterThanTen.and(isLessThanTwenty);
        System.out.println("\n--- Combined Predicate Example ---");
        // Input: 15, Output: true
        System.out.println("Is 15 between 10 and 20? " + isBetweenTenAndTwenty.test(15)); 
        // Input: 8, Output: false
        System.out.println("Is 8 between 10 and 20? " + isBetweenTenAndTwenty.test(8)); 
        // Input: 25, Output: false
        System.out.println("Is 25 between 10 and 20? " + isBetweenTenAndTwenty.test(25)); 

        // Predicate using negate()
        Predicate<Integer> isNotEven = isEven.negate();
        System.out.println("\n--- Negated Predicate Example ---");
        // Input: 4, Output: false (since isEven.test(4) is true, negate makes it false)
        System.out.println("Is 4 not even? " + isNotEven.test(4)); 
        // Input: 7, Output: true (since isEven.test(7) is false, negate makes it true)
        System.out.println("Is 7 not even? " + isNotEven.test(7)); 
    }
}
```

### 1.2. Consumer&lt;T&gt;

*   **Package:** `java.util.function`
*   **Abstract Method:** `void accept(T t)`
*   **Purpose:** Represents an operation that takes a single input argument and returns no result. It's often used for side effects, like printing, modifying state, or logging.
*   **Default Methods:** `andThen(Consumer after)`

**Example:** Printing a message or performing an action on an object.

```java
import java.util.function.Consumer;

public class ConsumerExample {
    public static void main(String[] args) {
        // Consumer to print a String to the console
        Consumer<String> printMessage = message -> System.out.println("Message: " + message);

        System.out.println("--- Consumer<String> Example ---");
        // Input: "Hello Java!", Output: "Message: Hello Java!"
        printMessage.accept("Hello Java!"); 
        // Input: "Lambda expressions are great.", Output: "Message: Lambda expressions are great."
        printMessage.accept("Lambda expressions are great."); 

        // Consumer to increment an Integer array element (demonstrates side effect)
        // Note: For primitive values, you'd need a wrapper class or an array/list to modify state.
        int[] counter = {0}; // An array to hold a mutable integer
        Consumer<Integer> incrementCounter = value -> {
            counter[0] += value;
            System.out.println("Counter updated to: " + counter[0]);
        };
        
        System.out.println("\n--- Consumer with Side Effect Example ---");
        // Initial state: counter[0] = 0
        // Input: 5, Output: "Counter updated to: 5"
        incrementCounter.accept(5); 
        // Input: 3, Output: "Counter updated to: 8"
        incrementCounter.accept(3); 
        // Final state: counter[0] = 8

        // Using default method: andThen()
        Consumer<String> toUpperCase = s -> System.out.println("Uppercase: " + s.toUpperCase());
        Consumer<String> printLength = s -> System.out.println("Length: " + s.length());

        // Combines two consumers: first converts to uppercase, then prints length
        Consumer<String> processString = toUpperCase.andThen(printLength);
        System.out.println("\n--- Chained Consumer Example (andThen) ---");
        // Input: "hello", Output:
        // "Uppercase: HELLO"
        // "Length: 5"
        processString.accept("hello"); 
        // Input: "World", Output:
        // "Uppercase: WORLD"
        // "Length: 5"
        processString.accept("World"); 
    }
}
```

### 1.3. Function&lt;T, R&gt;

*   **Package:** `java.util.function`
*   **Abstract Method:** `R apply(T t)`
*   **Purpose:** Represents an operation that takes one argument of type `T` and produces a result of type `R`. It's used for transformation or mapping.
*   **Default/Static Methods:** `compose(Function before)`, `andThen(Function after)`, `identity()`

**Example:** Converting a String to an Integer, or an Integer to a String.

```java
import java.util.function.Function;

public class FunctionExample {
    public static void main(String[] args) {
        // Function to convert a String to its length (Integer)
        Function<String, Integer> stringLength = String::length; // Using method reference

        System.out.println("--- Function<String, Integer> Example ---");
        // Input: "Programming", Output: 11
        System.out.println("Length of 'Programming': " + stringLength.apply("Programming")); 
        // Input: "Java", Output: 4
        System.out.println("Length of 'Java': " + stringLength.apply("Java")); 

        // Function to convert an Integer to its String representation
        Function<Integer, String> intToString = String::valueOf;

        System.out.println("\n--- Function<Integer, String> Example ---");
        // Input: 123, Output: "123"
        System.out.println("String representation of 123: " + intToString.apply(123)); 
        // Input: -45, Output: "-45"
        System.out.println("String representation of -45: " + intToString.apply(-45));

        // Using default methods: andThen() and compose()
        Function<Integer, Integer> multiplyByTwo = num -> num * 2;
        Function<Integer, Integer> addFive = num -> num + 5;

        // andThen(): first multiplyByTwo, then addFive
        // (x * 2) + 5
        Function<Integer, Integer> multiplyThenAdd = multiplyByTwo.andThen(addFive);
        System.out.println("\n--- Chained Function (andThen) Example ---");
        // Input: 10, Output: (10 * 2) + 5 = 25
        System.out.println("Multiply 10 by 2 then add 5: " + multiplyThenAdd.apply(10)); 

        // compose(): first addFive, then multiplyByTwo
        // (x + 5) * 2
        Function<Integer, Integer> addThenMultiply = multiplyByTwo.compose(addFive);
        System.out.println("\n--- Chained Function (compose) Example ---");
        // Input: 10, Output: (10 + 5) * 2 = 30
        System.out.println("Add 5 to 10 then multiply by 2: " + addThenMultiply.apply(10)); 

        // Static method: identity()
        Function<String, String> identityFunction = Function.identity();
        System.out.println("\n--- Identity Function Example ---");
        // Input: "same", Output: "same"
        System.out.println("Identity for 'same': " + identityFunction.apply("same")); 
    }
}
```

### 1.4. Supplier&lt;T&gt;

*   **Package:** `java.util.function`
*   **Abstract Method:** `T get()`
*   **Purpose:** Represents an operation that supplies a result of type `T` without taking any arguments. It's used for deferring computation or lazy initialization.
*   **No default/static methods.**

**Example:** Generating a random number, fetching a configuration value, or creating a new object.

```java
import java.util.function.Supplier;
import java.time.LocalDateTime;
import java.util.Random;

public class SupplierExample {
    public static void main(String[] args) {
        // Supplier to get the current date and time
        Supplier<LocalDateTime> currentDateTimeSupplier = LocalDateTime::now;

        System.out.println("--- Supplier<LocalDateTime> Example ---");
        // Input: None, Output: Current LocalDateTime (e.g., 2023-10-27T10:30:45.123)
        System.out.println("Current Date and Time: " + currentDateTimeSupplier.get()); 
        System.out.println("Current Date and Time: " + currentDateTimeSupplier.get()); // Calling again gives new time

        // Supplier to generate a random Integer
        Supplier<Integer> randomNumberSupplier = () -> new Random().nextInt(100); // Random number between 0 (inclusive) and 100 (exclusive)

        System.out.println("\n--- Supplier<Integer> Random Number Example ---");
        // Input: None, Output: A random integer (e.g., 42)
        System.out.println("Random number: " + randomNumberSupplier.get()); 
        // Input: None, Output: Another random integer (e.g., 91)
        System.out.println("Random number: " + randomNumberSupplier.get()); 

        // Supplier for lazy initialization (e.g., a heavy object)
        class MyResource {
            private String name;
            public MyResource() {
                System.out.println("MyResource object created (heavy operation)");
                this.name = "Default Resource";
            }
            public String getName() { return name; }
        }

        System.out.println("\n--- Supplier for Lazy Initialization Example ---");
        System.out.println("Program starts, but resource not yet created.");
        Supplier<MyResource> resourceSupplier = MyResource::new; 

        System.out.println("Now we need the resource...");
        // The resource is only created when .get() is called
        // Input: None, Output: "MyResource object created (heavy operation)\nResource name: Default Resource"
        MyResource resource = resourceSupplier.get(); 
        System.out.println("Resource name: " + resource.getName());
    }
}
```

### 1.5. UnaryOperator&lt;T&gt;

*   **Package:** `java.util.function`
*   **Abstract Method:** `T apply(T t)`
*   **Purpose:** Represents an operation on a single operand that produces a result of the same type as its operand. It's a specialization of `Function<T, T>`.
*   **Static Methods:** `identity()`

**Example:** Incrementing a number, uppercasing a string.

```java
import java.util.function.UnaryOperator;

public class UnaryOperatorExample {
    public static void main(String[] args) {
        // UnaryOperator to square an Integer
        UnaryOperator<Integer> square = num -> num * num;

        System.out.println("--- UnaryOperator<Integer> Example ---");
        // Input: 5, Output: 25
        System.out.println("Square of 5: " + square.apply(5)); 
        // Input: 10, Output: 100
        System.out.println("Square of 10: " + square.apply(10)); 

        // UnaryOperator to convert a String to uppercase
        UnaryOperator<String> toUpperCase = String::toUpperCase;

        System.out.println("\n--- UnaryOperator<String> Example ---");
        // Input: "hello world", Output: "HELLO WORLD"
        System.out.println("Uppercase 'hello world': " + toUpperCase.apply("hello world")); 
        // Input: "java", Output: "JAVA"
        System.out.println("Uppercase 'java': " + toUpperCase.apply("java")); 

        // Static method: identity()
        UnaryOperator<Double> identityDouble = UnaryOperator.identity();
        System.out.println("\n--- UnaryOperator.identity() Example ---");
        // Input: 3.14, Output: 3.14
        System.out.println("Identity for 3.14: " + identityDouble.apply(3.14));
    }
}
```

### 1.6. BinaryOperator&lt;T&gt;

*   **Package:** `java.util.function`
*   **Abstract Method:** `T apply(T t1, T t2)`
*   **Purpose:** Represents an operation upon two operands of the same type, producing a result of the same type as the operands. It's a specialization of `BiFunction<T, T, T>`.
*   **Static Methods:** `minBy(Comparator comparator)`, `maxBy(Comparator comparator)`

**Example:** Summing two numbers, concatenating two strings.

```java
import java.util.function.BinaryOperator;
import java.util.Comparator;

public class BinaryOperatorExample {
    public static void main(String[] args) {
        // BinaryOperator to sum two Integers
        BinaryOperator<Integer> sum = (a, b) -> a + b;

        System.out.println("--- BinaryOperator<Integer> Example ---");
        // Input: 10, 20, Output: 30
        System.out.println("Sum of 10 and 20: " + sum.apply(10, 20)); 
        // Input: -5, 15, Output: 10
        System.out.println("Sum of -5 and 15: " + sum.apply(-5, 15)); 

        // BinaryOperator to concatenate two Strings
        BinaryOperator<String> concatenate = (s1, s2) -> s1 + " " + s2;

        System.out.println("\n--- BinaryOperator<String> Example ---");
        // Input: "Hello", "World", Output: "Hello World"
        System.out.println("Concatenated string: " + concatenate.apply("Hello", "World")); 
        // Input: "Java", "Programming", Output: "Java Programming"
        System.out.println("Concatenated string: " + concatenate.apply("Java", "Programming")); 

        // Static methods: minBy() and maxBy()
        BinaryOperator<Integer> findMin = BinaryOperator.minBy(Comparator.naturalOrder());
        BinaryOperator<Integer> findMax = BinaryOperator.maxBy(Comparator.naturalOrder());

        System.out.println("\n--- BinaryOperator minBy/maxBy Example ---");
        // Input: 7, 3, Output: 3
        System.out.println("Min of 7 and 3: " + findMin.apply(7, 3)); 
        // Input: 7, 3, Output: 7
        System.out.println("Max of 7 and 3: " + findMax.apply(7, 3)); 
    }
}
```

---

## 2. Bi-Functional Interfaces (Two Arguments)

These interfaces are similar to their single-argument counterparts but operate on two input arguments.

### 2.1. BiPredicate&lt;T, U&gt;

*   **Package:** `java.util.function`
*   **Abstract Method:** `boolean test(T t, U u)`
*   **Purpose:** Represents an operation that takes two arguments of potentially different types and returns a boolean result.
*   **Default Methods:** `and(BiPredicate other)`, `or(BiPredicate other)`, `negate()`

**Example:** Checking if two numbers meet a condition, or if a string starts with another.

```java
import java.util.function.BiPredicate;

public class BiPredicateExample {
    public static void main(String[] args) {
        // BiPredicate to check if the sum of two integers is greater than 10
        BiPredicate<Integer, Integer> sumGreaterThanTen = (a, b) -> (a + b) > 10;

        System.out.println("--- BiPredicate<Integer, Integer> Example ---");
        // Input: 5, 8, Output: true (5 + 8 = 13 > 10)
        System.out.println("Is sum of 5 and 8 greater than 10? " + sumGreaterThanTen.test(5, 8)); 
        // Input: 2, 3, Output: false (2 + 3 = 5 <= 10)
        System.out.println("Is sum of 2 and 3 greater than 10? " + sumGreaterThanTen.test(2, 3)); 

        // BiPredicate to check if a String starts with another String
        BiPredicate<String, String> startsWith = String::startsWith;

        System.out.println("\n--- BiPredicate<String, String> Example ---");
        // Input: "programming", "pro", Output: true
        System.out.println("'programming' starts with 'pro'? " + startsWith.test("programming", "pro")); 
        // Input: "java", "script", Output: false
        System.out.println("'java' starts with 'script'? " + startsWith.test("java", "script")); 
    }
}
```

### 2.2. BiConsumer&lt;T, U&gt;

*   **Package:** `java.util.function`
*   **Abstract Method:** `void accept(T t, U u)`
*   **Purpose:** Represents an operation that takes two input arguments of potentially different types and returns no result.
*   **Default Methods:** `andThen(BiConsumer after)`

**Example:** Printing two values, or putting a key-value pair into a map.

```java
import java.util.function.BiConsumer;
import java.util.HashMap;
import java.util.Map;

public class BiConsumerExample {
    public static void main(String[] args) {
        // BiConsumer to print two values
        BiConsumer<String, Integer> printDetails = (name, age) -> 
            System.out.println("Name: " + name + ", Age: " + age);

        System.out.println("--- BiConsumer<String, Integer> Example ---");
        // Input: "Alice", 30, Output: "Name: Alice, Age: 30"
        printDetails.accept("Alice", 30); 
        // Input: "Bob", 25, Output: "Name: Bob, Age: 25"
        printDetails.accept("Bob", 25); 

        // BiConsumer to put key-value pairs into a Map
        Map<String, String> capitalCities = new HashMap<>();
        BiConsumer<String, String> addEntryToMap = (country, capital) -> {
            capitalCities.put(country, capital);
            System.out.println("Added: " + country + " -> " + capital);
        };

        System.out.println("\n--- BiConsumer for Map Example ---");
        // Input: "France", "Paris", Output: "Added: France -> Paris"
        addEntryToMap.accept("France", "Paris"); 
        // Input: "Germany", "Berlin", Output: "Added: Germany -> Berlin"
        addEntryToMap.accept("Germany", "Berlin"); 

        System.out.println("Current map: " + capitalCities);
        // Output: Current map: {France=Paris, Germany=Berlin} (order may vary)
    }
}
```

### 2.3. BiFunction&lt;T, U, R&gt;

*   **Package:** `java.util.function`
*   **Abstract Method:** `R apply(T t, U u)`
*   **Purpose:** Represents an operation that takes two arguments of potentially different types and produces a result of a third type.
*   **Default Methods:** `andThen(Function after)`

**Example:** Calculating the product of two numbers, or combining two strings.

```java
import java.util.function.BiFunction;

public class BiFunctionExample {
    public static void main(String[] args) {
        // BiFunction to calculate the product of two Integers
        BiFunction<Integer, Integer, Integer> multiply = (a, b) -> a * b;

        System.out.println("--- BiFunction<Integer, Integer, Integer> Example ---");
        // Input: 5, 4, Output: 20
        System.out.println("Product of 5 and 4: " + multiply.apply(5, 4)); 
        // Input: 10, -2, Output: -20
        System.out.println("Product of 10 and -2: " + multiply.apply(10, -2)); 

        // BiFunction to combine a String and an Integer into a formatted String
        BiFunction<String, Integer, String> formatInfo = (name, score) -> 
            name + " scored " + score + " points.";

        System.out.println("\n--- BiFunction<String, Integer, String> Example ---");
        // Input: "Player1", 100, Output: "Player1 scored 100 points."
        System.out.println(formatInfo.apply("Player1", 100)); 
        // Input: "Player2", 75, Output: "Player2 scored 75 points."
        System.out.println(formatInfo.apply("Player2", 75)); 
    }
}
```

---

## 3. Primitive Functional Interfaces

### Purpose
To avoid the overhead of auto-boxing and auto-unboxing when dealing with primitive types (like `int`, `long`, `double`), the `java.util.function` package provides specialized functional interfaces for them. This improves performance, especially in scenarios involving many operations.

For example, instead of `Function<Integer, Integer>`, you might use `IntUnaryOperator`. Instead of `Predicate<Double>`, you might use `DoublePredicate`.

Common patterns:
*   `Int-`, `Long-`, `Double-` prefix: For functional interfaces whose arguments are primitives (e.g., `IntPredicate`, `LongConsumer`, `DoubleFunction<R>`).
*   `-To-` suffix: For functional interfaces that convert a primitive to another primitive (e.g., `LongToIntFunction`, `IntToDoubleFunction`).
*   `Obj-` prefix: For functional interfaces that take an object and a primitive (e.g., `ObjIntConsumer<T>`).

### Examples (IntPredicate, ToIntFunction, IntConsumer)

```java
import java.util.function.IntPredicate;
import java.util.function.ToIntFunction;
import java.util.function.IntConsumer;

public class PrimitiveFunctionalInterfacesExample {
    public static void main(String[] args) {
        // IntPredicate: Takes an int, returns boolean
        IntPredicate isPositive = num -> num > 0;
        System.out.println("--- IntPredicate Example ---");
        // Input: 5, Output: true
        System.out.println("Is 5 positive? " + isPositive.test(5)); 
        // Input: -3, Output: false
        System.out.println("Is -3 positive? " + isPositive.test(-3)); 

        // ToIntFunction<T>: Takes an object T, returns an int
        ToIntFunction<String> parseStringToInt = Integer::parseInt;
        System.out.println("\n--- ToIntFunction<String> Example ---");
        // Input: "123", Output: 123
        System.out.println("Parsed '123' to int: " + parseStringToInt.applyAsInt("123")); 
        // Input: "45", Output: 45
        System.out.println("Parsed '45' to int: " + parseStringToInt.applyAsInt("45")); 

        // IntConsumer: Takes an int, returns nothing (void)
        IntConsumer printSquared = num -> System.out.println("Squared: " + (num * num));
        System.out.println("\n--- IntConsumer Example ---");
        // Input: 6, Output: "Squared: 36"
        printSquared.accept(6); 
        // Input: 9, Output: "Squared: 81"
        printSquared.accept(9); 
    }
}
```

---

## Conclusion

The predefined functional interfaces in `java.util.function` are fundamental to modern Java programming. They provide a standardized, type-safe, and efficient way to work with lambda expressions and method references, enabling:

*   **Concise Code:** Expressing behavior directly without verbose anonymous inner classes.
*   **Functional Programming Style:** Promoting immutability, side-effect-free functions, and higher-order functions.
*   **API Design:** Serving as targets for many methods in the Java Stream API (e.g., `filter` takes a `Predicate`, `map` takes a `Function`, `forEach` takes a `Consumer`).
*   **Performance:** Primitive specializations avoid boxing/unboxing overhead.

By understanding and utilizing these interfaces, developers can write more expressive, powerful, and maintainable Java applications.