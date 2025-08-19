Understanding `Class`, `Abstract Class`, and `Interface` is fundamental to mastering Object-Oriented Programming (OOP) in Java. They are all mechanisms for achieving abstraction, polymorphism, and code organization, but they serve different purposes and have distinct characteristics.

Let's break them down in detail with examples.

---

# Class Vs Abstract Class Vs Interface in Java

## Table of Contents
1.  [Introduction to OOP Concepts](#1-introduction-to-oop-concepts)
2.  [Class](#2-class)
    *   [Definition](#definition)
    *   [Key Characteristics](#key-characteristics)
    *   [When to Use](#when-to-use)
    *   [Example](#example)
3.  [Abstract Class](#3-abstract-class)
    *   [Definition](#definition-1)
    *   [Key Characteristics](#key-characteristics-1)
    *   [When to Use](#when-to-use-1)
    *   [Example](#example-1)
4.  [Interface](#4-interface)
    *   [Definition](#definition-2)
    *   [Key Characteristics](#key-characteristics-2)
    *   [When to Use](#when-to-use-2)
    *   [Example](#example-2)
5.  [Detailed Comparison Table](#5-detailed-comparison-table)
6.  [Conclusion](#6-conclusion)

---

## 1. Introduction to OOP Concepts

Before diving into each, let's briefly touch upon what they help achieve:
*   **Abstraction:** Hiding complex implementation details and showing only the essential features of an object.
*   **Polymorphism:** The ability of an object to take on many forms. A single interface can be used for different data types.
*   **Inheritance:** A mechanism where one class acquires the properties and behaviors of another class.
*   **Encapsulation:** Bundling data (variables) and methods (functions) that operate on the data into a single unit (class).

---

## 2. Class

### Definition
A `class` is a blueprint or a template for creating objects. It defines the data (fields/attributes) and the behavior (methods/functions) that an object of that class will have. It represents a concrete entity or concept.

### Key Characteristics
*   **Instantiable:** You can create objects (instances) directly from a class using the `new` keyword.
*   **Concrete:** Classes typically provide full implementations for all their methods.
*   **Fields and Methods:** Can have variables (data) and methods (behavior).
*   **Constructors:** Can have constructors to initialize objects.
*   **Inheritance:** Can inherit from only one other class (single inheritance in Java) using the `extends` keyword.
*   **Access Modifiers:** Can use `public`, `protected`, `default`, `private` for its members.

### When to Use
*   When you need to define a concrete object with specific states and behaviors that can be directly instantiated.
*   When you want to create a reusable component that groups related data and functions.

### Example

Let's create a simple `Car` class.

**File: `Car.java`**
```java
// Car.java
public class Car {
    // Fields (attributes)
    String make;
    String model;
    int year;
    String color;

    // Constructor
    public Car(String make, String model, int year, String color) {
        this.make = make;
        this.model = model;
        this.year = year;
        this.color = color;
        System.out.println("Car object created: " + this.make + " " + this.model);
    }

    // Method (behavior)
    public void startEngine() {
        System.out.println(make + " " + model + "'s engine started!");
    }

    public void drive() {
        System.out.println(make + " " + model + " is driving...");
    }

    public void displayInfo() {
        System.out.println("--- Car Info ---");
        System.out.println("Make: " + make);
        System.out.println("Model: " + model);
        System.out.println("Year: " + year);
        System.out.println("Color: " + color);
        System.out.println("----------------");
    }

    // Main method to test the Car class
    public static void main(String[] args) {
        // Input: Creating instances of Car and calling their methods
        Car myCar = new Car("Toyota", "Camry", 2020, "Silver");
        myCar.displayInfo();
        myCar.startEngine();
        myCar.drive();

        System.out.println("\n--- Another Car ---");
        Car anotherCar = new Car("Honda", "Civic", 2022, "Blue");
        anotherCar.displayInfo();
        anotherCar.drive();
    }
}
```

**Input (Implicit):**
Compiling and running the `Car.java` file:
```bash
javac Car.java
java Car
```

**Output:**
```
Car object created: Toyota Camry
--- Car Info ---
Make: Toyota
Model: Camry
Year: 2020
Color: Silver
----------------
Toyota Camry's engine started!
Toyota Camry is driving...

--- Another Car ---
Car object created: Honda Civic
--- Car Info ---
Make: Honda
Model: Civic
Year: 2022
Color: Blue
----------------
Honda Civic is driving...
```

---

## 3. Abstract Class

### Definition
An `abstract class` is a class that cannot be instantiated directly. It's designed to be a base class (a superclass) for other classes. It can have both abstract methods (methods declared without an implementation) and concrete methods (methods with an implementation).

### Key Characteristics
*   **`abstract` Keyword:** Must be declared with the `abstract` keyword.
*   **Cannot be Instantiated:** You cannot create objects of an abstract class using `new`.
*   **Partial Implementation:** Can have both `abstract` methods (no body) and concrete methods (with body).
*   **Abstract Methods:** An abstract method is declared using the `abstract` keyword and ends with a semicolon, having no curly braces `{}`. Any class that `extends` an abstract class *must* provide implementations for all its abstract methods, unless the subclass is also declared `abstract`.
*   **Concrete Methods:** Can have regular (non-abstract) methods with full implementations.
*   **Fields and Constructors:** Can have fields (variables) and constructors. Abstract classes can have constructors, which are typically called by the constructors of their subclasses using `super()`.
*   **Inheritance:** Can inherit from only one other class.
*   **Purpose:** To define a common interface and some common default behavior for a family of related classes, forcing subclasses to implement specific details.

### When to Use
*   When you want to provide a common base for related classes, but some behavior needs to be defined differently by each subclass.
*   When you want to enforce a standard set of methods that subclasses must implement, while also providing some default or shared functionality.
*   When you have a hierarchy of classes where some general concepts don't make sense to be fully implemented at the highest level.

### Example

Let's create an `abstract` class `Shape` with a common method `displayInfo` and an `abstract` method `calculateArea`.

**File: `Shape.java` (Abstract Class)**
```java
// Shape.java (Abstract Class)
public abstract class Shape {
    String name;

    public Shape(String name) {
        this.name = name;
    }

    // Abstract method: must be implemented by concrete subclasses
    public abstract double calculateArea();

    // Concrete method: provides default implementation
    public void displayInfo() {
        System.out.println("This is a " + name + ".");
    }

    // Non-abstract method (can also be present)
    public void printWelcomeMessage() {
        System.out.println("Welcome to the Shape calculator!");
    }
}
```

**File: `Circle.java` (Concrete Subclass)**
```java
// Circle.java
public class Circle extends Shape {
    double radius;

    public Circle(double radius) {
        super("Circle"); // Call parent constructor
        this.radius = radius;
    }

    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }

    public void displayCircleDetails() {
        System.out.println("Circle with radius: " + radius);
    }
}
```

**File: `Rectangle.java` (Concrete Subclass)**
```java
// Rectangle.java
public class Rectangle extends Shape {
    double length;
    double width;

    public Rectangle(double length, double width) {
        super("Rectangle"); // Call parent constructor
        this.length = length;
        this.width = width;
    }

    @Override
    public double calculateArea() {
        return length * width;
    }

    public void displayRectangleDetails() {
        System.out.println("Rectangle with length: " + length + ", width: " + width);
    }
}
```

**File: `ShapeDemo.java` (Main Class to test)**
```java
// ShapeDemo.java
public class ShapeDemo {
    public static void main(String[] args) {
        // Input: Creating instances of concrete subclasses and using polymorphism
        // Shape s = new Shape("Generic"); // ERROR: Cannot instantiate abstract class!

        Circle circle = new Circle(5.0);
        circle.printWelcomeMessage(); // Method inherited from abstract class
        circle.displayInfo();         // Method inherited from abstract class
        circle.displayCircleDetails(); // Method specific to Circle
        System.out.println("Area of Circle: " + circle.calculateArea()); // Abstract method implemented

        System.out.println("\n---------------------\n");

        Rectangle rectangle = new Rectangle(4.0, 6.0);
        rectangle.displayInfo();           // Method inherited from abstract class
        rectangle.displayRectangleDetails(); // Method specific to Rectangle
        System.out.println("Area of Rectangle: " + rectangle.calculateArea()); // Abstract method implemented

        System.out.println("\n--- Polymorphism Example ---");
        // We can use the abstract class type to refer to concrete objects
        Shape polyShape1 = new Circle(7.0);
        Shape polyShape2 = new Rectangle(3.0, 8.0);

        System.out.println("Area of polyShape1 (Circle): " + polyShape1.calculateArea());
        System.out.println("Area of polyShape2 (Rectangle): " + polyShape2.calculateArea());
    }
}
```

**Input (Implicit):**
Compile and run the `ShapeDemo.java` file (requires all other .java files in the same directory):
```bash
javac *.java
java ShapeDemo
```

**Output:**
```
Welcome to the Shape calculator!
This is a Circle.
Circle with radius: 5.0
Area of Circle: 78.53981633974483

---------------------

This is a Rectangle.
Rectangle with length: 4.0, width: 6.0
Area of Rectangle: 24.0

--- Polymorphism Example ---
Area of polyShape1 (Circle): 153.93804002589985
Area of polyShape2 (Rectangle): 24.0
```

---

## 4. Interface

### Definition
An `interface` is a blueprint of a class. It contains abstract methods (before Java 8, all methods were implicitly `public abstract`) and constants (`public static final`). It defines a contract for behavior. A class `implements` an interface, thereby agreeing to provide concrete implementations for all the methods declared in the interface.

### Key Characteristics
*   **`interface` Keyword:** Declared with the `interface` keyword.
*   **Cannot be Instantiated:** Like abstract classes, you cannot create objects of an interface.
*   **Pure Abstraction:** Traditionally, all methods were `public abstract` (implicitly). All fields are `public static final` (implicitly).
*   **Java 8+ Features:**
    *   **`default` methods:** Methods with an implementation. Allow adding new methods to interfaces without breaking existing implementing classes.
    *   **`static` methods:** Methods with an implementation that belong to the interface itself, not to any implementing object.
*   **No Constructors:** Interfaces cannot have constructors.
*   **Multiple Inheritance:** A class can implement multiple interfaces, providing a way to achieve "multiple inheritance of type" (though not multiple inheritance of implementation, like C++).
*   **Implementation:** Classes use the `implements` keyword to implement an interface.
*   **Purpose:** To define a contract for behavior that unrelated classes can fulfill, promoting loose coupling and polymorphism.

### When to Use
*   When you want to define a contract for behavior that can be implemented by any class, regardless of its inheritance hierarchy.
*   When you want to achieve complete abstraction.
*   When you need to support multiple inheritance of type (a class needing to exhibit multiple distinct behaviors).
*   When designing APIs where you want to specify a set of operations without dictating the concrete implementation.

### Example

Let's define `Flyable` and `Swimmable` interfaces.

**File: `Flyable.java`**
```java
// Flyable.java (Interface)
public interface Flyable {
    // Methods are implicitly public abstract (before Java 8)
    void fly();

    // Java 8+ feature: default method with implementation
    default void glide() {
        System.out.println("Gliding through the air...");
    }

    // Java 8+ feature: static method
    static void describeFlying() {
        System.out.println("Flying is the act of moving through the air using wings or an engine.");
    }
}
```

**File: `Swimmable.java`**
```java
// Swimmable.java (Interface)
public interface Swimmable {
    void swim();
    void dive(int depth);
}
```

**File: `Duck.java` (Implements multiple interfaces)**
```java
// Duck.java
public class Duck implements Flyable, Swimmable {
    String name;

    public Duck(String name) {
        this.name = name;
    }

    @Override
    public void fly() {
        System.out.println(name + " is flapping its wings and flying!");
    }

    @Override
    public void swim() {
        System.out.println(name + " is paddling its feet and swimming.");
    }

    @Override
    public void dive(int depth) {
        System.out.println(name + " is diving to a depth of " + depth + " meters.");
    }

    // Duck specific method
    public void quack() {
        System.out.println(name + " says Quack!");
    }
}
```

**File: `Aeroplane.java` (Implements a single interface)**
```java
// Aeroplane.java
public class Aeroplane implements Flyable {
    String model;

    public Aeroplane(String model) {
        this.model = model;
    }

    @Override
    public void fly() {
        System.out.println(model + " is taking off and flying high with engines!");
    }

    // Aeroplane specific method
    public void land() {
        System.out.println(model + " is landing safely.");
    }
}
```

**File: `InterfaceDemo.java` (Main Class to test)**
```java
// InterfaceDemo.java
public class InterfaceDemo {
    public static void main(String[] args) {
        // Input: Creating instances and using interface references
        System.out.println("--- Duck Behavior ---");
        Duck myDuck = new Duck("Daffy");
        myDuck.quack();
        myDuck.fly();
        myDuck.glide(); // Inherited default method from Flyable
        myDuck.swim();
        myDuck.dive(2);

        System.out.println("\n--- Aeroplane Behavior ---");
        Aeroplane jet = new Aeroplane("Boeing 747");
        jet.fly();
        jet.glide(); // Inherited default method from Flyable
        jet.land();

        System.out.println("\n--- Polymorphism with Interfaces ---");
        // An object implementing an interface can be referred to by the interface type
        Flyable flyer1 = myDuck; // Daffy the Duck, now referred to as a Flyable
        Flyable flyer2 = jet;    // Boeing 747, referred to as a Flyable

        Swimmable swimmer1 = myDuck; // Daffy the Duck, now referred to as a Swimmable
        // Swimmable swimmer2 = jet; // ERROR: Aeroplane does not implement Swimmable

        System.out.print("Flyer 1: ");
        flyer1.fly();
        System.out.print("Flyer 2: ");
        flyer2.fly();

        System.out.print("Swimmer 1: ");
        swimmer1.swim();

        System.out.println("\n--- Static Interface Method ---");
        Flyable.describeFlying(); // Calling static method directly on interface
    }
}
```

**Input (Implicit):**
Compile and run the `InterfaceDemo.java` file (requires all other .java files in the same directory):
```bash
javac *.java
java InterfaceDemo
```

**Output:**
```
--- Duck Behavior ---
Daffy says Quack!
Daffy is flapping its wings and flying!
Gliding through the air...
Daffy is paddling its feet and swimming.
Daffy is diving to a depth of 2 meters.

--- Aeroplane Behavior ---
Boeing 747 is taking off and flying high with engines!
Gliding through the air...
Boeing 747 is landing safely.

--- Polymorphism with Interfaces ---
Flyer 1: Daffy is flapping its wings and flying!
Flyer 2: Boeing 747 is taking off and flying high with engines!
Swimmer 1: Daffy is paddling its feet and swimming.

--- Static Interface Method ---
Flying is the act of moving through the air using wings or an engine.
```

---

## 5. Detailed Comparison Table

| Feature                 | Class                                | Abstract Class                               | Interface                                    |
| :---------------------- | :----------------------------------- | :------------------------------------------- | :------------------------------------------- |
| **Instantiability**     | Can be instantiated (`new Class()`)  | Cannot be instantiated directly              | Cannot be instantiated directly              |
| **Keyword**             | `class`                              | `abstract class`                             | `interface`                                  |
| **Methods**             | Can have concrete methods only.      | Can have concrete and abstract methods.      | Before Java 8: All methods `public abstract` (implicitly).<br>Java 8+: Can have `public abstract`, `default`, and `static` methods. |
| **Variables/Fields**    | Can have any type of variables.      | Can have any type of variables.              | All variables are `public static final` (implicitly constants). |
| **Constructors**        | Can have constructors.               | Can have constructors (called by subclasses). | Cannot have constructors.                    |
| **Inheritance/Impl.**   | `extends` another class.             | `extends` another class.                     | `implements` one or more interfaces.         |
| **Multiple Inheritance**| No (single inheritance).             | No (single inheritance).                     | Yes (a class can implement multiple interfaces). |
| **Access Modifiers**    | Members can be `public`, `protected`, `default`, `private`. | Members can be `public`, `protected`, `default`, `private`. | Methods are `public` (implicitly). Variables are `public static final` (implicitly). |
| **Implementation**      | Provides full implementation.        | Provides partial implementation.             | Provides contract/specification (no implementation for abstract methods). |
| **Purpose**             | Defines a concrete object.           | Defines a common base for related subclasses; provides partial implementation and enforces a contract. | Defines a contract for behavior; promotes loose coupling and polymorphism across unrelated classes. |
| **Typical Use Case**    | Representing concrete entities (e.g., `Car`, `Student`). | Building a hierarchy where common behavior is defined, but specific details differ (e.g., `Shape`, `Animal`). | Defining capabilities/roles (e.g., `Flyable`, `Runnable`, `Comparable`). |

---

## 6. Conclusion

*   Use a **Class** when you need a concrete blueprint for creating objects that have specific states and behaviors. It represents a "what it is."
*   Use an **Abstract Class** when you have a set of related classes that share common functionality, but also need to implement some specific behaviors differently. It's about "what it is" but allows for some incomplete parts. It's good for code reuse within an inheritance hierarchy.
*   Use an **Interface** when you want to define a contract for behavior that can be implemented by any class, regardless of its position in the inheritance hierarchy. It's about "what it can do." It promotes high flexibility and loose coupling in your design.

In essence, they all contribute to abstraction and polymorphism, but offer different degrees of implementation and flexibility, catering to various design needs in Java.