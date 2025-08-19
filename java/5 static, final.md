The `static` and `final` keywords in Java are fundamental concepts that control the behavior and scope of members (variables and methods) and even classes. When combined as `static final`, they create powerful, unchangeable constants.

Let's break them down in detail with examples.

---

# `static` Keyword in Java

The `static` keyword is primarily used for **memory management**. It applies to members (variables and methods) of a class, making them belong to the class itself rather than to any specific instance (object) of that class.

## 1. `static` Variables (Class Variables)

*   **Belong to the class:** There is only one copy of a `static` variable per class, regardless of how many objects are created.
*   **Memory allocation:** `static` variables are stored in a common memory location and are initialized only once when the class is loaded into memory.
*   **Access:** You can access `static` variables directly using the class name (e.g., `ClassName.variableName`) without creating an object. While you *can* access them via an object reference, it's discouraged as it gives a misleading impression of instance ownership.

### Example: `static` Variable

**Filename:** `Car.java`

```java
public class Car {
    // This is a static variable (class variable)
    // It keeps track of the total number of Car objects created across all instances.
    public static int numberOfCars = 0;

    // Instance variable
    String model;

    public Car(String model) {
        this.model = model;
        // Increment the static counter every time a new Car object is created
        numberOfCars++;
        System.out.println("Created a new car: " + model);
    }

    public void displayCarInfo() {
        System.out.println("Model: " + model + ", Total Cars: " + numberOfCars);
    }

    // Main method to demonstrate static variable usage
    public static void main(String[] args) {
        System.out.println("Initial number of cars: " + Car.numberOfCars); // Accessing via class name

        Car ford = new Car("Ford Fiesta");
        Car toyota = new Car("Toyota Camry");
        Car honda = new Car("Honda Civic");

        // All objects share the same static variable 'numberOfCars'
        System.out.println("\nNumber of cars created so far (via object ford): " + ford.numberOfCars);
        System.out.println("Number of cars created so far (via object toyota): " + toyota.numberOfCars);
        System.out.println("Number of cars created so far (via class Car): " + Car.numberOfCars); // Recommended way

        Car nissan = new Car("Nissan Altima");
        System.out.println("Final number of cars: " + Car.numberOfCars);
    }
}
```

**How to Compile and Run:**

```bash
javac Car.java
java Car
```

**Expected Output:**

```
Initial number of cars: 0
Created a new car: Ford Fiesta
Created a new car: Toyota Camry
Created a new car: Honda Civic

Number of cars created so far (via object ford): 3
Number of cars created so far (via object toyota): 3
Number of cars created so far (via class Car): 3
Created a new car: Nissan Altima
Final number of cars: 4
```

**Explanation:**
Notice how `numberOfCars` is shared across all `Car` objects. When one object increments it, the change is visible to all other objects and directly through the `Car` class itself.

## 2. `static` Methods (Class Methods)

*   **Belong to the class:** Like `static` variables, `static` methods belong to the class, not to any specific instance.
*   **Access:** Can be called directly using the class name (e.g., `ClassName.methodName()`) without creating an object.
*   **Limitations:**
    *   A `static` method can only directly call other `static` methods and access `static` variables.
    *   It cannot access non-static (instance) variables or call non-static (instance) methods directly because non-static members require an object instance to exist.
    *   It cannot use the `this` or `super` keywords, as these refer to the current object instance.

### Example: `static` Method

**Filename:** `MathUtility.java`

```java
public class MathUtility {

    // This is a static method (class method)
    // It performs an operation that doesn't depend on any specific object's state.
    public static int add(int a, int b) {
        return a + b;
    }

    // Another static method
    public static double multiply(double a, double b) {
        return a * b;
    }

    // A static variable that might be used by static methods
    public static final double PI = 3.14159;

    // Instance method (requires an object)
    public double calculateCircumference(double radius) {
        // Can access static variable PI
        return 2 * PI * radius;
    }

    public static void main(String[] args) {
        // Calling static methods directly using the class name
        int sum = MathUtility.add(10, 5);
        System.out.println("10 + 5 = " + sum);

        double product = MathUtility.multiply(2.5, 4.0);
        System.out.println("2.5 * 4.0 = " + product);

        // Accessing static variable directly
        System.out.println("Value of PI: " + MathUtility.PI);

        // To call an instance method, you need an object
        MathUtility mu = new MathUtility();
        double circumference = mu.calculateCircumference(5.0);
        System.out.println("Circumference of a circle with radius 5.0: " + circumference);

        // Example of what you CANNOT do:
        // MathUtility.calculateCircumference(10.0); // ERROR: Non-static method cannot be referenced from a static context
    }
}
```

