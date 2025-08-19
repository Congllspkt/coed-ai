# Rules While Handling Exceptions in Java

Handling exceptions effectively is crucial for building robust, reliable, and maintainable Java applications. This document details the key rules and best practices for exception handling, accompanied by illustrative examples.

## Table of Contents
1.  [Introduction to Exceptions](#1-introduction-to-exceptions)
    *   [Exception Hierarchy](#11-exception-hierarchy)
    *   [Checked vs. Unchecked Exceptions](#12-checked-vs-unchecked-exceptions)
    *   [`try-catch-finally` Block](#13-try-catch-finally-block)
    *   [`throws` Keyword](#14-throws-keyword)
2.  [Key Rules for Exception Handling](#2-key-rules-for-exception-handling)
    *   [Rule 1: Be Specific with Catch Blocks](#rule-1-be-specific-with-catch-blocks)
    *   [Rule 2: Don't Catch `Throwable` or `Error` (Generally)](#rule-2-dont-catch-throwable-or-error-generally)
    *   [Rule 3: Always Clean Up Resources (`finally` or `try-with-resources`)](#rule-3-always-clean-up-resources-finally-or-try-with-resources)
    *   [Rule 4: Don't Suppress Exceptions Silently](#rule-4-dont-suppress-exceptions-silently)
    *   [Rule 5: Log Exceptions Properly](#rule-5-log-exceptions-properly)
    *   [Rule 6: Throw Specific Exceptions](#rule-6-throw-specific-exceptions)
    *   [Rule 7: Wrap and Rethrow (Exception Chaining)](#rule-7-wrap-and-rethrow-exception-chaining)
    *   [Rule 8: Use `try-with-resources` for Auto-Closable Objects](#rule-8-use-try-with-resources-for-auto-closable-objects)
    *   [Rule 9: Fail Fast (Validate Inputs)](#rule-9-fail-fast-validate-inputs)
    *   [Rule 10: Don't Use Exceptions for Control Flow](#rule-10-dont-use-exceptions-for-control-flow)
    *   [Rule 11: Create Custom Exceptions When Needed](#rule-11-create-custom-exceptions-when-needed)
    *   [Rule 12: Document Exceptions (`@throws`)](#rule-12-document-exceptions-throws)
3.  [Conclusion](#3-conclusion)

---

## 1. Introduction to Exceptions

In Java, an exception is an event that disrupts the normal flow of a program's execution. It's an object that encapsulates an error or an abnormal event that occurred during runtime. Exception handling provides a way to gracefully manage these events, preventing the program from crashing and allowing it to recover or degrade gracefully.

### 1.1. Exception Hierarchy

All exceptions and errors in Java are subclasses of the `java.lang.Throwable` class.

```
Throwable
  ├── Error (Unrecoverable problems, e.g., OutOfMemoryError, StackOverflowError)
  └── Exception
      ├── IOException (Checked, e.g., FileNotFoundException, SocketException)
      ├── SQLException (Checked)
      ├── InterruptedException (Checked)
      └── RuntimeException (Unchecked)
          ├── NullPointerException
          ├── IllegalArgumentException
          ├── ArithmeticException
          └── IndexOutOfBoundsException
```

*   **`Error`**: Represents serious problems that applications should not try to catch. These usually indicate unrecoverable conditions, such as JVM internal errors or resource exhaustion.
*   **`Exception`**: Represents conditions that an application might want to catch. These are problems that occur during normal execution, like `IOException` (file not found) or `SQLException` (database error).
*   **`RuntimeException`**: A special type of `Exception` that the compiler does *not* force you to catch. These typically indicate programming errors (e.g., `NullPointerException`, `ArrayIndexOutOfBoundsException`).

### 1.2. Checked vs. Unchecked Exceptions

*   **Checked Exceptions**: These are `Exception` and its subclasses (excluding `RuntimeException`). The compiler *forces* you to either catch them using a `try-catch` block or declare them using the `throws` keyword in the method signature. If you don't, your code won't compile. They represent conditions that a well-written application should anticipate and recover from.
*   **Unchecked Exceptions**: These are `RuntimeException` and its subclasses, as well as `Error` and its subclasses. The compiler does *not* force you to catch or declare them. They often indicate programming bugs (e.g., trying to access an array out of bounds). While you *can* catch them, it's often better to fix the underlying code bug.

### 1.3. `try-catch-finally` Block

This is the fundamental construct for handling exceptions.

*   **`try`**: Contains the code that might throw an exception.
*   **`catch`**: Contains the code that executes if a specific type of exception is thrown within the `try` block. A `try` block can have multiple `catch` blocks for different exception types.
*   **`finally`**: Contains code that *always* executes, regardless of whether an exception occurred or was caught. It's commonly used for resource cleanup.

**Example:**

```java
import java.io.FileReader;
import java.io.IOException;

public class TryCatchFinallyExample {
    public static void main(String[] args) {
        FileReader reader = null; // Initialize to null
        try {
            // Code that might throw an exception
            reader = new FileReader("nonExistentFile.txt");
            int data = reader.read(); // This will throw if file not found earlier
            System.out.println("File content read successfully (first char: " + (char)data + ")");
        } catch (IOException e) {
            // Code to handle the specific exception
            System.err.println("Error reading file: " + e.getMessage());
            // Optionally, log the full stack trace for debugging
            // e.printStackTrace();
        } finally {
            // Code that always executes, typically for cleanup
            if (reader != null) {
                try {
                    reader.close(); // Close the resource
                    System.out.println("FileReader closed in finally block.");
                } catch (IOException e) {
                    System.err.println("Error closing FileReader: " + e.getMessage());
                }
            }
        }
        System.out.println("Program continues after exception handling.");
    }
}
```

**Input:** (No explicit input for this example, as it tries to open a fixed, non-existent file.)

**Output:**
```
Error reading file: nonExistentFile.txt (The system cannot find the file specified)
FileReader closed in finally block.
Program continues after exception handling.
```

### 1.4. `throws` Keyword

The `throws` keyword is used in a method signature to declare that the method *might* throw one or more specified checked exceptions. This delegates the responsibility of handling the exception to the caller of the method.

**Example:**

```java
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class ThrowsExample {

    // Declares that this method might throw FileNotFoundException and IOException
    public void readFileContent(String fileName) throws FileNotFoundException, IOException {
        FileReader reader = new FileReader(fileName);
        int data = reader.read(); // This can throw IOException
        System.out.println("First character of " + fileName + ": " + (char) data);
        reader.close(); // Important to close resources
    }

    public static void main(String[] args) {
        ThrowsExample app = new ThrowsExample();
        String existingFile = "mytext.txt"; // Create this file manually for successful run
        String nonExistentFile = "nonExistent.txt";

        // Scenario 1: File exists
        // Input: mytext.txt contains "Hello"
        try {
            app.readFileContent(existingFile);
        } catch (FileNotFoundException e) {
            System.err.println("Error: The file '" + existingFile + "' was not found.");
        } catch (IOException e) {
            System.err.println("Error reading '" + existingFile + "': " + e.getMessage());
        }

        System.out.println("\n--- Attempting non-existent file ---");

        // Scenario 2: File does not exist
        // Input: nonExistent.txt does not exist
        try {
            app.readFileContent(nonExistentFile);
        } catch (FileNotFoundException e) {
            System.err.println("Error: The file '" + nonExistentFile + "' was not found.");
        } catch (IOException e) {
            System.err.println("Error reading '" + nonExistentFile + "': " + e.getMessage());
        }
    }
}
```

**Input:**
1.  Create a file named `mytext.txt` in the same directory as `ThrowsExample.java` with content like "Hello World!".
2.  `nonExistent.txt` should not exist.

**Output:**
```
First character of mytext.txt: H

--- Attempting non-existent file ---
Error: The file 'nonExistent.txt' was not found.
```

---

## 2. Key Rules for Exception Handling

These rules guide you in writing effective and robust exception handling code.

### Rule 1: Be Specific with Catch Blocks

Catch the most specific exception first, then broader ones. This allows for precise handling of different error conditions. A general `catch (Exception e)` should be avoided unless absolutely necessary as the last resort, and it should always log the exception.

**Bad Practice:**

```java
// Bad: Catches all exceptions, obscuring specific error types
try {
    // ... some file operation or network call
    int result = 10 / 0; // ArithmeticException
} catch (Exception e) {
    System.err.println("An unexpected error occurred: " + e.getMessage());
}
```

**Good Practice:**

```java
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class SpecificCatchExample {

    public static void processFile(String filePath, String divisionValue) {
        try {
            // Scenario 1: Arithmetic operation
            int num = Integer.parseInt(divisionValue);
            int result = 100 / num;
            System.out.println("Division result: " + result);

            // Scenario 2: File operation
            List<String> lines = Files.readAllLines(Paths.get(filePath));
            lines.forEach(System.out::println);

        } catch (NumberFormatException e) {
            System.err.println("Error: Invalid number format for division. " + e.getMessage());
        } catch (ArithmeticException e) {
            System.err.println("Error: Cannot divide by zero. " + e.getMessage());
        } catch (FileNotFoundException e) { // Specific file not found
            System.err.println("Error: The file '" + filePath + "' was not found. " + e.getMessage());
        } catch (IOException e) { // Broader I/O errors
            System.err.println("Error: An I/O problem occurred while accessing '" + filePath + "'. " + e.getMessage());
        } catch (Exception e) { // General fallback for unexpected issues
            System.err.println("An unhandled general error occurred: " + e.getClass().getSimpleName() + " - " + e.getMessage());
            e.printStackTrace(); // Always print stack trace for unexpected errors
        }
    }

    public static void main(String[] args) {
        System.out.println("--- Scenario 1: Valid input ---");
        // Input: "mydata.txt" exists with content, division by 5
        // Create mydata.txt with some lines, e.g., "Line 1", "Line 2"
        processFile("mydata.txt", "5");

        System.out.println("\n--- Scenario 2: Division by zero ---");
        // Input: "mydata.txt" exists, division by 0
        processFile("mydata.txt", "0");

        System.out.println("\n--- Scenario 3: Non-existent file ---");
        // Input: "nonExistent.txt" does not exist
        processFile("nonExistent.txt", "10");

        System.out.println("\n--- Scenario 4: Invalid number format ---");
        // Input: "mydata.txt" exists, invalid number
        processFile("mydata.txt", "abc");
    }
}
```

**Input:**
1.  Create `mydata.txt` in the same directory:
    ```
    First line
    Second line
    ```
2.  `nonExistent.txt` should not exist.

**Output:**
```
--- Scenario 1: Valid input ---
Division result: 20
First line
Second line

--- Scenario 2: Division by zero ---
Error: Cannot divide by zero. / by zero

--- Scenario 3: Non-existent file ---
Error: The file 'nonExistent.txt' was not found. nonExistent.txt (The system cannot find the file specified)

--- Scenario 4: Invalid number format ---
Error: Invalid number format for division. For input string: "abc"
```

### Rule 2: Don't Catch `Throwable` or `Error` (Generally)

Catching `Throwable` or `Error` is almost always a bad idea. `Error` indicates severe JVM-level problems that your application cannot recover from (e.g., `OutOfMemoryError`, `StackOverflowError`). Catching them might prevent the JVM from properly shutting down or addressing the critical issue.

*   If you catch `Throwable`, you are effectively catching `Error` as well.
*   The only acceptable cases might be at the very top level of an application (e.g., in a main thread's run method or a global exception handler) for logging purposes before the application terminates, but even then, it's typically better to let `Error`s propagate.

**Bad Practice:**

```java
// Very Bad: Masks critical JVM issues
try {
    // ... code that might cause an OutOfMemoryError
} catch (Throwable t) {
    System.err.println("Caught a Throwable: " + t.getMessage());
    // Program might be in an inconsistent state or crash anyway
}
```

### Rule 3: Always Clean Up Resources (`finally` or `try-with-resources`)

Ensure that resources (like file handles, network connections, database connections) are properly closed, even if an exception occurs. This prevents resource leaks. The `finally` block is perfect for this, or better yet, `try-with-resources` for `AutoCloseable` objects (see Rule 8).

**Good Practice (using `finally`):**

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class ResourceCleanupFinally {
    public static void readFile(String fileName) {
        BufferedReader reader = null;
        try {
            reader = new BufferedReader(new FileReader(fileName));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                    System.out.println("Resource closed in finally.");
                } catch (IOException e) {
                    System.err.println("Error closing resource: " + e.getMessage());
                }
            }
        }
    }

    public static void main(String[] args) {
        System.out.println("--- Scenario 1: Successful read ---");
        // Input: mydata.txt exists
        readFile("mydata.txt");

        System.out.println("\n--- Scenario 2: File not found ---");
        // Input: nonExistent.txt does not exist
        readFile("nonExistent.txt");
    }
}
```

**Input:**
1.  Create `mydata.txt`:
    ```
    Hello from mydata.txt
    Line two
    ```
2.  `nonExistent.txt` should not exist.

**Output:**
```
--- Scenario 1: Successful read ---
Hello from mydata.txt
Line two
Resource closed in finally.

--- Scenario 2: File not found ---
Error reading file: nonExistent.txt (The system cannot find the file specified)
Resource closed in finally.
```

### Rule 4: Don't Suppress Exceptions Silently

An empty `catch` block (swallowing the exception) is one of the worst things you can do. It hides problems, making debugging extremely difficult. At the very least, log the exception.

**Bad Practice:**

```java
// Very Bad: Hides errors completely
try {
    int[] numbers = {1, 2};
    System.out.println(numbers[3]); // ArrayIndexOutOfBoundsException
} catch (Exception e) {
    // This looks like everything is fine, but a bug is hidden!
}
System.out.println("Program continues silently after error.");
```

**Good Practice:**

```java
public class DontSuppressExample {
    public static void main(String[] args) {
        try {
            int[] numbers = {1, 2};
            System.out.println(numbers[3]); // This line throws ArrayIndexOutOfBoundsException
        } catch (ArrayIndexOutOfBoundsException e) {
            System.err.println("Caught an array index out of bounds error: " + e.getMessage());
            // Log the stack trace for debugging purposes
            e.printStackTrace();
        }
        System.out.println("Program continues, but the error was acknowledged.");
    }
}
```

**Output:**
```
Caught an array index out of bounds error: Index 3 out of bounds for length 2
java.lang.ArrayIndexOutOfBoundsException: Index 3 out of bounds for length 2
	at DontSuppressExample.main(DontSuppressExample.java:8)
Program continues, but the error was acknowledged.
```

### Rule 5: Log Exceptions Properly

When you catch an exception, log it with sufficient detail, including the full stack trace. This is crucial for debugging and understanding the context of the error. Use a proper logging framework (like SLF4J/Logback, Log4j, or even `java.util.logging`) instead of `System.err.println` in production code.

**Good Practice:**

```java
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class LogExceptionsExample {

    private static final Logger logger = Logger.getLogger(LogExceptionsExample.class.getName());

    public static void readFile(String fileName) {
        try (FileReader reader = new FileReader(fileName)) { // Using try-with-resources
            int character = reader.read();
            if (character != -1) {
                System.out.println("First character: " + (char) character);
            } else {
                System.out.println("File is empty.");
            }
        } catch (FileNotFoundException e) {
            logger.log(Level.WARNING, "File not found: " + fileName, e); // Log with stack trace
        } catch (IOException e) {
            logger.log(Level.SEVERE, "An I/O error occurred while reading file: " + fileName, e); // Log with stack trace
        }
    }

    public static void main(String[] args) {
        System.out.println("--- Reading existing file ---");
        // Input: some_data.txt exists and has content
        // Create 'some_data.txt' with "Hello"
        readFile("some_data.txt");

        System.out.println("\n--- Reading non-existent file ---");
        // Input: non_existent.txt does not exist
        readFile("non_existent.txt");
    }
}
```

**Input:**
1.  Create `some_data.txt` with content "Hello World!".
2.  `non_existent.txt` should not exist.

**Output:**
```
--- Reading existing file ---
First character: H

--- Reading non-existent file ---
Oct 26, 2023 10:30:00 AM LogExceptionsExample readFile
WARNING: File not found: non_existent.txt
java.io.FileNotFoundException: non_existent.txt (The system cannot find the file specified)
	at java.base/java.io.FileInputStream.open0(Native Method)
	at java.base/java.io.FileInputStream.<init>(FileInputStream.java:150)
	at java.base/java.io.FileInputStream.<init>(FileInputStream.java:105)
	at java.base/java.io.FileReader.<init>(FileReader.java:60)
	at LogExceptionsExample.readFile(LogExceptionsExample.java:16)
	at LogExceptionsExample.main(LogExceptionsExample.java:30)
```
*(Note: Actual timestamp and line numbers may vary based on execution environment and code changes.)*

### Rule 6: Throw Specific Exceptions

When creating or re-throwing exceptions, choose the most specific exception class that accurately describes the problem. This provides more meaningful information to the caller and allows for more granular error handling.

**Bad Practice:**

```java
// Bad: Too generic, doesn't convey specific meaning
public void processUserData(String data) throws Exception {
    if (data == null || data.isEmpty()) {
        throw new Exception("Input data is invalid."); // General Exception
    }
    // ... process data
}
```

**Good Practice:**

```java
public class ThrowSpecificExample {
    // Throws a specific IllegalArgumentException for invalid input
    public void processUserData(String data) { // RuntimeException, so no 'throws' needed
        if (data == null || data.trim().isEmpty()) {
            throw new IllegalArgumentException("Input data cannot be null or empty.");
        }
        System.out.println("Processing data: '" + data.trim() + "'");
        // ... actual data processing
    }

    public static void main(String[] args) {
        ThrowSpecificExample app = new ThrowSpecificExample();

        System.out.println("--- Scenario 1: Valid data ---");
        // Input: "  some valid data  "
        try {
            app.processUserData("  some valid data  ");
        } catch (IllegalArgumentException e) {
            System.err.println("Caught: " + e.getMessage());
        }

        System.out.println("\n--- Scenario 2: Null data ---");
        // Input: null
        try {
            app.processUserData(null);
        } catch (IllegalArgumentException e) {
            System.err.println("Caught: " + e.getMessage());
        }

        System.out.println("\n--- Scenario 3: Empty string data ---");
        // Input: ""
        try {
            app.processUserData("");
        } catch (IllegalArgumentException e) {
            System.err.println("Caught: " + e.getMessage());
        }

        System.out.println("\n--- Scenario 4: Blank string data ---");
        // Input: "   "
        try {
            app.processUserData("   ");
        } catch (IllegalArgumentException e) {
            System.err.println("Caught: " + e.getMessage());
        }
    }
}
```

**Output:**
```
--- Scenario 1: Valid data ---
Processing data: 'some valid data'

--- Scenario 2: Null data ---
Caught: Input data cannot be null or empty.

--- Scenario 3: Empty string data ---
Caught: Input data cannot be null or empty.

--- Scenario 4: Blank string data ---
Caught: Input data cannot be null or empty.
```

### Rule 7: Wrap and Rethrow (Exception Chaining)

When a lower-level exception occurs, you might want to catch it and then throw a higher-level, more meaningful exception (often a custom one, see Rule 11) that provides context for your application's domain. The original exception should be passed as the "cause" to the new exception, preserving the stack trace.

**Example:**

```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

// Custom exception for application-specific errors
class DataProcessingException extends Exception {
    public DataProcessingException(String message, Throwable cause) {
        super(message, cause);
    }
}

public class ExceptionChainingExample {

    public void readAndProcessConfig(String configPath) throws DataProcessingException {
        try {
            String content = new String(Files.readAllBytes(Paths.get(configPath)));
            // Simulate a parsing error
            if (content.contains("error")) {
                throw new IOException("Simulated parsing error in config content.");
            }
            System.out.println("Config processed: " + content.substring(0, Math.min(content.length(), 20)) + "...");
        } catch (IOException e) {
            // Catch the low-level IOException and wrap it in a high-level DataProcessingException
            throw new DataProcessingException("Failed to read or parse configuration from " + configPath, e);
        }
    }

    public static void main(String[] args) {
        ExceptionChainingExample app = new ExceptionChainingExample();
        String validConfig = "config.txt";
        String erroredConfig = "errored_config.txt";
        String nonExistentConfig = "non_existent_config.txt";

        // Create these files
        // config.txt: "key=value"
        // errored_config.txt: "key=value error"

        System.out.println("--- Scenario 1: Valid config ---");
        // Input: config.txt
        try {
            app.readAndProcessConfig(validConfig);
        } catch (DataProcessingException e) {
            System.err.println("Caught application error: " + e.getMessage());
            System.err.println("Original cause: " + e.getCause().getClass().getName() + ": " + e.getCause().getMessage());
        }

        System.out.println("\n--- Scenario 2: Errored config ---");
        // Input: errored_config.txt
        try {
            app.readAndProcessConfig(erroredConfig);
        } catch (DataProcessingException e) {
            System.err.println("Caught application error: " + e.getMessage());
            System.err.println("Original cause: " + e.getCause().getClass().getName() + ": " + e.getCause().getMessage());
            e.printStackTrace(); // Print full stack trace to see chain
        }

        System.out.println("\n--- Scenario 3: Non-existent config ---");
        // Input: non_existent_config.txt (does not exist)
        try {
            app.readAndProcessConfig(nonExistentConfig);
        } catch (DataProcessingException e) {
            System.err.println("Caught application error: " + e.getMessage());
            System.err.println("Original cause: " + e.getCause().getClass().getName() + ": " + e.getCause().getMessage());
        }
    }
}
```

**Input:**
1.  Create `config.txt` with content: `application.name=MyWebApp`
2.  Create `errored_config.txt` with content: `application.name=MyWebApp error`
3.  `non_existent_config.txt` should not exist.

**Output:**
```
--- Scenario 1: Valid config ---
Config processed: application.name=MyW...

--- Scenario 2: Errored config ---
Caught application error: Failed to read or parse configuration from errored_config.txt
Original cause: java.io.IOException: Simulated parsing error in config content.
DataProcessingException: Failed to read or parse configuration from errored_config.txt
	at ExceptionChainingExample.readAndProcessConfig(ExceptionChainingExample.java:23)
	at ExceptionChainingExample.main(ExceptionChainingExample.java:46)
Caused by: java.io.IOException: Simulated parsing error in config content.
	at ExceptionChainingExample.readAndProcessConfig(ExceptionChainingExample.java:18)
	... 1 more

--- Scenario 3: Non-existent config ---
Caught application error: Failed to read or parse configuration from non_existent_config.txt
Original cause: java.nio.file.NoSuchFileException: non_existent_config.txt
```

### Rule 8: Use `try-with-resources` for Auto-Closable Objects

Introduced in Java 7, `try-with-resources` automatically closes any resource that implements the `java.lang.AutoCloseable` interface. This is the preferred way to handle resources as it's cleaner and safer than manual `finally` block closures, especially when multiple resources are involved or when a `close()` operation itself can throw an exception.

**Good Practice (Preferred over `finally` for closable resources):**

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class TryWithResourcesExample {
    public static void readFile(String fileName) {
        // Resources declared in try-parentheses are automatically closed
        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            System.out.println("File read successfully (automatic close).");
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }
        // No explicit finally block needed for closing
    }

    public static void main(String[] args) {
        System.out.println("--- Scenario 1: Successful read ---");
        // Input: my_data_twr.txt exists
        // Create my_data_twr.txt: "Hello from TWR"
        readFile("my_data_twr.txt");

        System.out.println("\n--- Scenario 2: File not found ---");
        // Input: no_such_file.txt does not exist
        readFile("no_such_file.txt");
    }
}
```

**Input:**
1.  Create `my_data_twr.txt` with content: `This is a test for try-with-resources.`
2.  `no_such_file.txt` should not exist.

**Output:**
```
--- Scenario 1: Successful read ---
This is a test for try-with-resources.
File read successfully (automatic close).

--- Scenario 2: File not found ---
Error reading file: no_such_file.txt (The system cannot find the file specified)
```

### Rule 9: Fail Fast (Validate Inputs)

Validate method arguments and conditions early to prevent NullPointerExceptions, IllegalArgumentExceptions, etc., from occurring deep within the code logic. This makes errors easier to pinpoint and debug.

**Bad Practice:**

```java
// Bad: NullPointerException will occur deep inside `doSomething`
public void process(String data) {
    // ... many lines of code ...
    int length = data.length(); // NPE if data is null
    System.out.println(length);
}
```

**Good Practice:**

```java
public class FailFastExample {
    public void process(String data) {
        if (data == null || data.trim().isEmpty()) {
            throw new IllegalArgumentException("Input 'data' cannot be null or empty.");
        }
        // Now you are guaranteed 'data' is valid
        System.out.println("Processing data with length: " + data.length());
        // ... rest of the logic
    }

    public static void main(String[] args) {
        FailFastExample app = new FailFastExample();

        System.out.println("--- Scenario 1: Valid input ---");
        // Input: "Hello"
        try {
            app.process("Hello");
        } catch (IllegalArgumentException e) {
            System.err.println("Caught: " + e.getMessage());
        }

        System.out.println("\n--- Scenario 2: Null input ---");
        // Input: null
        try {
            app.process(null);
        } catch (IllegalArgumentException e) {
            System.err.println("Caught: " + e.getMessage());
        }

        System.out.println("\n--- Scenario 3: Empty input ---");
        // Input: ""
        try {
            app.process("");
        } catch (IllegalArgumentException e) {
            System.err.println("Caught: " + e.getMessage());
        }
    }
}
```

**Output:**
```
--- Scenario 1: Valid input ---
Processing data with length: 5

--- Scenario 2: Null input ---
Caught: Input 'data' cannot be null or empty.

--- Scenario 3: Empty input ---
Caught: Input 'data' cannot be null or empty.
```

### Rule 10: Don't Use Exceptions for Control Flow

Exceptions are for *exceptional* situations, not for normal program flow control. Using them to guide `if/else` logic makes code harder to read, debug, and can have performance overhead.

**Bad Practice:**

```java
// Bad: Using exception for control flow (checking if a string is a number)
public int parseNumberBad(String str) {
    try {
        return Integer.parseInt(str);
    } catch (NumberFormatException e) {
        // This is used as an if-else for "is it a number?"
        return -1; // Returning a magic number, also bad
    }
}
```

**Good Practice:**

For cases like parsing, where an invalid format is an *expected* deviation from the norm, catching `NumberFormatException` *is* appropriate. The rule is about *not* using exceptions to decide which path to take when `if` conditions would suffice (e.g., iterating through a list until `IndexOutOfBoundsException` is thrown).

```java
public class ControlFlowExample {

    // Good: This is an appropriate use of catch for an expected parsing error
    public Integer parseNumberGood(String str) {
        try {
            return Integer.parseInt(str);
        } catch (NumberFormatException e) {
            System.err.println("Warning: '" + str + "' is not a valid number. Returning null.");
            return null; // Return null or throw a specific exception if not recoverable
        }
    }

    // Example of when NOT to use exceptions for control flow (iterating an array)
    public void iterateArrayBad(int[] arr) {
        System.out.println("Bad iteration using exceptions:");
        int i = 0;
        try {
            while (true) {
                System.out.println(arr[i++]); // ArrayIndexOutOfBoundsException for control
            }
        } catch (ArrayIndexOutOfBoundsException e) {
            // End of array reached
            System.out.println("Finished iterating (via exception).");
        }
    }

    // Good: Correct way to iterate an array
    public void iterateArrayGood(int[] arr) {
        System.out.println("Good iteration using standard control flow:");
        for (int i = 0; i < arr.length; i++) {
            System.out.println(arr[i]);
        }
        System.out.println("Finished iterating (via loop).");
    }


    public static void main(String[] args) {
        ControlFlowExample app = new ControlFlowExample();

        System.out.println("--- Parsing Numbers ---");
        // Input: "123", "abc"
        System.out.println("Parsed '123': " + app.parseNumberGood("123"));
        System.out.println("Parsed 'abc': " + app.parseNumberGood("abc"));

        System.out.println("\n--- Array Iteration ---");
        int[] numbers = {10, 20, 30};
        app.iterateArrayBad(numbers);
        System.out.println("\n--- Array Iteration (Good Way) ---");
        app.iterateArrayGood(numbers);
    }
}
```

**Output:**
```
--- Parsing Numbers ---
Parsed '123': 123
Warning: 'abc' is not a valid number. Returning null.
Parsed 'abc': null

--- Array Iteration ---
Bad iteration using exceptions:
10
20
30
Finished iterating (via exception).

--- Array Iteration (Good Way) ---
Good iteration using standard control flow:
10
20
30
Finished iterating (via loop).
```

### Rule 11: Create Custom Exceptions When Needed

When existing exceptions don't accurately describe an application-specific error, create your own custom checked or unchecked exceptions. This improves code readability, clarity, and allows callers to handle specific business logic errors.

*   Extend `Exception` for checked exceptions (caller *must* handle).
*   Extend `RuntimeException` for unchecked exceptions (caller *may* handle, often indicates programming error or unrecoverable business logic issue).

**Example:**

```java
// Custom Checked Exception for a business rule violation
class InsufficientFundsException extends Exception {
    private double balance;
    private double withdrawalAmount;

    public InsufficientFundsException(String message, double balance, double withdrawalAmount) {
        super(message);
        this.balance = balance;
        this.withdrawalAmount = withdrawalAmount;
    }

    public double getBalance() { return balance; }
    public double getWithdrawalAmount() { return withdrawalAmount; }
}

public class BankAccount {
    private double balance;

    public BankAccount(double initialBalance) {
        this.balance = initialBalance;
    }

    public void withdraw(double amount) throws InsufficientFundsException {
        if (amount <= 0) {
            throw new IllegalArgumentException("Withdrawal amount must be positive.");
        }
        if (balance < amount) {
            throw new InsufficientFundsException(
                "Insufficient funds for withdrawal.",
                balance, amount);
        }
        balance -= amount;
        System.out.printf("Successfully withdrew %.2f. New balance: %.2f%n", amount, balance);
    }

    public static void main(String[] args) {
        BankAccount myAccount = new BankAccount(500.0);

        System.out.println("--- Scenario 1: Successful withdrawal ---");
        // Input: withdraw 100.0
        try {
            myAccount.withdraw(100.0);
        } catch (InsufficientFundsException e) {
            System.err.println("Withdrawal failed: " + e.getMessage());
        } catch (IllegalArgumentException e) {
            System.err.println("Input error: " + e.getMessage());
        }

        System.out.println("\n--- Scenario 2: Insufficient funds ---");
        // Input: withdraw 450.0 (current balance is 400.0)
        try {
            myAccount.withdraw(450.0);
        } catch (InsufficientFundsException e) {
            System.err.println("Withdrawal failed: " + e.getMessage());
            System.err.printf("Details: Current Balance: %.2f, Attempted Withdrawal: %.2f%n",
                              e.getBalance(), e.getWithdrawalAmount());
        } catch (IllegalArgumentException e) {
            System.err.println("Input error: " + e.getMessage());
        }

        System.out.println("\n--- Scenario 3: Invalid withdrawal amount ---");
        // Input: withdraw -50.0
        try {
            myAccount.withdraw(-50.0);
        } catch (InsufficientFundsException e) {
            System.err.println("Withdrawal failed: " + e.getMessage());
        } catch (IllegalArgumentException e) {
            System.err.println("Input error: " + e.getMessage());
        }
    }
}
```

**Output:**
```
--- Scenario 1: Successful withdrawal ---
Successfully withdrew 100.00. New balance: 400.00

--- Scenario 2: Insufficient funds ---
Withdrawal failed: Insufficient funds for withdrawal.
Details: Current Balance: 400.00, Attempted Withdrawal: 450.00

--- Scenario 3: Invalid withdrawal amount ---
Input error: Withdrawal amount must be positive.
```

### Rule 12: Document Exceptions (`@throws`)

Use Javadoc's `@throws` tag to clearly document the exceptions a method might throw. This helps callers understand what errors to anticipate and how to handle them.

**Example:**

```java
/**
 * Processes a financial transaction.
 *
 * @param amount The amount of the transaction. Must be positive.
 * @param accountId The ID of the account involved. Cannot be null or empty.
 * @return A confirmation message.
 * @throws IllegalArgumentException If the amount is not positive or accountId is invalid.
 * @throws InsufficientFundsException If the account does not have sufficient balance for the transaction.
 * @throws ServiceUnavailableException If the banking service is temporarily down. (Hypothetical checked exception)
 * @throws NetworkConnectionException If there's a problem connecting to the banking network. (Hypothetical checked exception)
 */
public String processTransaction(double amount, String accountId)
    throws IllegalArgumentException, InsufficientFundsException, ServiceUnavailableException, NetworkConnectionException {
    // ... method implementation
    return "Transaction successful.";
}
```
*(No direct runtime input/output for this example, as it's about documentation.)*

---

## 3. Conclusion

Effective exception handling is a cornerstone of writing robust Java applications. By adhering to these rules:

1.  **Specificity**: Catch specific exceptions and rethrow meaningful ones.
2.  **Resource Management**: Always clean up resources using `finally` or `try-with-resources`.
3.  **Visibility**: Never swallow exceptions silently; always log them.
4.  **Context**: Use exception chaining to provide full context.
5.  **Prevention**: Validate inputs early (fail-fast).
6.  **Clarity**: Don't use exceptions for normal control flow.
7.  **Customization**: Create custom exceptions for domain-specific errors.
8.  **Documentation**: Clearly document exceptions a method can throw.

You can create Java applications that are more resilient, easier to debug, and provide a better user experience even when things go wrong.