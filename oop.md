# Object-Oriented Programming (OOP) in Java

## Introduction to OOP

Object-Oriented Programming (OOP) is a programming paradigm that organizes software design around data, or objects, rather than functions and logic. It's a way of structuring programs into "objects" that combine data and behavior.

**Why OOP?**
*   **Modularity:** Breaking down software into smaller, manageable modules (objects).
*   **Reusability:** Objects or classes can be reused in different parts of the program or in different projects.
*   **Maintainability:** Easier to debug, update, and manage complex codebases.
*   **Extensibility:** New features can be added without affecting existing functionality.
*   **Real-world Modeling:** OOP concepts often map well to real-world entities and their interactions.

Java is a fundamentally object-oriented language, meaning almost everything you do in Java involves classes and objects.

## Core Concepts of OOP in Java

The four pillars of OOP are:

1.  **Encapsulation**
2.  **Inheritance**
3.  **Polymorphism**
4.  **Abstraction**

Let's also start with the fundamental building blocks: **Classes and Objects**.

---

### 1. Classes and Objects

At the heart of OOP are classes and objects.

*   **Class:** A blueprint or a template for creating objects. It defines the properties (data/attributes) and behaviors (methods) that objects of that type will have. A class itself does not occupy memory, it's just a definition.
*   **Object:** An instance of a class. When a class is defined, no memory is allocated until an object of that class is created. An object is a real-world entity that has state and behavior.

**Example:**

```java
// 1. Class Definition
class Car {
    // Properties (Attributes/Data Members)
    String make;
    String model;
    int year;
    String color;
    boolean isEngineOn;

    // Constructor (a special method to initialize objects)
    public Car(String make, String model, int year, String color) {
        this.make = make;
        this.model = model;
        this.year = year;
        this.color = color;
        this.isEngineOn = false; // Initial state
    }

    // Behaviors (Methods)
    public void startEngine() {
        if (!isEngineOn) {
            isEngineOn = true;
            System.out.println(make + " " + model + "'s engine started.");
        } else {
            System.out.println(make + " " + model + "'s engine is already on.");
        }
    }

    public void stopEngine() {
        if (isEngineOn) {
            isEngineOn = false;
            System.out.println(make + " " + model + "'s engine stopped.");
        } else {
            System.out.println(make + " " + model + "'s engine is already off.");
        }
    }

    public void displayCarInfo() {
        System.out.println("--- Car Info ---");
        System.out.println("Make: " + make);
        System.out.println("Model: " + model);
        System.out.println("Year: " + year);
        System.out.println("Color: " + color);
        System.out.println("Engine On: " + (isEngineOn ? "Yes" : "No"));
        System.out.println("----------------");
    }
}

// Main class to demonstrate creating and using objects
public class OOPConceptsDemo {
    public static void main(String[] args) {
        // 2. Object Creation (Instantiating the Car class)
        Car myCar = new Car("Toyota", "Camry", 2022, "Blue");
        Car anotherCar = new Car("Honda", "Civic", 2023, "Red");

        // Accessing object properties and calling methods
        myCar.displayCarInfo();
        myCar.startEngine();
        myCar.displayCarInfo();
        myCar.stopEngine();
        myCar.displayCarInfo();

        System.out.println("\n");

        anotherCar.displayCarInfo();
        anotherCar.startEngine();
        anotherCar.startEngine(); // Try starting again
    }
}
```
**Explanation:**
*   The `Car` class is a blueprint. It defines what a `Car` *is* (make, model, year, etc.) and what it *can do* (startEngine, stopEngine, displayInfo).
*   `myCar` and `anotherCar` are objects (instances) of the `Car` class. Each object has its own unique set of property values (e.g., `myCar` is a blue Toyota, `anotherCar` is a red Honda).

---

### 2. Encapsulation

**Definition:** Encapsulation is the bundling of data (attributes) and methods (behaviors) that operate on the data into a single unit (class). It also means restricting direct access to some of an object's components, which is known as **data hiding**.

