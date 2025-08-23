This document provides a detailed explanation of `Object`, `Class`, `Abstract Class`, and `Interface` in Java, including their definitions, characteristics, use cases, and practical examples with input and output.

---

# Java Concepts: Object, Class, Abstract Class, Interface

## 1. Object

An **Object** is a real-world entity and an instance of a class. It is the fundamental unit of Object-Oriented Programming (OOP) in Java. When a class is defined, no memory is allocated until an object of that class is created.

### Key Characteristics:
*   **State:** Represents the data (values of instance variables) of an object.
*   **Behavior:** Represents the functionality (methods) of an object.
*   **Identity:** A unique name that distinguishes one object from another.

### When to Use:
You create objects when you want to use the blueprint (class) to represent a specific, concrete entity in your program.

### Example: `Dog` Object

Let's define a `Dog` class and then create an object of that class.

**File: `Dog.java`**
```java
// Dog.java
public class Dog {
    // State (instance variables)
    String name;
    String breed;
    int age;

    // Behavior (method)
    public void bark() {
        System.out.println(name + " barks: Woof! Woof!");
    }

    public void eat() {
        System.out.println(name + " is eating.");
    }

    // Constructor to initialize the dog's state
    public Dog(String name, String breed, int age) {
        this.name = name;
        this.breed = breed;
        this.age = age;
    }

    // Method to display dog's details
    public void displayDetails() {
        System.out.println("Name: " + name);
        System.out.println("Breed: " + breed);
        System.out.println("Age: " + age + " years");
    }
}
```

**File: `ObjectExample.java`**
```java
// ObjectExample.java
public class ObjectExample {
    public static void main(String[] args) {
        // Creating an object (instance) of the Dog class
        Dog myDog = new Dog("Buddy", "Golden Retriever", 3);

        System.out.println("--- Dog Object Created ---");
        // Accessing object's state
        System.out.println("My dog's name is: " + myDog.name);
        System.out.println("My dog's breed is: " + myDog.breed);

        // Invoking object's behavior
        myDog.bark();
        myDog.eat();
        myDog.displayDetails();

        System.out.println("\n--- Another Dog Object ---");
        Dog anotherDog = new Dog("Lucy", "Labrador", 5);
        anotherDog.displayDetails();
        anotherDog.bark();
    }
}
```

**Explanation:**
1.  The `Dog` class is a blueprint.
2.  In `ObjectExample.java`, `new Dog("Buddy", "Golden Retriever", 3)` creates an actual `Dog` object named `myDog` in memory, initializing its state (`name`, `breed`, `age`).
3.  We then use the `myDog` object to access its state (`myDog.name`, `myDog.breed`) and invoke its behaviors (`myDog.bark()`, `myDog.eat()`, `myDog.displayDetails()`).
4.  Another object `anotherDog` is created, demonstrating that multiple objects can exist based on the same class blueprint, each with its own state.

**To Compile and Run:**
1.  Save `Dog.java` and `ObjectExample.java` in the same directory.
2.  Open a terminal or command prompt in that directory.
3.  Compile: `javac Dog.java ObjectExample.java`
4.  Run: `java ObjectExample`

**Output:**
```
--- Dog Object Created ---
My dog's name is: Buddy
My dog's breed is: Golden Retriever
Buddy barks: Woof! Woof!
Buddy is eating.
Name: Buddy
Breed: Golden Retriever
Age: 3 years

--- Another Dog Object ---
Name: Lucy
Breed: Labrador
Age: 5 years
Lucy barks: Woof! Woof!
```

---

## 2. Class

A **Class** is a blueprint or a template for creating objects. It defines the structure and behavior that objects of that class will have. It doesn't consume any memory until objects are created from it.

### Key Characteristics:
*   **Blueprint:** Defines the fields (data) and methods (behavior) that objects of that class will possess.
*   **Encapsulation:** Binds data and methods that operate on the data within a single unit.
*   **Declaration:** Declared using the `class` keyword.
*   **No Memory Allocation:** A class itself doesn't occupy memory; objects created from it do.
*   **Constructors:** Special methods used to initialize objects.

### When to Use:
You define a class when you need to model a new type of entity in your program that has specific attributes and actions.

### Example: `Book` Class

