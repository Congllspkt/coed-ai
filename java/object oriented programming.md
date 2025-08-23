# Object-Oriented Programming (OOP) in Java

Object-Oriented Programming (OOP) is a programming paradigm based on the concept of "objects," which can contain data and code: data in the form of fields (attributes) and code in the form of procedures (methods). Java is one of the most popular object-oriented programming languages.

## 1. Introduction to OOP

### What is OOP?
OOP is a methodology or a paradigm to design a program using classes and objects. It simplifies software development and maintenance by providing a way to model real-world entities into software components.

### Why OOP? (Benefits)
1.  **Modularity:** Objects create self-contained modules, making the system easier to understand, design, and maintain.
2.  **Reusability:** Code defined in a class can be reused across different parts of the program or even in different programs through inheritance.
3.  **Flexibility (Polymorphism):** Allows objects to take on multiple forms, enabling more flexible and extensible code.
4.  **Maintainability:** Easier to debug and update code due to its modular and organized structure.
5.  **Scalability:** Easier to extend the system with new features without significantly altering existing code.
6.  **Security (Encapsulation):** Data hiding helps protect data from unauthorized access, leading to more robust programs.

### Core Concepts (Pillars) of OOP
The four fundamental pillars of OOP are:
1.  **Encapsulation**
2.  **Inheritance**
3.  **Polymorphism**
4.  **Abstraction**

We will explore each of these in detail with Java examples.

---

## 2. Classes and Objects

Before diving into the pillars, let's understand the fundamental building blocks: Classes and Objects.

### Class
A class is a blueprint or a template for creating objects. It defines the structure (fields) and behavior (methods) that all objects of that class will have. A class itself is not an object; it's a definition.

**Syntax:**
````java
class ClassName {
    // Fields (attributes)
    dataType fieldName;

    // Methods (behaviors)
    returnType methodName(parameters) {
        // method body
    }
}
````

### Object
An object is an instance of a class. When a class is defined, no memory is allocated until an object of that class is created. An object is a real-world entity that has state (data stored in fields) and behavior (actions performed by methods).

**Syntax for creating an object:**
````java
ClassName objectName = new ClassName();
````
The `new` keyword is used to create an instance (object) of a class.

### Example: `Car` Class and Objects

Let's define a `Car` class with some fields (make, model, year) and methods (start, stop, accelerate).

**Input (Java Code):**
```java
// Car.java
class Car {
    // Fields (attributes)
    String make;
    String model;
    int year;
    boolean isRunning;

    // Constructor (a special method to initialize objects)
    public Car(String make, String model, int year) {
        this.make = make;
        this.model = model;
        this.year = year;
        this.isRunning = false; // By default, car is not running
    }

    // Methods (behaviors)
    public void start() {
        if (!isRunning) {
            isRunning = true;
            System.out.println(make + " " + model + " started.");
        } else {
            System.out.println(make + " " + model + " is already running.");
        }
    }

    public void stop() {
        if (isRunning) {
            isRunning = false;
            System.out.println(make + " " + model + " stopped.");
        } else {
            System.out.println(make + " " + model + " is already stopped.");
        }
    }

    public void accelerate() {
        if (isRunning) {
            System.out.println(make + " " + model + " is accelerating.");
        } else {
            System.out.println("Cannot accelerate. " + make + " " + model + " is not running.");
        }
    }

    public void displayInfo() {
        System.out.println("Make: " + make + ", Model: " + model + ", Year: " + year + ", Running: " + isRunning);
    }
}

// Main.java (to create and use Car objects)
public class Main {
    public static void main(String[] args) {
        // Creating objects (instances) of the Car class
        Car myCar = new Car("Toyota", "Camry", 2020);
        Car yourCar = new Car("Honda", "Civic", 2018);

        System.out.println("--- My Car ---");
        myCar.displayInfo(); // Initial state
        myCar.start();       // Start my car
        myCar.accelerate();  // Accelerate my car
        myCar.stop();        // Stop my car
        myCar.accelerate();  // Try to accelerate after stopping
        myCar.displayInfo(); // Final state

        System.out.println("\n--- Your Car ---");
        yourCar.displayInfo(); // Initial state
        yourCar.start();       // Start your car
        yourCar.start();       // Try to start again
        yourCar.stop();        // Stop your car
        yourCar.displayInfo(); // Final state
    }
}
```