**How to achieve in Java:**
*   Declare instance variables (attributes) as `private`. This prevents direct access from outside the class.
*   Provide `public` methods (getters and setters) to access and modify these private variables. These methods provide controlled access to the data.

**Benefits:**
*   **Data Integrity:** Prevents unauthorized direct modification of data.
*   **Flexibility:** Allows changes to the internal implementation without affecting external code that uses the class.
*   **Controlled Access:** You can add validation logic inside setters to ensure data is always valid.

**Example:**

```java
class BankAccount {
    // Private attributes - data is encapsulated
    private String accountNumber;
    private double balance;
    private String accountHolderName;

    // Constructor
    public BankAccount(String accountNumber, String accountHolderName, double initialBalance) {
        this.accountNumber = accountNumber;
        this.accountHolderName = accountHolderName;
        // Validate initial balance
        if (initialBalance >= 0) {
            this.balance = initialBalance;
        } else {
            System.out.println("Initial balance cannot be negative. Setting to 0.");
            this.balance = 0;
        }
    }

    // Public Getter methods to read data
    public String getAccountNumber() {
        return accountNumber;
    }

    public String getAccountHolderName() {
        return accountHolderName;
    }

    public double getBalance() {
        return balance;
    }

    // Public Setter methods to modify data (with validation)
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("Deposited: $" + amount + ". New balance: $" + balance);
        } else {
            System.out.println("Deposit amount must be positive.");
        }
    }

    public void withdraw(double amount) {
        if (amount > 0 && balance >= amount) {
            balance -= amount;
            System.out.println("Withdrew: $" + amount + ". New balance: $" + balance);
        } else if (amount <= 0) {
            System.out.println("Withdrawal amount must be positive.");
        } else {
            System.out.println("Insufficient funds. Current balance: $" + balance);
        }
    }
}

public class EncapsulationDemo {
    public static void main(String[] args) {
        BankAccount account1 = new BankAccount("12345", "Alice Smith", 1000.0);

        // Accessing data using getters
        System.out.println("Account Number: " + account1.getAccountNumber());
        System.out.println("Account Holder: " + account1.getAccountHolderName());
        System.out.println("Initial Balance: $" + account1.getBalance());

        // Modifying data using public methods (setters/behaviors)
        account1.deposit(500.0);
        account1.withdraw(200.0);
        account1.withdraw(1500.0); // Attempt to withdraw more than balance
        account1.deposit(-100.0); // Attempt to deposit negative amount

        System.out.println("Final Balance: $" + account1.getBalance());

        // Trying to directly access private variable (will cause compile error)
        // account1.balance = 100000.0; // ERROR: balance has private access
    }
}
```
**Explanation:**
*   The `balance`, `accountNumber`, and `accountHolderName` are `private`, preventing direct manipulation.
*   The `deposit` and `withdraw` methods provide controlled access, ensuring that deposits are positive and withdrawals don't exceed the balance.

---

### 3. Inheritance

**Definition:** Inheritance is a mechanism where one class acquires the properties and behaviors (fields and methods) of another class. It represents an "is-a" relationship (e.g., "A Car *is-a* Vehicle").

**Key Concepts:**
*   **Superclass (Parent/Base Class):** The class whose features are inherited.
*   **Subclass (Child/Derived/Extended Class):** The class that inherits the features.
*   **`extends` keyword:** Used to indicate that a class inherits from another.
*   **`super` keyword:** Used to refer to the superclass's members (constructors, methods, fields).

**Benefits:**
*   **Code Reusability:** Avoids writing the same code repeatedly.
*   **Polymorphism:** Enables run-time polymorphism.
*   **Hierarchy:** Creates a clear hierarchical structure for classes.

**Example:**

