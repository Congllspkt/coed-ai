# Java 8: `BigDecimal` Arithmetic Methods

In Java, when dealing with precise decimal arithmetic, especially in financial applications, the `double` and `float` primitive types are unsuitable due to their inherent floating-point inaccuracies. The `java.math.BigDecimal` class provides arbitrary-precision signed decimal numbers, making it the go-to choice for such scenarios.

You've asked about `multipliedBy()`, `dividedBy()`, and `negated()`. While these names are semantically equivalent to the operations you're looking for, the actual method names in the `BigDecimal` class are `multiply()`, `divide()`, and `negate()`. We will detail these actual methods below.

All `BigDecimal` operations return a new `BigDecimal` object, as `BigDecimal` objects are **immutable**. This means methods like `multiply()`, `divide()`, and `negate()` do not modify the original object but instead return a new `BigDecimal` instance with the result.

---

## 1. `multiply()` (Equivalent to `multipliedBy()`)

The `multiply()` method returns a `BigDecimal` whose value is `(this × multiplicand)`. Its scale is `(this.scale() + multiplicand.scale())`.

### Method Signature

```java
public BigDecimal multiply(BigDecimal multiplicand)
```

### Description

*   Takes another `BigDecimal` object as an argument.
*   Calculates the product of the current `BigDecimal` instance and the argument.
*   The result's scale is the sum of the scales of the two operands. This ensures no precision is lost during multiplication.
*   Returns a new `BigDecimal` instance representing the product.

### Example

```java
import java.math.BigDecimal;

public class BigDecimalMultiplyExample {
    public static void main(String[] args) {
        // Input values using String constructor for precision
        BigDecimal value1 = new BigDecimal("10.5");
        BigDecimal value2 = new BigDecimal("2.0");
        BigDecimal value3 = new BigDecimal("0.123");
        BigDecimal value4 = new BigDecimal("100");

        System.out.println("--- multiply() Example ---");

        // Example 1: Basic multiplication
        // Input: value1 = 10.5, value2 = 2.0
        BigDecimal result1 = value1.multiply(value2);
        System.out.println("Input: " + value1 + " * " + value2);
        System.out.println("Output: " + result1); // Expected: 21.00 (scale = 1+1 = 2)

        // Example 2: Multiplication with smaller decimal
        // Input: value3 = 0.123, value4 = 100
        BigDecimal result2 = value3.multiply(value4);
        System.out.println("\nInput: " + value3 + " * " + value4);
        System.out.println("Output: " + result2); // Expected: 12.300 (scale = 3+0 = 3)

        // Example 3: Chaining operations (optional, demonstrates immutability)
        // (10.5 * 2.0) * 0.123
        BigDecimal chainedResult = value1.multiply(value2).multiply(value3);
        System.out.println("\nInput: (" + value1 + " * " + value2 + ") * " + value3);
        System.out.println("Output: " + chainedResult); // Expected: 2.583000 (scale = 2+3 = 5)
    }
}
```

### Output

```
--- multiply() Example ---
Input: 10.5 * 2.0
Output: 21.00

Input: 0.123 * 100
Output: 12.300

Input: (10.5 * 2.0) * 0.123
Output: 2.583000
```

---

## 2. `divide()` (Equivalent to `dividedBy()`)

The `divide()` method returns a `BigDecimal` whose value is `(this / divisor)`.

**Crucially, division with `BigDecimal` can be tricky because not all divisions result in a terminating decimal expansion (e.g., 10 / 3 = 3.333...).** If you perform a division that results in a non-terminating decimal and you don't specify a scale and rounding mode, an `ArithmeticException` will be thrown. Therefore, it's highly recommended to use the overloads that allow you to specify the desired scale and rounding behavior.

### Method Signatures (Commonly Used)

```java
// Throws ArithmeticException if exact division is not possible
public BigDecimal divide(BigDecimal divisor)

// Recommended: Specifies desired scale and rounding mode
public BigDecimal divide(BigDecimal divisor, int scale, RoundingMode roundingMode)

// Alternative: Uses MathContext for precision and rounding mode
public BigDecimal divide(BigDecimal divisor, MathContext mc)
```