**Output:**
```
--- My Car ---
Make: Toyota, Model: Camry, Year: 2020, Running: false
Toyota Camry started.
Toyota Camry is accelerating.
Toyota Camry stopped.
Cannot accelerate. Toyota Camry is not running.
Make: Toyota, Model: Camry, Year: 2020, Running: false

--- Your Car ---
Make: Honda, Model: Civic, Year: 2018, Running: false
Honda Civic started.
Honda Civic is already running.
Honda Civic stopped.
Make: Honda, Model: Civic, Year: 2018, Running: false
```

---

## 3. Encapsulation

### Definition
Encapsulation is the mechanism of wrapping the data (variables) and code (methods) together as a single unit. In Java, this is achieved by making the instance variables `private` and providing `public` getter and setter methods to access and modify the variable values.

**Key Benefits:**
*   **Data Hiding:** Prevents direct access to data, protecting it from external misuse.
*   **Control over Data:** Getters and setters provide a controlled way to interact with the object's state, allowing for validation or other logic.
*   **Flexibility:** The internal implementation of a class can be changed without affecting external code that uses the class.

### Access Modifiers
Java uses access modifiers to control the visibility of classes, fields, methods, and constructors:
*   `private`: Accessible only within the defining class. (Ideal for fields in encapsulation)
*   `default` (no keyword): Accessible within the same package.
*   `protected`: Accessible within the same package and by subclasses in other packages.
*   `public`: Accessible from anywhere. (Ideal for getter/setter methods)

### Getters and Setters (Accessor and Mutator Methods)
*   **Getters:** Public methods that return the value of a private field. (e.g., `getMake()`)
*   **Setters:** Public methods that set the value of a private field, often including validation logic. (e.g., `setYear(int newYear)`)

### Example: Encapsulated `Car` Class

Let's modify our `Car` class to encapsulate its fields.

**Input (Java Code):**
```java
// EncapsulatedCar.java
class EncapsulatedCar {
    // Private fields (data hiding)
    private String make;
    private String model;
    private int year;
    private boolean isRunning;
    private int speed; // New field

    // Constructor
    public EncapsulatedCar(String make, String model, int year) {
        this.make = make;
        this.model = model;
        // Basic validation for year
        if (year > 1900 && year <= 2024) { // Assuming current year is 2024
            this.year = year;
        } else {
            System.err.println("Invalid year provided for " + make + " " + model + ". Setting to 2000.");
            this.year = 2000;
        }
        this.isRunning = false;
        this.speed = 0;
    }

    // Public Getter methods
    public String getMake() {
        return make;
    }

    public String getModel() {
        return model;
    }

    public int getYear() {
        return year;
    }

    public boolean isRunning() { // Convention for boolean getters
        return isRunning;
    }

    public int getSpeed() {
        return speed;
    }

    // Public Setter methods (with validation)
    // Note: Make and Model are often set only via constructor for immutability,
    // but demonstrating for completeness.
    public void setMake(String make) {
        if (make != null && !make.trim().isEmpty()) {
            this.make = make;
        } else {
            System.err.println("Make cannot be empty.");
        }
    }

    public void setModel(String model) {
        if (model != null && !model.trim().isEmpty()) {
            this.model = model;
        } else {
            System.err.println("Model cannot be empty.");
        }
    }

    public void setYear(int year) {
        if (year > 1900 && year <= 2024) {
            this.year = year;
        } else {
            System.err.println("Invalid year provided. Year not changed.");
        }
    }

    // Encapsulated methods (behaviors)
    public void start() {
        if (!isRunning) {
            isRunning = true;
            System.out.println(make + " " + model + " started.");
        } else {
            System.out.println(make + " " + model + " is already running.");
        }
    }

    public void stop() {
        if (isRunning) {
            isRunning = false;
            speed = 0; // Reset speed on stop
            System.out.println(make + " " + model + " stopped.");
        } else {
            System.out.println(make + " " + model + " is already stopped.");
        }
    }

    public void accelerate(int increment) {
        if (isRunning) {
            if (increment > 0) {
                speed += increment;
                System.out.println(make + " " + model + " accelerating to " + speed + " mph.");
            } else {
                System.out.println("Acceleration increment must be positive.");
            }
        } else {
            System.out.println("Cannot accelerate. " + make + " " + model + " is not running.");
        }
    }

    public void brake(int decrement) {
        if (isRunning) {
            if (decrement > 0) {
                speed = Math.max(0, speed - decrement); // Speed cannot go below 0
                System.out.println(make + " " + model + " braking to " + speed + " mph.");
            } else {
                System.out.println("Brake decrement must be positive.");
            }
        } else {
            System.out.println("Cannot brake. " + make + " " + model + " is not running.");
        }
    }

    public void displayInfo() {
        System.out.println("Make: " + make + ", Model: " + model + ", Year: " + year + ", Running: " + isRunning + ", Speed: " + speed + " mph");
    }
}

// Main.java
public class MainEncapsulation {
    public static void main(String[] args) {
        EncapsulatedCar myCar = new EncapsulatedCar("Tesla", "Model 3", 2022);

        System.out.println("--- Initial State ---");
        myCar.displayInfo();

        System.out.println("\n--- Attempting direct access (compile-time error if fields were private) ---");
        // myCar.make = "Ford"; // This would cause a compile-time error if 'make' is private

        System.out.println("\n--- Using Getters ---");
        System.out.println("My car's model: " + myCar.getModel());
        System.out.println("Is my car running? " + myCar.isRunning());

        System.out.println("\n--- Using Setters and Methods ---");
        myCar.start();
        myCar.accelerate(50);
        myCar.brake(20);
        myCar.setYear(2025); // Attempt to set an invalid year
        myCar.setYear(2023); // Set a valid year
        myCar.setModel(""); // Attempt to set an invalid model

        System.out.println("\n--- Final State ---");
        myCar.displayInfo();
        myCar.stop();
    }
}
```

