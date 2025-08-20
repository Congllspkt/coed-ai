# Deep Dive on `java.util.function.UnaryOperator`

The `java.util.function.UnaryOperator` interface is a specialized functional interface introduced in Java 8 as part of the `java.util.function` package. It extends the `Function` interface and is designed for operations where the input type and the output type are the same.

## 1. What is `UnaryOperator`?

At its core, a `UnaryOperator` represents an operation that takes a **single operand** of a specific type and produces a **result of the same type** as its operand.

It's essentially a `Function<T, T>`, meaning its `apply` method takes an argument of type `T` and returns a result of type `T`. The `UnaryOperator` interface simply provides a convenient and semantically clearer alias for this common pattern.

## 2. Interface Signature and Type Parameters

```java
@FunctionalInterface
public interface UnaryOperator<T> extends Function<T, T> {

    /**
     * Returns a unary operator that always returns its input argument.
     *
     * @param <T> the type of the input and output of the operator
     * @return a unary operator that always returns its input argument
     */
    static <T> UnaryOperator<T> identity() {
        return t -> t;
    }
}
```

*   **`@FunctionalInterface`**: This annotation indicates that `UnaryOperator` is a functional interface, meaning it has exactly one abstract method. This allows it to be used with lambda expressions and method references.
*   **`<T>`**: This is a type parameter representing the type of both the input argument and the result of the operation.
*   **`extends Function<T, T>`**: This is the key detail. `UnaryOperator` doesn't define any new abstract methods. It inherits the `apply(T t)` method from `Function<T, T>`.

## 3. Key Characteristics

*   **Single Argument**: Takes one input.
*   **Same Type Input/Output**: The type of the input argument is identical to the type of the result.
*   **Functional Interface**: Can be implemented using lambda expressions or method references.
*   **Specialization of `Function`**: It's a convenient alias for `Function<T, T>`.

## 4. Difference from `Function`

This is a common point of confusion.

*   **`Function<T, R>`**: Takes an input of type `T` and produces an output of type `R`. `T` and `R` can be, and often are, different types.
    *   *Example*: `Function<String, Integer>` (calculates string length)
    *   *Example*: `Function<Integer, String>` (converts an integer to a string)

*   **`UnaryOperator<T>`**: Takes an input of type `T` and produces an output of type `T`. The input and output types *must* be the same.
    *   *Example*: `UnaryOperator<Integer>` (squares an integer)
    *   *Example*: `UnaryOperator<String>` (converts a string to uppercase)

In essence, every `UnaryOperator<T>` *is a* `Function<T, T>`, but not every `Function<T, R>` is a `UnaryOperator` (unless `T` and `R` happen to be the same type).

## 5. Inherited Method: `apply(T t)`

Since `UnaryOperator` extends `Function<T, T>`, its single abstract method is `apply(T t)`.

*   **Signature**: `T apply(T t)`
*   **Purpose**: To perform the operation on the given argument `t` and return the result of the same type `T`.

## 6. Static Method: `identity()`

`UnaryOperator` provides a useful static factory method:

*   **Signature**: `static <T> UnaryOperator<T> identity()`
*   **Purpose**: Returns a `UnaryOperator` that always returns its input argument unchanged. It's like the mathematical identity function `f(x) = x`.
*   **Use Case**: This is often useful as a default operation or when you need a "no-op" operator in a chain of transformations.

## 7. Practical Examples

Let's illustrate with various scenarios.

### Example 1: Integer Transformation

**Goal**: Create operators to square an integer and to increment an integer.

```java
import java.util.function.UnaryOperator;

public class IntegerOperatorExample {

    public static void main(String[] args) {
        // 1. UnaryOperator to square an integer
        UnaryOperator<Integer> square = x -> x * x;

        // 2. UnaryOperator to increment an integer by 1
        UnaryOperator<Integer> increment = x -> x + 1;

        // Test cases
        System.out.println("--- Integer Transformations ---");

        // Input: 5
        int input1 = 5;
        // Output: 25
        int result1 = square.apply(input1);
        System.out.println("Input: " + input1 + ", Square: " + result1);

        // Input: 10
        int input2 = 10;
        // Output: 11
        int result2 = increment.apply(input2);
        System.out.println("Input: " + input2 + ", Increment: " + result2);

        // Chaining operators (inherited from Function)
        // Square then increment: (5 * 5) + 1 = 26
        UnaryOperator<Integer> squareThenIncrement = square.andThen(increment);
        int input3 = 5;
        int result3 = squareThenIncrement.apply(input3);
        System.out.println("Input: " + input3 + ", Square then Increment: " + result3);
    }
}
```

**Output:**
```
--- Integer Transformations ---
Input: 5, Square: 25
Input: 10, Increment: 11
Input: 5, Square then Increment: 26
```

### Example 2: String Manipulation

**Goal**: Create operators to convert a string to uppercase and to reverse a string.

```java
import java.util.function.UnaryOperator;

public class StringOperatorExample {

    public static void main(String[] args) {
        // 1. UnaryOperator to convert string to uppercase
        UnaryOperator<String> toUpperCase = String::toUpperCase; // Using method reference

        // 2. UnaryOperator to reverse a string
        UnaryOperator<String> reverseString = s -> new StringBuilder(s).reverse().toString();

        // Test cases
        System.out.println("\n--- String Manipulations ---");

        // Input: "hello world"
        String input1 = "hello world";
        // Output: "HELLO WORLD"
        String result1 = toUpperCase.apply(input1);
        System.out.println("Input: \"" + input1 + "\", To Uppercase: \"" + result1 + "\"");

        // Input: "java"
        String input2 = "java";
        // Output: "avaj"
        String result2 = reverseString.apply(input2);
        System.out.println("Input: \"" + input2 + "\", Reverse: \"" + result2 + "\"");
    }
}
```