```java
// Superclass
class Vehicle {
    protected String brand; // protected allows access within the same package and subclasses
    protected int year;

    public Vehicle(String brand, int year) {
        this.brand = brand;
        this.year = year;
        System.out.println("Vehicle constructor called.");
    }

    public void start() {
        System.out.println(brand + " vehicle is starting.");
    }

    public void stop() {
        System.out.println(brand + " vehicle is stopping.");
    }

    public void displayInfo() {
        System.out.println("Brand: " + brand + ", Year: " + year);
    }
}

// Subclass Car inherits from Vehicle
class Car extends Vehicle {
    private String model;
    private int numberOfDoors;

    public Car(String brand, int year, String model, int numberOfDoors) {
        super(brand, year); // Calls the constructor of the superclass (Vehicle)
        this.model = model;
        this.numberOfDoors = numberOfDoors;
        System.out.println("Car constructor called.");
    }

    // Car-specific method
    public void accelerate() {
        System.out.println(brand + " " + model + " is accelerating.");
    }

    // Overriding the displayInfo method from Vehicle
    @Override // Good practice to use this annotation
    public void displayInfo() {
        super.displayInfo(); // Call superclass's displayInfo first
        System.out.println("Model: " + model + ", Doors: " + numberOfDoors);
    }
}

// Subclass Motorcycle inherits from Vehicle
class Motorcycle extends Vehicle {
    private boolean hasSidecar;

    public Motorcycle(String brand, int year, boolean hasSidecar) {
        super(brand, year);
        this.hasSidecar = hasSidecar;
        System.out.println("Motorcycle constructor called.");
    }

    public void wheelie() {
        System.out.println(brand + " motorcycle is doing a wheelie!");
    }

    @Override
    public void displayInfo() {
        super.displayInfo();
        System.out.println("Has Sidecar: " + (hasSidecar ? "Yes" : "No"));
    }
}

public class InheritanceDemo {
    public static void main(String[] args) {
        Car myCar = new Car("Tesla", 2023, "Model 3", 4);
        System.out.println("\n");
        Motorcycle myBike = new Motorcycle("Harley-Davidson", 2021, false);
        System.out.println("\n");

        myCar.displayInfo(); // Calls overridden method in Car
        myCar.start();       // Inherited from Vehicle
        myCar.accelerate();  // Car-specific method
        myCar.stop();        // Inherited from Vehicle
        System.out.println("\n");

        myBike.displayInfo(); // Calls overridden method in Motorcycle
        myBike.start();       // Inherited from Vehicle
        myBike.wheelie();     // Motorcycle-specific method
        myBike.stop();        // Inherited from Vehicle
    }
}
```
**Explanation:**
*   `Car` and `Motorcycle` are `Vehicle`s, so they inherit `brand`, `year`, `start()`, `stop()`, and `displayInfo()` from `Vehicle`.
*   They also add their own specific attributes (`model`, `numberOfDoors`, `hasSidecar`) and behaviors (`accelerate()`, `wheelie()`).
*   The `displayInfo()` method is **overridden** in both `Car` and `Motorcycle` to provide more specific information, demonstrating polymorphism (runtime).
*   `super(brand, year)` is used in the subclass constructors to call the parent class's constructor and initialize inherited properties.

---

### 4. Polymorphism

**Definition:** Polymorphism literally means "many forms." In OOP, it refers to the ability of an object to take on many forms. It allows you to define one interface or common method and have multiple implementations.

There are two main types of polymorphism in Java:

1.  **Compile-time Polymorphism (Method Overloading):**
    *   Achieved by having multiple methods with the same name in the same class but with different method signatures (different number of parameters, different types of parameters, or different order of parameters).
    *   The compiler decides which method to call based on the arguments provided at compile time.

2.  **Run-time Polymorphism (Method Overriding):**
    *   Achieved when a subclass provides a specific implementation for a method that is already defined in its superclass.
    *   The method to be called is determined at run-time based on the actual object type. This typically involves inheritance and interfaces/abstract classes.

**Example:**