**Output:**
```
--- Initial State ---
Make: Tesla, Model: Model 3, Year: 2022, Running: false, Speed: 0 mph

--- Attempting direct access (compile-time error if fields were private) ---

--- Using Getters ---
My car's model: Model 3
Is my car running? false

--- Using Setters and Methods ---
Tesla Model 3 started.
Tesla Model 3 accelerating to 50 mph.
Tesla Model 3 braking to 30 mph.
Invalid year provided. Year not changed.
Model cannot be empty.

--- Final State ---
Make: Tesla, Model: Model 3, Year: 2023, Running: true, Speed: 30 mph
Tesla Model 3 stopped.
```
Notice how the `year` and `model` fields were not changed by invalid `setYear` and `setModel` calls, demonstrating the control encapsulation provides.

---

## 4. Inheritance

### Definition
Inheritance is a mechanism where one class acquires the properties (fields) and behaviors (methods) of another class. It promotes code reusability and establishes an "is-a" relationship between classes.
*   **Superclass (Parent Class):** The class being inherited from.
*   **Subclass (Child Class):** The class that inherits from another class.

**Keywords:**
*   `extends`: Used by a subclass to inherit from a superclass.

**Syntax:**
````java
class SubclassName extends SuperclassName {
    // new fields and methods specific to SubclassName
}
````

### `super` Keyword
The `super` keyword refers to the immediate parent class object. It can be used to:
1.  Call the parent class's constructor (`super(...)`). Must be the first statement in the child constructor.
2.  Access parent class's methods (`super.methodName()`).
3.  Access parent class's fields (`super.fieldName`).

### Method Overriding
When a subclass provides a specific implementation for a method that is already defined in its superclass, it is called method overriding. The method signature (name, return type, parameters) must be the same. The `@Override` annotation is optional but recommended for clarity and compile-time checks.

### Example: `Vehicle` and `Car`, `Motorcycle`

Let's create a `Vehicle` superclass and two subclasses: `Car` and `Motorcycle`.

