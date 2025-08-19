
The `switch` statement in Java is a control flow statement that allows a programmer to execute different blocks of code based on the value of a single expression. It provides an alternative to a long `if-else if` chain when you have multiple execution paths based on a single variable.

---

# Java `switch` Statement

## 1. Introduction

The `switch` statement evaluates an expression and then attempts to match the result against various `case` labels. If a match is found, the code block associated with that `case` is executed. It's often used for scenarios like:

*   Menu selections
*   Mapping numerical or string codes to actions
*   Handling different states in a finite state machine

## 2. Basic Syntax (Traditional `switch` Statement - Java 1.0 to Java 13)

```java
switch (expression) {
    case value1:
        // Code block to be executed if expression == value1
        break; // Optional: exits the switch statement
    case value2:
        // Code block to be executed if expression == value2
        break; // Optional: exits the switch statement
    // ... more cases
    default:
        // Code block to be executed if no match is found
        // Optional: Can be placed anywhere, but usually at the end
}
```

**Explanation of Components:**

*   **`expression`**: An expression that evaluates to a value. This value is then compared against the `case` values.
*   **`case valueN`**: A label that specifies a possible value for the `expression`. `valueN` must be a **constant** (literal, enum constant, or final variable initialized at declaration). Duplicate `case` values are not allowed.
*   **`break`**: The `break` keyword is crucial in traditional `switch` statements. When encountered, it terminates the `switch` statement immediately, preventing "fall-through" to subsequent `case` blocks.
*   **`default`**: The `default` block is optional. If no `case` value matches the `expression`, the code inside the `default` block is executed. It can be placed anywhere within the `switch` statement, but it's common practice to put it at the end.

## 3. How the Traditional `switch` Statement Works

1.  The `expression` is evaluated once.
2.  The resulting value is compared with the value of each `case` label.
3.  If a match is found, the code block associated with that `case` label is executed.
4.  If a `break` statement is encountered, the `switch` statement terminates, and execution continues with the statement immediately following the `switch` block.
5.  If no `break` is found, execution "falls through" to the next `case` block, regardless of whether its value matches, until a `break` or the end of the `switch` statement is reached.
6.  If no `case` matches the `expression` and a `default` block is present, the `default` block is executed.

## 4. Supported Data Types for `expression`

In the traditional `switch` statement, the `expression` can be of the following types:

*   `byte`, `short`, `char`, `int` (and their corresponding wrapper classes: `Byte`, `Short`, `Character`, `Integer`)
*   `enum` types
*   `String` (since Java 7)

## 5. Important Points & Rules

*   **Fall-through:** Without `break` statements, execution will continue into subsequent `case` blocks. This can be used intentionally for grouping cases (as shown in Example 3), but it's a common source of bugs if not intended.
*   **`case` values must be constants:** They cannot be variables or expressions that are evaluated at runtime (e.g., `case myVariable:` or `case a + b:` are not allowed).
*   **No duplicate `case` values:** Each `case` label must have a unique value.
*   **`null` in `switch` (Java 17+ / Java 21+):**
    *   Prior to Java 17, passing `null` to a `switch` statement would result in a `NullPointerException`.
    *   From Java 17 (as a preview feature, standard in Java 21), you can explicitly handle `null` using `case null:` or include `null` in a multi-label `case` (`case 1, 2, null:`).
    *   If `null` is passed and `case null:` is not handled, it will still throw a `NullPointerException`.

---

## Examples (Traditional `switch` Statement)

### Example 1: Basic `int` `switch`

This example takes an integer representing a day number and prints the corresponding day name.

```java
import java.util.Scanner;

public class DayOfWeek {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a day number (1-7): ");
        int dayNumber = scanner.nextInt();

        String dayName;

        switch (dayNumber) {
            case 1:
                dayName = "Sunday";
                break;
            case 2:
                dayName = "Monday";
                break;
            case 3:
                dayName = "Tuesday";
                break;
            case 4:
                dayName = "Wednesday";
                break;
            case 5:
                dayName = "Thursday";
                break;
            case 6:
                dayName = "Friday";
                break;
            case 7:
                dayName = "Saturday";
                break;
            default:
                dayName = "Invalid day number";
                break; // Optional break here as it's the last case
        }

        System.out.println("Day: " + dayName);
        scanner.close();
    }
}
```

**Input:**
```
Enter a day number (1-7): 3
```

**Output:**
```
Day: Tuesday
```

---

### Example 2: `String` `switch` (Java 7+)

This example takes a command as a `String` and performs an action.

```java
import java.util.Scanner;

public class CommandProcessor {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter command (start, stop, pause, resume): ");
        String command = scanner.nextLine();

        switch (command.toLowerCase()) { // Convert to lowercase for case-insensitivity
            case "start":
                System.out.println("Starting service...");
                break;
            case "stop":
                System.out.println("Stopping service...");
                break;
            case "pause":
                System.out.println("Pausing service...");
                break;
            case "resume":
                System.out.println("Resuming service...");
                break;
            default:
                System.out.println("Unknown command. Please try again.");
                break;
        }

        scanner.close();
    }
}
```

