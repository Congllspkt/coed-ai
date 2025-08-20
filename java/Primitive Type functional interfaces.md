# Primitive Type Functional Interfaces in Java

Java 8 introduced the concept of functional interfaces, which are interfaces with a single abstract method (SAM). These interfaces are the cornerstone of lambda expressions and method references, enabling functional programming paradigms in Java.

While the `java.util.function` package provides general-purpose functional interfaces like `Predicate<T>`, `Consumer<T>`, `Function<T, R>`, and `Supplier<T>`, using them with primitive types (like `int`, `long`, `double`) can lead to **auto-boxing** and **auto-unboxing** overhead. This process involves converting primitive values to their corresponding wrapper objects (e.g., `int` to `Integer`) and vice-versa, which consumes extra memory and CPU cycles, potentially impacting performance in high-performance or large-scale applications.

To address this, Java provides specialized **primitive type functional interfaces** within the same `java.util.function` package. These interfaces operate directly on primitive values, avoiding the boxing/unboxing overhead. They primarily focus on `int`, `long`, and `double` because these are the most common primitive types used in numerical computations where performance is critical.

## Key Categories and Examples

The naming convention for these interfaces generally follows the pattern: `[Primitive]Type[ReturnPrimitive]FunctionalInterface`.

### 1. Primitive Predicates

**General Purpose:** `java.util.function.Predicate<T>`
*   Tests an input argument and returns a `boolean` result.
*   Abstract method: `boolean test(T t)`

**Primitive Versions:**
*   `IntPredicate`: `boolean test(int value)`
*   `LongPredicate`: `boolean test(long value)`
*   `DoublePredicate`: `boolean test(double value)`

**Why use it?** To perform boolean checks on primitive values without boxing.

**Example: `IntPredicate`**
```java
import java.util.function.IntPredicate;

public class PrimitivePredicateExample {
    public static void main(String[] args) {
        // Define an IntPredicate to check if a number is even
        IntPredicate isEven = (num) -> num % 2 == 0;

        // Test with int values
        boolean result1 = isEven.test(10);
        boolean result2 = isEven.test(7);

        System.out.println("Is 10 even? " + result1);
        System.out.println("Is 7 even? " + result2);
    }
}
```
*   **Input:** `isEven.test(10)`, `isEven.test(7)`
*   **Output:**
    ```
    Is 10 even? true
    Is 7 even? false
    ```

### 2. Primitive Consumers

**General Purpose:** `java.util.function.Consumer<T>`
*   Accepts a single input argument and returns no result (i.e., `void`). Used for side-effects.
*   Abstract method: `void accept(T t)`

**Primitive Versions:**
*   `IntConsumer`: `void accept(int value)`
*   `LongConsumer`: `void accept(long value)`
*   `DoubleConsumer`: `void accept(double value)`

**Why use it?** To perform an action on a primitive value, like printing it or modifying an external state.

**Example: `IntConsumer`**
```java
import java.util.function.IntConsumer;

public class PrimitiveConsumerExample {
    public static void main(String[] args) {
        // Define an IntConsumer to print an integer
        IntConsumer printNumber = (num) -> System.out.println("Processed number: " + num);

        // Accept int values
        printNumber.accept(42);
        printNumber.accept(-5);
    }
}
```
*   **Input:** `printNumber.accept(42)`, `printNumber.accept(-5)`
*   **Output:**
    ```
    Processed number: 42
    Processed number: -5
    ```

### 3. Primitive Functions

**General Purpose:** `java.util.function.Function<T, R>`
*   Applies a function to an input argument `T` and returns a result `R`.
*   Abstract method: `R apply(T t)`

Primitive functions come in several flavors to handle different input and output types:

*   **`[Primitive]Function<R>`:** Takes a primitive, returns a generic object.
    *   `IntFunction<R>`: `R apply(int value)`
    *   `LongFunction<R>`: `R apply(long value)`
    *   `DoubleFunction<R>`: `R apply(double value)`

*   **`To[Primitive]Function<T>`:** Takes a generic object, returns a primitive.
    *   `ToIntFunction<T>`: `int applyAsInt(T value)`
    *   `ToLongFunction<T>`: `long applyAsLong(T value)`
    *   `ToDoubleFunction<T>`: `double applyAsDouble(T value)`

