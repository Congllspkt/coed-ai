The `Scanner` class in Java is a powerful utility for parsing primitive types and strings using regular expressions. It's part of the `java.util` package and is primarily used for reading input from various sources like the console (`System.in`), files, or even strings.

---

# Scanner in Java

## 1. Introduction

The `java.util.Scanner` class is designed for simple text scanning. It can parse primitive types (like `int`, `double`, `boolean`) and strings from any input source. It breaks its input into tokens using a delimiter pattern, which by default matches whitespace.

**Key Features:**
*   Reads data from `System.in`, files, strings, etc.
*   Parses various data types.
*   Uses a default whitespace delimiter, but can be customized.
*   Offers methods to check for the next token's availability and type.

## 2. Key Concepts

### 2.1. Importing the `Scanner` Class

Before you can use `Scanner`, you need to import it:

```java
import java.util.Scanner;
```

### 2.2. Instantiating `Scanner`

To use `Scanner`, you need to create an object of the `Scanner` class, specifying the input source. The most common source is `System.in` (the standard input stream, typically your keyboard).

```java
Scanner scanner = new Scanner(System.in);
```

### 2.3. Delimiters

By default, `Scanner` uses whitespace (spaces, tabs, newlines) as its delimiter. This means methods like `next()`, `nextInt()`, etc., will read tokens separated by these characters.

You can change the delimiter using the `useDelimiter()` method, which takes a regular expression as an argument.

## 3. Core Methods with Examples

Here are the most commonly used `Scanner` methods:

### 3.1. `next()` and `hasNext()`

*   **`next()`**: Reads the next complete token from the input. It returns a `String`.
*   **`hasNext()`**: Returns `true` if this scanner has another token in its input.

**Example 1: Reading a single word**

```java
// BasicScanner.java
import java.util.Scanner;

public class BasicScanner {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in); // Create a Scanner object

        System.out.print("Enter your first name: ");
        String firstName = scanner.next(); // Read the next word (token)

        System.out.println("Hello, " + firstName + "!");

        scanner.close(); // Close the scanner to release resources
    }
}
```

**Execution:**

```bash
# Compile
javac BasicScanner.java

# Run
java BasicScanner
```

**Input:**
```
Enter your first name: Alice
```

**Output:**
```
Hello, Alice!
```

---

### 3.2. `next<Type>()` and `hasNext<Type>()`

`Scanner` provides methods to directly parse the next token into specific primitive types.

*   `nextInt()`: Reads the next token as an `int`.
*   `nextDouble()`: Reads the next token as a `double`.
*   `nextBoolean()`: Reads the next token as a `boolean`.
*   ... and similarly for `nextLong()`, `nextFloat()`, `nextShort()`, `nextByte()`.

Corresponding `hasNext<Type>()` methods (`hasNextInt()`, `hasNextDouble()`, etc.) check if the next token can be interpreted as the specified type.

**Example 2: Reading different primitive types**

```java
// PrimitiveScanner.java
import java.util.Scanner;
import java.util.InputMismatchException; // For error handling

public class PrimitiveScanner {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Read an integer
        int age = 0;
        boolean validInput = false;
        while (!validInput) {
            System.out.print("Enter your age (a whole number): ");
            if (scanner.hasNextInt()) { // Check if the next token is an integer
                age = scanner.nextInt();
                validInput = true;
            } else {
                System.out.println("Invalid input. Please enter a number.");
                scanner.next(); // Consume the invalid token to avoid an infinite loop
            }
        }

        // Read a double
        double temperature = 0.0;
        validInput = false;
        while (!validInput) {
            System.out.print("Enter today's temperature (e.g., 25.5): ");
            if (scanner.hasNextDouble()) { // Check if the next token is a double
                temperature = scanner.nextDouble();
                validInput = true;
            } else {
                System.out.println("Invalid input. Please enter a decimal number.");
                scanner.next(); // Consume the invalid token
            }
        }

        System.out.println("\nYou are " + age + " years old.");
        System.out.println("Today's temperature is " + temperature + " degrees.");

        scanner.close();
    }
}
```

**Execution:**

```bash
# Compile
javac PrimitiveScanner.java

# Run
java PrimitiveScanner
```

**Input (Scenario 1: Correct Input):**
```
Enter your age (a whole number): 30
Enter today's temperature (e.g., 25.5): 23.7
```

**Output (Scenario 1):**
```
You are 30 years old.
Today's temperature is 23.7 degrees.
```

**Input (Scenario 2: Incorrect Input followed by Correct Input):**
```
Enter your age (a whole number): thirty
Invalid input. Please enter a number.
Enter your age (a whole number): 25
Enter today's temperature (e.g., 25.5): cold
Invalid input. Please enter a decimal number.
Enter today's temperature (e.g., 25.5): 18.2
```

**Output (Scenario 2):**
```
Invalid input. Please enter a number.
You are 25 years old.
Invalid input. Please enter a decimal number.
Today's temperature is 18.2 degrees.
```

