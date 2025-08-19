Multiple inheritance in Java is a topic that often leads to confusion because Java explicitly does *not* support multiple inheritance of *classes*. However, it *does* allow a form of multiple inheritance through **interfaces**.

This guide will explain:
1.  Why Java does not support multiple inheritance of classes (the "Diamond Problem").
2.  How interfaces provide a solution for achieving a form of multiple inheritance.
3.  Key features of interfaces that enable this (especially `default` methods).
4.  Detailed examples with code, input, and output.

---

## Table of Contents

1.  [Understanding Multiple Inheritance](#1-understanding-multiple-inheritance)
2.  [Why Java Does Not Support Multiple Class Inheritance (The Diamond Problem)](#2-why-java-does-not-support-multiple-class-inheritance-the-diamond-problem)
3.  [How Interfaces Enable "Multiple Inheritance" in Java](#3-how-interfaces-enable-multiple-inheritance-in-java)
    *   [Key Features of Interfaces](#key-features-of-interfaces)
    *   [Achieving Multiple Inheritance through Interfaces](#achieving-multiple-inheritance-through-interfaces)
        *   [A. Class Implementing Multiple Interfaces](#a-class-implementing-multiple-interfaces)
        *   [B. Interface Extending Multiple Interfaces](#b-interface-extending-multiple-interfaces)
4.  [Detailed Examples](#4-detailed-examples)
    *   [Example 1: Class Implementing Multiple Interfaces (Type and Behavior Inheritance)](#example-1-class-implementing-multiple-interfaces-type-and-behavior-inheritance)
    *   [Example 2: Interface Extending Multiple Interfaces (Combining Contracts)](#example-2-interface-extending-multiple-interfaces-combining-contracts)
5.  [Conclusion](#5-conclusion)

---

## 1. Understanding Multiple Inheritance

Multiple Inheritance is a feature in some object-oriented programming languages (like C++) where a class can inherit properties and behaviors from more than one parent class. This means a single class can have multiple direct superclasses.

## 2. Why Java Does Not Support Multiple Class Inheritance (The Diamond Problem)

Java designers chose to avoid multiple class inheritance primarily due to the "Diamond Problem" (also known as the "Deadly Diamond of Death") and to keep the language simpler and more robust.

Imagine a scenario where:
*   Class `A` has a method `foo()`.
*   Class `B` extends `A` and overrides `foo()`.
*   Class `C` also extends `A` and overrides `foo()` differently.
*   Now, if class `D` tries to extend both `B` and `C` (multiple class inheritance), which version of `foo()` should `D` inherit? The one from `B` or the one from `C`?

```
      A (foo())
     / \
    B   C
   (foo()) (foo())
    \   /
      D
```

This ambiguity creates complexity, potential bugs, and makes the inheritance hierarchy harder to manage. To avoid this, Java enforces **single class inheritance**, meaning a class can only extend one other class.

## 3. How Interfaces Enable "Multiple Inheritance" in Java

While Java doesn't support multiple class inheritance, it achieves a similar concept using **interfaces**. An interface is a blueprint of a class. It can specify methods that a class must implement, but it doesn't provide the implementation itself (before Java 8).

### Key Features of Interfaces

*   **Abstract Methods (implicitly `public abstract`):** Methods declared without a body. Any class implementing the interface must provide an implementation for these methods.
*   **Constants (implicitly `public static final`):** Variables declared in interfaces are constants.
*   **Default Methods (since Java 8):** Methods with a body. These provide a default implementation that implementing classes can use directly or override. This is crucial for "inheriting" behavior.
*   **Static Methods (since Java 8):** Methods tied to the interface itself, not to implementing objects. They must be called directly on the interface name.
*   **Private Methods (since Java 9):** Helper methods for `default` or `static` methods within the interface, improving code reusability within the interface.

### Achieving Multiple Inheritance through Interfaces

Java allows two main ways to achieve a form of multiple inheritance using interfaces:

#### A. Class Implementing Multiple Interfaces

A Java class can **implement multiple interfaces**. When a class implements an interface, it essentially signs a "contract" to provide implementations for all the abstract methods declared in that interface. By implementing multiple interfaces, a single class can acquire multiple distinct sets of behaviors and types.

*   **Syntax:** `class MyClass implements Interface1, Interface2, Interface3 { ... }`
*   **What it provides:**
    *   **Multiple Type Inheritance:** An object of `MyClass` can be treated as an `Interface1` type, an `Interface2` type, and an `Interface3` type. This is pure polymorphism.
    *   **Multiple Behavior Inheritance (via Default Methods):** Since Java 8, interfaces can contain `default` methods with implementations. When a class implements multiple interfaces, it "inherits" these default behaviors. If there's a conflict (same default method signature in multiple implemented interfaces), the class is *forced* to override that method, resolving the ambiguity cleanly.

#### B. Interface Extending Multiple Interfaces

An interface can **extend multiple other interfaces**. This allows you to combine the contracts of several interfaces into a single new interface. Any class that implements the new, extended interface must then provide implementations for all abstract methods defined in all of its parent interfaces.

*   **Syntax:** `interface CombinedInterface extends InterfaceA, InterfaceB { ... }`
*   **What it provides:**
    *   **Combining Contracts:** A way to group related functionalities without having to duplicate method declarations.
    *   **Hierarchical Structure:** Allows building complex interface hierarchies.

---

## 4. Detailed Examples

Let's illustrate these concepts with code examples.

### Example 1: Class Implementing Multiple Interfaces (Type and Behavior Inheritance)

**Scenario:** We want to model a `Smartphone` that has capabilities of both a `Phone` and a `Camera`.

**`Phone` Interface:** Represents calling and messaging features (some abstract, some default behavior).
**`Camera` Interface:** Represents photo and video features (all abstract for now).
**`Smartphone` Class:** Implements both `Phone` and `Camera`.

```java
// File: Phone.java
public interface Phone {
    void makeCall(String number); // Abstract method
    void receiveCall(String number); // Abstract method

    // Default method (since Java 8) - provides a default implementation
    default void sendSMS(String number, String message) {
        System.out.println("Sending SMS to " + number + ": \"" + message + "\" (via Phone interface default)");
    }
}
```

```java
// File: Camera.java
public interface Camera {
    void takePhoto(); // Abstract method
    void recordVideo(int durationSeconds); // Abstract method

    // Another default method
    default void showPreview() {
        System.out.println("Displaying camera preview (via Camera interface default)");
    }
}
```

```java
// File: Smartphone.java
public class Smartphone implements Phone, Camera {

    private String model;

    public Smartphone(String model) {
        this.model = model;
    }

    // Implementing Phone interface methods
    @Override
    public void makeCall(String number) {
        System.out.println(model + " is calling " + number + "...");
    }

    @Override
    public void receiveCall(String number) {
        System.out.println(model + " is receiving a call from " + number + ".");
    }

    // Optionally overriding the default sendSMS method
    @Override
    public void sendSMS(String number, String message) {
        System.out.println(model + " custom SMS to " + number + ": \"" + message + "\"");
    }

    // Implementing Camera interface methods
    @Override
    public void takePhoto() {
        System.out.println(model + " is taking a photo.");
    }

    @Override
    public void recordVideo(int durationSeconds) {
        System.out.println(model + " is recording a video for " + durationSeconds + " seconds.");
    }

    // Can optionally override showPreview too, but let's use the default for this example.
    // @Override
    // public void showPreview() {
    //     System.out.println(model + " custom preview.");
    // }

    public void displayModel() {
        System.out.println("This is a " + model);
    }

    public static void main(String[] args) {
        System.out.println("--- Smartphone Capabilities ---");
        Smartphone myPhone = new Smartphone("AwesomePhone X");
        myPhone.displayModel();

        // Accessing Phone functionalities
        System.out.println("\n--- Phone Features ---");
        myPhone.makeCall("123-456-7890");
        myPhone.receiveCall("987-654-3210");
        myPhone.sendSMS("555-111-2222", "Hello there!"); // Uses Smartphone's overridden method

        // Accessing Camera functionalities
        System.out.println("\n--- Camera Features ---");
        myPhone.takePhoto();
        myPhone.recordVideo(30);
        myPhone.showPreview(); // Uses Camera interface's default method

        // Polymorphism in action:
        System.out.println("\n--- Polymorphism ---");
        // A Smartphone can be treated as a Phone
        Phone generalPhone = new Smartphone("BasicPhone Y");
        generalPhone.makeCall("111-222-3333");
        generalPhone.sendSMS("444-555-6666", "Another message.");

        // A Smartphone can be treated as a Camera
        Camera generalCamera = new Smartphone("ProCam Z");
        generalCamera.takePhoto();
        generalCamera.showPreview();
    }
}
```

**Compilation and Execution:**

1.  **Save:** Save the code above into three separate files: `Phone.java`, `Camera.java`, and `Smartphone.java`.
2.  **Compile:** Open a terminal or command prompt, navigate to the directory where you saved the files, and compile them:
    ```bash
    javac Phone.java Camera.java Smartphone.java
    ```
3.  **Run:** Execute the `Smartphone` class:
    ```bash
    java Smartphone
    ```

**Output:**

```
--- Smartphone Capabilities ---
This is a AwesomePhone X

--- Phone Features ---
AwesomePhone X is calling 123-456-7890...
AwesomePhone X is receiving a call from 987-654-3210.
AwesomePhone X custom SMS to 555-111-2222: "Hello there!"

--- Camera Features ---
AwesomePhone X is taking a photo.
AwesomePhone X is recording a video for 30 seconds.
Displaying camera preview (via Camera interface default)

--- Polymorphism ---
BasicPhone Y is calling 111-222-3333...
BasicPhone Y custom SMS to 444-555-6666: "Another message."
ProCam Z is taking a photo.
Displaying camera preview (via Camera interface default)
```

**Explanation:**
*   The `Smartphone` class implements both `Phone` and `Camera`. This allows `Smartphone` objects to be used wherever a `Phone` or a `Camera` type is expected, demonstrating multiple type inheritance.
*   `Smartphone` provides implementations for all abstract methods (`makeCall`, `receiveCall`, `takePhoto`, `recordVideo`).
*   It **overrides** the `sendSMS` default method from `Phone`, demonstrating that default methods can be customized.
*   It **uses** the `showPreview` default method from `Camera` without overriding it, showing how default behavior is inherited.
*   This setup avoids the diamond problem because if `Phone` and `Camera` *both* had a default method with the *exact same signature* (e.g., `void display()`), the `Smartphone` class would be *forced* by the compiler to provide its own `display()` implementation, resolving the ambiguity explicitly.

### Example 2: Interface Extending Multiple Interfaces (Combining Contracts)

**Scenario:** We want to define a `SmartDevice` that encompasses the capabilities of both a `Connectable` device and an `Operable` device.

**`Connectable` Interface:** Defines methods for network connectivity.
**`Operable` Interface:** Defines methods for basic power operations.
**`SmartDevice` Interface:** Combines `Connectable` and `Operable`.
**`SmartTV` Class:** Implements `SmartDevice`.

```java
// File: Connectable.java
public interface Connectable {
    void connectToNetwork(String networkName); // Abstract method
    void disconnectFromNetwork(); // Abstract method

    // Default method for quick connection
    default void quickConnect() {
        System.out.println("Attempting quick connection to default network...");
    }
}
```

```java
// File: Operable.java
public interface Operable {
    void powerOn(); // Abstract method
    void powerOff(); // Abstract method

    // Default method for status
    default void checkStatus() {
        System.out.println("Device status: Operational");
    }
}
```

```java
// File: SmartDevice.java
// An interface extending multiple other interfaces
public interface SmartDevice extends Connectable, Operable {
    // Can also add its own abstract or default methods
    void runDiagnostic(); // New abstract method specific to SmartDevice

    default void updateSoftware() {
        System.out.println("Updating software for SmartDevice...");
    }
}
```

```java
// File: SmartTV.java
public class SmartTV implements SmartDevice {

    private String model;
    private boolean isOn;
    private String connectedNetwork;

    public SmartTV(String model) {
        this.model = model;
        this.isOn = false;
        this.connectedNetwork = "None";
    }

    // Implement methods from Connectable
    @Override
    public void connectToNetwork(String networkName) {
        if (isOn) {
            this.connectedNetwork = networkName;
            System.out.println(model + " connected to " + networkName);
        } else {
            System.out.println(model + " cannot connect, TV is off.");
        }
    }

    @Override
    public void disconnectFromNetwork() {
        if (isOn && !connectedNetwork.equals("None")) {
            System.out.println(model + " disconnected from " + connectedNetwork);
            this.connectedNetwork = "None";
        } else {
            System.out.println(model + " not connected to any network.");
        }
    }

    // Implement methods from Operable
    @Override
    public void powerOn() {
        if (!isOn) {
            this.isOn = true;
            System.out.println(model + " is now ON.");
        } else {
            System.out.println(model + " is already ON.");
        }
    }

    @Override
    public void powerOff() {
        if (isOn) {
            this.isOn = false;
            System.out.println(model + " is now OFF.");
            this.connectedNetwork = "None"; // Disconnect on power off
        } else {
            System.out.println(model + " is already OFF.");
        }
    }

    // Implement method from SmartDevice
    @Override
    public void runDiagnostic() {
        System.out.println(model + " running system diagnostics...");
        System.out.println("Current status: " + (isOn ? "On" : "Off") + ", Network: " + connectedNetwork);
    }

    public static void main(String[] args) {
        System.out.println("--- Smart TV Operations ---");
        SmartTV mySmartTV = new SmartTV("LG NanoCell 65");

        // Using Operable functionalities (some implemented, some default)
        mySmartTV.powerOn();
        mySmartTV.checkStatus(); // Default method from Operable

        // Using Connectable functionalities (implemented and default)
        mySmartTV.connectToNetwork("Home_Wifi_5G");
        mySmartTV.quickConnect(); // Default method from Connectable
        mySmartTV.disconnectFromNetwork();

        // Using SmartDevice specific and inherited default functionalities
        mySmartTV.runDiagnostic();
        mySmartTV.updateSoftware(); // Default method from SmartDevice

        mySmartTV.powerOff();
        mySmartTV.connectToNetwork("Office_LAN"); // Fails because TV is off

        System.out.println("\n--- Polymorphism with Combined Interface ---");
        SmartDevice device = new SmartTV("Samsung QLED 55");
        device.powerOn();
        device.connectToNetwork("Guest_Wifi");
        device.runDiagnostic();
        device.updateSoftware();
    }
}
```

**Compilation and Execution:**

1.  **Save:** Save the code above into four separate files: `Connectable.java`, `Operable.java`, `SmartDevice.java`, and `SmartTV.java`.
2.  **Compile:** Open a terminal or command prompt, navigate to the directory where you saved the files, and compile them:
    ```bash
    javac Connectable.java Operable.java SmartDevice.java SmartTV.java
    ```
3.  **Run:** Execute the `SmartTV` class:
    ```bash
    java SmartTV
    ```

**Output:**

```
--- Smart TV Operations ---
LG NanoCell 65 is now ON.
Device status: Operational
LG NanoCell 65 connected to Home_Wifi_5G
Attempting quick connection to default network...
LG NanoCell 65 disconnected from Home_Wifi_5G
LG NanoCell 65 running system diagnostics...
Current status: On, Network: None
Updating software for SmartDevice...
LG NanoCell 65 is now OFF.
LG NanoCell 65 cannot connect, TV is off.

--- Polymorphism with Combined Interface ---
Samsung QLED 55 is now ON.
Samsung QLED 55 connected to Guest_Wifi
Samsung QLED 55 running system diagnostics...
Current status: On, Network: Guest_Wifi
Updating software for SmartDevice...
```

**Explanation:**
*   `SmartDevice` interface extends `Connectable` and `Operable`. This means `SmartDevice` effectively inherits all abstract and default methods from both parent interfaces.
*   The `SmartTV` class then only needs to implement `SmartDevice`, and by doing so, it automatically commits to implementing all abstract methods from `Connectable`, `Operable`, and `SmartDevice` itself.
*   It also gains access to the default methods like `quickConnect()` from `Connectable`, `checkStatus()` from `Operable`, and `updateSoftware()` from `SmartDevice`.
*   This demonstrates how interfaces can be combined to form more complex contracts, which then a single class can implement.

---

## 5. Conclusion

Java achieves a flexible and powerful form of "multiple inheritance" through interfaces, effectively allowing a class to acquire multiple types and inherit default behaviors from different sources without suffering from the ambiguities of the diamond problem that plague traditional multiple class inheritance.

*   **Key takeaway for classes:** A class can `implement` multiple interfaces, thereby acting as multiple types and inheriting multiple sets of behaviors (via default methods).
*   **Key takeaway for interfaces:** An interface can `extend` multiple other interfaces, combining their contracts into a single new interface.

This design choice makes Java robust, avoids complex inheritance hierarchies, and promotes clean API design and polymorphism.