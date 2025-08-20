# Introduction to Method References in Java

Method References, introduced in Java 8 alongside Lambda Expressions, provide a concise and readable way to refer to methods without executing them. They are a special type of lambda expression that just calls an existing method.

## What are Method References?

In essence, a Method Reference is a shorthand syntax for a lambda expression that does nothing but call an existing method. When you have a lambda expression that simply calls an existing method, you can use a Method Reference instead, making the code more readable and compact.

**For example:**

A lambda expression `(args) -> Class.staticMethod(args)` can be written as `Class::staticMethod`.
A lambda expression `(args) -> object.instanceMethod(args)` can be written as `object::instanceMethod`.

Method references are used to simplify code by allowing you to treat methods as if they were values. They are compatible with functional interfaces, as they provide an implementation for the abstract method of that functional interface.

## Why use Method References?

1.  **Readability and Conciseness:** They make your code cleaner and easier to understand, especially when the lambda expression's body is a simple method call.
2.  **Reduced Boilerplate:** They eliminate the need for verbose lambda expressions in certain scenarios.
3.  **Leveraging Existing Code:** They encourage the reuse of existing methods, promoting a more functional programming style.

## General Syntax

The syntax for a method reference is `ClassName::methodName` or `objectName::methodName` or `ClassName::new`. The `::` is a new operator introduced in Java 8, used specifically for method references.

## Types of Method References with Examples

There are four main types of method references:

### 1. Reference to a Static Method

This type refers to a `static` method of a class. The functional interface's abstract method signature must be compatible with the static method's signature.

*   **Syntax:** `ClassName::staticMethodName`

**Example:**
Let's say we have a utility class `MyMathUtils` with a static method `add`. We can use a method reference to pass this `add` method to a functional interface like `IntBinaryOperator`.

```java
// MyMathUtils.java
class MyMathUtils {
    public static int add(int a, int b) {
        return a + b;
    }

    public static int subtract(int a, int b) {
        return a - b;
    }
}

// MethodReferenceStatic.java
import java.util.function.IntBinaryOperator;

public class MethodReferenceStatic {
    public static void main(String[] args) {
        // Using a lambda expression
        IntBinaryOperator adderLambda = (a, b) -> MyMathUtils.add(a, b);
        System.out.println("Lambda Result (5 + 3): " + adderLambda.applyAsInt(5, 3));

        // Using a method reference to a static method
        // MyMathUtils::add is equivalent to (a, b) -> MyMathUtils.add(a, b)
        IntBinaryOperator adderMethodRef = MyMathUtils::add;
        System.out.println("Method Reference Result (10 + 7): " + adderMethodRef.applyAsInt(10, 7));

        // Another example with subtract
        IntBinaryOperator subtractorMethodRef = MyMathUtils::subtract;
        System.out.println("Method Reference Result (20 - 8): " + subtractorMethodRef.applyAsInt(20, 8));
    }
}
```

**Input (Implicit):** The `main` method directly provides the input values for `applyAsInt`.

**Output:**

```
Lambda Result (5 + 3): 8
Method Reference Result (10 + 7): 17
Method Reference Result (20 - 8): 12
```

### 2. Reference to an Instance Method of a Particular Object

This type refers to an instance method of a specific, already-created object.

*   **Syntax:** `objectName::instanceMethodName`

**Example:**
Consider a `Logger` class. We can create an instance of `Logger` and then refer to its `log` method.

```java
// Logger.java
class Logger {
    private String prefix;

    public Logger(String prefix) {
        this.prefix = prefix;
    }

    public void log(String message) {
        System.out.println("[" + prefix + "] " + message);
    }
}

// MethodReferenceInstanceObject.java
import java.util.function.Consumer;

public class MethodReferenceInstanceObject {
    public static void main(String[] args) {
        Logger appLogger = new Logger("APP");
        Logger errorLogger = new Logger("ERROR");

        // Using a lambda expression with appLogger
        Consumer<String> logLambda = message -> appLogger.log(message);
        logLambda.accept("User logged in.");

        // Using a method reference to an instance method of a particular object (appLogger)
        // appLogger::log is equivalent to message -> appLogger.log(message)
        Consumer<String> logMethodRefApp = appLogger::log;
        logMethodRefApp.accept("Data processed successfully.");

        // Using a method reference with errorLogger
        Consumer<String> logMethodRefError = errorLogger::log;
        logMethodRefError.accept("Failed to connect to database.");
    }
}
```

