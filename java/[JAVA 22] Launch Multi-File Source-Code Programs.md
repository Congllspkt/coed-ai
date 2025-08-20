To launch multi-file source-code programs in Java 22, you primarily use the `javac` (Java Compiler) and `java` (Java Launcher) commands. While the core process has remained consistent across many Java versions, understanding how to manage compilation paths, execution paths, and packaging is crucial.

This guide will cover:
1.  **Basic Principles: Single-File Compilation & Execution** (as a foundation).
2.  **Multiple Files in the Same Directory.**
3.  **Multiple Files with Packages & Directories.**
4.  **Packaging with JAR Files.**
5.  **The `java` command's Single-File Source-Code Program Launcher** (relevant for simpler multi-file scenarios in Java 11+).
6.  **Brief Mention of Build Tools** (for larger projects).

---

## Launching Multi-File Source-Code Programs in Java 22

### 1. Basic Principles: Single-File Compilation & Execution

Before diving into multiple files, let's establish the foundation with a single file.

**File: `HelloWorld.java`**

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, Java 22!");
    }
}
```

**Steps:**

1.  **Compile:**
    ```bash
    javac HelloWorld.java
    ```
    This creates `HelloWorld.class` in the same directory.

2.  **Execute:**
    ```bash
    java HelloWorld
    ```

**Output:**

```
Hello, Java 22!
```

---

### 2. Multiple Files in the Same Directory

When you have multiple `.java` files that depend on each other and are located in the same directory, compilation is straightforward.

**Directory Structure:**

```
myprogram/
├── Main.java
└── Greeter.java
```

**Files:**

**`Greeter.java`**
```java
public class Greeter {
    public String getGreeting(String name) {
        return "Hello, " + name + " from Greeter!";
    }
}
```

**`Main.java`**
```java
public class Main {
    public static void main(String[] args) {
        Greeter greeter = new Greeter();
        System.out.println(greeter.getGreeting("World"));
    }
}
```

**Steps:**

1.  **Navigate to the directory:**
    ```bash
    cd myprogram
    ```

2.  **Compile:**
    You can compile them individually, or all at once.
    *   **Individual:**
        ```bash
        javac Greeter.java
        javac Main.java
        ```
    *   **All at once (recommended for same directory):**
        ```bash
        javac *.java
        # OR
        javac Main.java Greeter.java
        ```
    This will create `Greeter.class` and `Main.class` in the `myprogram` directory.

3.  **Execute:**
    Run the class containing the `main` method.
    ```bash
    java Main
    ```

**Output:**

```
Hello, World from Greeter!
```

---

### 3. Multiple Files with Packages & Directories

For any non-trivial Java application, you'll organize your code into packages, which map to directory structures. This requires using the `javac -d` and `java -cp` (or `--class-path`) options.

**Desired Directory Structure:**

```
myproject/
├── src/
│   ├── com/
│   │   ├── example/
│   │   │   ├── app/
│   │   │   │   └── Main.java
│   │   │   └── util/
│   │   │       └── StringUtils.java
└── bin/ (This directory will be created by compilation for compiled .class files)
```

**Files:**

**`src/com/example/util/StringUtils.java`**
```java
package com.example.util;

public class StringUtils {
    public static String capitalize(String text) {
        if (text == null || text.isEmpty()) {
            return text;
        }
        return Character.toUpperCase(text.charAt(0)) + text.substring(1).toLowerCase();
    }
}
```

**`src/com/example/app/Main.java`**
```java
package com.example.app;

import com.example.util.StringUtils;

