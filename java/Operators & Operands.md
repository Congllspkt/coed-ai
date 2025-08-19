This document provides a detailed explanation of operators and operands in Java, complete with examples demonstrating their usage, input, and output.

---

# Operators & Operands in Java

In Java, as in most programming languages, **operators** and **operands** are fundamental components used to construct expressions and perform computations.

## I. Operands

An **operand** is a piece of data on which an operator performs its action. Operands can be:

1.  **Literals:** Fixed values (e.g., `10`, `3.14`, `"Hello"`, `true`).
2.  **Variables:** Names that refer to memory locations storing data (e.g., `x`, `name`, `isLoggedIn`).
3.  **Method Return Values:** The result of a method call (e.g., `Math.sqrt(25)`).
4.  **Expressions:** The result of another expression can serve as an operand for a subsequent operation (e.g., `(a + b)` is an expression whose result can be an operand for `*`).

**Example:**

```java
public class OperandExample {
    public static void main(String[] args) {
        int a = 10;             // 10 is a literal operand
        int b = 5;              // 5 is a literal operand

        int sum = a + b;        // 'a' and 'b' are variable operands
                                // The result of (a + b) is an operand for the assignment operator '='

        double result = Math.sqrt(sum); // 'sum' is a variable operand.
                                      // Math.sqrt(sum) is an expression whose return value is an operand.

        System.out.println("Sum: " + sum);
        System.out.println("Square root of sum: " + result);
    }
}
```

**Input:** (Implicit values assigned in code)
`a = 10`
`b = 5`

**Output:**
```
Sum: 15
Square root of sum: 3.872983346207417
```

---

## II. Operators

An **operator** is a special symbol that performs a specific operation on one or more operands, producing a result. Java provides a rich set of operators categorized by the type of operation they perform.

Let's explore the different types of operators in Java with examples:

### 1. Arithmetic Operators

These operators are used to perform basic mathematical calculations.

| Operator | Name         | Description                                     |
| :------- | :----------- | :---------------------------------------------- |
| `+`      | Addition     | Adds two operands.                              |
| `-`      | Subtraction  | Subtracts the second operand from the first.    |
| `*`      | Multiplication | Multiplies two operands.                        |
| `/`      | Division     | Divides the first operand by the second. For integers, it performs integer division (truncates decimals). |
| `%`      | Modulus      | Returns the remainder of the division.          |

**Example:**

```java
public class ArithmeticOperators {
    public static void main(String[] args) {
        int num1 = 20;
        int num2 = 6;

        System.out.println("Arithmetic Operations:");
        System.out.println("num1 + num2 = " + (num1 + num2));   // Addition
        System.out.println("num1 - num2 = " + (num1 - num2));   // Subtraction
        System.out.println("num1 * num2 = " + (num1 * num2));   // Multiplication
        System.out.println("num1 / num2 = " + (num1 / num2));   // Division (integer division)
        System.out.println("num1 % num2 = " + (num1 % num2));   // Modulus
        
        double d1 = 20.0;
        double d2 = 6.0;
        System.out.println("d1 / d2 = " + (d1 / d2)); // Division (floating point)
    }
}
```

**Input:** (Implicit values)
`num1 = 20`
`num2 = 6`

**Output:**
```
Arithmetic Operations:
num1 + num2 = 26
num1 - num2 = 14
num1 * num2 = 120
num1 / num2 = 3
num1 % num2 = 2
d1 / d2 = 3.3333333333333335
```

### 2. Relational (Comparison) Operators

These operators compare two operands and return a boolean result (`true` or `false`).

| Operator | Name                | Description                                     |
| :------- | :------------------ | :---------------------------------------------- |
| `==`     | Equal to            | Returns `true` if operands are equal.           |
| `!=`     | Not equal to        | Returns `true` if operands are not equal.       |
| `>`      | Greater than        | Returns `true` if the first operand is greater. |
| `<`      | Less than           | Returns `true` if the first operand is less.    |
| `>=`     | Greater than or equal to | Returns `true` if the first operand is greater than or equal to. |
| `<=`     | Less than or equal to    | Returns `true` if the first operand is less than or equal to.    |

**Example:**