**Input (Java Code):**
```java
// Vehicle.java (Superclass)
class Vehicle {
    protected String brand;
    protected String fuelType;
    protected int topSpeed;

    public Vehicle(String brand, String fuelType, int topSpeed) {
        this.brand = brand;
        this.fuelType = fuelType;
        this.topSpeed = topSpeed;
        System.out.println("Vehicle constructor called for " + brand);
    }

    public void startEngine() {
        System.out.println(brand + "'s engine started.");
    }

    public void stopEngine() {
        System.out.println(brand + "'s engine stopped.");
    }

    public void displayVehicleInfo() {
        System.out.println("Brand: " + brand + ", Fuel Type: " + fuelType + ", Top Speed: " + topSpeed + " mph");
    }
}

// Car.java (Subclass of Vehicle)
class Car extends Vehicle {
    private int numberOfDoors;
    private String carType; // e.g., Sedan, SUV

    public Car(String brand, String fuelType, int topSpeed, int numberOfDoors, String carType) {
        super(brand, fuelType, topSpeed); // Call to superclass constructor
        this.numberOfDoors = numberOfDoors;
        this.carType = carType;
        System.out.println("Car constructor called for " + brand);
    }

    public void drive() {
        System.out.println("The " + brand + " " + carType + " is driving.");
    }

    @Override // Annotation for clarity and compile-time check
    public void displayVehicleInfo() {
        // Calling superclass method and adding more details
        super.displayVehicleInfo();
        System.out.println("  Doors: " + numberOfDoors + ", Type: " + carType);
    }
}

// Motorcycle.java (Subclass of Vehicle)
class Motorcycle extends Vehicle {
    private boolean hasSidecar;

    public Motorcycle(String brand, String fuelType, int topSpeed, boolean hasSidecar) {
        super(brand, fuelType, topSpeed); // Call to superclass constructor
        this.hasSidecar = hasSidecar;
        System.out.println("Motorcycle constructor called for " + brand);
    }

    public void wheelie() {
        System.out.println("The " + brand + " motorcycle is doing a wheelie!");
    }

    @Override
    public void displayVehicleInfo() {
        super.displayVehicleInfo();
        System.out.println("  Has Sidecar: " + hasSidecar);
    }
}

// Main.java
public class MainInheritance {
    public static void main(String[] args) {
        System.out.println("--- Creating a Car ---");
        Car myCar = new Car("Ford", "Petrol", 220, 4, "Sedan");
        myCar.startEngine();
        myCar.drive();
        myCar.displayVehicleInfo();
        myCar.stopEngine();

        System.out.println("\n--- Creating a Motorcycle ---");
        Motorcycle myMotorcycle = new Motorcycle("Harley-Davidson", "Petrol", 180, true);
        myMotorcycle.startEngine();
        myMotorcycle.wheelie();
        myMotorcycle.displayVehicleInfo();
        myMotorcycle.stopEngine();

        System.out.println("\n--- Creating a generic Vehicle ---");
        Vehicle genericVehicle = new Vehicle("Bicycle", "Human Power", 30);
        genericVehicle.displayVehicleInfo();
        // genericVehicle.drive(); // This would be a compile-time error as drive() is not in Vehicle
    }
}
```

**Output:**
```
--- Creating a Car ---
Vehicle constructor called for Ford
Car constructor called for Ford
Ford's engine started.
The Ford Sedan is driving.
Brand: Ford, Fuel Type: Petrol, Top Speed: 220 mph
  Doors: 4, Type: Sedan
Ford's engine stopped.

--- Creating a Motorcycle ---
Vehicle constructor called for Harley-Davidson
Motorcycle constructor called for Harley-Davidson
Harley-Davidson's engine started.
The Harley-Davidson motorcycle is doing a wheelie!
Brand: Harley-Davidson, Fuel Type: Petrol, Top Speed: 180 mph
  Has Sidecar: true
Harley-Davidson's engine stopped.

--- Creating a generic Vehicle ---
Vehicle constructor called for Bicycle
Brand: Bicycle, Fuel Type: Human Power, Top Speed: 30 mph
```
This example shows how `Car` and `Motorcycle` inherit `startEngine()`, `stopEngine()`, and `displayVehicleInfo()` from `Vehicle`, and also how they override `displayVehicleInfo()` to add their specific details.

---

## 5. Polymorphism

### Definition
Polymorphism means "many forms." In OOP, it refers to the ability of an object to take on many forms. Specifically, it allows objects of different classes to be treated as objects of a common superclass. This is achieved primarily through method overriding.

**Types of Polymorphism:**
1.  **Compile-time Polymorphism (Method Overloading):**
    *   Methods with the same name but different parameters (number, type, or order of parameters) within the *same* class.
    *   The compiler decides which method to call based on the arguments provided.