```java
// Compile-time Polymorphism (Method Overloading)
class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public double add(double a, double b) { // Same method name, different parameter types
        return a + b;
    }

    public int add(int a, int b, int c) {   // Same method name, different number of parameters
        return a + b + c;
    }
}

// Run-time Polymorphism (Method Overriding)
class Animal {
    public void makeSound() {
        System.out.println("Animal makes a sound.");
    }
}

class Dog extends Animal {
    @Override // Indicates that this method is intended to override a superclass method
    public void makeSound() {
        System.out.println("Dog barks: Woof! Woof!");
    }
}

class Cat extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Cat meows: Meow!");
    }
}

class Cow extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Cow moos: Moo!");
    }
}

public class PolymorphismDemo {
    public static void main(String[] args) {
        // Compile-time Polymorphism (Method Overloading)
        Calculator calc = new Calculator();
        System.out.println("Sum of two integers: " + calc.add(5, 10));         // Calls add(int, int)
        System.out.println("Sum of two doubles: " + calc.add(5.5, 10.5));      // Calls add(double, double)
        System.out.println("Sum of three integers: " + calc.add(1, 2, 3));    // Calls add(int, int, int)
        System.out.println("\n");

        // Run-time Polymorphism (Method Overriding)
        Animal myAnimal = new Animal();
        Animal myDog = new Dog(); // A Dog object is treated as an Animal reference
        Animal myCat = new Cat(); // A Cat object is treated as an Animal reference
        Animal myCow = new Cow(); // A Cow object is treated as an Animal reference

        myAnimal.makeSound(); // Output: Animal makes a sound.
        myDog.makeSound();    // Output: Dog barks: Woof! Woof! (Dog's method is called)
        myCat.makeSound();    // Output: Cat meows: Meow! (Cat's method is called)
        myCow.makeSound();    // Output: Cow moos: Moo! (Cow's method is called)
        System.out.println("\n");

        // Polymorphic Array/List:
        // An array of Animal references can hold objects of Animal, Dog, Cat, Cow.
        Animal[] farmAnimals = new Animal[4];
        farmAnimals[0] = new Dog();
        farmAnimals[1] = new Cat();
        farmAnimals[2] = new Cow();
        farmAnimals[3] = new Animal(); // Can also hold base type

        System.out.println("Sounds from the farm:");
        for (Animal animal : farmAnimals) {
            animal.makeSound(); // At runtime, the correct makeSound() method is invoked
        }
    }
}
```
**Explanation:**
*   **Overloading:** `Calculator` has three `add` methods. The compiler selects the correct one based on the number and types of arguments you pass.
*   **Overriding:** When `myDog.makeSound()` is called, even though `myDog` is declared as an `Animal` type, the JVM knows it's actually a `Dog` object, so it calls `Dog`'s `makeSound()` method. This is a powerful feature for designing flexible and extensible systems. The `Animal[] farmAnimals` example clearly shows how a single method call (`animal.makeSound()`) behaves differently based on the actual object type at runtime.

---

### 5. Abstraction

**Definition:** Abstraction is the concept of hiding the complex implementation details and showing only the essential features of an object. It focuses on "what" an object does rather than "how" it does it.

**How to achieve in Java:**
*   **Abstract Classes:** Classes that cannot be instantiated directly. They can contain abstract methods (methods declared without an implementation) and concrete methods. Subclasses *must* provide implementations for all abstract methods, or they must also be declared abstract. Declared using the `abstract` keyword.
*   **Interfaces:** A contract that defines a set of methods that a class must implement. Prior to Java 8, interfaces could only have abstract methods. From Java 8 onwards, they can also have default and static methods. A class `implements` an interface.

**Benefits:**
*   **Simplifies Complexity:** Users only interact with the essential features, ignoring unnecessary details.
*   **Enforces Design:** Ensures that subclasses implement specific methods (defined by abstract methods or interfaces).
*   **Flexibility:** Allows for different implementations of the same abstract concept.

**Example (using Abstract Class):**

