This document provides a detailed explanation of Unnamed Variables and Patterns in Java 22, including their purpose, syntax, use cases, and examples.

---

# Unnamed Variables & Patterns in Java 22

## Introduction

Java 22, following previews in Java 21, finalizes **Unnamed Variables and Patterns** (JEP 443). This feature introduces the single underscore character (`_`) as a special identifier to represent a variable or pattern component that is not intended to be used. Its primary goal is to improve code readability, conciseness, and reduce the noise of unused variable warnings, especially in situations where a variable or a part of a pattern match is required by the syntax but is semantically irrelevant to the logic.

Before Java 9, `_` was a valid identifier. Since Java 9, `_` has been a keyword and cannot be used as an identifier to avoid conflicts with future uses. Unnamed variables and patterns are the intended future use of this keyword.

## The `_` Identifier: More Than Just a Discard

The underscore `_` acts as a "silent" placeholder. It signifies to both the compiler and other developers that a particular binding or component is intentionally ignored.

### Benefits:

*   **Readability:** Clearly indicates when a variable or pattern component is intentionally unused.
*   **Conciseness:** Reduces boilerplate code and the need for artificial variable names.
*   **Reduced Warnings:** Eliminates compiler warnings for unused variables, which helps keep the codebase clean and focus on genuine issues.
*   **Clarity of Intent:** Makes the programmer's intent explicit.

## 1. Unnamed Variables

An unnamed variable is a local variable declared with `_` as its name. It can only be used in contexts where a local variable declaration is syntactically required but its value is not needed for the program's logic.

### Syntax:

```java
Type _ = expression; // Not allowed as a standalone declaration
```
Unnamed variables are not for general-purpose variable declaration. They are specifically for situations where a variable *must* be declared but its value is discarded.

### Common Use Cases with Examples:

#### a) Catch Block Parameters

Often, in a `try-catch` block, the caught exception object itself is not used, but merely the fact that an exception occurred is sufficient (e.g., for logging or cleanup).

**Before Java 22:**

```java
// Input: BeforeJava22.java
public class BeforeJava22 {
    public static void main(String[] args) {
        try {
            int result = 10 / 0; // This will throw ArithmeticException
        } catch (ArithmeticException e) { // 'e' is not used
            System.out.println("An arithmetic error occurred.");
            // Compiler might warn about unused variable 'e'
        }
    }
}
```

**Output (Console):**

```
An arithmetic error occurred.
```
*(You might also get a compiler warning like "The value of the local variable e is not used")*

**With Java 22 (Unnamed Variable):**

```java
// Input: WithUnnamedVariable.java
public class WithUnnamedVariable {
    public static void main(String[] args) {
        try {
            int result = 10 / 0; // This will throw ArithmeticException
        } catch (ArithmeticException _) { // '_' clearly indicates exception object is ignored
            System.out.println("An arithmetic error occurred.");
        }
    }
}
```

**Output (Console):**

```
An arithmetic error occurred.
```
*(No compiler warning for unused variable `_`)*

#### b) `for` Loop Iteration Variables

In an enhanced `for` loop, if you only care about the number of iterations or side effects within the loop body, but not the iterated element itself.

**Before Java 22:**

```java
// Input: BeforeForLoop.java
public class BeforeForLoop {
    public static void main(String[] args) {
        int count = 0;
        int[] numbers = {1, 2, 3, 4, 5};
        for (int number : numbers) { // 'number' is not used
            count++;
        }
        System.out.println("Number of elements: " + count);
    }
}
```

**Output (Console):**

```
Number of elements: 5
```
*(Compiler might warn about unused variable 'number')*

**With Java 22 (Unnamed Variable):**

```java
// Input: WithUnnamedForLoop.java
public class WithUnnamedForLoop {
    public static void main(String[] args) {
        int count = 0;
        int[] numbers = {1, 2, 3, 4, 5};
        for (int _ : numbers) { // '_' indicates the element itself is ignored
            count++;
        }
        System.out.println("Number of elements: " + count);
    }
}
```

**Output (Console):**

```
Number of elements: 5
```
*(No compiler warning for unused variable `_`)*

#### c) Lambda Expression Parameters

When a lambda expression requires multiple parameters but only some of them are used.

**Before Java 22:**

```java
// Input: BeforeLambda.java
import java.util.function.BiConsumer;

public class BeforeLambda {
    public static void main(String[] args) {
        BiConsumer<String, Integer> logger = (message, unusedValue) -> { // 'unusedValue' is not used
            System.out.println("Log: " + message);
        };
        logger.accept("Application started", 42);
        logger.accept("Processing data", 100);
    }
}
```