```java
public class RelationalOperators {
    public static void main(String[] args) {
        int a = 15;
        int b = 10;

        System.out.println("Relational Operations:");
        System.out.println("a == b: " + (a == b)); // Is a equal to b?
        System.out.println("a != b: " + (a != b)); // Is a not equal to b?
        System.out.println("a > b: " + (a > b));   // Is a greater than b?
        System.out.println("a < b: " + (a < b));   // Is a less than b?
        System.out.println("a >= b: " + (a >= b)); // Is a greater than or equal to b?
        System.out.println("a <= b: " + (a <= b)); // Is a less than or equal to b?
    }
}
```

**Input:** (Implicit values)
`a = 15`
`b = 10`

**Output:**
```
Relational Operations:
a == b: false
a != b: true
a > b: true
a < b: false
a >= b: true
a <= b: false
```

### 3. Logical Operators

These operators combine multiple boolean expressions and return a single boolean result.

| Operator | Name         | Description                                     |
| :------- | :----------- | :---------------------------------------------- |
| `&&`     | Logical AND  | Returns `true` if **both** operands are `true`. (Short-circuits: if the first is `false`, the second isn't evaluated). |
| `||`     | Logical OR   | Returns `true` if **at least one** operand is `true`. (Short-circuits: if the first is `true`, the second isn't evaluated). |
| `!`      | Logical NOT  | Inverts the boolean value of its operand (`true` becomes `false`, `false` becomes `true`). (Unary operator). |

**Example:**

```java
public class LogicalOperators {
    public static void main(String[] args) {
        boolean isSunny = true;
        boolean isWarm = false;
        int temperature = 25;

        System.out.println("Logical Operations:");
        // Logical AND
        System.out.println("isSunny && isWarm: " + (isSunny && isWarm)); // true && false -> false
        System.out.println("(temperature > 20) && isSunny: " + ((temperature > 20) && isSunny)); // true && true -> true

        // Logical OR
        System.out.println("isSunny || isWarm: " + (isSunny || isWarm)); // true || false -> true
        System.out.println("(temperature < 10) || isWarm: " + ((temperature < 10) || isWarm)); // false || false -> false

        // Logical NOT
        System.out.println("!isSunny: " + (!isSunny));     // !true -> false
        System.out.println("!(temperature == 25): " + !(temperature == 25)); // !(true) -> false
    }
}
```

**Input:** (Implicit values)
`isSunny = true`
`isWarm = false`
`temperature = 25`

**Output:**
```
Logical Operations:
isSunny && isWarm: false
(temperature > 20) && isSunny: true
isSunny || isWarm: true
(temperature < 10) || isWarm: false
!isSunny: false
!(temperature == 25): false
```

### 4. Assignment Operators

These operators are used to assign a value to a variable. The simple assignment operator is `=`. Compound assignment operators combine an arithmetic or bitwise operation with assignment.

| Operator | Example      | Equivalent To       | Description                                     |
| :------- | :----------- | :------------------ | :---------------------------------------------- |
| `=`      | `x = 5`      |                     | Assigns the value on the right to the variable on the left. |
| `+=`     | `x += 5`     | `x = x + 5`         | Adds the right operand to the left operand and assigns the result to the left operand. |
| `-=`     | `x -= 5`     | `x = x - 5`         | Subtracts the right operand from the left operand and assigns the result. |
| `*=`     | `x *= 5`     | `x = x * 5`         | Multiplies the left operand by the right operand and assigns the result. |
| `/=`     | `x /= 5`     | `x = x / 5`         | Divides the left operand by the right operand and assigns the result. |
| `%=`     | `x %= 5`     | `x = x % 5`         | Takes modulus using two operands and assigns the result to the left operand. |
| `&=`     | `x &= 5`     | `x = x & 5`         | Bitwise AND and assignment.                     |
| `|=`     | `x |= 5`     | `x = x | 5`         | Bitwise OR and assignment.                      |
| `^=`     | `x ^= 5`     | `x = x ^ 5`         | Bitwise XOR and assignment.                     |
| `<<=`    | `x <<= 5`    | `x = x << 5`        | Left shift and assignment.                      |
| `>>=`    | `x >>= 5`    | `x = x >> 5`        | Right shift and assignment.                     |
| `>>>=`   | `x >>>= 5`   | `x = x >>> 5`       | Unsigned right shift and assignment.            |

**Example:**

```java
public class AssignmentOperators {
    public static void main(String[] args) {
        int value = 10;
        System.out.println("Initial value: " + value); // 10

        value += 5; // value = value + 5;
        System.out.println("After value += 5: " + value); // 15

        value -= 3; // value = value - 3;
        System.out.println("After value -= 3: " + value); // 12

        value *= 2; // value = value * 2;
        System.out.println("After value *= 2: " + value); // 24

        value /= 4; // value = value / 4;
        System.out.println("After value /= 4: " + value); // 6

        value %= 5; // value = value % 5;
        System.out.println("After value %= 5: " + value); // 1
    }
}
```

**Input:** (Implicit initial value)
`value = 10`

**Output:**
```
Initial value: 10
After value += 5: 15
After value -= 3: 12
After value *= 2: 24
After value /= 4: 6
After value %= 5: 1
```

### 5. Unary Operators

These operators require only one operand.

| Operator | Name                 | Description                                     |
| :------- | :------------------- | :---------------------------------------------- |
| `+`      | Unary Plus           | Indicates a positive value (rarely used, numbers are positive by default). |
| `-`      | Unary Minus          | Negates the value of an expression.             |
| `++`     | Increment            | Increases the operand's value by 1. (`++x` pre-increment, `x++` post-increment). |
| `--`     | Decrement            | Decreases the operand's value by 1. (`--x` pre-decrement, `x--` post-decrement). |
| `!`      | Logical NOT          | Inverts the boolean value of its operand.       |

**Example (Increment/Decrement):**

```java
public class UnaryOperators {
    public static void main(String[] args) {
        int i = 5;
        int j = 5;

        System.out.println("Unary Operations:");

        // Unary Plus/Minus
        int positiveNum = +10; // Redundant but valid
        int negativeNum = -20;
        System.out.println("Positive: " + positiveNum + ", Negative: " + negativeNum); // Positive: 10, Negative: -20

        // Pre-increment (changes value, then uses it)
        System.out.println("Value of i before pre-increment: " + i);   // 5
        System.out.println("Value of ++i: " + (++i));                  // 6 (i becomes 6, then 6 is printed)
        System.out.println("Value of i after pre-increment: " + i);    // 6

        // Post-increment (uses value, then changes it)
        System.out.println("\nValue of j before post-increment: " + j); // 5
        System.out.println("Value of j++: " + (j++));                   // 5 (j is printed as 5, then j becomes 6)
        System.out.println("Value of j after post-increment: " + j);   // 6

        // Pre-decrement and Post-decrement work similarly
        int k = 8;
        System.out.println("\nValue of --k: " + (--k)); // 7
        System.out.println("Value of k after pre-decrement: " + k); // 7

        int l = 8;
        System.out.println("Value of l--: " + (l--)); // 8
        System.out.println("Value of l after post-decrement: " + l); // 7
    }
}
```

**Input:** (Implicit initial values)
`i = 5`
`j = 5`
`k = 8`
`l = 8`

**Output:**
```
Unary Operations:
Positive: 10, Negative: -20
Value of i before pre-increment: 5
Value of ++i: 6
Value of i after pre-increment: 6

Value of j before post-increment: 5
Value of j++: 5
Value of j after post-increment: 6

Value of --k: 7
Value of k after pre-decrement: 7
Value of l--: 8
Value of l after post-decrement: 7
```

### 6. Bitwise Operators

These operators perform operations on individual bits of integer types (`byte`, `short`, `int`, `long`).

| Operator | Name                | Description                                     |
| :------- | :------------------ | :---------------------------------------------- |
| `&`      | Bitwise AND         | Performs a bitwise AND operation.               |
| `\|`     | Bitwise OR          | Performs a bitwise OR operation.                |
| `^`      | Bitwise XOR         | Performs a bitwise XOR (exclusive OR) operation. |
| `~`      | Bitwise Complement (NOT) | Inverts all bits of an operand.             |
| `<<`     | Left Shift          | Shifts bits to the left, filling with zeros on the right. Equivalent to multiplying by powers of 2. |
| `>>`     | Signed Right Shift  | Shifts bits to the right, preserving the sign bit (fills with sign bit on the left). Equivalent to dividing by powers of 2. |
| `>>>`    | Unsigned Right Shift | Shifts bits to the right, filling with zeros on the left (ignores sign bit). |

**Example:**

```java
public class BitwiseOperators {
    public static void main(String[] args) {
        int a = 5;  // Binary: 0101
        int b = 3;  // Binary: 0011

        System.out.println("Bitwise Operations (a=5, b=3):");
        System.out.println("a & b (AND): " + (a & b));     // 0001 = 1
        System.out.println("a | b (OR): " + (a | b));      // 0111 = 7
        System.out.println("a ^ b (XOR): " + (a ^ b));     // 0110 = 6
        System.out.println("~a (NOT): " + (~a));           // Inverts bits. For 5 (0...0101), results in -6 (1...1010) due to 2's complement.

        int num = 16; // Binary: 00010000
        System.out.println("\nShift Operations (num=16):");
        System.out.println("num << 2 (Left Shift by 2): " + (num << 2)); // 01000000 = 64 (16 * 2^2)
        System.out.println("num >> 2 (Right Shift by 2): " + (num >> 2)); // 00000100 = 4 (16 / 2^2)

        int negativeNum = -16; // Binary (in 2's complement for 32-bit): 11111111 11111111 11111111 11110000
        System.out.println("\nShift Operations (negativeNum=-16):");
        System.out.println("negativeNum >> 2 (Signed Right Shift by 2): " + (negativeNum >> 2)); // Result is -4 (1111...1111100)
        System.out.println("negativeNum >>> 2 (Unsigned Right Shift by 2): " + (negativeNum >>> 2)); // Result is large positive (0011...1111100)
    }
}
```

**Input:** (Implicit initial values)
`a = 5`
`b = 3`
`num = 16`
`negativeNum = -16`

**Output:**
```
Bitwise Operations (a=5, b=3):
a & b (AND): 1
a | b (OR): 7
a ^ b (XOR): 6
~a (NOT): -6

Shift Operations (num=16):
num << 2 (Left Shift by 2): 64
num >> 2 (Right Shift by 2): 4

Shift Operations (negativeNum=-16):
negativeNum >> 2 (Signed Right Shift by 2): -4
negativeNum >>> 2 (Unsigned Right Shift by 2): 1073741820
```

### 7. Ternary (Conditional) Operator

This is the only operator in Java that takes three operands. It's a shorthand for an `if-else` statement.

| Operator | Syntax                               | Description                                     |
| :------- | :----------------------------------- | :---------------------------------------------- |
| `? :`    | `condition ? expression1 : expression2;` | If `condition` is `true`, `expression1` is evaluated and its result is returned. Otherwise, `expression2` is evaluated and its result is returned. |

**Example:**

```java
public class TernaryOperator {
    public static void main(String[] args) {
        int score = 75;
        String result;

        // Using ternary operator
        result = (score >= 60) ? "Pass" : "Fail";
        System.out.println("Score: " + score + ", Result: " + result);

        score = 50;
        result = (score >= 60) ? "Pass" : "Fail";
        System.out.println("Score: " + score + ", Result: " + result);

        // Example with different data types
        int age = 19;
        String eligibility = (age >= 18) ? "Eligible for voting" : "Not eligible for voting";
        System.out.println("Age: " + age + ", Eligibility: " + eligibility);
    }
}
```

**Input:** (Implicit initial values)
`score = 75` (then `50`)
`age = 19`

**Output:**
```
Score: 75, Result: Pass
Score: 50, Result: Fail
Age: 19, Eligibility: Eligible for voting
```

### 8. `instanceof` Operator

The `instanceof` operator is used to check if an object is an instance of a particular class or an interface. It returns a boolean value.

| Operator    | Syntax                          | Description                                     |
| :---------- | :------------------------------ | :---------------------------------------------- |
| `instanceof` | `object_name instanceof ClassName` | Returns `true` if `object_name` is an instance of `ClassName` (or a subclass), otherwise `false`. |

**Example:**

```java
class Animal {
    // base class
}

class Dog extends Animal {
    // subclass
}

public class InstanceofOperator {
    public static void main(String[] args) {
        Animal myAnimal = new Animal();
        Animal myDog = new Dog(); // A Dog IS-A Animal

        System.out.println("instanceof Operator:");
        System.out.println("myAnimal instanceof Animal: " + (myAnimal instanceof Animal)); // true
        System.out.println("myAnimal instanceof Dog: " + (myAnimal instanceof Dog));     // false

        System.out.println("myDog instanceof Animal: " + (myDog instanceof Animal));     // true
        System.out.println("myDog instanceof Dog: " + (myDog instanceof Dog));         // true

        String str = "Hello";
        System.out.println("str instanceof String: " + (str instanceof String));       // true
        System.out.println("str instanceof Object: " + (str instanceof Object));       // true (String is a subclass of Object)

        // Using with null: If the object is null, instanceof always returns false
        String nullStr = null;
        System.out.println("nullStr instanceof String: " + (nullStr instanceof String)); // false
    }
}
```

**Input:** (Implicit object creation and assignments)

**Output:**
```
instanceof Operator:
myAnimal instanceof Animal: true
myAnimal instanceof Dog: false
myDog instanceof Animal: true
myDog instanceof Dog: true
str instanceof String: true
str instanceof Object: true
nullStr instanceof String: false
```

---

## III. Operator Precedence and Associativity

When multiple operators are used in a single expression, their order of evaluation is determined by **precedence** and **associativity**.

*   **Precedence:** Determines which operator is evaluated first. Operators with higher precedence are evaluated before operators with lower precedence. For example, `*` and `/` have higher precedence than `+` and `-`. So, `2 + 3 * 4` evaluates to `2 + (3 * 4) = 14`, not `(2 + 3) * 4 = 20`.

*   **Associativity:** When operators have the *same* precedence, associativity determines the order of evaluation (left-to-right or right-to-left). Most operators in Java are left-to-right associative, meaning they are evaluated from left to right. Assignment operators (`=`, `+=`, etc.) are right-to-left associative.

**General Precedence (Highest to Lowest, simplified):**

1.  Parentheses `()` (highest)
2.  Unary operators (`++`, `--`, `+`, `-`, `!`, `~`)
3.  Multiplicative (`*`, `/`, `%`)
4.  Additive (`+`, `-`)
5.  Shift (`<<`, `>>`, `>>>`)
6.  Relational (`<`, `>`, `<=`, `>=`, `instanceof`)
7.  Equality (`==`, `!=`)
8.  Bitwise AND (`&`)
9.  Bitwise XOR (`^`)
10. Bitwise OR (`|`)
11. Logical AND (`&&`)
12. Logical OR (`||`)
13. Ternary (`? :`)
14. Assignment (`=`, `+=`, `-=`, etc.) (lowest)

**Example demonstrating Precedence:**

```java
public class PrecedenceExample {
    public static void main(String[] args) {
        int a = 10;
        int b = 5;
        int c = 2;

        // Example 1: Multiplication before Addition
        // 10 + 5 * 2
        // 10 + 10
        // 20
        int result1 = a + b * c;
        System.out.println("a + b * c = " + result1);

        // Example 2: Using parentheses to override precedence
        // (10 + 5) * 2
        // 15 * 2
        // 30
        int result2 = (a + b) * c;
        System.out.println("(a + b) * c = " + result2);

        // Example 3: Mixed logical and relational
        boolean condition1 = (a > b && b < c); // (10 > 5 && 5 < 2) -> (true && false) -> false
        System.out.println("(a > b && b < c) = " + condition1);

        boolean condition2 = (a > b || b < c); // (10 > 5 || 5 < 2) -> (true || false) -> true
        System.out.println("(a > b || b < c) = " + condition2);
    }
}
```

**Input:** (Implicit values)
`a = 10`
`b = 5`
`c = 2`

**Output:**
```
a + b * c = 20
(a + b) * c = 30
(a > b && b < c) = false
(a > b || b < c) = true
```

---

## Conclusion

Operators and operands are the building blocks of expressions in Java. Understanding their types, behavior, and the rules of precedence and associativity is crucial for writing correct, efficient, and readable Java code. By combining various operators with appropriate operands, programmers can perform complex computations, control program flow, and manipulate data effectively.