**Input (Implicit):** The `main` method directly provides the input strings for `accept`.

**Output:**

```
[APP] User logged in.
[APP] Data processed successfully.
[ERROR] Failed to connect to database.
```

### 3. Reference to an Instance Method of an Arbitrary Object of a Particular Type

This type is used when the method reference is to an instance method, but the target object is specified by the first argument to the functional interface's abstract method. This is common with methods that operate on their own type (e.g., `String::compareTo`).

*   **Syntax:** `ClassName::instanceMethodName`

**Example:**
Sorting a list of strings ignoring case using `String.compareToIgnoreCase`. Here, `compareToIgnoreCase` is an instance method, but the *first* argument to the `Comparator` functional interface `(s1, s2)` will be the object on which the method is called (`s1`), and the second argument will be passed to the method (`s2`).

```java
// MethodReferenceArbitraryInstance.java
import java.util.Arrays;
import java.util.List;
import java.util.Collections;
import java.util.Comparator;

public class MethodReferenceArbitraryInstance {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "bob", "Charlie", "David", "alice");

        System.out.println("Original List: " + names);

        // Using a lambda expression for case-insensitive sort
        // (s1, s2) -> s1.compareToIgnoreCase(s2)
        Comparator<String> caseInsensitiveLambda = (s1, s2) -> s1.compareToIgnoreCase(s2);
        Collections.sort(names, caseInsensitiveLambda);
        System.out.println("Sorted (Lambda): " + names);

        // Reset list for second sort example
        names = Arrays.asList("Gamma", "alpha", "Beta", "delta");
        System.out.println("\nOriginal List for Method Reference: " + names);

        // Using a method reference for case-insensitive sort
        // String::compareToIgnoreCase is equivalent to (s1, s2) -> s1.compareToIgnoreCase(s2)
        Comparator<String> caseInsensitiveMethodRef = String::compareToIgnoreCase;
        Collections.sort(names, caseInsensitiveMethodRef);
        System.out.println("Sorted (Method Reference): " + names);
    }
}
```

**Input (Implicit):** The `main` method directly provides the list of strings.

**Output:**

```
Original List: [Alice, bob, Charlie, David, alice]
Sorted (Lambda): [Alice, alice, bob, Charlie, David]

Original List for Method Reference: [Gamma, alpha, Beta, delta]
Sorted (Method Reference): [alpha, Beta, delta, Gamma]
```

### 4. Reference to a Constructor

This type refers to a constructor. It's useful when you need to create new objects of a specific class. The functional interface's abstract method signature must be compatible with the constructor's signature (i.e., the number and types of arguments).

*   **Syntax:** `ClassName::new`

**Example:**
Let's define a `Person` class with different constructors. We can use constructor references to create `Person` objects through functional interfaces.

```java
// Person.java
class Person {
    private String name;
    private int age;

    public Person(String name) {
        this.name = name;
        this.age = 0; // Default age
    }

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + "}";
    }
}

// MethodReferenceConstructor.java
import java.util.function.Function;
import java.util.function.BiFunction;

public class MethodReferenceConstructor {
    public static void main(String[] args) {
        // Reference to a constructor with one argument (String name)
        // Person::new (for Person(String name)) is equivalent to name -> new Person(name)
        Function<String, Person> personCreatorByName = Person::new;
        Person alice = personCreatorByName.apply("Alice");
        System.out.println("Created using 1-arg constructor ref: " + alice);

        // Reference to a constructor with two arguments (String name, int age)
        // Person::new (for Person(String name, int age)) is equivalent to (name, age) -> new Person(name, age)
        BiFunction<String, Integer, Person> personCreatorByNameAndAge = Person::new;
        Person bob = personCreatorByNameAndAge.apply("Bob", 30);
        System.out.println("Created using 2-arg constructor ref: " + bob);
    }
}
```

**Input (Implicit):** The `main` method directly provides the arguments for `apply`.

**Output:**

```
Created using 1-arg constructor ref: Person{name='Alice', age=0}
Created using 2-arg constructor ref: Person{name='Bob', age=30}
```

## Conclusion

Method references are a powerful feature in Java 8 that enhance the readability and conciseness of code, especially when working with lambda expressions and functional interfaces. By allowing you to directly refer to existing methods, they promote a more elegant and functional programming style, reducing boilerplate and making your code easier to maintain. Understanding the four types of method references is key to effectively utilizing this feature in your Java applications.