**Output (Console):**

```
Log: Application started
Log: Processing data
```
*(Compiler might warn about unused variable 'unusedValue')*

**With Java 22 (Unnamed Variable):**

```java
// Input: WithUnnamedLambda.java
import java.util.function.BiConsumer;

public class WithUnnamedLambda {
    public static void main(String[] args) {
        BiConsumer<String, Integer> logger = (message, _) -> { // '_' clearly indicates the integer is ignored
            System.out.println("Log: " + message);
        };
        logger.accept("Application started", 42);
        logger.accept("Processing data", 100);
    }
}
```

**Output (Console):**

```
Log: Application started
Log: Processing data
```
*(No compiler warning for unused variable `_`)*

**Note:** An unnamed variable cannot be the *only* parameter in a lambda expression. If you have a single-parameter lambda and don't use the parameter, you must still name it (e.g., `(unused) -> ...`). This is to prevent ambiguity with a no-argument lambda `() -> ...`.

```java
// Not allowed:
// Consumer<String> printer = (_) -> System.out.println("Hello"); 
// This will result in a compile error.
```

## 2. Unnamed Patterns

Unnamed patterns allow you to discard components within a pattern match, especially useful with record patterns and type patterns in `instanceof` and `switch` expressions/statements. They allow you to match against a structure without binding all its components to variables.

### Syntax:

```java
_ // As a standalone pattern (e.g., in switch)
Type _ // As a type pattern (e.g., instanceof)
Record(_, component2, _) // Inside a record pattern
```

### Common Use Cases with Examples:

#### a) `instanceof` with Pattern Matching

You might want to check an object's type or a partial structure without needing to extract all its components.

Assume a `Point` record:

```java
// Input: PointRecord.java
record Point(int x, int y) {}
```

**Before Java 22:**

```java
// Input: BeforeInstanceOf.java
public class BeforeInstanceOf {
    public static void main(String[] args) {
        Object obj1 = new Point(10, 20);
        Object obj2 = "Hello";

        if (obj1 instanceof Point p) { // 'p' itself or its components might not be fully used
            System.out.println("obj1 is a Point.");
            // If only checking type, 'p' is unused: if (obj1 instanceof Point point) { /* ... */ }
        }

        // Example with Record pattern (Java 16+) where 'x' is not used
        if (obj1 instanceof Point(int x, int y)) { // 'x' is not used
            System.out.println("Point coordinates (y only): " + y);
        }
    }
}
```

**Output (Console):**

```
obj1 is a Point.
Point coordinates (y only): 20
```
*(Compiler might warn about unused variables `p` or `x`)*

**With Java 22 (Unnamed Patterns):**

```java
// Input: WithUnnamedInstanceOf.java
public class WithUnnamedInstanceOf {
    record Point(int x, int y) {} // Define record here for self-containment

    public static void main(String[] args) {
        Object obj1 = new Point(10, 20);
        Object obj2 = "Hello";

        // Unnamed type pattern: only check if it's a Point, don't bind to a variable
        if (obj1 instanceof Point _) { // '_' indicates we don't need the Point object itself
            System.out.println("obj1 is a Point (type only check).");
        }

        // Unnamed record pattern: Check if it's a Point, only extract 'y'
        if (obj1 instanceof Point(_, int y)) { // '_' discards 'x' component
            System.out.println("obj1 is a Point. Y coordinate: " + y);
        }

        // Unnamed record pattern: Check if it's a Point, discard all components
        if (obj1 instanceof Point(_, _)) { // '_' discards both 'x' and 'y' components
             System.out.println("obj1 is a Point (components ignored).");
        }

        // A standalone unnamed pattern (e.g., in a switch statement)
        if (obj2 instanceof String _) {
            System.out.println("obj2 is a String (type check only).");
        }
    }
}
```

**Output (Console):**

```
obj1 is a Point (type only check).
obj1 is a Point. Y coordinate: 20
obj1 is a Point (components ignored).
obj2 is a String (type check only).
```
*(No compiler warnings)*

#### b) `switch` Expressions/Statements with Pattern Matching

Unnamed patterns are especially powerful in `switch` statements or expressions when dealing with sealed classes or records where you need to exhaustively cover types or specific structures, but don't need all the extracted data.

Assume a `Shape` sealed interface and its implementations:

```java
// Input: Shapes.java
sealed interface Shape permits Circle, Rectangle, Triangle {}
record Circle(double radius) implements Shape {}
record Rectangle(double width, double height) implements Shape {}
record Triangle(double side1, double side2, double side3) implements Shape {}
```

**Before Java 22:**