```java
// Abstract Class
abstract class Shape {
    String name;

    public Shape(String name) {
        this.name = name;
    }

    // Abstract method (no body) - subclasses MUST implement this
    public abstract double getArea();

    // Concrete method (with body) - subclasses inherit this
    public void display() {
        System.out.println("Shape: " + name);
    }
}

// Concrete Subclass inheriting from Shape
class Circle extends Shape {
    private double radius;

    public Circle(String name, double radius) {
        super(name);
        this.radius = radius;
    }

    @Override
    public double getArea() {
        return Math.PI * radius * radius;
    }
}

// Concrete Subclass inheriting from Shape
class Rectangle extends Shape {
    private double width;
    private double height;

    public Rectangle(String name, double width, double height) {
        super(name);
        this.width = width;
        this.height = height;
    }

    @Override
    public double getArea() {
        return width * height;
    }
}

public class AbstractionDemoAbstractClass {
    public static void main(String[] args) {
        // Cannot instantiate an abstract class directly
        // Shape s = new Shape("Generic Shape"); // Compile Error!

        Circle circle = new Circle("My Circle", 5.0);
        Rectangle rectangle = new Rectangle("My Rectangle", 4.0, 6.0);

        // Using polymorphic references
        Shape s1 = circle;
        Shape s2 = rectangle;

        s1.display();
        System.out.println("Area: " + s1.getArea());
        System.out.println("\n");

        s2.display();
        System.out.println("Area: " + s2.getArea());
    }
}
```

**Example (using Interface):**

```java
// Interface
interface Drawable {
    // All methods in an interface are implicitly public and abstract (before Java 8)
    void draw();
    
    // Default method (from Java 8) - provides a default implementation
    default void resize() {
        System.out.println("Resizing the drawable object.");
    }

    // Static method (from Java 8)
    static void showInstructions() {
        System.out.println("To draw, implement the draw() method.");
    }
}

// Class implementing the interface
class Square implements Drawable {
    private double side;

    public Square(double side) {
        this.side = side;
    }

    @Override
    public void draw() {
        System.out.println("Drawing a Square with side " + side);
    }
    // No need to implement resize(), as it has a default implementation
}

// Another class implementing the interface
class Triangle implements Drawable {
    private double base;
    private double height;

    public Triangle(double base, double height) {
        this.base = base;
        this.height = height;
    }

    @Override
    public void draw() {
        System.out.println("Drawing a Triangle with base " + base + " and height " + height);
    }
}

public class AbstractionDemoInterface {
    public static void main(String[] args) {
        Drawable square = new Square(7.0);
        Drawable triangle = new Triangle(5.0, 8.0);

        square.draw();
        square.resize(); // Calls default method
        System.out.println("\n");

        triangle.draw();
        triangle.resize(); // Calls default method
        System.out.println("\n");

        // Calling static method of interface
        Drawable.showInstructions();

        // Using an array of interfaces (polymorphism)
        Drawable[] drawings = new Drawable[2];
        drawings[0] = new Square(10);
        drawings[1] = new Triangle(6, 9);

        System.out.println("\nDrawing all shapes:");
        for (Drawable d : drawings) {
            d.draw();
        }
    }
}
```
**Explanation:**
*   **Abstract Class:** `Shape` defines the common `display()` method and an abstract `getArea()` method. Subclasses like `Circle` and `Rectangle` *must* provide their own implementation for `getArea()` as the concept of area differs for each shape.
*   **Interface:** `Drawable` defines a contract: any class implementing `Drawable` *must* provide a `draw()` method. It doesn't care *how* it's drawn, just that it *can* be drawn. This allows different classes (e.g., `Square`, `Triangle`) to fulfill the same contract in their own way. Interfaces are great for defining capabilities (`can-do` relationship).

---

## Conclusion

Object-Oriented Programming is a powerful paradigm that helps developers create robust, scalable, and maintainable software. By understanding and applying the core principles of Classes & Objects, Encapsulation, Inheritance, Polymorphism, and Abstraction, you can write cleaner, more efficient, and more flexible Java applications that model real-world problems effectively. Mastering these concepts is fundamental to becoming proficient in Java development.