### Description

*   Takes another `BigDecimal` object (the `divisor`) as an argument.
*   Calculates the quotient of the current `BigDecimal` instance and the `divisor`.
*   `scale`: The number of digits to the right of the decimal point in the result.
*   `roundingMode`: Specifies how the result should be rounded if it needs to be truncated to fit the specified scale. Common modes include `RoundingMode.HALF_UP` (round up if the discarded fraction is >= 0.5) and `RoundingMode.DOWN` (truncate).
*   `MathContext`: An object that encapsulates a `precision` (total number of significant digits) and a `RoundingMode`.
*   Returns a new `BigDecimal` instance representing the quotient.
*   **Important:** Avoid the `divide(BigDecimal divisor)` overload for general use unless you are absolutely sure the division will result in a terminating decimal, as it will throw `ArithmeticException` otherwise.

### Example

```java
import java.math.BigDecimal;
import java.math.RoundingMode; // Required for RoundingMode
import java.math.MathContext; // Required for MathContext

public class BigDecimalDivideExample {
    public static void main(String[] args) {
        // Input values
        BigDecimal value1 = new BigDecimal("10");
        BigDecimal value2 = new BigDecimal("3");
        BigDecimal value3 = new BigDecimal("2.5");
        BigDecimal value4 = new BigDecimal("0.5");

        System.out.println("--- divide() Example ---");

        // Example 1: Division that results in an exact value (no rounding needed)
        // Input: 10 / 2.5
        BigDecimal result1 = value1.divide(value3); // No ArithmeticException here
        System.out.println("Input: " + value1 + " / " + value3);
        System.out.println("Output: " + result1); // Expected: 4

        // Example 2: Division with non-terminating decimal (requires scale and rounding)
        // Input: 10 / 3, round to 4 decimal places using HALF_UP
        BigDecimal result2 = value1.divide(value2, 4, RoundingMode.HALF_UP);
        System.out.println("\nInput: " + value1 + " / " + value2 + " (scale 4, HALF_UP)");
        System.out.println("Output: " + result2); // Expected: 3.3333

        // Example 3: Division using MathContext (precision is total digits)
        // Input: 10 / 3, precision 5, HALF_UP
        MathContext mc = new MathContext(5, RoundingMode.HALF_UP);
        BigDecimal result3 = value1.divide(value2, mc);
        System.out.println("\nInput: " + value1 + " / " + value2 + " (MathContext: precision 5, HALF_UP)");
        System.out.println("Output: " + result3); // Expected: 3.3333

        // Example 4: Demonstrating ArithmeticException if no scale/rounding for non-terminating
        // Input: 10 / 3
        try {
            BigDecimal errorResult = value1.divide(value2);
            System.out.println("\nShould not reach here: " + errorResult);
        } catch (ArithmeticException e) {
            System.out.println("\nInput: " + value1 + " / " + value2 + " (no scale/rounding)");
            System.out.println("Output: Caught ArithmeticException as expected: " + e.getMessage());
        }

        // Example 5: Divide by a smaller decimal
        // Input: 2.5 / 0.5
        BigDecimal result5 = value3.divide(value4);
        System.out.println("\nInput: " + value3 + " / " + value4);
        System.out.println("Output: " + result5); // Expected: 5
    }
}
```

### Output

```
--- divide() Example ---
Input: 10 / 2.5
Output: 4

Input: 10 / 3 (scale 4, HALF_UP)
Output: 3.3333

Input: 10 / 3 (MathContext: precision 5, HALF_UP)
Output: 3.3333

Input: 10 / 3 (no scale/rounding)
Output: Caught ArithmeticException as expected: Non-terminating decimal expansion; no exact representable decimal result.

Input: 2.5 / 0.5
Output: 5
```

---

## 3. `negate()` (Equivalent to `negated()`)

The `negate()` method returns a `BigDecimal` whose value is `(-this)`.

### Method Signature

```java
public BigDecimal negate()
```