**File: `Book.java`**
```java
// Book.java
public class Book {
    // Fields (data/state)
    String title;
    String author;
    int publicationYear;
    boolean isAvailable;

    // Constructor (to initialize objects)
    public Book(String title, String author, int publicationYear) {
        this.title = title;
        this.author = author;
        this.publicationYear = publicationYear;
        this.isAvailable = true; // By default, a new book is available
    }

    // Methods (behavior)
    public void displayBookDetails() {
        System.out.println("Title: " + title);
        System.out.println("Author: " + author);
        System.out.println("Publication Year: " + publicationYear);
        System.out.println("Available: " + (isAvailable ? "Yes" : "No"));
    }

    public void borrowBook() {
        if (isAvailable) {
            isAvailable = false;
            System.out.println("'" + title + "' has been borrowed.");
        } else {
            System.out.println("'" + title + "' is currently not available.");
        }
    }

    public void returnBook() {
        if (!isAvailable) {
            isAvailable = true;
            System.out.println("'" + title + "' has been returned.");
        } else {
            System.out.println("'" + title + "' was already available.");
        }
    }
}
```

**File: `ClassExample.java`**
```java
// ClassExample.java
public class ClassExample {
    public static void main(String[] args) {
        System.out.println("--- Creating Book objects ---");
        // Creating an object of the Book class
        Book book1 = new Book("The Lord of the Rings", "J.R.R. Tolkien", 1954);
        book1.displayBookDetails();

        System.out.println("\n--- Interacting with Book1 ---");
        book1.borrowBook();
        book1.displayBookDetails();
        book1.borrowBook(); // Try to borrow again
        book1.returnBook();
        book1.displayBookDetails();

        System.out.println("\n--- Creating another Book object ---");
        Book book2 = new Book("1984", "George Orwell", 1949);
        book2.displayBookDetails();
    }
}
```

**Explanation:**
1.  The `Book` class defines what a book "is" (its `title`, `author`, `publicationYear`, `isAvailable`) and what it "does" (`displayBookDetails()`, `borrowBook()`, `returnBook()`).
2.  `ClassExample.java` demonstrates how to use this blueprint to create actual `Book` objects (`book1`, `book2`) and interact with them. Each object has its own copy of the fields and can invoke the defined methods.

**To Compile and Run:**
1.  Save `Book.java` and `ClassExample.java` in the same directory.
2.  Open a terminal or command prompt in that directory.
3.  Compile: `javac Book.java ClassExample.java`
4.  Run: `java ClassExample`

**Output:**
```
--- Creating Book objects ---
Title: The Lord of the Rings
Author: J.R.R. Tolkien
Publication Year: 1954
Available: Yes

--- Interacting with Book1 ---
'The Lord of the Rings' has been borrowed.
Title: The Lord of the Rings
Author: J.R.R. Tolkien
Publication Year: 1954
Available: No
'The Lord of the Rings' is currently not available.
'The Lord of the Rings' has been returned.
Title: The Lord of the Rings
Author: J.R.R. Tolkien
Publication Year: 1954
Available: Yes

--- Creating another Book object ---
Title: 1984
Author: George Orwell
Publication Year: 1949
Available: Yes
```

---

## 3. Abstract Class

An **Abstract Class** is a class that cannot be instantiated directly. It's designed to be a base class (a template) for other classes to extend. It can contain both concrete (implemented) methods and abstract (unimplemented) methods.

### Key Characteristics:
*   **`abstract` Keyword:** Must be declared with the `abstract` keyword.
*   **Cannot be Instantiated:** You cannot create objects directly from an abstract class (e.g., `new AbstractClass()` is not allowed).
*   **Abstract Methods:** Can have methods without an implementation (method body). These are also declared with the `abstract` keyword and end with a semicolon.
*   **Concrete Methods:** Can have regular, fully implemented methods.
*   **Constructors:** Can have constructors, which are invoked by its subclasses using `super()`.
*   **Subclass Requirement:** If a class extends an abstract class, it *must* implement all of its abstract methods, or it must also be declared `abstract` itself.

### When to Use:
*   **Define Common Behavior:** When you want to provide a common base for a group of related classes, sharing some implemented methods while forcing others to be implemented by subclasses.
*   **Template Method Pattern:** When you want to define a template of an algorithm in a method, deferring some steps to subclasses.
*   **Partial Implementation:** When you have a class that cannot provide a complete implementation for all of its methods, but you still want to define some default behavior.