**How to Compile and Run:**

```bash
javac MathUtility.java
java MathUtility
```

**Expected Output:**

```
10 + 5 = 15
2.5 * 4.0 = 10.0
Value of PI: 3.14159
Circumference of a circle with radius 5.0: 31.4159
```

**Explanation:**
`static` methods are perfect for utility functions or operations that don't need access to object-specific data. `Math.max()`, `Integer.parseInt()` are classic examples of `static` methods in Java's standard library.

## 3. `static` Blocks (Static Initializer Blocks)

*   **Purpose:** Used to initialize `static` variables that require more complex logic than a simple one-liner assignment.
*   **Execution:** A `static` block is executed only once, when the class is loaded into memory by the Java Virtual Machine (JVM), and before any `static` methods are called or any objects are created.
*   **Order:** If multiple `static` blocks exist in a class, they are executed in the order they appear.

### Example: `static` Block

**Filename:** `SystemConfig.java`

```java
import java.time.LocalDateTime;

public class SystemConfig {
    public static String OS_NAME;
    public static int PROCESSOR_COUNT;
    public static LocalDateTime BOOT_TIME;

    // Static block to initialize static variables
    static {
        System.out.println("--- Static block executed ---");
        OS_NAME = System.getProperty("os.name");
        PROCESSOR_COUNT = Runtime.getRuntime().availableProcessors();
        BOOT_TIME = LocalDateTime.now();
        System.out.println("--- Static block finished ---");
    }

    public static void displayConfig() {
        System.out.println("\nSystem Configuration:");
        System.out.println("OS Name: " + OS_NAME);
        System.out.println("Processor Count: " + PROCESSOR_COUNT);
        System.out.println("System Boot Time (approx): " + BOOT_TIME);
    }

    public static void main(String[] args) {
        System.out.println("Main method started.");
        // The static block will be executed when SystemConfig class is loaded.
        // This happens before displayConfig() is called or any objects are created.
        SystemConfig.displayConfig();

        System.out.println("Main method finished.");
    }
}
```

**How to Compile and Run:**

```bash
javac SystemConfig.java
java SystemConfig
```

**Expected Output (will vary based on your system and time of execution):**

```
--- Static block executed ---
--- Static block finished ---
Main method started.

System Configuration:
OS Name: Mac OS X
Processor Count: 8
System Boot Time (approx): 2023-10-27T10:30:45.123456789
Main method finished.
```

**Explanation:**
The output clearly shows that the `static` block runs *before* the `main` method even begins, because the `SystemConfig` class is loaded and initialized when the JVM starts executing `java SystemConfig`.

---

# `final` Keyword in Java

The `final` keyword is used to restrict modifications. Its meaning changes slightly depending on whether it's applied to a variable, a method, or a class.

## 1. `final` Variables

*   **Primitive types:** Once a `final` primitive variable is initialized, its value cannot be changed (it becomes a constant).
*   **Reference types:** Once a `final` reference variable is initialized, it cannot be reassigned to point to a different object. However, the *contents* of the object it refers to *can* be modified, unless the object itself is immutable (like `String` or `Integer`).
*   **Initialization:**
    *   **At declaration:** `final int x = 10;`
    *   **In a constructor:** For instance `final` variables, they must be initialized in *all* constructors.
    *   **In an initializer block:** For instance `final` variables, this block runs before constructors.
    *   **In a static block:** For `static final` variables.

### Example: `final` Variables

**Filename:** `FinalVariableDemo.java`