### Description

*   Changes the sign of the `BigDecimal` instance.
*   If the original value is positive, the result will be negative.
*   If the original value is negative, the result will be positive.
*   If the original value is zero, the result is zero.
*   Returns a new `BigDecimal` instance with the negated value. The scale remains the same.

### Example

```java
import java.math.BigDecimal;

public class BigDecimalNegateExample {
    public static void main(String[] args) {
        // Input values
        BigDecimal value1 = new BigDecimal("10.50");
        BigDecimal value2 = new BigDecimal("-5.25");
        BigDecimal value3 = new BigDecimal("0.00");

        System.out.println("--- negate() Example ---");

        // Example 1: Negating a positive value
        // Input: 10.50
        BigDecimal result1 = value1.negate();
        System.out.println("Input: " + value1);
        System.out.println("Output (negated): " + result1); // Expected: -10.50

        // Example 2: Negating a negative value
        // Input: -5.25
        BigDecimal result2 = value2.negate();
        System.out.println("\nInput: " + value2);
        System.out.println("Output (negated): " + result2); // Expected: 5.25

        // Example 3: Negating zero
        // Input: 0.00
        BigDecimal result3 = value3.negate();
        System.out.println("\nInput: " + value3);
        System.out.println("Output (negated): " + result3); // Expected: 0.00

        // Example 4: Chaining (e.g., - (10.5 * 2.0))
        BigDecimal chainedResult = new BigDecimal("10.5").multiply(new BigDecimal("2.0")).negate();
        System.out.println("\nInput: -(10.5 * 2.0)");
        System.out.println("Output: " + chainedResult); // Expected: -21.00
    }
}
```

### Output

```
--- negate() Example ---
Input: 10.50
Output (negated): -10.50

Input: -5.25
Output (negated): 5.25

Input: 0.00
Output (negated): 0.00

Input: -(10.5 * 2.0)
Output: -21.00
```

---

## Important Considerations for `BigDecimal`

1.  **Immutability:** As mentioned, `BigDecimal` objects are immutable. Every arithmetic operation returns a *new* `BigDecimal` object. This allows for safe sharing of `BigDecimal` instances and simplifies concurrent programming.
    ```java
    BigDecimal original = new BigDecimal("10");
    BigDecimal tenTimes = original.multiply(new BigDecimal("10")); // original is still "10"
    System.out.println(original); // Output: 10
    System.out.println(tenTimes); // Output: 100
    ```

2.  **Constructor Usage:** Always use the `String` constructor `new BigDecimal("...")` when creating `BigDecimal` instances from decimal literals to avoid floating-point inaccuracies that can arise from the `double` constructor.
    ```java
    // BAD: Can introduce subtle errors
    BigDecimal bdBad = new BigDecimal(0.1); // bdBad might be 0.1000000000000000055511151231257827021181583404541015625

    // GOOD: Ensures exact representation
    BigDecimal bdGood = new BigDecimal("0.1"); // bdGood is exactly 0.1
    ```

3.  **Scale and Precision:** Be mindful of `BigDecimal`'s scale (number of digits to the right of the decimal point) and precision (total number of significant digits). Operations can affect these, especially division.

4.  **`RoundingMode`:** When using `divide()`, always specify a `RoundingMode` unless you are absolutely certain the division will terminate exactly. `RoundingMode.HALF_UP` is a common choice for financial calculations.

5.  **Chaining Operations:** Due to immutability, `BigDecimal` operations can be chained for more concise code:
    ```java
    BigDecimal a = new BigDecimal("10");
    BigDecimal b = new BigDecimal("3");
    BigDecimal c = new BigDecimal("2");

    BigDecimal result = a.divide(b, 2, RoundingMode.HALF_UP).multiply(c);
    // (10 / 3, rounded to 2 decimals) * 2
    // (3.33) * 2 = 6.66
    System.out.println(result); // Output: 6.66
    ```

By understanding and correctly applying these `BigDecimal` methods and best practices, you can ensure accurate and reliable decimal arithmetic in your Java applications.