### Example: `Vehicle` Abstract Class

**File: `Vehicle.java`**
```java
// Vehicle.java (Abstract Class)
public abstract class Vehicle {
    String brand;
    int year;

    public Vehicle(String brand, int year) {
        this.brand = brand;
        this.year = year;
    }

    // Abstract method (no implementation)
    // Subclasses must provide their own implementation for this.
    public abstract void startEngine();

    // Concrete method (with implementation)
    public void displayInfo() {
        System.out.println("Brand: " + brand);
        System.out.println("Year: " + year);
    }

    public void stopEngine() {
        System.out.println(brand + "'s engine stopped.");
    }
}
```

**File: `Car.java`**
```java
// Car.java (Concrete Subclass)
public class Car extends Vehicle {
    int numberOfDoors;

    public Car(String brand, int year, int numberOfDoors) {
        super(brand, year); // Call abstract class constructor
        this.numberOfDoors = numberOfDoors;
    }

    // Implementing the abstract method from Vehicle
    @Override
    public void startEngine() {
        System.out.println(brand + " car engine started with a key.");
    }

    // Car-specific method
    public void honk() {
        System.out.println("Car honks: Beep beep!");
    }

    @Override
    public void displayInfo() {
        super.displayInfo(); // Call parent's displayInfo
        System.out.println("Number of Doors: " + numberOfDoors);
    }
}
```

**File: `Motorcycle.java`**
```java
// Motorcycle.java (Concrete Subclass)
public class Motorcycle extends Vehicle {
    boolean hasSidecar;

    public Motorcycle(String brand, int year, boolean hasSidecar) {
        super(brand, year); // Call abstract class constructor
        this.hasSidecar = hasSidecar;
    }

    // Implementing the abstract method from Vehicle
    @Override
    public void startEngine() {
        System.out.println(brand + " motorcycle engine started with a kick.");
    }

    // Motorcycle-specific method
    public void wheelie() {
        System.out.println("Motorcycle performs a wheelie!");
    }

    @Override
    public void displayInfo() {
        super.displayInfo(); // Call parent's displayInfo
        System.out.println("Has Sidecar: " + (hasSidecar ? "Yes" : "No"));
    }
}
```

**File: `AbstractClassExample.java`**
```java
// AbstractClassExample.java
public class AbstractClassExample {
    public static void main(String[] args) {
        // Vehicle vehicle = new Vehicle("Generic", 2000); // ERROR: Cannot instantiate abstract class

        System.out.println("--- Working with Car ---");
        Car myCar = new Car("Toyota", 2020, 4);
        myCar.displayInfo();
        myCar.startEngine();
        myCar.honk();
        myCar.stopEngine();

        System.out.println("\n--- Working with Motorcycle ---");
        Motorcycle myMotorcycle = new Motorcycle("Harley-Davidson", 2022, true);
        myMotorcycle.displayInfo();
        myMotorcycle.startEngine();
        myMotorcycle.wheelie();
        myMotorcycle.stopEngine();

        System.out.println("\n--- Polymorphism with Abstract Class ---");
        // An abstract class reference can point to its concrete subclass objects
        Vehicle genericVehicle1 = new Car("Honda", 2018, 2);
        Vehicle genericVehicle2 = new Motorcycle("Ducati", 2023, false);

        genericVehicle1.displayInfo();
        genericVehicle1.startEngine(); // Calls Car's startEngine()
        // genericVehicle1.honk(); // ERROR: Cannot call subclass specific methods on superclass reference
        
        System.out.println("--------------------");
        genericVehicle2.displayInfo();
        genericVehicle2.startEngine(); // Calls Motorcycle's startEngine()
    }
}
```

**Explanation:**
1.  `Vehicle` is an `abstract` class. It defines common properties (`brand`, `year`) and behaviors (`displayInfo()`, `stopEngine()`) for all vehicles.
2.  It also declares an `abstract` method `startEngine()`, meaning every subclass *must* provide its own specific implementation for starting the engine.
3.  `Car` and `Motorcycle` are concrete subclasses that extend `Vehicle`. They *must* implement `startEngine()` and can add their own unique properties and methods (`numberOfDoors`, `honk()` for `Car`; `hasSidecar`, `wheelie()` for `Motorcycle`).
4.  You cannot create an object of `Vehicle` directly, as shown in the commented line.
5.  Polymorphism is demonstrated: a `Vehicle` reference can point to either a `Car` or `Motorcycle` object, and the appropriate `startEngine()` method is invoked at runtime.

