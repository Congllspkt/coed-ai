# Reading and Writing Files in Java

File I/O (Input/Output) is a fundamental aspect of many applications. Java provides robust mechanisms for interacting with the file system, primarily through the `java.io` package (traditional) and the `java.nio.file` package (modern New I/O, or NIO.2).

This guide will cover both approaches with detailed explanations and examples.

## Table of Contents
1.  [Introduction to File I/O](#1-introduction-to-file-io)
2.  [Core Concepts](#2-core-concepts)
    *   [Streams: Byte vs. Character](#streams-byte-vs-character)
    *   [The `java.io` Package](#the-javaio-package-traditional-io)
    *   [The `java.nio.file` Package (NIO.2)](#the-javaniofile-package-nio2---new-io)
    *   [Exception Handling (`IOException`)](#exception-handling-ioexception)
    *   [Resource Management (`try-with-resources`)](#resource-management-try-with-resources)
3.  [Writing Files](#3-writing-files)
    *   [Writing Text Files (Traditional `java.io`)](#writing-text-files-traditional-javaio)
        *   [`FileWriter`](#filewriter)
        *   [`BufferedWriter`](#bufferedwriter)
        *   [`PrintWriter`](#printwriter)
    *   [Writing Text Files (Modern `java.nio.file`)](#writing-text-files-modern-javaniofile)
        *   [`Files.writeString` (Java 11+)](#fileswritestringpath-charsequence-openoption-java-11)
        *   [`Files.write`](#fileswritepath-iterablecharsequence-openoption-or-fileswritepath-byte-openoption)
    *   [Appending to Files](#appending-to-files)
    *   [Writing Binary Files (`FileOutputStream`, `DataOutputStream`)](#writing-binary-files-fileoutputstream-dataoutputstream)
4.  [Reading Files](#4-reading-files)
    *   [Reading Text Files (Traditional `java.io`)](#reading-text-files-traditional-javaio-1)
        *   [`FileReader`](#filereader)
        *   [`BufferedReader`](#bufferedreader-1)
        *   [`Scanner`](#scanner)
    *   [Reading Text Files (Modern `java.nio.file`)](#reading-text-files-modern-javaniofile-1)
        *   [`Files.readString(Path)` (Java 11+)](#filesreadstringpath-java-11)
        *   [`Files.readAllLines(Path)`](#filesreadalllinespath)
        *   [`Files.lines(Path)` (Stream API)](#fileslinespath-stream-api)
    *   [Reading Binary Files (`FileInputStream`, `DataInputStream`)](#reading-binary-files-fileinputstream-datainputstream)
5.  [NIO.2 Enhancements (`java.nio.file`)](#5-nio2-enhancements-javaniofile)
    *   [`Path` and `Paths`](#path-and-paths)
    *   [`Files` Utility Class](#files-utility-class)
6.  [Best Practices and Summary](#6-best-practices-and-summary)

---

## 1. Introduction to File I/O

Java's I/O system is built around the concept of **streams**, which represent a sequence of data flowing from a source to a destination.

*   **Input Stream**: Reads data from a source (e.g., a file, network connection, keyboard).
*   **Output Stream**: Writes data to a destination (e.g., a file, network connection, screen).

## 2. Core Concepts

### Streams: Byte vs. Character

Java streams are primarily categorized into two types:

*   **Byte Streams**: Handle raw binary data, one byte at a time. They are suitable for any type of data (text, images, audio, etc.). Classes typically end with `InputStream` or `OutputStream` (e.g., `FileInputStream`, `FileOutputStream`).
*   **Character Streams**: Handle character data, which is more convenient for text processing, especially with different character encodings (like UTF-8). They typically use an internal buffer to read/write bytes and convert them to/from characters. Classes typically end with `Reader` or `Writer` (e.g., `FileReader`, `FileWriter`, `BufferedReader`, `BufferedWriter`).

**Rule of Thumb**:
*   Use **Character Streams** (Reader/Writer) for text files.
*   Use **Byte Streams** (InputStream/OutputStream) for binary files.

### The `java.io` Package (Traditional I/O)

This package contains the foundational classes for traditional I/O operations. It's still widely used but can be a bit verbose for simple operations and requires careful resource management.

### The `java.nio.file` Package (NIO.2 - New I/O)

Introduced in Java 7, NIO.2 provides a more modern, efficient, and flexible API for file system operations. It addresses many shortcomings of `java.io`, offering better error handling, symbolic link support, and atomic operations. It works with `Path` objects instead of `File` objects.

### Exception Handling (`IOException`)

File operations are inherently risky. Files might not exist, permissions might be denied, or the disk might be full. All file I/O methods in Java declare `IOException` (or its subclasses) as a checked exception, meaning you *must* handle it.

```java
try {
    // File I/O operations
} catch (IOException e) {
    System.err.println("An I/O error occurred: " + e.getMessage());
    e.printStackTrace(); // For debugging, but consider logging in production
}
```

### Resource Management (`try-with-resources`)

Prior to Java 7, developers had to explicitly close I/O streams in a `finally` block to prevent resource leaks. This was cumbersome and error-prone.

Java 7 introduced the **`try-with-resources`** statement, which automatically closes any resource that implements the `java.lang.AutoCloseable` interface (which all I/O streams do) once the `try` block finishes, whether normally or due to an exception. **This is the recommended way to handle I/O resources.**

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class TryWithResourcesExample {
    public static void main(String[] args) {
        String fileName = "input.txt"; // Make sure this file exists for the example

        // Create a dummy file for demonstration
        try (FileWriter fw = new FileWriter(fileName)) {
            fw.write("Hello from try-with-resources!\n");
            fw.write("This line is also automatically closed.");
        } catch (IOException e) {
            System.err.println("Error creating dummy file: " + e.getMessage());
        }

        // Reading using try-with-resources
        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
            System.out.println("Reading from " + fileName + ":");
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }
        // The reader is automatically closed here
    }
}
```

**Input**: (Code execution, `input.txt` is created by the code)
**Output (Console)**:
```
Reading from input.txt:
Hello from try-with-resources!
This line is also automatically closed.
```
**Output (File `input.txt`)**:
```
Hello from try-with-resources!
This line is also automatically closed.
```

---

## 3. Writing Files

### Writing Text Files (Traditional `java.io`)

#### `FileWriter`
`FileWriter` is a basic character stream for writing text to files. It's often wrapped by `BufferedWriter` for efficiency.

**Example: `FileWriterExample.java`**
```java
import java.io.FileWriter;
import java.io.IOException;

public class FileWriterExample {
    public static void main(String[] args) {
        String fileName = "output_fw.txt";
        String content = "Hello, this is a test line written using FileWriter.\n";
        content += "This is the second line.";

        try (FileWriter writer = new FileWriter(fileName)) {
            writer.write(content);
            System.out.println("Content successfully written to " + fileName);
        } catch (IOException e) {
            System.err.println("An error occurred while writing to the file: " + e.getMessage());
        }
    }
}
```

**Input**: (Code execution, no explicit user input)
**Output (Console)**:
```
Content successfully written to output_fw.txt
```
**Output (File `output_fw.txt`)**:
```
Hello, this is a test line written using FileWriter.
This is the second line.
```

#### `BufferedWriter`
`BufferedWriter` improves performance by buffering characters before writing them to the underlying writer. It's almost always recommended to wrap a `FileWriter` with a `BufferedWriter` for better performance. It also provides a `newLine()` method.

**Example: `BufferedWriterExample.java`**
```java
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class BufferedWriterExample {
    public static void main(String[] args) {
        String fileName = "output_bw.txt";
        String line1 = "This is the first line written with BufferedWriter.";
        String line2 = "And this is the second line.";

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
            writer.write(line1);
            writer.newLine(); // Writes a line separator
            writer.write(line2);
            System.out.println("Content successfully written to " + fileName);
        } catch (IOException e) {
            System.err.println("An error occurred while writing to the file: " + e.getMessage());
        }
    }
}
```

**Input**: (Code execution)
**Output (Console)**:
```
Content successfully written to output_bw.txt
```
**Output (File `output_bw.txt`)**:
```
This is the first line written with BufferedWriter.
And this is the second line.
```

#### `PrintWriter`
`PrintWriter` provides convenience methods like `print()`, `println()`, and `format()`, similar to `System.out.print()`. It can also be configured to auto-flush the buffer.

**Example: `PrintWriterExample.java`**
```java
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class PrintWriterExample {
    public static void main(String[] args) {
        String fileName = "output_pw.txt";

        try (PrintWriter writer = new PrintWriter(new FileWriter(fileName))) {
            writer.println("This is the first line from PrintWriter.");
            writer.printf("The answer is %d and the value is %.2f%n", 42, 3.14159);
            writer.print("This is a final line without newline.");
            System.out.println("Content successfully written to " + fileName);
        } catch (IOException e) {
            System.err.println("An error occurred while writing to the file: " + e.getMessage());
        }
    }
}
```

**Input**: (Code execution)
**Output (Console)**:
```
Content successfully written to output_pw.txt
```
**Output (File `output_pw.txt`)**:
```
This is the first line from PrintWriter.
The answer is 42 and the value is 3.14
This is a final line without newline.
```

### Writing Text Files (Modern `java.nio.file`)

NIO.2 offers simpler methods for common file operations, especially for text files.

#### `Files.writeString(Path, CharSequence, OpenOption...)` (Java 11+)
This is the simplest way to write a string to a file. It creates the file if it doesn't exist, and overwrites it by default if it does.

**Example: `NIOWriteStringExample.java`**
```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
// import java.nio.file.StandardOpenOption; // Can be used for options like APPEND

public class NIOWriteStringExample {
    public static void main(String[] args) {
        String fileName = "output_nio_string.txt";
        String content = "This content is written using Files.writeString (Java 11+).\n";
        content += "It's very concise!";
        Path filePath = Paths.get(fileName);

        try {
            Files.writeString(filePath, content); // Overwrites if file exists by default
            System.out.println("Content successfully written to " + fileName);
        } catch (IOException e) {
            System.err.println("An error occurred while writing to the file: " + e.getMessage());
        }
    }
}
```

**Input**: (Code execution)
**Output (Console)**:
```
Content successfully written to output_nio_string.txt
```
**Output (File `output_nio_string.txt`)**:
```
This content is written using Files.writeString (Java 11+).
It's very concise!
```

#### `Files.write(Path, Iterable<CharSequence>, OpenOption...)` or `Files.write(Path, byte[], OpenOption...)`
For older Java versions or when writing lines from a collection, you can use `Files.write`. It takes an `Iterable<CharSequence>` (like a `List<String>`) or a `byte[]`.

**Example: `NIOWriteLinesExample.java`**
```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;

public class NIOWriteLinesExample {
    public static void main(String[] args) {
        String fileName = "output_nio_lines.txt";
        List<String> lines = Arrays.asList(
            "First line using Files.write(Path, List<String>)",
            "Second line, it handles newlines automatically.",
            "Third and final line."
        );
        Path filePath = Paths.get(fileName);

        try {
            Files.write(filePath, lines); // Each string in the list becomes a line in the file
            System.out.println("Content successfully written to " + fileName);
        } catch (IOException e) {
            System.err.println("An error occurred while writing to the file: " + e.getMessage());
        }
    }
}
```

**Input**: (Code execution)
**Output (Console)**:
```
Content successfully written to output_nio_lines.txt
```
**Output (File `output_nio_lines.txt`)**:
```
First line using Files.write(Path, List<String>)
Second line, it handles newlines automatically.
Third and final line.
```

### Appending to Files

To add content to the end of an existing file instead of overwriting it, you use specific options.

**Traditional `java.io` (`FileWriter`)**:
Pass `true` as the second argument to the `FileWriter` constructor.

**Example: `AppendFileWriterExample.java`**
```java
import java.io.FileWriter;
import java.io.IOException;

public class AppendFileWriterExample {
    public static void main(String[] args) {
        String fileName = "append_file.txt";
        String contentToAppend = "This content is appended to the file.\n";

        // First, create or overwrite the file with initial content
        try (FileWriter writer = new FileWriter(fileName)) {
            writer.write("Initial content.\n");
            System.out.println("Initial content written to " + fileName);
        } catch (IOException e) {
            System.err.println("Error writing initial content: " + e.getMessage());
        }

        // Now, append to the file
        try (FileWriter writer = new FileWriter(fileName, true)) { // 'true' for append mode
            writer.write(contentToAppend);
            System.out.println("Content successfully appended to " + fileName);
        } catch (IOException e) {
            System.err.println("An error occurred while appending to the file: " + e.getMessage());
        }
    }
}
```

**Input**: (Code execution)
**Output (Console)**:
```
Initial content written to append_file.txt
Content successfully appended to append_file.txt
```
**Output (File `append_file.txt`)**:
```
Initial content.
This content is appended to the file.
```

**Modern `java.nio.file` (`Files.write` or `Files.writeString`)**:
Use `StandardOpenOption.APPEND`.

**Example: `AppendNIOExample.java`**
```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.Arrays;
import java.util.List;

public class AppendNIOExample {
    public static void main(String[] args) {
        String fileName = "append_nio_file.txt";
        Path filePath = Paths.get(fileName);
        List<String> linesToAppend = Arrays.asList(
            "Appended line 1 via NIO.",
            "Appended line 2 via NIO."
        );

        // First, create or overwrite the file with initial content
        try {
            Files.writeString(filePath, "Initial content for NIO append example.\n");
            System.out.println("Initial content written to " + fileName);
        } catch (IOException e) {
            System.err.println("Error writing initial content: " + e.getMessage());
        }

        // Now, append to the file
        try {
            // StandardOpenOption.CREATE will create the file if it doesn't exist
            // StandardOpenOption.APPEND will append to the end
            Files.write(filePath, linesToAppend, StandardOpenOption.APPEND, StandardOpenOption.CREATE);
            System.out.println("Content successfully appended to " + fileName);
        } catch (IOException e) {
            System.err.println("An error occurred while appending to the file: " + e.getMessage());
        }
    }
}
```

**Input**: (Code execution)
**Output (Console)**:
```
Initial content written to append_nio_file.txt
Content successfully appended to append_nio_file.txt
```
**Output (File `append_nio_file.txt`)**:
```
Initial content for NIO append example.
Appended line 1 via NIO.
Appended line 2 via NIO.
```

### Writing Binary Files (`FileOutputStream`, `DataOutputStream`)

For writing raw bytes or specific primitive data types, you use byte streams.

#### `FileOutputStream`
Writes raw bytes to a file.

**Example: `FileOutputStreamExample.java`**
```java
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

public class FileOutputStreamExample {
    public static void main(String[] args) {
        String fileName = "output_fos.dat";
        String text = "This is some binary data (as bytes).";
        byte[] data = text.getBytes(StandardCharsets.UTF_8); // Convert string to bytes

        try (FileOutputStream fos = new FileOutputStream(fileName)) {
            fos.write(data);
            System.out.println("Binary data successfully written to " + fileName);
        } catch (IOException e) {
            System.err.println("An error occurred while writing binary data: " + e.getMessage());
        }
    }
}
```

**Input**: (Code execution)
**Output (Console)**:
```
Binary data successfully written to output_fos.dat
```
**Output (File `output_fos.dat`)**: (Contents would appear as the UTF-8 bytes of the string. If opened in a text editor, it would likely display as `This is some binary data (as bytes).`)

#### `DataOutputStream`
Wraps another output stream (like `FileOutputStream`) to write primitive Java data types (int, double, boolean, etc.) in a machine-independent way.

**Example: `DataOutputStreamExample.java`**
```java
import java.io.DataOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class DataOutputStreamExample {
    public static void main(String[] args) {
        String fileName = "output_dos.dat";

        try (DataOutputStream dos = new DataOutputStream(new FileOutputStream(fileName))) {
            dos.writeInt(12345);
            dos.writeDouble(3.14159);
            dos.writeBoolean(true);
            dos.writeUTF("Hello from DataOutputStream!"); // Writes a String in modified UTF-8 format
            System.out.println("Primitive data successfully written to " + fileName);
        } catch (IOException e) {
            System.err.println("An error occurred while writing primitive data: " + e.getMessage());
        }
    }
}
```

**Input**: (Code execution)
**Output (Console)**:
```
Primitive data successfully written to output_dos.dat
```
**Output (File `output_dos.dat`)**: (This file is binary and will **not** be human-readable in a text editor. It contains the raw byte representations of the int, double, boolean, and UTF string. Reading it back correctly requires a `DataInputStream` in the exact same order.)

---

## 4. Reading Files

### Reading Text Files (Traditional `java.io`)

#### `FileReader`
`FileReader` is a basic character stream for reading text from files. Like `FileWriter`, it's often wrapped by `BufferedReader` for efficiency and convenience.

**Example: `FileReaderExample.java`**
```java
import java.io.FileReader;
import java.io.IOException;

public class FileReaderExample {
    public static void main(String[] args) {
        String fileName = "output_fw.txt"; // Assuming this file was created by FileWriterExample

        try (FileReader reader = new FileReader(fileName)) {
            int character;
            System.out.println("Reading content from " + fileName + ":");
            while ((character = reader.read()) != -1) { // -1 indicates end of stream
                System.out.print((char) character);
            }
            System.out.println("\nSuccessfully read content.");
        } catch (IOException e) {
            System.err.println("An error occurred while reading the file: " + e.getMessage());
        }
    }
}
```

**Input**: File `output_fw.txt` must exist with some content (e.g., from `FileWriterExample.java`).
**Output (Console)**:
```
Reading content from output_fw.txt:
Hello, this is a test line written using FileWriter.
This is the second line.
Successfully read content.
```

#### `BufferedReader`
`BufferedReader` reads text from a character-input stream, buffering characters to provide for the efficient reading of characters, arrays, and lines. Its `readLine()` method is very convenient for reading line by line.

**Example: `BufferedReaderExample.java`**
```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class BufferedReaderExample {
    public static void main(String[] args) {
        String fileName = "output_bw.txt"; // Assuming this file was created by BufferedWriterExample

        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
            String line;
            System.out.println("Reading content from " + fileName + " line by line:");
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            System.out.println("Successfully read content.");
        } catch (IOException e) {
            System.err.println("An error occurred while reading the file: " + e.getMessage());
        }
    }
}
```

**Input**: File `output_bw.txt` must exist with some content.
**Output (Console)**:
```
Reading content from output_bw.txt line by line:
This is the first line written with BufferedWriter.
And this is the second line.
Successfully read content.
```

#### `Scanner`
The `Scanner` class (from `java.util`) is versatile for parsing primitive types and strings using regular expressions. It can read from various input sources, including files. It's often easier for tokenized input.

**Example: `ScannerFileExample.java`**
```java
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class ScannerFileExample {
    public static void main(String[] args) {
        String fileName = "output_pw.txt"; // Assuming this file was created by PrintWriterExample

        try (Scanner scanner = new Scanner(new File(fileName))) {
            System.out.println("Reading content from " + fileName + " using Scanner:");
            while (scanner.hasNextLine()) {
                System.out.println(scanner.nextLine());
            }
            System.out.println("Successfully read content.");
        } catch (FileNotFoundException e) {
            System.err.println("File not found: " + e.getMessage());
        }
    }
}
```

**Input**: File `output_pw.txt` must exist with some content.
**Output (Console)**:
```
Reading content from output_pw.txt using Scanner:
This is the first line from PrintWriter.
The answer is 42 and the value is 3.14
This is a final line without newline.
Successfully read content.
```

### Reading Text Files (Modern `java.nio.file`)

NIO.2 provides very convenient methods for reading entire files or processing them line by line.

#### `Files.readString(Path)` (Java 11+)
The simplest way to read an entire file into a single string.

**Example: `NIOReadStringExample.java`**
```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class NIOReadStringExample {
    public static void main(String[] args) {
        String fileName = "output_nio_string.txt"; // Assuming this file was created earlier
        Path filePath = Paths.get(fileName);

        try {
            String content = Files.readString(filePath);
            System.out.println("Content from " + fileName + " (using Files.readString):\n" + content);
        } catch (IOException e) {
            System.err.println("An error occurred while reading the file: " + e.getMessage());
        }
    }
}
```

**Input**: File `output_nio_string.txt` must exist with some content.
**Output (Console)**:
```
Content from output_nio_string.txt (using Files.readString):
This content is written using Files.writeString (Java 11+).
It's very concise!
```

#### `Files.readAllLines(Path)`
Reads all lines from a file as a `List<String>`. Useful for smaller files that can fit entirely into memory.

**Example: `NIOReadAllLinesExample.java`**
```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class NIOReadAllLinesExample {
    public static void main(String[] args) {
        String fileName = "output_nio_lines.txt"; // Assuming this file was created earlier
        Path filePath = Paths.get(fileName);

        try {
            List<String> lines = Files.readAllLines(filePath);
            System.out.println("Content from " + fileName + " (using Files.readAllLines):");
            for (String line : lines) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.err.println("An error occurred while reading the file: " + e.getMessage());
        }
    }
}
```

**Input**: File `output_nio_lines.txt` must exist with some content.
**Output (Console)**:
```
Content from output_nio_lines.txt (using Files.readAllLines):
First line using Files.write(Path, List<String>)
Second line, it handles newlines automatically.
Third and final line.
```

#### `Files.lines(Path)` (Stream API)
Returns a `Stream<String>` of lines from a file. This is highly efficient for large files as it reads lines on demand (lazy evaluation) and works well with the Java Stream API. Remember to close the stream.

**Example: `NIOLinesStreamExample.java`**
```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Stream;

public class NIOLinesStreamExample {
    public static void main(String[] args) {
        String fileName = "output_bw.txt"; // Using a multi-line file created earlier
        Path filePath = Paths.get(fileName);

        // try-with-resources ensures the Stream is closed automatically
        try (Stream<String> lines = Files.lines(filePath)) {
            System.out.println("Content from " + fileName + " (using Files.lines Stream API):");
            lines.filter(line -> line.contains("line")) // Process lines containing "line"
                 .map(String::toUpperCase)              // Convert to uppercase
                 .forEach(System.out.println);          // Print each result
        } catch (IOException e) {
            System.err.println("An error occurred while reading the file: " + e.getMessage());
        }
    }
}
```

**Input**: File `output_bw.txt` must exist.
**Output (Console)**:
```
Content from output_bw.txt (using Files.lines Stream API):
THIS IS THE FIRST LINE WRITTEN WITH BUFFEREDWRITER.
AND THIS IS THE SECOND LINE.
```

### Reading Binary Files (`FileInputStream`, `DataInputStream`)

For reading raw bytes or specific primitive data types that were written with `DataOutputStream`.

#### `FileInputStream`
Reads raw bytes from a file.

**Example: `FileInputStreamExample.java`**
```java
import java.io.FileInputStream;
import java.io.IOException;

public class FileInputStreamExample {
    public static void main(String[] args) {
        String fileName = "output_fos.dat"; // Assuming this file was created by FileOutputStreamExample

        try (FileInputStream fis = new FileInputStream(fileName)) {
            int byteRead;
            System.out.println("Reading binary data from " + fileName + ":");
            while ((byteRead = fis.read()) != -1) {
                // For demonstration, print as character if it's printable ASCII, otherwise as byte value
                if (byteRead >= 32 && byteRead <= 126) {
                    System.out.print((char) byteRead);
                } else {
                    System.out.printf("[%d]", byteRead); // Print byte value for non-printable characters
                }
            }
            System.out.println("\nSuccessfully read binary data.");
        } catch (IOException e) {
            System.err.println("An error occurred while reading binary data: " + e.getMessage());
        }
    }
}
```

**Input**: File `output_fos.dat` must exist with some content.
**Output (Console)**:
```
Reading binary data from output_fos.dat:
This is some binary data (as bytes).
Successfully read binary data.
```

#### `DataInputStream`
Wraps an input stream (like `FileInputStream`) to read primitive Java data types that were written by a `DataOutputStream`. It's crucial that the data types are read in the exact same order they were written.

**Example: `DataInputStreamExample.java`**
```java
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.IOException;

public class DataInputStreamExample {
    public static void main(String[] args) {
        String fileName = "output_dos.dat"; // Assuming this file was created by DataOutputStreamExample

        try (DataInputStream dis = new DataInputStream(new FileInputStream(fileName))) {
            int intValue = dis.readInt();
            double doubleValue = dis.readDouble();
            boolean booleanValue = dis.readBoolean();
            String stringValue = dis.readUTF();

            System.out.println("Reading primitive data from " + fileName + ":");
            System.out.println("Int Value: " + intValue);
            System.out.println("Double Value: " + doubleValue);
            System.out.println("Boolean Value: " + booleanValue);
            System.out.println("String Value: " + stringValue);
            System.out.println("Successfully read primitive data.");
        } catch (IOException e) {
            System.err.println("An error occurred while reading primitive data: " + e.getMessage());
        }
    }
}
```

**Input**: File `output_dos.dat` must exist, created by `DataOutputStreamExample`.
**Output (Console)**:
```
Reading primitive data from output_dos.dat:
Int Value: 12345
Double Value: 3.14159
Boolean Value: true
String Value: Hello from DataOutputStream!
Successfully read primitive data.
```

---

## 5. NIO.2 Enhancements (`java.nio.file`)

The `java.nio.file` package, often referred to as NIO.2, provides a more object-oriented and robust way to interact with the file system.

### `Path` and `Paths`

Instead of `java.io.File`, NIO.2 uses `java.nio.file.Path` to represent a file or directory path. `Paths` is a utility class for obtaining `Path` instances.

```java
import java.nio.file.Path;
import java.nio.file.Paths;

public class PathExample {
    public static void main(String[] args) {
        // Creating Path instances
        Path path1 = Paths.get("myDirectory", "myFile.txt");       // Relative path
        Path path2 = Paths.get("/home/user/documents/report.pdf"); // Absolute path (Linux/macOS)
        Path path3 = Paths.get("C:\\Users\\admin\\data.csv");      // Absolute path (Windows)

        System.out.println("Path 1: " + path1);
        System.out.println("  File Name: " + path1.getFileName());
        System.out.println("  Parent Directory: " + path1.getParent());
        System.out.println("  Is Absolute: " + path1.isAbsolute());
        System.out.println("  To Absolute Path: " + path1.toAbsolutePath());
        System.out.println("\nPath 2: " + path2);
        System.out.println("  File Name: " + path2.getFileName());
        System.out.println("  Root: " + path2.getRoot());
        System.out.println("  Is Absolute: " + path2.isAbsolute());
    }
}
```

**Output (Console - may vary based on OS and current directory)**:
```
Path 1: myDirectory/myFile.txt
  File Name: myFile.txt
  Parent Directory: myDirectory
  Is Absolute: false
  To Absolute Path: /Users/yourusername/java_projects/myDirectory/myFile.txt
Path 2: /home/user/documents/report.pdf
  File Name: report.pdf
  Root: /
  Is Absolute: true
```

### `Files` Utility Class

The `Files` class provides static methods for a wide range of file system operations like creating, deleting, copying, and moving files and directories.

**Example: File Management with `Files`**
```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

public class NIOFileOperationsExample {
    public static void main(String[] args) {
        Path sourceFile = Paths.get("source.txt");
        Path targetFile = Paths.get("target.txt");
        Path directory = Paths.get("my_new_directory");
        Path movedFile = Paths.get("my_new_directory", "source_moved.txt");

        try {
            // 1. Create a file
            Files.writeString(sourceFile, "Content of the source file.");
            System.out.println("Created file: " + sourceFile.toAbsolutePath());

            // 2. Check if file exists
            boolean exists = Files.exists(sourceFile);
            System.out.println("Does " + sourceFile + " exist? " + exists);

            // 3. Create a directory (and parents if needed with createDirectories)
            Files.createDirectory(directory);
            System.out.println("Created directory: " + directory.toAbsolutePath());

            // 4. Copy a file
            // StandardCopyOption.REPLACE_EXISTING ensures target.txt is overwritten if it exists
            Files.copy(sourceFile, targetFile, StandardCopyOption.REPLACE_EXISTING);
            System.out.println("Copied " + sourceFile + " to " + targetFile);
            System.out.println("Content of " + targetFile + ": " + Files.readString(targetFile));

            // 5. Move/Rename a file (atomically if possible)
            // Note: Moving can be used for renaming within the same directory
            Files.move(sourceFile, movedFile, StandardCopyOption.REPLACE_EXISTING);
            System.out.println("Moved " + sourceFile + " to " + movedFile);

            // 6. Delete files and directory
            Files.delete(targetFile);
            System.out.println("Deleted file: " + targetFile);
            Files.delete(movedFile); // Delete the file after it was moved
            System.out.println("Deleted file: " + movedFile);
            Files.delete(directory); // Directory must be empty to be deleted
            System.out.println("Deleted directory: " + directory);

        } catch (IOException e) {
            System.err.println("An I/O error occurred: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

**Input**: (Code execution)
**Output (Console - absolute paths will vary based on execution environment)**:
```
Created file: /path/to/your/project/source.txt
Does source.txt exist? true
Created directory: /path/to/your/project/my_new_directory
Copied source.txt to target.txt
Content of target.txt: Content of the source file.
Moved source.txt to my_new_directory/source_moved.txt
Deleted file: target.txt
Deleted file: my_new_directory/source_moved.txt
Deleted directory: my_new_directory
```
**Output (File System)**: Files and directories are created, modified, and then removed by the program.

---

## 6. Best Practices and Summary

*   **Use `try-with-resources`**: Always use `try-with-resources` for any I/O stream (`Reader`, `Writer`, `InputStream`, `OutputStream`, `Scanner`, `Stream<String>` from `Files.lines()`, etc.) to ensure resources are properly closed, even if exceptions occur. This prevents resource leaks and simplifies code.
*   **Buffer for Performance**: For character-based I/O (text files), always wrap `FileReader`/`FileWriter` with `BufferedReader`/`BufferedWriter` for significant performance improvements, especially when reading/writing large amounts of data.
*   **Choose `java.nio.file` for Modern Applications**: For new development in Java 7+, the `java.nio.file` package offers a more robust, flexible, and often simpler API for file system interactions. Methods like `Files.readString()`, `Files.writeString()`, `Files.readAllLines()`, and `Files.lines()` are extremely convenient for text files.
*   **Handle `IOException`**: File operations are prone to errors (file not found, permission denied, disk full). Always handle `IOException` (or specific subclasses) gracefully.
*   **Byte vs. Character Streams**: Use `Reader`/`Writer` for text data, and `InputStream`/`OutputStream` for binary data. Be mindful of character encodings (e.g., `StandardCharsets.UTF_8`) when converting between byte and character streams.
*   **`Scanner` for Parsing**: If you need to parse structured text data (e.g., numbers, words separated by delimiters) from a file, `Scanner` can be more convenient than `BufferedReader`.
*   **`DataInputStream`/`DataOutputStream` for Primitive Types**: When you need to read/write specific primitive data types (like `int`, `double`, `boolean`) to/from a binary file in a type-safe and platform-independent manner, use `DataInputStream` and `DataOutputStream`. Ensure you read them back in the exact order they were written.

By following these guidelines and understanding the different tools available, you can efficiently and safely perform file I/O operations in your Java applications.