```java
// Input: BeforeSwitch.java
public class BeforeSwitch {
    public static void main(String[] args) {
        Shape shape1 = new Circle(5.0);
        Shape shape2 = new Rectangle(10.0, 20.0);
        Shape shape3 = new Triangle(3.0, 4.0, 5.0);
        Shape shape4 = null; // To demonstrate default/null handling

        printShapeInfo(shape1);
        printShapeInfo(shape2);
        printShapeInfo(shape3);
        printShapeInfo(shape4);
    }

    public static void printShapeInfo(Shape shape) {
        // Here, if we only care about the type of Rectangle, but not its dimensions
        String info = switch (shape) {
            case Circle c -> "Circle with radius " + c.radius();
            case Rectangle r -> "It's a Rectangle (dimensions ignored)"; // 'r' is unused if we only print this
            case Triangle t -> "Triangle (sides: " + t.side1() + ", " + t.side2() + ", " + t.side3() + ")";
            case null -> "Null shape"; // null pattern (Java 17+)
            default -> "Unknown shape"; // Exhaustive for sealed types sometimes requires this
        };
        System.out.println(info);
    }
}
```

**Output (Console):**

```
Circle with radius 5.0
It's a Rectangle (dimensions ignored)
Triangle (sides: 3.0, 4.0, 5.0)
Null shape
```
*(Compiler might warn about unused variable `r`)*

**With Java 22 (Unnamed Patterns):**

```java
// Input: WithUnnamedSwitch.java
public class WithUnnamedSwitch {
    // Define sealed interface and records for self-containment
    sealed interface Shape permits Circle, Rectangle, Triangle {}
    record Circle(double radius) implements Shape {}
    record Rectangle(double width, double height) implements Shape {}
    record Triangle(double side1, double side2, double side3) implements Shape {}

    public static void main(String[] args) {
        Shape shape1 = new Circle(5.0);
        Shape shape2 = new Rectangle(10.0, 20.0);
        Shape shape3 = new Triangle(3.0, 4.0, 5.0);
        Shape shape4 = null;

        printShapeInfo(shape1);
        printShapeInfo(shape2);
        printShapeInfo(shape3);
        printShapeInfo(shape4);
    }

    public static void printShapeInfo(Shape shape) {
        String info = switch (shape) {
            case Circle c -> "Circle with radius " + c.radius();
            // Unnamed type pattern: Match Rectangle, but don't bind it to a variable
            case Rectangle _ -> "It's a Rectangle (dimensions ignored)";
            // Unnamed record pattern: Match Triangle, but discard all its components
            case Triangle(_, _, _) -> "It's a Triangle (specific sides ignored)";
            case null -> "Null shape";
            // Unnamed pattern as a default case.
            // This is useful for exhaustiveness when a specific value/type doesn't matter,
            // or for a truly "default" case in non-sealed scenarios.
            case _ -> "Unhandled shape type"; // Matches any other non-null object
        };
        System.out.println(info);
    }
}
```

**Output (Console):**

```
Circle with radius 5.0
It's a Rectangle (dimensions ignored)
It's a Triangle (specific sides ignored)
Null shape
```
*(No compiler warnings)*

## Key Restrictions and Limitations

*   **Not a General-Purpose Identifier:** `_` cannot be used as a name for fields, method parameters (unless it's part of a lambda), constructor parameters, or local variables that are intended to be used. It's strictly for discarding values.
*   **Cannot be Reassigned/Accessed:** An unnamed variable or pattern cannot be assigned to or read from. Attempting to do so will result in a compile-time error.
    ```java
    // Example:
    try {
        // ...
    } catch (Exception _) {
        // System.out.println(_); // COMPILE ERROR: Cannot access '_'
        // _ = new IOException();  // COMPILE ERROR: Cannot assign to '_'
    }
    ```
*   **No `var` with `_`:** You cannot use `var _ = ...;`. The type must be explicit.
*   **Not for Field/Method/Constructor Parameters:** `private int _;` or `public void myMethod(int _) {}` are not allowed.
*   **Not for Type Names:** You cannot define a class, interface, or enum named `_`.
*   **Single Lambda Parameter:** As mentioned, `_` cannot be the *only* parameter in a lambda expression.

## Conclusion

Unnamed Variables and Patterns in Java 22 provide a clean and explicit way to handle situations where variables or pattern components are syntactically required but semantically irrelevant. By using the underscore `_`, developers can write more readable, concise, and warning-free code, clearly signaling their intent to ignore certain values. This feature is a valuable addition to Java's ongoing efforts to modernize its language constructs for better expressiveness and developer experience.