**To Compile and Run:**
1.  Save `Vehicle.java`, `Car.java`, `Motorcycle.java`, and `AbstractClassExample.java` in the same directory.
2.  Open a terminal or command prompt in that directory.
3.  Compile: `javac Vehicle.java Car.java Motorcycle.java AbstractClassExample.java`
4.  Run: `java AbstractClassExample`

**Output:**
```
--- Working with Car ---
Brand: Toyota
Year: 2020
Number of Doors: 4
Toyota car engine started with a key.
Car honks: Beep beep!
Toyota's engine stopped.

--- Working with Motorcycle ---
Brand: Harley-Davidson
Year: 2022
Has Sidecar: Yes
Harley-Davidson motorcycle engine started with a kick.
Motorcycle performs a wheelie!
Harley-Davidson's engine stopped.

--- Polymorphism with Abstract Class ---
Brand: Honda
Year: 2018
Number of Doors: 2
Honda car engine started with a key.
--------------------
Brand: Ducati
Year: 2023
Has Sidecar: No
Ducati motorcycle engine started with a kick.
```

---

## 4. Interface

An **Interface** is a blueprint of a class. It can contain method signatures (abstract methods without a body), default methods, static methods, and private methods (from Java 9). It specifies a contract that implementing classes must adhere to.

### Key Characteristics:
*   **`interface` Keyword:** Declared with the `interface` keyword.
*   **No Instantiation:** Cannot be instantiated directly.
*   **Abstract Methods:** Prior to Java 8, all methods were implicitly `public abstract`. From Java 8, interfaces can have `default` and `static` methods with implementations. From Java 9, `private` methods are also allowed.
*   **Fields:** All fields declared in an interface are implicitly `public static final`.
*   **No Constructors:** Interfaces do not have constructors.
*   **Multiple Inheritance:** A class can `implement` multiple interfaces, achieving a form of multiple inheritance of type (and behavior since Java 8 default methods).
*   **Loose Coupling:** Promotes loose coupling between components.

### When to Use:
*   **Define a Contract:** To specify a set of behaviors that a class *must* implement, without dictating *how* those behaviors are implemented.
*   **Achieve Loose Coupling:** When different classes need to interact but you want to decouple them from each other's concrete implementations.
*   **Support Multiple Inheritance of Behavior:** When a class needs to acquire behaviors from multiple sources (via `default` methods).
*   **Callback Mechanisms:** Useful for designing APIs where objects need to be notified of events.

### Example: `Flyable` and `Swimmable` Interfaces

**File: `Flyable.java`**
```java
// Flyable.java (Interface)
public interface Flyable {
    // Methods are implicitly public abstract (prior to Java 8)
    void fly();
    void land();

    // Default method (Java 8+) - provides a default implementation
    default void describeFlight() {
        System.out.println("This object is capable of flying.");
    }
}
```

**File: `Swimmable.java`**
```java
// Swimmable.java (Interface)
public interface Swimmable {
    void swim();
    void dive();
}
```

**File: `Bird.java`**
```java
// Bird.java (Implements Flyable)
public class Bird implements Flyable {
    String name;

    public Bird(String name) {
        this.name = name;
    }

    @Override
    public void fly() {
        System.out.println(name + " is flying high in the sky!");
    }

    @Override
    public void land() {
        System.out.println(name + " gracefully lands on a branch.");
    }

    // Bird-specific method
    public void buildNest() {
        System.out.println(name + " is building a nest.");
    }
}
```

**File: `Fish.java`**
```java
// Fish.java (Implements Swimmable)
public class Fish implements Swimmable {
    String species;

    public Fish(String species) {
        this.species = species;
    }

    @Override
    public void swim() {
        System.out.println(species + " is swimming gracefully in the water.");
    }

    @Override
    public void dive() {
        System.out.println(species + " dives deep into the ocean.");
    }

    // Fish-specific method
    public void layEggs() {
        System.out.println(species + " is laying eggs.");
    }
}
```

