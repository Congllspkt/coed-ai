# Arithmetic Operators in Java

Arithmetic operators are fundamental to performing mathematical calculations in Java. They are used to perform common arithmetic operations like addition, subtraction, multiplication, division, and modulus.

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Binary Arithmetic Operators](#2-binary-arithmetic-operators)
    *   [2.1. Addition (`+`)](#21-addition-)
    *   [2.2. Subtraction (`-`)](#22-subtraction--)
    *   [2.3. Multiplication (`*`)](#23-multiplication--)
    *   [2.4. Division (`/`)](#24-division--)
    *   [2.5. Modulus (`%`)](#25-modulus--)
3.  [Unary Arithmetic Operators](#3-unary-arithmetic-operators)
    *   [3.1. Increment (`++`)](#31-increment--)
    *   [3.2. Decrement (`--`)](#32-decrement--)
4.  [Special Considerations](#4-special-considerations)
    *   [4.1. Integer Division](#41-integer-division)
    *   [4.2. Modulus with Negative Numbers](#42-modulus-with-negative-numbers)
    *   [4.3. Division by Zero](#43-division-by-zero)
    *   [4.4. Operator Precedence](#44-operator-precedence)
    *   [4.5. Type Promotion / Casting](#45-type-promotion--casting)
    *   [4.6. String Concatenation (`+`)](#46-string-concatenation--)
5.  [How to Run Examples](#5-how-to-run-examples)
6.  [Conclusion](#6-conclusion)

---

## 1. Introduction

Arithmetic operators in Java take numerical values (literals or variables) as operands and return a single numerical value. They are primarily used for mathematical computations.

Java's arithmetic operators can be categorized into two main types:

*   **Binary Operators:** Require two operands (e.g., `a + b`).
*   **Unary Operators:** Require a single operand (e.g., `++a`).

---

## 2. Binary Arithmetic Operators

These operators perform operations on two operands.

### 2.1. Addition (`+`)

*   **Description:** Adds two operands.
*   **Syntax:** `operand1 + operand2`
*   **Example:**

    ```java
    public class AdditionExample {
        public static void main(String[] args) {
            int num1 = 25;
            int num2 = 10;
            int sum = num1 + num2;

            double price1 = 15.50;
            double price2 = 7.25;
            double total = price1 + price2;

            System.out.println("Integer Sum: " + sum);
            System.out.println("Double Total: " + total);
        }
    }
    ```

    **Input:**
    `num1 = 25`, `num2 = 10`
    `price1 = 15.50`, `price2 = 7.25`

    **Output:**
    ```text
    Integer Sum: 35
    Double Total: 22.75
    ```

### 2.2. Subtraction (`-`)

*   **Description:** Subtracts the second operand from the first.
*   **Syntax:** `operand1 - operand2`
*   **Example:**

    ```java
    public class SubtractionExample {
        public static void main(String[] args) {
            int val1 = 50;
            int val2 = 15;
            int difference = val1 - val2;

            double temp1 = 98.6;
            double temp2 = 10.5;
            double finalTemp = temp1 - temp2;

            System.out.println("Integer Difference: " + difference);
            System.out.println("Double Final Temp: " + finalTemp);
        }
    }
    ```

    **Input:**
    `val1 = 50`, `val2 = 15`
    `temp1 = 98.6`, `temp2 = 10.5`

    **Output:**
    ```text
    Integer Difference: 35
    Double Final Temp: 88.1
    ```

### 2.3. Multiplication (`*`)

*   **Description:** Multiplies two operands.
*   **Syntax:** `operand1 * operand2`
*   **Example:**

    ```java
    public class MultiplicationExample {
        public static void main(String[] args) {
            int factor1 = 7;
            int factor2 = 8;
            int product = factor1 * factor2;

            double rate = 2.5;
            double hours = 40.0;
            double salary = rate * hours;

            System.out.println("Integer Product: " + product);
            System.out.println("Double Salary: " + salary);
        }
    }
    ```

    **Input:**
    `factor1 = 7`, `factor2 = 8`
    `rate = 2.5`, `hours = 40.0`

    **Output:**
    ```text
    Integer Product: 56
    Double Salary: 100.0
    ```

### 2.4. Division (`/`)

*   **Description:** Divides the first operand by the second.
*   **Syntax:** `operand1 / operand2`
*   **Important Note:** The behavior of division depends on the data types of the operands.
    *   **Integer Division:** If both operands are integers, the result will also be an integer, truncating any fractional part (i.e., it discards the remainder).
    *   **Floating-Point Division:** If at least one operand is a floating-point type (`float` or `double`), the result will be a floating-point type, preserving the decimal part.
*   **Example:**

    ```java
    public class DivisionExample {
        public static void main(String[] args) {
            int intDividend = 10;
            int intDivisor = 3;
            int intResult = intDividend / intDivisor; // Integer division

            double doubleDividend = 10.0;
            double doubleDivisor = 3.0;
            double doubleResult = doubleDividend / doubleDivisor; // Floating-point division

            int mixedInt = 10;
            double mixedDouble = 3.0;
            double mixedResult = mixedInt / mixedDouble; // Type promotion to double

            System.out.println("Integer Division (10 / 3): " + intResult);
            System.out.println("Double Division (10.0 / 3.0): " + doubleResult);
            System.out.println("Mixed Type Division (10 / 3.0): " + mixedResult);
        }
    }
    ```

    **Input:**
    `intDividend = 10`, `intDivisor = 3`
    `doubleDividend = 10.0`, `doubleDivisor = 3.0`
    `mixedInt = 10`, `mixedDouble = 3.0`

    **Output:**
    ```text
    Integer Division (10 / 3): 3
    Double Division (10.0 / 3.0): 3.3333333333333335
    Mixed Type Division (10 / 3.0): 3.3333333333333335
    ```

### 2.5. Modulus (`%`)

*   **Description:** Returns the remainder of the division of the first operand by the second.
*   **Syntax:** `operand1 % operand2`
*   **Important Note:** The sign of the result of the modulus operation is always the same as the sign of the **dividend** (the first operand).
*   **Example:**

    ```java
    public class ModulusExample {
        public static void main(String[] args) {
            int num1 = 10;
            int num2 = 3;
            int remainder1 = num1 % num2; // 10 / 3 = 3 with remainder 1

            int num3 = 15;
            int num4 = 4;
            int remainder2 = num3 % num4; // 15 / 4 = 3 with remainder 3

            // Modulus with negative numbers
            int negNum1 = -10;
            int negNum2 = 3;
            int remainder3 = negNum1 % negNum2; // -10 / 3 = -3 with remainder -1 (sign of dividend)

            int negNum3 = 10;
            int negNum4 = -3;
            int remainder4 = negNum3 % negNum4; // 10 / -3 = -3 with remainder 1 (sign of dividend)

            System.out.println("10 % 3 = " + remainder1);
            System.out.println("15 % 4 = " + remainder2);
            System.out.println("-10 % 3 = " + remainder3);
            System.out.println("10 % -3 = " + remainder4);
        }
    }
    ```

    **Input:**
    `num1 = 10`, `num2 = 3`
    `num3 = 15`, `num4 = 4`
    `negNum1 = -10`, `negNum2 = 3`
    `negNum3 = 10`, `negNum4 = -3`

    **Output:**
    ```text
    10 % 3 = 1
    15 % 4 = 3
    -10 % 3 = -1
    10 % -3 = 1
    ```

---

## 3. Unary Arithmetic Operators

These operators work on a single operand. They are often used as shorthand for adding or subtracting 1.

### 3.1. Increment (`++`)

*   **Description:** Increases the value of the operand by 1.
*   **Syntax:**
    *   **Pre-increment:** `++operand` (increments the value *before* it's used in the expression)
    *   **Post-increment:** `operand++` (uses the original value in the expression, then increments the value)
*   **Example:**

    ```java
    public class IncrementExample {
        public static void main(String[] args) {
            int x = 5;
            System.out.println("Initial x: " + x); // Output: 5

            // Pre-increment
            int y = ++x; // x becomes 6, then y is assigned 6
            System.out.println("After pre-increment (++x):");
            System.out.println("x: " + x); // Output: 6
            System.out.println("y: " + y); // Output: 6

            int a = 10;
            System.out.println("\nInitial a: " + a); // Output: 10

            // Post-increment
            int b = a++; // b is assigned 10, then a becomes 11
            System.out.println("After post-increment (a++):");
            System.out.println("a: " + a); // Output: 11
            System.out.println("b: " + b); // Output: 10
        }
    }
    ```

    **Input:**
    `x = 5`
    `a = 10`

    **Output:**
    ```text
    Initial x: 5
    After pre-increment (++x):
    x: 6
    y: 6

    Initial a: 10
    After post-increment (a++):
    a: 11
    b: 10
    ```

### 3.2. Decrement (`--`)

*   **Description:** Decreases the value of the operand by 1.
*   **Syntax:**
    *   **Pre-decrement:** `--operand` (decrements the value *before* it's used in the expression)
    *   **Post-decrement:** `operand--` (uses the original value in the expression, then decrements the value)
*   **Example:**

    ```java
    public class DecrementExample {
        public static void main(String[] args) {
            int x = 5;
            System.out.println("Initial x: " + x); // Output: 5

            // Pre-decrement
            int y = --x; // x becomes 4, then y is assigned 4
            System.out.println("After pre-decrement (--x):");
            System.out.println("x: " + x); // Output: 4
            System.out.println("y: " + y); // Output: 4

            int a = 10;
            System.out.println("\nInitial a: " + a); // Output: 10

            // Post-decrement
            int b = a--; // b is assigned 10, then a becomes 9
            System.out.println("After post-decrement (a--):");
            System.out.println("a: " + a); // Output: 9
            System.out.println("b: " + b); // Output: 10
        }
    }
    ```

    **Input:**
    `x = 5`
    `a = 10`

    **Output:**
    ```text
    Initial x: 5
    After pre-decrement (--x):
    x: 4
    y: 4

    Initial a: 10
    After post-decrement (a--):
    a: 9
    b: 10
    ```

---

## 4. Special Considerations

### 4.1. Integer Division

As mentioned, integer division truncates the decimal part. If you want a floating-point result from integer operands, you must cast at least one of them to a floating-point type.

**Example:**

```java
public class IntegerDivisionCast {
    public static void main(String[] args) {
        int dividend = 10;
        int divisor = 3;

        // Integer division (truncates)
        int resultInt = dividend / divisor;

        // Floating-point division using casting
        double resultDouble = (double) dividend / divisor; // Cast one operand
        // Or: double resultDouble = dividend / (double) divisor;
        // Or: double resultDouble = (double) dividend / (double) divisor;

        System.out.println("Result of 10 / 3 (integer): " + resultInt);
        System.out.println("Result of 10 / 3 (double after cast): " + resultDouble);
    }
}
```

**Input:**
`dividend = 10`, `divisor = 3`

**Output:**
```text
Result of 10 / 3 (integer): 3
Result of 10 / 3 (double after cast): 3.3333333333333335
```

### 4.2. Modulus with Negative Numbers

The sign of the modulus result always matches the sign of the **dividend** (the first operand).

### 4.3. Division by Zero

*   **Integer division by zero:** Results in an `ArithmeticException` at runtime.
*   **Floating-point division by zero:** Does not throw an exception. Instead, it results in `Infinity`, `-Infinity`, or `NaN` (Not a Number).

**Example:**

```java
public class DivisionByZero {
    public static void main(String[] args) {
        int intNum = 10;
        double doubleNum = 10.0;
        double zeroDouble = 0.0;

        // Integer division by zero (will cause ArithmeticException)
        try {
            int result = intNum / 0;
            System.out.println("This line will not be executed for integer division by zero.");
        } catch (ArithmeticException e) {
            System.out.println("Caught an exception: " + e.getMessage());
        }

        // Floating-point division by zero
        System.out.println("10.0 / 0.0 = " + (doubleNum / zeroDouble)); // Infinity
        System.out.println("-10.0 / 0.0 = " + (-doubleNum / zeroDouble)); // -Infinity
        System.out.println("0.0 / 0.0 = " + (zeroDouble / zeroDouble)); // NaN (Not a Number)
    }
}
```

**Output:**
```text
Caught an exception: / by zero
10.0 / 0.0 = Infinity
-10.0 / 0.0 = -Infinity
0.0 / 0.0 = NaN
```

### 4.4. Operator Precedence

Arithmetic operators follow standard mathematical precedence rules (similar to PEMDAS/BODMAS):

1.  **Parentheses `()`:** Expressions inside parentheses are evaluated first.
2.  **Multiplication `*`, Division `/`, Modulus `%`:** Evaluated next, from left to right.
3.  **Addition `+`, Subtraction `-`:** Evaluated last, from left to right.

**Example:**

```java
public class OperatorPrecedence {
    public static void main(String[] args) {
        int result1 = 5 + 2 * 3; // Multiplication before addition
        int result2 = (5 + 2) * 3; // Parentheses first

        System.out.println("5 + 2 * 3 = " + result1); // Output: 5 + 6 = 11
        System.out.println("(5 + 2) * 3 = " + result2); // Output: 7 * 3 = 21
    }
}
```

**Input:** (Implicit in the expression)

**Output:**
```text
5 + 2 * 3 = 11
(5 + 2) * 3 = 21
```

### 4.5. Type Promotion / Casting

When different numeric data types are involved in an arithmetic operation, Java performs automatic type promotion (widening conversion) to ensure the operation is performed on compatible types. The result will be of the larger type. If you need a specific type, you might need explicit casting (narrowing conversion).

**Rules (simplified):**
*   `byte`, `short`, `char` are promoted to `int` before most operations.
*   If one operand is `long`, the other is promoted to `long`.
*   If one operand is `float`, the other is promoted to `float`.
*   If one operand is `double`, the other is promoted to `double`.

### 4.6. String Concatenation (`+`)

It's important to note that the `+` operator has a dual purpose. Besides arithmetic addition, it is also used for string concatenation. When one of the operands is a `String`, the `+` operator will perform string concatenation.

**Example:**

```java
public class StringConcatenation {
    public static void main(String[] args) {
        int num = 10;
        String text = "The number is: ";
        String combined = text + num; // Concatenation

        System.out.println(combined);
        System.out.println("Result: " + (5 + 3)); // Addition inside parentheses, then concatenation
        System.out.println(5 + 3 + " is the result."); // Addition first (left to right), then concatenation
        System.out.println("The result is: " + 5 + 3); // Concatenation first (left to right)
    }
}
```

**Input:** (Implicit)

**Output:**
```text
The number is: 10
Result: 8
8 is the result.
The result is: 53
```

---

## 5. How to Run Examples

To run these Java examples:

1.  **Save:** Save each code block as a `.java` file (e.g., `AdditionExample.java`). Ensure the class name matches the file name.
2.  **Compile:** Open a terminal or command prompt, navigate to the directory where you saved the file, and compile it using the Java compiler:
    ```bash
    javac AdditionExample.java
    ```
3.  **Run:** After successful compilation, run the compiled class file:
    ```bash
    java AdditionExample
    ```
    The output will be displayed in your terminal.

---

## 6. Conclusion

Arithmetic operators are foundational to any programming language, and Java provides a comprehensive set for various mathematical computations. Understanding their behavior, especially concerning integer division, modulus with negative numbers, type promotion, and operator precedence, is crucial for writing correct and efficient Java code.