public class Main {
    public static void main(String[] args) {
        String original = "hello java world";
        String capitalized = StringUtils.capitalize(original);
        System.out.println("Original: " + original);
        System.out.println("Capitalized: " + capitalized);
    }
}
```

**Steps:**

1.  **Navigate to the project root:**
    ```bash
    cd myproject
    ```

2.  **Create the source and output directories:**
    ```bash
    mkdir -p src/com/example/app
    mkdir -p src/com/example/util
    mkdir bin
    ```
    Then place the `.java` files in their respective `src` subdirectories.

3.  **Compile:**
    Use `javac -d <output_directory> <source_files>`. The `-d` flag tells `javac` where to place the compiled `.class` files, recreating the package structure under that directory.

    ```bash
    javac -d bin src/com/example/app/Main.java src/com/example/util/StringUtils.java
    ```
    *Alternatively, to compile all files under `src` that match the package structure:*
    ```bash
    javac -d bin src/com/example/app/*.java src/com/example/util/*.java
    # Or for more complex projects, you might use -sourcepath:
    # javac -d bin -sourcepath src src/com/example/app/Main.java
    ```

    After compilation, your `myproject` directory will look like this:

    ```
    myproject/
    ├── src/
    │   ├── com/
    │   │   ├── example/
    │   │   │   ├── app/
    │   │   │   │   └── Main.java
    │   │   │   └── util/
    │   │   │       └── StringUtils.java
    └── bin/
        └── com/
            └── example/
                ├── app/
                │   └── Main.class
                └── util/
                    └── StringUtils.class
    ```

4.  **Execute:**
    Use `java -cp <classpath> <main_class_fully_qualified_name>`. The `-cp` (or `--class-path`) flag tells the Java Virtual Machine (JVM) where to look for `.class` files. In this case, it's our `bin` directory. You must specify the *fully qualified name* of your main class (including its package).

    ```bash
    java -cp bin com.example.app.Main
    ```

**Output:**

```
Original: hello java world
Capitalized: Hello java world
```

**Explanation of Flags:**
*   `-d <directory>`: Specifies the root directory where the compiler should place the generated `.class` files. It will create the necessary package subdirectories within this root.
*   `-cp <path>` / `--class-path <path>`: Specifies the classpath, which is a list of directories or JAR files where the JVM should search for `.class` files and resources. Multiple paths can be separated by a colon (`:`) on Unix/Linux/macOS or a semicolon (`;`) on Windows.

---

### 4. Packaging with JAR Files

For deployment or easier distribution, you can package your compiled `.class` files into a Java Archive (JAR) file. A JAR file is essentially a ZIP file containing compiled Java bytecode and other resources.

**Prerequisite:** You have compiled your classes into the `bin` directory as shown in Section 3.

**Steps:**

1.  **Create a Manifest File (Optional but Recommended for Executable JARs):**
    A `MANIFEST.MF` file within the JAR specifies metadata, including the `Main-Class` which allows the JAR to be executed directly using `java -jar`.

    Create a file named `MANIFEST.MF` in your `myproject` directory (or a `META-INF` subdirectory).

    **`MANIFEST.MF`**
    ```
    Manifest-Version: 1.0
    Main-Class: com.example.app.Main
    ```
    *   **Important:** Ensure there is a newline character at the end of the `Main-Class` line.

2.  **Create the JAR:**
    Use the `jar` command to archive the contents of your `bin` directory.

    ```bash
    # From the myproject directory
    jar cvfm myapp.jar MANIFEST.MF -C bin .
    ```
    *   `c`: create new archive
    *   `v`: generate verbose output
    *   `f`: specify archive file name
    *   `m`: include manifest file (here, `MANIFEST.MF`)
    *   `myapp.jar`: the name of the JAR file to create
    *   `MANIFEST.MF`: the manifest file to include
    *   `-C bin .`: change directory to `bin` before adding files. The `.` means "add all contents of the current directory (`bin`)". This ensures that the `com` directory (and thus the package structure) is at the root of the JAR.

    This command will create `myapp.jar` in your `myproject` directory.

3.  **Execute the JAR:**
    ```bash
    java -jar myapp.jar
    ```

**Output:**

```
Original: hello java world
Capitalized: Hello java world
```

---

### 5. The `java` command's Single-File Source-Code Program Launcher (Java 11+ / Java 22 Context)

Introduced in Java 11 (JEP 330), this feature allows you to directly run a `.java` source file without explicit `javac` compilation. While primarily designed for single-file scripts, it *can* resolve other classes in the *same directory*.

**Directory Structure:**

```
simplescript/
├── MainScript.java
└── HelperClass.java
```

**Files:**

**`HelperClass.java`**
```java
public class HelperClass {
    public String getData() {
        return "Data from HelperClass.";
    }
}
```

**`MainScript.java`**
```java
// No package declaration needed for this simple use case
public class MainScript {
    public static void main(String[] args) {
        HelperClass helper = new HelperClass();
        System.out.println("Running MainScript...");
        System.out.println(helper.getData());
    }
}
```

**Steps:**

1.  **Navigate to the directory:**
    ```bash
    cd simplescript
    ```

2.  **Execute directly:**
    ```bash
    java MainScript.java
    ```
    The `java` launcher will implicitly compile `MainScript.java` and `HelperClass.java` (if `HelperClass` is used by `MainScript` and found in the same directory), then run `MainScript`. It temporarily compiles the `.java` files into memory or a temporary directory.

**Output:**

```
Running MainScript...
Data from HelperClass.
```

**Limitations:**
*   This approach is best for simple scripts or small projects without complex package structures.
*   It does not automatically resolve classes in different directories or within complex package hierarchies without explicit `--source-path` arguments, which makes it less suitable for typical multi-package applications.
*   It's not a replacement for `javac` and explicit classpaths for larger, structured projects.

---

### 6. Beyond `javac`/`java`: Build Tools (Brief Mention)

For professional, large-scale Java projects, directly using `javac` and `java` commands becomes cumbersome due to:
*   **Dependency Management:** Projects often rely on external libraries (JARs). Managing these manually is prone to errors.
*   **Complex Build Processes:** Tasks like running tests, generating documentation, packaging different kinds of artifacts (WARs, EARs), and deploying.
*   **Project Standardization:** Ensuring consistent builds across different development environments.

This is where **Build Automation Tools** come into play:

*   **Apache Maven:** A widely used tool that uses a Project Object Model (POM) in XML to describe the project, its dependencies, and the build lifecycle.
*   **Gradle:** A newer, more flexible build automation system that uses a Groovy or Kotlin DSL (Domain Specific Language) for build scripts.

These tools handle compilation, dependency resolution, testing, packaging, and more, significantly simplifying the development workflow for multi-file and multi-module projects. While they abstract away the direct `javac` and `java` calls, understanding the underlying principles explained above remains valuable.