**File: `Duck.java`**
```java
// Duck.java (Implements Flyable and Swimmable)
public class Duck implements Flyable, Swimmable {
    String name;

    public Duck(String name) {
        this.name = name;
    }

    @Override
    public void fly() {
        System.out.println(name + " flaps its wings and takes off.");
    }

    @Override
    public void land() {
        System.out.println(name + " lands on water.");
    }

    @Override
    public void swim() {
        System.out.println(name + " paddles its feet and swims.");
    }

    @Override
    public void dive() {
        System.out.println(name + " dives under the water to find food.");
    }

    // Duck-specific method
    public void quack() {
        System.out.println(name + " says: Quack! Quack!");
    }
}
```

**File: `InterfaceExample.java`**
```java
// InterfaceExample.java
public class InterfaceExample {
    public static void main(String[] args) {
        System.out.println("--- Bird Actions ---");
        Bird eagle = new Bird("Eagle");
        eagle.fly();
        eagle.describeFlight(); // Using default method from Flyable
        eagle.land();
        eagle.buildNest();

        System.out.println("\n--- Fish Actions ---");
        Fish salmon = new Fish("Salmon");
        salmon.swim();
        salmon.dive();
        salmon.layEggs();

        System.out.println("\n--- Duck Actions (Multiple Interfaces) ---");
        Duck donald = new Duck("Donald");
        donald.fly();
        donald.swim();
        donald.describeFlight(); // Using default method from Flyable
        donald.dive();
        donald.land();
        donald.quack();

        System.out.println("\n--- Polymorphism with Interfaces ---");
        // An interface reference can point to any object that implements it
        Flyable flyer1 = new Bird("Sparrow");
        Flyable flyer2 = new Duck("Daisy");

        Swimmable swimmer1 = new Fish("Tuna");
        Swimmable swimmer2 = new Duck("Scrooge");

        flyer1.fly();
        flyer2.fly();
        flyer2.describeFlight();

        System.out.println("--------------------");
        swimmer1.swim();
        swimmer2.swim();
        swimmer2.dive();
    }
}
```

**Explanation:**
1.  `Flyable` and `Swimmable` are interfaces defining capabilities. They specify *what* an object can do (`fly`, `land`, `swim`, `dive`), but not *how*. `Flyable` also includes a `default` method `describeFlight()` which provides a common implementation that can be overridden by implementing classes.
2.  `Bird` implements `Flyable`, providing concrete implementations for `fly()` and `land()`.
3.  `Fish` implements `Swimmable`, providing concrete implementations for `swim()` and `dive()`.
4.  `Duck` implements *both* `Flyable` and `Swimmable`, demonstrating how a class can gain behaviors from multiple interfaces.
5.  Polymorphism is shown: an `Flyable` reference can hold a `Bird` or `Duck` object, and a `Swimmable` reference can hold a `Fish` or `Duck` object. When an interface method is called through the reference, the specific implementation of the underlying object is executed.

**To Compile and Run:**
1.  Save `Flyable.java`, `Swimmable.java`, `Bird.java`, `Fish.java`, `Duck.java`, and `InterfaceExample.java` in the same directory.
2.  Open a terminal or command prompt in that directory.
3.  Compile: `javac Flyable.java Swimmable.java Bird.java Fish.java Duck.java InterfaceExample.java`
4.  Run: `java InterfaceExample`

**Output:**
```
--- Bird Actions ---
Eagle is flying high in the sky!
This object is capable of flying.
Eagle gracefully lands on a branch.
Eagle is building a nest.

--- Fish Actions ---
Salmon is swimming gracefully in the water.
Salmon dives deep into the ocean.
Salmon is laying eggs.

--- Duck Actions (Multiple Interfaces) ---
Donald flaps its wings and takes off.
Donald paddles its feet and swims.
This object is capable of flying.
Donald dives under the water to find food.
Donald lands on water.
Donald says: Quack! Quack!

--- Polymorphism with Interfaces ---
Sparrow is flying high in the sky!
Daisy flaps its wings and takes off.
This object is capable of flying.
--------------------
Tuna is swimming gracefully in the water.
Scrooge paddles its feet and swims.
Scrooge dives under the water to find food.
```