---

### 3.3. `nextLine()`

*   **`nextLine()`**: Reads the entire line until the next line separator (e.g., Enter key press `\n`). It includes the line separator in the internal buffer but does not return it.

**Example 3: Reading a full line**

```java
// NextLineScanner.java
import java.util.Scanner;

public class NextLineScanner {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter your full name: ");
        String fullName = scanner.nextLine(); // Reads the entire line

        System.out.print("Enter your favorite quote: ");
        String quote = scanner.nextLine(); // Reads another entire line

        System.out.println("\nHello, " + fullName + "!");
        System.out.println("Your favorite quote is: \"" + quote + "\"");

        scanner.close();
    }
}
```

**Execution:**

```bash
# Compile
javac NextLineScanner.java

# Run
java NextLineScanner
```

**Input:**
```
Enter your full name: Jane Doe
Enter your favorite quote: The only way to do great work is to love what you do.
```

**Output:**
```
Hello, Jane Doe!
Your favorite quote is: "The only way to do great work is to love what you do."
```

---

### 3.4. `close()`

*   **`close()`**: Closes the scanner and releases any system resources associated with it. It's crucial to call this method to prevent resource leaks, especially when dealing with file inputs.

You've seen `scanner.close();` in all previous examples.

## 4. Advanced Usage / Specific Scenarios

### 4.1. Changing Delimiters (`useDelimiter()`)

You can change the default whitespace delimiter to any regular expression.

**Example 4: Using a custom delimiter (comma separated values)**

```java
// CustomDelimiterScanner.java
import java.util.Scanner;

public class CustomDelimiterScanner {
    public static void main(String[] args) {
        String data = "Apples,10,Red|Bananas,5,Yellow|Oranges,8,Orange";
        Scanner scanner = new Scanner(data);

        // Use a regular expression to delimit by comma (,) or pipe (|)
        // "\\s*" means zero or more whitespace characters
        scanner.useDelimiter("[,|]\\s*"); 

        System.out.println("Parsing data with custom delimiter:");
        while (scanner.hasNext()) {
            System.out.println("Token: " + scanner.next());
        }

        scanner.close();
    }
}
```

**Execution:**

```bash
# Compile
javac CustomDelimiterScanner.java

# Run
java CustomDelimiterScanner
```

**Output:**
```
Parsing data with custom delimiter:
Token: Apples
Token: 10
Token: Red
Token: Bananas
Token: 5
Token: Yellow
Token: Oranges
Token: 8
Token: Orange
```

### 4.2. Reading from a String

You can also initialize a `Scanner` with a `String` to parse its content.

**Example 5: Scanning a String**

```java
// StringScanner.java
import java.util.Scanner;

public class StringScanner {
    public static void main(String[] args) {
        String inputString = "The quick brown fox jumps over the lazy dog. 123";
        Scanner scanner = new Scanner(inputString);

        System.out.println("Scanning from a String:");

        // Read word by word
        while (scanner.hasNext()) {
            System.out.println("Word: " + scanner.next());
        }

        scanner.close();

        // Another example: parsing numbers and text from a string
        String itemDetails = "ItemName:Laptop Price:1200.50 Quantity:5";
        Scanner itemScanner = new Scanner(itemDetails);
        itemScanner.useDelimiter("[: ]+"); // Delimit by colon or space

        itemScanner.next(); // Consume "ItemName"
        String name = itemScanner.next();

        itemScanner.next(); // Consume "Price"
        double price = itemScanner.nextDouble();

        itemScanner.next(); // Consume "Quantity"
        int quantity = itemScanner.nextInt();

        System.out.println("\nParsed Item Details:");
        System.out.println("Name: " + name);
        System.out.println("Price: $" + price);
        System.out.println("Quantity: " + quantity);

        itemScanner.close();
    }
}
```

**Execution:**

```bash
# Compile
javac StringScanner.java

# Run
java StringScanner
```

**Output:**
```
Scanning from a String:
Word: The
Word: quick
Word: brown
Word: fox
Word: jumps
Word: over
Word: the
Word: lazy
Word: dog.
Word: 123

Parsed Item Details:
Name: Laptop
Price: $1200.5
Quantity: 5
```

## 5. Important Considerations & Best Practices

### 5.1. The `next()` vs. `nextLine()` Pitfall (The Leftover Newline)

This is one of the most common issues beginners face with `Scanner`. When you use `nextInt()`, `nextDouble()`, `next()`, etc., they read *only* the token and leave the newline character (`\n`) that you pressed (Enter key) in the input buffer. If you then call `nextLine()`, it immediately consumes this leftover newline and appears to skip your input prompt.

**Example 6: Demonstrating the `nextLine()` pitfall and its solution**