2.  **Runtime Polymorphism (Method Overriding / Dynamic Method Dispatch):**
    *   A superclass reference variable referring to an object of a subclass.
    *   The method call is resolved at runtime based on the actual object type, not the reference type.

### Upcasting
Assigning a subclass object to a superclass reference variable is called upcasting. It's implicit and safe.
`SuperclassType obj = new SubclassType();`

### Example: Runtime Polymorphism with `Vehicle` Hierarchy

Using our `Vehicle`, `Car`, and `Motorcycle` classes.

**Input (Java Code):**
```java
// Vehicle, Car, Motorcycle classes are the same as in Inheritance section.
// (Assume they are defined in their respective files or above)

// Main.java
public class MainPolymorphism {
    public static void main(String[] args) {
        // Polymorphic array: A single array can hold objects of different types
        // that share a common superclass (Vehicle).
        Vehicle[] vehicles = new Vehicle[3];

        vehicles[0] = new Car("Toyota", "Hybrid", 190, 4, "Sedan");
        vehicles[1] = new Motorcycle("Ducati", "Petrol", 250, false);
        vehicles[2] = new Car("Tesla", "Electric", 260, 4, "SUV");

        System.out.println("--- Demonstrating Polymorphism ---");
        for (Vehicle v : vehicles) {
            v.startEngine();        // Calls Vehicle's startEngine() (or overridden if it was)
            v.displayVehicleInfo(); // Calls the overridden displayVehicleInfo() based on actual object type
            // v.drive(); // Compile-time error: drive() is specific to Car, not in Vehicle
            // If you want to call subclass-specific methods, you need explicit casting
            if (v instanceof Car) {
                ((Car) v).drive(); // Downcasting to Car to call its specific method
            }
            if (v instanceof Motorcycle) {
                ((Motorcycle) v).wheelie(); // Downcasting to Motorcycle
            }
            v.stopEngine();
            System.out.println("--------------------");
        }

        System.out.println("\n--- Method Overloading (Compile-time Polymorphism) ---");
        // Example of overloading (can be in any class)
        Calculator calc = new Calculator();
        System.out.println("Sum of two ints: " + calc.add(5, 10));
        System.out.println("Sum of three ints: " + calc.add(5, 10, 15));
        System.out.println("Sum of two doubles: " + calc.add(5.5, 10.5));
    }
}

// Calculator.java (for method overloading example)
class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public int add(int a, int b, int c) {
        return a + b + c;
    }

    public double add(double a, double b) {
        return a + b;
    }
}

// Vehicle.java, Car.java, Motorcycle.java (re-include for completeness or assume they are available)
class Vehicle { /* ... as defined in Inheritance ... */
    protected String brand;
    protected String fuelType;
    protected int topSpeed;

    public Vehicle(String brand, String fuelType, int topSpeed) {
        this.brand = brand;
        this.fuelType = fuelType;
        this.topSpeed = topSpeed;
        //System.out.println("Vehicle constructor called for " + brand); // Removed for cleaner output
    }

    public void startEngine() {
        System.out.println(brand + "'s engine started.");
    }

    public void stopEngine() {
        System.out.println(brand + "'s engine stopped.");
    }

    public void displayVehicleInfo() {
        System.out.println("Brand: " + brand + ", Fuel Type: " + fuelType + ", Top Speed: " + topSpeed + " mph");
    }
}

class Car extends Vehicle { /* ... as defined in Inheritance ... */
    private int numberOfDoors;
    private String carType;

    public Car(String brand, String fuelType, int topSpeed, int numberOfDoors, String carType) {
        super(brand, fuelType, topSpeed);
        this.numberOfDoors = numberOfDoors;
        this.carType = carType;
        //System.out.println("Car constructor called for " + brand); // Removed for cleaner output
    }

    public void drive() {
        System.out.println("The " + brand + " " + carType + " is driving.");
    }

    @Override
    public void displayVehicleInfo() {
        super.displayVehicleInfo();
        System.out.println("  Doors: " + numberOfDoors + ", Type: " + carType);
    }
}

class Motorcycle extends Vehicle { /* ... as defined in Inheritance ... */
    private boolean hasSidecar;

    public Motorcycle(String brand, String fuelType, int topSpeed, boolean hasSidecar) {
        super(brand, fuelType, topSpeed);
        this.hasSidecar = hasSidecar;
        //System.out.println("Motorcycle constructor called for " + brand); // Removed for cleaner output
    }

    public void wheelie() {
        System.out.println("The " + brand + " motorcycle is doing a wheelie!");
    }

    @Override
    public void displayVehicleInfo() {
        super.displayVehicleInfo();
        System.out.println("  Has Sidecar: " + hasSidecar);
    }
}
```