**Output:**
```
--- String Manipulations ---
Input: "hello world", To Uppercase: "HELLO WORLD"
Input: "java", Reverse: "avaj"
```

### Example 3: Custom Object Transformation

**Goal**: Create a `UnaryOperator` to apply a discount to a `Product` object.

```java
import java.util.Objects;
import java.util.function.UnaryOperator;

// Define a simple Product class
class Product {
    private String name;
    private double price;

    public Product(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    @Override
    public String toString() {
        return "Product{name='" + name + "', price=" + String.format("%.2f", price) + "}";
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Product product = (Product) o;
        return Double.compare(product.price, price) == 0 && Objects.equals(name, product.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, price);
    }
}

public class ProductOperatorExample {

    public static void main(String[] args) {
        // UnaryOperator to apply a 10% discount
        // Note: For immutability, you might prefer to return a new Product instance.
        // For simplicity here, we're modifying the existing object.
        UnaryOperator<Product> applyDiscount = product -> {
            product.setPrice(product.getPrice() * 0.90); // Apply 10% discount
            return product; // Return the modified product
        };

        // Test cases
        System.out.println("\n--- Product Transformations ---");

        // Input: Product("Laptop", 1000.0)
        Product laptop = new Product("Laptop", 1000.0);
        System.out.println("Original Product: " + laptop);
        // Output: Product{name='Laptop', price=900.00}
        Product discountedLaptop = applyDiscount.apply(laptop);
        System.out.println("Discounted Product: " + discountedLaptop);

        // Input: Product("Mouse", 25.0)
        Product mouse = new Product("Mouse", 25.0);
        System.out.println("Original Product: " + mouse);
        // Output: Product{name='Mouse', price=22.50}
        Product discountedMouse = applyDiscount.apply(mouse);
        System.out.println("Discounted Product: " + discountedMouse);
    }
}
```

**Output:**
```
--- Product Transformations ---
Original Product: Product{name='Laptop', price=1000.00}
Discounted Product: Product{name='Laptop', price=900.00}
Original Product: Product{name='Mouse', price=25.00}
Discounted Product: Product{name='Mouse', price=22.50}
```
*Note*: In a real-world scenario, especially with financial data, you might prefer to create a new `Product` instance with the updated price rather than modifying the existing one, to maintain immutability and avoid side effects.

### Example 4: Using `identity()`

**Goal**: Demonstrate the `identity()` operator, which returns the input unchanged.

```java
import java.util.function.UnaryOperator;

public class IdentityOperatorExample {

    public static void main(String[] args) {
        // Get the identity operator for Strings
        UnaryOperator<String> identityStringOp = UnaryOperator.identity();

        // Get the identity operator for Integers
        UnaryOperator<Integer> identityIntegerOp = UnaryOperator.identity();

        // Test cases
        System.out.println("\n--- Identity Operator ---");

        // Input: "Hello"
        String input1 = "Hello";
        // Output: "Hello"
        String result1 = identityStringOp.apply(input1);
        System.out.println("Input: \"" + input1 + "\", Identity Output: \"" + result1 + "\"");

        // Input: 123
        Integer input2 = 123;
        // Output: 123
        Integer result2 = identityIntegerOp.apply(input2);
        System.out.println("Input: " + input2 + ", Identity Output: " + result2);
    }
}
```

**Output:**
```
--- Identity Operator ---
Input: "Hello", Identity Output: "Hello"
Input: 123, Identity Output: 123
```

## 8. Common Use Cases

`UnaryOperator` is commonly used in scenarios where you need to transform a value *of the same type*.

*   **Stream API**:
    *   While `map` in `Stream` generally takes a `Function<T, R>`, if `T` and `R` are the same, a `UnaryOperator` can be used.
    *   Less direct, but conceptually, it's about transforming elements within the stream into elements of the same type.
*   **Map Operations**: In `java.util.Map`, methods like `compute` or `merge` might implicitly use `UnaryOperator` logic if the key or value is updated to a value of the same type.
*   **Configuration Updates**: Applying a transformation to a configuration value (e.g., trimming whitespace from a string setting).
*   **Mathematical Operations**: Functions like `abs`, `negate`, `square` where input and output are numerical types.
*   **Default Behavior**: Providing a `UnaryOperator.identity()` as a default transformation when no custom transformation is specified.

## 9. Advantages

*   **Readability and Clarity**: By using `UnaryOperator` instead of `Function<T, T>`, the code explicitly communicates the intent that the input and output types are identical.
*   **Type Safety**: The compiler ensures that the lambda or method reference provided is compatible with the `T` type for both input and output.
*   **Conciseness**: Allows for writing expressive and compact code using lambda expressions and method references.
*   **Functional Programming Style**: Promotes writing pure functions (ideally) that transform data without side effects, contributing to more maintainable and testable code.

## 10. Limitations

*   **Type Constraint**: It's limited to scenarios where the input and output types are exactly the same. If they differ, you must use `Function<T, R>`.
*   **Single Argument**: Like all `Function` interfaces in `java.util.function`, it only handles a single input argument. For multiple arguments, you'd need `BiFunction` or custom functional interfaces.

## 11. Conclusion

The `java.util.function.UnaryOperator` is a valuable addition to Java's functional programming toolkit. While it is technically just a specialized `Function<T, T>`, its dedicated name improves code clarity and expressiveness, making it easier to understand operations that transform a value into another value of the exact same type. It's an excellent example of how the `java.util.function` package provides semantic aliases for common functional patterns, aiding in writing more readable and maintainable Java code.