*   **`[Primitive1]To[Primitive2]Function`:** Takes one primitive type, returns another primitive type.
    *   `IntToLongFunction`: `long applyAsLong(int value)`
    *   `IntToDoubleFunction`: `double applyAsDouble(int value)`
    *   `LongToIntFunction`: `int applyAsInt(long value)`
    *   ...and so on for all combinations.

**Why use it?** To transform primitive values or transform objects to primitive values, avoiding boxing/unboxing during the transformation.

**Example 1: `IntFunction<R>` (int to Object)**
```java
import java.util.function.IntFunction;

public class PrimitiveFunctionExample1 {
    public static void main(String[] args) {
        // Converts an int to a String
        IntFunction<String> intToString = (num) -> "Number is: " + num;

        String result1 = intToString.apply(123);
        String result2 = intToString.apply(-99);

        System.out.println(result1);
        System.out.println(result2);
    }
}
```
*   **Input:** `intToString.apply(123)`, `intToString.apply(-99)`
*   **Output:**
    ```
    Number is: 123
    Number is: -99
    ```

**Example 2: `ToIntFunction<T>` (Object to int)**
```java
import java.util.function.ToIntFunction;

public class PrimitiveFunctionExample2 {
    public static void main(String[] args) {
        // Extracts the length of a String as an int
        ToIntFunction<String> stringLength = (str) -> str.length();

        int len1 = stringLength.applyAsInt("Hello World");
        int len2 = stringLength.applyAsInt("Java");

        System.out.println("Length of 'Hello World': " + len1);
        System.out.println("Length of 'Java': " + len2);
    }
}
```
*   **Input:** `stringLength.applyAsInt("Hello World")`, `stringLength.applyAsInt("Java")`
*   **Output:**
    ```
    Length of 'Hello World': 11
    Length of 'Java': 4
    ```

**Example 3: `IntToDoubleFunction` (int to double)**
```java
import java.util.function.IntToDoubleFunction;

public class PrimitiveFunctionExample3 {
    public static void main(String[] args) {
        // Converts an int to its square root as a double
        IntToDoubleFunction sqrtFunction = (num) -> Math.sqrt(num);

        double sqrt1 = sqrtFunction.applyAsDouble(25);
        double sqrt2 = sqrtFunction.applyAsDouble(2);

        System.out.println("Square root of 25: " + sqrt1);
        System.out.println("Square root of 2: " + sqrt2);
    }
}
```
*   **Input:** `sqrtFunction.applyAsDouble(25)`, `sqrtFunction.applyAsDouble(2)`
*   **Output:**
    ```
    Square root of 25: 5.0
    Square root of 2: 1.4142135623730951
    ```

### 4. Primitive Suppliers

**General Purpose:** `java.util.function.Supplier<T>`
*   Represents a supplier of results. Takes no arguments.
*   Abstract method: `T get()`

**Primitive Versions:**
*   `IntSupplier`: `int getAsInt()`
*   `LongSupplier`: `long getAsLong()`
*   `DoubleSupplier`: `double getAsDouble()`

**Why use it?** To generate or retrieve a primitive value without arguments.

**Example: `IntSupplier`**
```java
import java.util.Random;
import java.util.function.IntSupplier;

public class PrimitiveSupplierExample {
    public static void main(String[] args) {
        // Supplies a random integer between 0 (inclusive) and 100 (exclusive)
        IntSupplier randomIntSupplier = () -> new Random().nextInt(100);

        int num1 = randomIntSupplier.getAsInt();
        int num2 = randomIntSupplier.getAsInt();

        System.out.println("Random number 1: " + num1);
        System.out.println("Random number 2: " + num2);
    }
}
```
*   **Input:** `randomIntSupplier.getAsInt()` (called twice)
*   **Output:** (Example, output will vary due to randomness)
    ```
    Random number 1: 57
    Random number 2: 12
    ```

### 5. Primitive Unary Operators

**General Purpose:** `java.util.function.UnaryOperator<T>`
*   Represents an operation on a single operand of type `T` that produces a result of type `T`. It's a specialization of `Function<T, T>`.
*   Abstract method: `T apply(T t)`

**Primitive Versions:**
*   `IntUnaryOperator`: `int applyAsInt(int operand)`
*   `LongUnaryOperator`: `long applyAsLong(long operand)`
*   `DoubleUnaryOperator`: `double applyAsDouble(double operand)`

**Why use it?** To perform an operation that transforms a primitive value into a primitive value of the same type.