**Output:**
```
--- Demonstrating Polymorphism ---
Toyota's engine started.
Brand: Toyota, Fuel Type: Hybrid, Top Speed: 190 mph
  Doors: 4, Type: Sedan
The Toyota Sedan is driving.
Toyota's engine stopped.
--------------------
Ducati's engine started.
Brand: Ducati, Fuel Type: Petrol, Top Speed: 250 mph
  Has Sidecar: false
The Ducati motorcycle is doing a wheelie!
Ducati's engine stopped.
--------------------
Tesla's engine started.
Brand: Tesla, Fuel Type: Electric, Top Speed: 260 mph
  Doors: 4, Type: SUV
The Tesla SUV is driving.
Tesla's engine stopped.
--------------------

--- Method Overloading (Compile-time Polymorphism) ---
Sum of two ints: 15
Sum of three ints: 30
Sum of two doubles: 16.0
```
The example clearly shows how `v.displayVehicleInfo()` behaves differently depending on whether `v` actually holds a `Car` object or a `Motorcycle` object, even though `v` is declared as a `Vehicle`. This is runtime polymorphism. Method overloading is also demonstrated with the `Calculator` class.

---

## 6. Abstraction

### Definition
Abstraction is the concept of hiding the complex implementation details and showing only the essential features of an object. It focuses on "what" an object does rather than "how" it does it. In Java, abstraction is achieved using **abstract classes** and **interfaces**.

### Abstract Classes
*   A class declared with the `abstract` keyword.
*   Cannot be instantiated (you cannot create an object of an abstract class).
*   Can have `abstract` methods (methods without a body) and concrete (non-abstract) methods.
*   If a class has at least one abstract method, it must be declared abstract.
*   A subclass that extends an abstract class must either implement all its abstract methods or declare itself abstract.
*   Can have constructors, fields, and access modifiers like a regular class.

**Syntax:**
````java
abstract class AbstractClassName {
    // fields
    // concrete methods
    // abstract methods
    abstract returnType methodName(parameters);
}
````

### Interfaces
*   A blueprint of a class. It can have abstract methods (implicitly `public abstract` before Java 8) and constants (implicitly `public static final`).
*   Introduced in Java 8, interfaces can also have `default` and `static` methods with implementations.
*   A class can `implement` multiple interfaces, providing a way to achieve multiple inheritances of type (behavior).
*   Cannot be instantiated.
*   A class that implements an interface must provide implementation for all its abstract methods (unless the class itself is abstract).

**Syntax:**
````java
interface InterfaceName {
    // constants (implicitly public static final)
    // abstract methods (implicitly public abstract)
    // default methods (Java 8+)
    // static methods (Java 8+)
}
````

### Difference between Abstract Class and Interface
| Feature           | Abstract Class                                  | Interface                                       |
| :---------------- | :---------------------------------------------- | :---------------------------------------------- |
| **Type of methods** | Can have abstract and non-abstract methods.     | Can only have abstract methods (pre-Java 8). Can have default/static methods (Java 8+). |
| **Variables**     | Can have final, non-final, static, non-static variables. | Has only static and final variables (constants). |
| **Implementation**| Uses `extends` keyword.                         | Uses `implements` keyword.                      |
| **Multiple Inher.**| Single inheritance. (`class A extends B`)       | Multiple inheritance (`class A implements B, C`) |
| **Constructors**  | Can have constructors.                          | Cannot have constructors.                       |
| **Access Modifiers** | Can have private, protected, public.            | All methods are implicitly public (until Java 9 private methods are allowed). |
| **Keywords**      | `abstract class`, `abstract method`             | `interface`                                     |

### Example 1: Abstract Class (`Shape`)

Let's create an abstract `Shape` class with an abstract method `getArea()` and a concrete method `display()`.