**Input:**
```
Enter command (start, stop, pause, resume): STOP
```

**Output:**
```
Stopping service...
```

---

### Example 3: Demonstrating Fall-through (Grouping Cases)

This example groups months into seasons using fall-through.

```java
import java.util.Scanner;

public class SeasonIdentifier {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a month number (1-12): ");
        int month = scanner.nextInt();

        String season;

        switch (month) {
            case 12: // December
            case 1:  // January
            case 2:  // February
                season = "Winter";
                break;
            case 3:  // March
            case 4:  // April
            case 5:  // May
                season = "Spring";
                break;
            case 6:  // June
            case 7:  // July
            case 8:  // August
                season = "Summer";
                break;
            case 9:  // September
            case 10: // October
            case 11: // November
                season = "Autumn";
                break;
            default:
                season = "Invalid month number";
        }

        System.out.println("The season is: " + season);
        scanner.close();
    }
}
```

**Input 1:**
```
Enter a month number (1-12): 7
```

**Output 1:**
```
The season is: Summer
```

**Input 2:**
```
Enter a month number (1-12): 2
```

**Output 2:**
```
The season is: Winter
```

---

## 6. `switch` Expressions (Java 14+)

Starting with Java 14 (after being a preview feature in Java 12 and 13), `switch` can also be used as an **expression**. This allows it to return a value, making the code more concise and often more readable.

**Key Features of `switch` Expressions:**

*   **Return a Value:** The `switch` statement can now yield a value, which can be assigned to a variable.
*   **Arrow Syntax (`->`):** Instead of `case value: ... break;`, you use `case value -> expression;`.
    *   This syntax implies an automatic `break`, eliminating fall-through by default.
    *   The right-hand side of the arrow can be an expression, a `throw` statement, or a block of statements.
*   **`yield` Keyword:** If the right-hand side of an arrow `case` is a block of statements, you use `yield` (similar to `return`) to provide the value for the `switch` expression.
*   **Exhaustiveness:** `switch` expressions must be *exhaustive*, meaning all possible cases for the `expression` must be covered. For `enum` types, all enum constants must be listed, or a `default` case must be present. For other types, a `default` case is usually required.

### Syntax (Modern `switch` Expression)

```java
// Assigning the result to a variable
DataType result = switch (expression) {
    case value1 -> value_for_value1; // Single expression
    case value2, value3 -> value_for_value2_or_3; // Multiple labels
    case value4 -> { // Code block
        // complex logic
        yield value_for_value4; // Use 'yield' to return a value from a block
    }
    default -> default_value; // Required if not all cases are covered
};

// Or directly printing
System.out.println(switch (expression) { ... });
```

---

### Example 4: `switch` Expression (Java 14+)

This example uses a `switch` expression to determine if a day is a weekday or weekend.

```java
import java.util.Scanner;

public class DayTypeIdentifier {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a day number (1-7): ");
        int dayNumber = scanner.nextInt();

        // Using switch as an expression
        String dayType = switch (dayNumber) {
            case 1, 7 -> "Weekend"; // Multiple labels, returns directly
            case 2, 3, 4, 5, 6 -> "Weekday";
            default -> { // A block is used here, so 'yield' is needed
                System.out.println("Debug: Invalid day number provided.");
                yield "Unknown"; // 'yield' returns the value from this block
            }
        };

        System.out.println("It's a " + dayType + " day!");
        scanner.close();
    }
}
```

**Input 1:**
```
Enter a day number (1-7): 6
```

**Output 1:**
```
It's a Weekday day!
```

**Input 2:**
```
Enter a day number (1-7): 1
```

**Output 2:**
```
It's a Weekend day!
```

**Input 3:**
```
Enter a day number (1-7): 9
```

**Output 3:**
```
Debug: Invalid day number provided.
It's a Unknown day!
```

**Note:** To compile and run code using `switch` expressions, ensure you are using Java 14 or newer. You might need to specify the `--enable-preview` flag if using Java 14-20 for preview features, or set your compiler's source/target to 14 or higher (e.g., `javac --release 14 YourFile.java`). From Java 21, it's a standard feature.

---

## 7. When to Use `switch` vs. `if-else if`

*   **Use `switch` when:**
    *   You are checking a single variable or expression against a discrete set of constant values.
    *   The conditions are simple equality checks (`==`).
    *   You want cleaner, more readable code for multiple fixed conditions.
    *   (With `switch` expressions) You want to compute a value based on the input.

*   **Use `if-else if` when:**
    *   You need to check a range of values (e.g., `if (score >= 90)`).
    *   You need to check multiple conditions (e.g., `if (age > 18 && hasLicense)`).
    *   The conditions involve complex boolean expressions.
    *   The conditions are not based on a single variable or constant values.

In essence, `switch` is a specialized, more optimized tool for specific scenarios, while `if-else if` is a more general-purpose conditional construct.