**Example: `IntUnaryOperator`**
```java
import java.util.function.IntUnaryOperator;

public class PrimitiveUnaryOperatorExample {
    public static void main(String[] args) {
        // Squares an integer
        IntUnaryOperator square = (num) -> num * num;

        int result1 = square.applyAsInt(5);
        int result2 = square.applyAsInt(-3);

        System.out.println("Square of 5: " + result1);
        System.out.println("Square of -3: " + result2);
    }
}
```
*   **Input:** `square.applyAsInt(5)`, `square.applyAsInt(-3)`
*   **Output:**
    ```
    Square of 5: 25
    Square of -3: 9
    ```

### 6. Primitive Binary Operators

**General Purpose:** `java.util.function.BinaryOperator<T>`
*   Represents an operation upon two operands of type `T` that produces a result of type `T`. It's a specialization of `BiFunction<T, T, T>`.
*   Abstract method: `T apply(T t1, T t2)`

**Primitive Versions:**
*   `IntBinaryOperator`: `int applyAsInt(int left, int right)`
*   `LongBinaryOperator`: `long applyAsLong(long left, long right)`
*   `DoubleBinaryOperator`: `double applyAsDouble(double left, double right)`

**Why use it?** To perform an operation that combines two primitive values of the same type into a single primitive value of that type.

**Example: `IntBinaryOperator`**
```java
import java.util.function.IntBinaryOperator;

public class PrimitiveBinaryOperatorExample {
    public static void main(String[] args) {
        // Adds two integers
        IntBinaryOperator add = (a, b) -> a + b;

        // Finds the maximum of two integers
        IntBinaryOperator max = (a, b) -> Math.max(a, b);

        int sum = add.applyAsInt(10, 20);
        int maximum = max.applyAsInt(15, 7);

        System.out.println("Sum of 10 and 20: " + sum);
        System.out.println("Max of 15 and 7: " + maximum);
    }
}
```
*   **Input:** `add.applyAsInt(10, 20)`, `max.applyAsInt(15, 7)`
*   **Output:**
    ```
    Sum of 10 and 20: 30
    Max of 15 and 7: 15
    ```

### 7. Mixed-Type Functional Interfaces

Besides the above, there are also interfaces that combine a generic type with a primitive type, for example:

*   **`ObjIntConsumer<T>`:** `void accept(T t, int value)`
*   **`ObjLongConsumer<T>`:** `void accept(T t, long value)`
*   **`ObjDoubleConsumer<T>`:** `void accept(T t, double value)`
*   **`ToIntBiFunction<T, U>`:** `int applyAsInt(T t, U u)`
*   ...and many more for various combinations.

**Example: `ObjIntConsumer`**
```java
import java.util.ArrayList;
import java.util.List;
import java.util.function.ObjIntConsumer;

public class ObjIntConsumerExample {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>();
        names.add("Alice");
        names.add("Bob");
        names.add("Charlie");

        // Print each name along with its index
        ObjIntConsumer<String> indexedPrinter = (name, index) ->
            System.out.println("Index " + index + ": " + name);

        for (int i = 0; i < names.size(); i++) {
            indexedPrinter.accept(names.get(i), i);
        }
    }
}
```
*   **Input:** Iterating through a `List<String>` and its index.
*   **Output:**
    ```
    Index 0: Alice
    Index 1: Bob
    Index 2: Charlie
    ```

## Advantages of Primitive Type Functional Interfaces

1.  **Performance:** Eliminates the overhead of auto-boxing and auto-unboxing, leading to faster execution, especially in loops or high-frequency operations.
2.  **Memory Efficiency:** Reduces memory consumption by avoiding the creation of numerous wrapper objects on the heap.
3.  **Clarity:** Makes it explicit that the operation deals with primitive types, improving code readability for developers familiar with these interfaces.
4.  **Avoids NullPointerExceptions:** Since primitives cannot be `null`, these interfaces inherently avoid `NullPointerExceptions` that could arise if wrapper objects were used (e.g., `Integer i = null; i.intValue();`).

## Conclusion

While `java.util.function` provides flexible generic functional interfaces, Java's primitive type functional interfaces are a crucial optimization for scenarios involving frequent operations on `int`, `long`, and `double` values. By using them judiciously, developers can write more performant and memory-efficient code while fully embracing the power of Java 8's functional programming features.