**Input (Java Code):**
```java
// Shape.java (Abstract Class)
abstract class Shape {
    protected String name;

    public Shape(String name) {
        this.name = name;
    }

    // Abstract method (no body)
    public abstract double getArea();

    // Concrete method
    public void display() {
        System.out.println("This is a " + name + ".");
    }
}

// Circle.java (Concrete Subclass)
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

// Rectangle.java (Concrete Subclass)
class Rectangle extends Shape {
    private double length;
    private double width;

    public Rectangle(String name, double length, double width) {
        super(name);
        this.length = length;
        this.width = width;
    }

    @Override
    public double getArea() {
        return length * width;
    }
}

// Main.java
public class MainAbstractionAbstractClass {
    public static void main(String[] args) {
        // Shape s = new Shape("Generic"); // Compile-time error: Cannot instantiate abstract class

        Circle circle = new Circle("My Circle", 5.0);
        Rectangle rectangle = new Rectangle("My Rectangle", 4.0, 6.0);

        System.out.println("--- Using Circle Object ---");
        circle.display();
        System.out.println("Area of " + circle.name + ": " + circle.getArea());

        System.out.println("\n--- Using Rectangle Object ---");
        rectangle.display();
        System.out.println("Area of " + rectangle.name + ": " + rectangle.getArea());

        System.out.println("\n--- Polymorphism with Abstract Class ---");
        Shape[] shapes = new Shape[2];
        shapes[0] = circle;
        shapes[1] = rectangle;

        for (Shape s : shapes) {
            System.out.println("Shape: " + s.name + ", Area: " + s.getArea());
        }
    }
}
```

**Output:**
```
--- Using Circle Object ---
This is a My Circle.
Area of My Circle: 78.53981633974483

--- Using Rectangle Object ---
This is a My Rectangle.
Area of My Rectangle: 24.0

--- Polymorphism with Abstract Class ---
Shape: My Circle, Area: 78.53981633974483
Shape: My Rectangle, Area: 24.0
```
This demonstrates how `Shape` enforces that all its concrete subclasses must provide an `getArea()` implementation, while `display()` is shared.

### Example 2: Interface (`Flyable`)

Let's create a `Flyable` interface and implement it with `Bird` and `Airplane` classes.

**Input (Java Code):**
```java
// Flyable.java (Interface)
interface Flyable {
    // implicitly public static final
    int MAX_ALTITUDE = 10000;

    // implicitly public abstract methods
    void fly();
    void land();
    String getFlightStatus();

    // Default method (Java 8+)
    default void takeoff() {
        System.out.println("Taking off...");
    }

    // Static method (Java 8+)
    static void showInstructions() {
        System.out.println("Always check weather before flying.");
    }
}

// Bird.java (Implements Flyable)
class Bird implements Flyable {
    private String species;
    private boolean inFlight;

    public Bird(String species) {
        this.species = species;
        this.inFlight = false;
    }

    @Override
    public void fly() {
        if (!inFlight) {
            inFlight = true;
            System.out.println(species + " is soaring high in the sky!");
        } else {
            System.out.println(species + " is already in flight.");
        }
    }

    @Override
    public void land() {
        if (inFlight) {
            inFlight = false;
            System.out.println(species + " gracefully landed.");
        } else {
            System.out.println(species + " is already on the ground.");
        }
    }

    @Override
    public String getFlightStatus() {
        return species + " is currently " + (inFlight ? "flying" : "on the ground") + ".";
    }

    // Bird-specific method
    public void sing() {
        System.out.println(species + " is singing a beautiful song.");
    }
}

// Airplane.java (Implements Flyable)
class Airplane implements Flyable {
    private String model;
    private int passengers;
    private boolean inFlight;

    public Airplane(String model, int passengers) {
        this.model = model;
        this.passengers = passengers;
        this.inFlight = false;
    }

    @Override
    public void fly() {
        if (!inFlight) {
            inFlight = true;
            System.out.println(model + " with " + passengers + " passengers is taking off.");
        } else {
            System.out.println(model + " is already airborne.");
        }
    }

    @Override
    public void land() {
        if (inFlight) {
            inFlight = false;
            System.out.println(model + " is landing safely.");
        } else {
            System.out.println(model + " is already on the tarmac.");
        }
    }

    @Override
    public String getFlightStatus() {
        return model + " is currently " + (inFlight ? "flying" : "on the ground") + ", carrying " + passengers + " passengers.";
    }

    // Airplane-specific method
    public void engageAutopilot() {
        if (inFlight) {
            System.out.println(model + " autopilot engaged.");
        } else {
            System.out.println(model + " cannot engage autopilot on ground.");
        }
    }
}

// Main.java
public class MainAbstractionInterface {
    public static void main(String[] args) {
        // Accessing interface static method and constant
        Flyable.showInstructions();
        System.out.println("Maximum allowed altitude: " + Flyable.MAX_ALTITUDE + " feet.");

        System.out.println("\n--- Bird Actions ---");
        Bird eagle = new Bird("Eagle");
        eagle.takeoff(); // Calls default method from interface
        eagle.fly();
        eagle.sing();
        System.out.println(eagle.getFlightStatus());
        eagle.land();
        System.out.println(eagle.getFlightStatus());

        System.out.println("\n--- Airplane Actions ---");
        Airplane boeing = new Airplane("Boeing 747", 400);
        boeing.takeoff(); // Calls default method from interface
        boeing.fly();
        boeing.engageAutopilot();
        System.out.println(boeing.getFlightStatus());
        boeing.land();
        System.out.println(boeing.getFlightStatus());

        System.out.println("\n--- Polymorphism with Interface ---");
        // An array of Flyable objects
        Flyable[] flyers = new Flyable[2];
        flyers[0] = eagle;
        flyers[1] = boeing;

        for (Flyable f : flyers) {
            f.fly();
            System.out.println(f.getFlightStatus());
            f.land();
        }
    }
}
```