```java
class Student {
    // Instance final variable - must be initialized in constructor or initializer block
    public final int studentId;
    public String name;

    public Student(int studentId, String name) {
        this.studentId = studentId; // Initializing final variable
        this.name = name;
    }

    public void updateName(String newName) {
        this.name = newName; // Allowed: 'name' is not final
    }

    // public void updateStudentId(int newId) {
    //     this.studentId = newId; // ERROR: Cannot assign a value to final variable 'studentId'
    // }

    public void displayStudent() {
        System.out.println("Student ID: " + studentId + ", Name: " + name);
    }
}

public class FinalVariableDemo {

    // Class-level constant (static final) - discussed in next section
    public static final double PI_VALUE = 3.14159;

    public static void main(String[] args) {
        // 1. Final primitive variable
        final int MAX_ATTEMPTS = 3;
        // MAX_ATTEMPTS = 5; // ERROR: Cannot assign a value to final variable 'MAX_ATTEMPTS'
        System.out.println("Max Attempts: " + MAX_ATTEMPTS);

        // 2. Final reference variable (object reference cannot change, but object state can)
        final StringBuilder greeting = new StringBuilder("Hello");
        greeting.append(", World!"); // Allowed: Modifying the object's content
        System.out.println("Greeting: " + greeting);

        // greeting = new StringBuilder("Goodbye"); // ERROR: Cannot assign a value to final variable 'greeting'

        // 3. Final instance variable in a class
        Student s1 = new Student(101, "Alice");
        s1.displayStudent();
        s1.updateName("Alicia"); // Allowed: Changing the state of the object referred to by s1
        s1.displayStudent();

        Student s2 = new Student(102, "Bob");
        // s2.studentId = 103; // ERROR: Cannot assign a value to final variable 'studentId'

        System.out.println("PI Value (from static final): " + FinalVariableDemo.PI_VALUE);
    }
}
```

**How to Compile and Run:**

```bash
javac FinalVariableDemo.java
java FinalVariableDemo
```

**Expected Output:**

```
Max Attempts: 3
Greeting: Hello, World!
Student ID: 101, Name: Alice
Student ID: 101, Name: Alicia
PI Value (from static final): 3.14159
```

**Explanation:**
The example clearly shows that `final` for primitives means the value is fixed, and for references, the reference itself is fixed, but the object it points to can still be mutable (unless the object's class itself is immutable).

## 2. `final` Methods

*   **Restriction:** A `final` method cannot be overridden by subclasses.
*   **Purpose:**
    *   **Security:** To prevent subclasses from altering critical behavior.
    *   **Performance:** The JVM can sometimes optimize calls to `final` methods because it knows they won't be overridden.
    *   **Design:** To ensure a specific implementation detail remains consistent throughout the inheritance hierarchy.

### Example: `final` Method

**Filename:** `ShapeDemo.java`

```java
class Shape {
    public final void draw() {
        System.out.println("Drawing a generic shape.");
    }

    public void calculateArea() {
        System.out.println("Calculating area for a generic shape.");
    }
}

class Circle extends Shape {
    // This will cause a compile-time error!
    // @Override
    // public void draw() {
    //     System.out.println("Drawing a circle.");
    // }

    @Override
    public void calculateArea() {
        System.out.println("Calculating area for a circle.");
    }
}

class Square extends Shape {
    // This will also cause a compile-time error if uncommented
    // @Override
    // public final void draw() { // Still cannot override
    //     System.out.println("Drawing a square.");
    // }

    @Override
    public void calculateArea() {
        System.out.println("Calculating area for a square.");
    }
}

public class ShapeDemo {
    public static void main(String[] args) {
        Shape genericShape = new Shape();
        Circle circle = new Circle();
        Square square = new Square();

        System.out.println("--- Generic Shape ---");
        genericShape.draw();         // Calls Shape's final draw()
        genericShape.calculateArea();

        System.out.println("\n--- Circle ---");
        circle.draw();               // Calls Shape's final draw()
        circle.calculateArea();      // Calls Circle's overridden calculateArea()

        System.out.println("\n--- Square ---");
        square.draw();               // Calls Shape's final draw()
        square.calculateArea();      // Calls Square's overridden calculateArea()
    }
}
```

**How to Compile and Run:**

```bash
javac ShapeDemo.java
java ShapeDemo
```

**Expected Output:**

```
--- Generic Shape ---
Drawing a generic shape.
Calculating area for a generic shape.

--- Circle ---
Drawing a generic shape.
Calculating area for a circle.

--- Square ---
Drawing a generic shape.
Calculating area for a square.
```

**Explanation:**
If you uncomment the `draw()` method in `Circle` or `Square`, the compiler will produce an error like "error: draw() in Circle cannot override draw() in Shape; overridden method is final". This demonstrates that `final` methods cannot be overridden.

## 3. `final` Classes

*   **Restriction:** A `final` class cannot be extended (subclassed).
*   **Purpose:**
    *   **Immutability:** Often used for immutable classes (like `String`, `Integer`, `Double`) to ensure their state cannot be changed or extended in a way that breaks their immutability contract.
    *   **Security:** To prevent malicious subclasses from altering core behavior or creating security vulnerabilities (e.g., `java.lang.System` is final).
    *   **Design:** When a class is explicitly not designed for inheritance.

### Example: `final` Class

**Filename:** `VaultDemo.java`

```java
// This class is final, meaning no other class can extend it.
final class SecretVault {
    private String secretCode;

    public SecretVault(String code) {
        this.secretCode = code;
    }

    public String getSecretCode() {
        // In a real scenario, you'd add security checks before revealing.
        return secretCode;
    }

    public void lockVault() {
        System.out.println("Vault is locked.");
    }
}

// This will cause a compile-time error!
// class CompromisedVault extends SecretVault {
//     public CompromisedVault(String code) {
//         super(code);
//     }
//     // Cannot override or add methods to a final class
// }

public class VaultDemo {
    public static void main(String[] args) {
        SecretVault vault = new SecretVault("ALPHA-OMEGA-777");
        System.out.println("Vault Code: " + vault.getSecretCode());
        vault.lockVault();

        // If you uncomment the `CompromisedVault` class,
        // you will get a compile-time error like:
        // "error: cannot inherit from final SecretVault"
    }
}
```

**How to Compile and Run:**

```bash
javac VaultDemo.java
java VaultDemo
```

**Expected Output:**

```
Vault Code: ALPHA-OMEGA-777
Vault is locked.
```

**Explanation:**
If you uncomment the `CompromisedVault` class, the Java compiler will prevent compilation because `SecretVault` is `final`. This ensures that the behavior of `SecretVault` cannot be altered by subclassing.

---

# `static final` Combination in Java

When `static` and `final` are used together for a variable, it creates a **compile-time constant**.

*   **`static`**: The variable belongs to the class, not to any object. There's only one copy.
*   **`final`**: The variable's value cannot be changed once initialized.

This means a `static final` variable is:
1.  **A constant:** Its value is fixed.
2.  **A class-level member:** It belongs to the class, not an instance.
3.  **Initialized once:** When the class is loaded.

It is common practice to name `static final` variables in `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`, `PI`).