```java
// NextLinePitfall.java
import java.util.Scanner;

public class NextLinePitfall {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // --- Pitfall Example ---
        System.out.println("--- Pitfall Demonstration ---");
        System.out.print("Enter your age (nextInt): ");
        int age = scanner.nextInt(); 
        // At this point, the newline character from pressing Enter after the age is still in the buffer.

        System.out.print("Enter your city (nextLine - WILL BE SKIPPED): ");
        String city = scanner.nextLine(); // This consumes the leftover newline, not user input!

        System.out.println("Your age is: " + age);
        System.out.println("Your city is: '" + city + "' (likely empty due to skip)");

        // --- Solution Example ---
        System.out.println("\n--- Solution Demonstration ---");
        System.out.print("Enter your favorite number (nextInt): ");
        int favNumber = scanner.nextInt();

        // Consume the leftover newline character before calling nextLine() again
        scanner.nextLine(); // This line is crucial!

        System.out.print("Enter your favorite color (nextLine): ");
        String favColor = scanner.nextLine(); // Now it waits for actual input

        System.out.println("Your favorite number is: " + favNumber);
        System.out.println("Your favorite color is: " + favColor);

        scanner.close();
    }
}
```

**Execution:**

```bash
# Compile
javac NextLinePitfall.java

# Run
java NextLinePitfall
```

**Input:**
```
--- Pitfall Demonstration ---
Enter your age (nextInt): 25
Enter your city (nextLine - WILL BE SKIPPED): Enter your favorite number (nextInt): 7
Enter your favorite color (nextLine): Blue
```

**Output:**
```
--- Pitfall Demonstration ---
Enter your age (nextInt): 25
Enter your city (nextLine - WILL BE SKIPPED): Your age is: 25
Your city is: '' (likely empty due to skip)

--- Solution Demonstration ---
Enter your favorite number (nextInt): 7
Enter your favorite color (nextLine): Blue
Your favorite number is: 7
Your favorite color is: Blue
```

**Solution:** Always add an extra `scanner.nextLine();` call after reading a numeric value (or `next()`) if you plan to read a full line using `nextLine()` immediately afterwards. This `scanner.nextLine();` call will consume the leftover newline character, allowing the subsequent `nextLine()` to wait for actual user input.

### 5.2. Error Handling (`InputMismatchException`)

If the user enters input that doesn't match the expected type (e.g., text for `nextInt()`), `Scanner` will throw an `InputMismatchException`. You should handle this using a `try-catch` block.

**Example 7: Robust Input with Error Handling**

```java
// ErrorHandlingScanner.java
import java.util.InputMismatchException;
import java.util.Scanner;

public class ErrorHandlingScanner {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int age = 0;
        boolean isValidInput = false;

        while (!isValidInput) {
            System.out.print("Please enter your age: ");
            try {
                age = scanner.nextInt();
                if (age >= 0 && age <= 120) { // Basic validation
                    isValidInput = true;
                } else {
                    System.out.println("Age must be between 0 and 120. Please try again.");
                }
            } catch (InputMismatchException e) {
                System.out.println("Invalid input! Please enter a whole number.");
                scanner.next(); // Consume the invalid token to prevent infinite loop
            }
        }

        System.out.println("You entered: " + age + " years old.");
        scanner.close();
    }
}
```

**Execution:**

```bash
# Compile
javac ErrorHandlingScanner.java

# Run
java ErrorHandlingScanner
```

**Input (Scenario 1: Invalid then Valid):**
```
Please enter your age: abc
Invalid input! Please enter a whole number.
Please enter your age: -5
Age must be between 0 and 120. Please try again.
Please enter your age: 30
```

**Output (Scenario 1):**
```
Invalid input! Please enter a whole number.
Age must be between 0 and 120. Please try again.
You entered: 30 years old.
```

### 5.3. Resource Management (`close()`) and `try-with-resources`

Always close the `Scanner` object when you are done with it to free up system resources. Failing to do so can lead to resource leaks, especially when dealing with files.

A more modern and safer way to handle resources like `Scanner` (which implements `AutoCloseable`) is to use the `try-with-resources` statement (available since Java 7). This ensures `close()` is automatically called, even if exceptions occur.

```java
// TryWithResourcesScanner.java
import java.util.Scanner;
import java.util.InputMismatchException;

public class TryWithResourcesScanner {
    public static void main(String[] args) {
        // Scanner is automatically closed when exiting the try block
        try (Scanner scanner = new Scanner(System.in)) { 
            System.out.print("Enter a number: ");
            if (scanner.hasNextInt()) {
                int number = scanner.nextInt();
                System.out.println("You entered: " + number);
            } else {
                System.out.println("That's not a valid number.");
            }
        } catch (InputMismatchException e) {
            System.out.println("An unexpected input error occurred.");
        }
        // No need for scanner.close() here; it's handled automatically
    }
}
```

This `try-with-resources` syntax is the recommended way to use `Scanner` in modern Java applications.

---

## Conclusion

The `Scanner` class is an indispensable tool for interactive Java programs, simplifying the process of reading and parsing user input or data from various sources. Understanding its methods, especially the nuances of `next()` vs. `nextLine()`, and implementing proper error handling and resource management, are key to writing robust and reliable Java applications.