**Output:**
```
Always check weather before flying.
Maximum allowed altitude: 10000 feet.

--- Bird Actions ---
Taking off...
Eagle is soaring high in the sky!
Eagle is singing a beautiful song.
Eagle is currently flying.
Eagle gracefully landed.
Eagle is currently on the ground.

--- Airplane Actions ---
Taking off...
Boeing 747 with 400 passengers is taking off.
Boeing 747 autopilot engaged.
Boeing 747 is currently flying, carrying 400 passengers.
Boeing 747 is landing safely.
Boeing 747 is currently on the tarmac, carrying 400 passengers.

--- Polymorphism with Interface ---
Eagle is soaring high in the sky!
Eagle is currently flying.
Eagle gracefully landed.
Boeing 747 with 400 passengers is taking off.
Boeing 747 is already airborne.
Boeing 747 is currently flying, carrying 400 passengers.
Boeing 747 is landing safely.
```
This shows how both `Bird` and `Airplane` implement the `Flyable` interface, providing their own specific ways of `fly()`, `land()`, and `getFlightStatus()`, yet they can be treated as `Flyable` objects. The `takeoff()` default method is shared, and `showInstructions()` is a static utility method.

---

## 7. Additional OOP Concepts (Briefly)

### Constructors
*   Special methods used to initialize objects.
*   Have the same name as the class.
*   Do not have a return type.
*   If no constructor is defined, Java provides a default no-argument constructor.
*   **Parameterized Constructor:** Takes arguments to initialize fields. (Seen in all examples above).

### `this` Keyword
*   Refers to the current instance of the class.
*   Used to:
    *   Distinguish instance variables from local variables (e.g., `this.make = make;`).
    *   Call another constructor in the same class (`this(...)`).

### `static` Keyword
*   Belongs to the class itself, not to any specific object instance.
*   **`static` fields:** Shared by all instances of the class.
*   **`static` methods:** Can be called directly on the class name (`ClassName.method()`) without creating an object. They can only access static members.
*   **`static` blocks:** Used for static initialization of a class.

### Packages
*   Used to organize related classes and interfaces into a single unit.
*   Helps in avoiding naming conflicts and controlling access.
*   `package com.mycompany.myapp;`
*   `import com.mycompany.myapp.MyClass;`

### `final` Keyword
*   **`final` variable:** Its value cannot be changed once assigned (constant).
*   **`final` method:** Cannot be overridden by subclasses.
*   **`final` class:** Cannot be inherited by other classes.

---

## 8. Conclusion

Object-Oriented Programming is a powerful paradigm that helps in building robust, scalable, and maintainable software. By understanding and applying the core principles of Classes & Objects, Encapsulation, Inheritance, Polymorphism, and Abstraction, Java developers can create well-structured applications that accurately model real-world problems. Mastering these concepts is fundamental to becoming a proficient Java programmer.