### Example: `static final`

**Filename:** `AppConstants.java`

```java
public class AppConstants {

    // A static final variable - a true constant.
    // Belongs to the class, initialized once, and its value cannot be changed.
    public static final String APPLICATION_NAME = "My Awesome App";
    public static final int MAX_USERS = 1000;
    public static final double VERSION = 1.0;

    // You can also initialize them in a static block if logic is complex
    public static final long START_TIMESTAMP;

    static {
        START_TIMESTAMP = System.currentTimeMillis();
        System.out.println("Application constants initialized. Start Timestamp: " + START_TIMESTAMP);
    }

    public static void main(String[] args) {
        System.out.println("\n--- Retrieving Application Constants ---");

        // Accessing static final variables directly via the class name
        System.out.println("App Name: " + AppConstants.APPLICATION_NAME);
        System.out.println("Max Users: " + AppConstants.MAX_USERS);
        System.out.println("Version: " + AppConstants.VERSION);
        System.out.println("Application Start Timestamp: " + AppConstants.START_TIMESTAMP);

        // Attempting to change them will result in a compile-time error
        // AppConstants.MAX_USERS = 2000; // ERROR: Cannot assign a value to final variable 'MAX_USERS'
    }
}
```

**How to Compile and Run:**

```bash
javac AppConstants.java
java AppConstants
```

**Expected Output (Timestamp will vary):**

```
Application constants initialized. Start Timestamp: 1678889900123

--- Retrieving Application Constants ---
App Name: My Awesome App
Max Users: 1000
Version: 1.0
Application Start Timestamp: 1678889900123
```

**Explanation:**
`static final` variables are perfect for defining global, unchangeable configuration values or mathematical constants within your application. They are loaded once and their values are fixed, making them efficient and reliable.

---

## Conclusion

| Keyword       | Applies to        | Meaning                                                     | Key Behavior                                                              |
| :------------ | :---------------- | :---------------------------------------------------------- | :------------------------------------------------------------------------ |
| `static`      | Variables, Methods, Blocks, Nested Classes | Belongs to the *class*, not an *instance*. Shared among all objects. | One copy in memory. Accessed via `ClassName.member`. `static` methods can only access `static` members. |
| `final`       | Variables, Methods, Classes | Cannot be changed/modified.                                 | **Variable:** Value/reference cannot be reassigned. <br> **Method:** Cannot be overridden by subclasses. <br> **Class:** Cannot be subclassed. |
| `static final`| Variables         | A class-level constant.                                     | One copy in memory. Value fixed. Initialized once when class loaded. Usually `UPPER_SNAKE_CASE`. |

Understanding these keywords is crucial for writing robust, efficient, and well-designed Java applications. They provide powerful mechanisms for controlling scope, mutability, and inheritance.