


Sealed Classes and Interfaces were first previewed in Java 15, refined in Java 16, and **finalized and made a standard feature in Java 17**. They provide a way to restrict which other classes or interfaces can extend or implement them. This allows developers to create a more controlled hierarchy, ensuring that only known and approved subtypes can exist.

---

# Sealed Classes & Interfaces (Java 17)

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Why Use Them?](#2-why-use-them)
3.  [Syntax](#3-syntax)
    *   [Sealed Class Syntax](#sealed-class-syntax)
    *   [Sealed Interface Syntax](#sealed-interface-syntax)
4.  [Rules and Restrictions](#4-rules-and-restrictions)
5.  [Benefits](#5-benefits)
6.  [Examples](#6-examples)
    *   [Example 1: Basic Sealed Class Hierarchy](#example-1-basic-sealed-class-hierarchy)
    *   [Example 2: Sealed Interface with Records and Exhaustive Switch](#example-2-sealed-interface-with-records-and-exhaustive-switch)
    *   [Example 3: Demonstrating `non-sealed` and `sealed` permitting `sealed`](#example-3-demonstrating-non-sealed-and-sealed-permitting-sealed)
7.  [Conclusion](#7-conclusion)

---

## 1. Introduction

Prior to Java 17, when you declared a public class or interface, it was implicitly open for extension or implementation by any other class or interface. While this flexibility is often desired, there are scenarios where you want to explicitly define a closed set of possibilities for inheritance or implementation.

**Sealed classes and interfaces** address this by allowing you to specify exactly which classes or interfaces are permitted to directly extend a sealed class or implement a sealed interface. This means you can declare a hierarchy that is "sealed," meaning it's open for extension only to a pre-defined set of subtypes.

## 2. Why Use Them?

*   **Controlled Evolution:** You can define a specific, finite set of direct subtypes, preventing unintended or unauthorized extensions of your API.
*   **Domain Modeling:** Ideal for modeling domains where you have a fixed and known set of variations for a concept (e.g., different types of `Shape`, `Expression`, `Vehicle`).
*   **Enhanced Type Safety:** The compiler can leverage the sealed hierarchy to perform more exhaustive checks, especially with pattern matching in `switch` expressions.
*   **Improved API Design:** Clearly communicates the intended structure of your type hierarchy to other developers.

## 3. Syntax

To declare a class or interface as sealed, you use the `sealed` modifier, followed by the `permits` clause, which lists the direct permitted subtypes.

### Sealed Class Syntax

```java
// Shape.java
public sealed class Shape permits Circle, Rectangle, Triangle {
    // Common properties/methods for all shapes
    public abstract double area();
    public abstract String describe();
}
```

### Sealed Interface Syntax

```java
// Expression.java
public sealed interface Expression permits Constant, Plus, Minus {
    double evaluate();
}
```

## 4. Rules and Restrictions

1.  **`sealed` Modifier:** The class or interface must be declared with the `sealed` modifier.
2.  **`permits` Clause:** A `permits` clause must follow the `sealed` modifier, listing all direct permitted subtypes.
    *   If the permitted subtypes are in the same source file and in the same package as the sealed type, the `permits` clause can be omitted. However, explicitly listing them is generally good practice for clarity.
3.  **Location of Permitted Subtypes:** All permitted subtypes must reside in the same module as the sealed class/interface, or if in an unnamed module (i.e., not using Java modules), they must be in the same package.
4.  **Declaration of Permitted Subtypes:** Every direct permitted subtype of a sealed class/interface *must* explicitly declare how it will continue the sealing. It has three options:
    *   `final`: Cannot be extended further. This terminates the hierarchy at this point.
    *   `sealed`: Can be extended further, but only by its own explicitly permitted subtypes. It must also use the `permits` clause.
    *   `non-sealed`: Can be extended by any class. This breaks the sealed hierarchy at this point, effectively reverting to the pre-Java 17 behavior for this specific branch.
5.  **Inheritance:** A sealed class cannot be extended by a class not listed in its `permits` clause. Similarly, a sealed interface cannot be implemented by a class or extended by an interface not listed in its `permits` clause.

## 5. Benefits

The primary benefit of sealed types is their integration with **pattern matching for `switch` expressions (Java 17)**. Because the compiler knows the exhaustive set of all direct and indirect permitted subtypes, it can:

*   **Guaranteed Exhaustiveness:** Warn or error if a `switch` expression over a sealed type does not cover all possible subtypes, *without* requiring a `default` clause. This removes the need for defensive `default` cases that might hide missing logic.
*   **Safer Refactoring:** If you add a new permitted subtype to a sealed hierarchy, the compiler will immediately flag all `switch` expressions that operate on that sealed type and don't handle the new subtype.

## 6. Examples

Let's illustrate with some practical examples.

---

### Example 1: Basic Sealed Class Hierarchy

This example shows a `sealed` abstract class `Shape` with three permitted subtypes: `Circle` (final), `Rectangle` (non-sealed), and `Triangle` (sealed itself).

**File Structure:**
```
.
├── src
│   ├── main
│   │   ├── java
│   │   │   ├── com
│   │   │   │   ├── example
│   │   │   │   │   ├── shapes
│   │   │   │   │   │   ├── Circle.java
│   │   │   │   │   │   ├── Rectangle.java
│   │   │   │   │   │   ├── Shape.java
│   │   │   │   │   │   ├── Square.java  (Extends non-sealed Rectangle)
│   │   │   │   │   │   ├── Triangle.java
│   │   │   │   │   │   ├── EquilateralTriangle.java (Extends sealed Triangle)
│   │   │   │   │   │   └── IsoscelesTriangle.java   (Extends sealed Triangle)
│   │   │   │   │   └── Main.java
```

**1. `src/main/java/com/example/shapes/Shape.java`**
```java
package com.example.shapes;

// Shape is sealed, permitting only Circle, Rectangle, and Triangle
public sealed abstract class Shape
    permits Circle, Rectangle, Triangle {

    public abstract double area();
    public abstract String describe();
}
```

**2. `src/main/java/com/example/shapes/Circle.java`**
```java
package com.example.shapes;

// Circle is final, meaning it cannot be extended further.
public final class Circle extends Shape {
    private final double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public double area() {
        return Math.PI * radius * radius;
    }

    @Override
    public String describe() {
        return "This is a Circle with radius " + radius;
    }

    public double getRadius() {
        return radius;
    }
}
```

**3. `src/main/java/com/example/shapes/Rectangle.java`**
```java
package com.example.shapes;

// Rectangle is non-sealed, meaning it can be extended by any class.
// This effectively breaks the 'seal' for this branch.
public non-sealed class Rectangle extends Shape {
    protected final double width;
    protected final double height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public double area() {
        return width * height;
    }

    @Override
    public String describe() {
        return "This is a Rectangle with width " + width + " and height " + height;
    }

    public double getWidth() {
        return width;
    }

    public double getHeight() {
        return height;
    }
}
```

**4. `src/main/java/com/example/shapes/Square.java`**
```java
package com.example.shapes;

// Square can extend Rectangle because Rectangle is non-sealed.
public class Square extends Rectangle {
    public Square(double side) {
        super(side, side); // A square is a rectangle with equal sides
    }

    @Override
    public String describe() {
        return "This is a Square with side " + width;
    }
}
```

**5. `src/main/java/com/example/shapes/Triangle.java`**
```java
package com.example.shapes;

// Triangle is sealed, meaning it can only be extended by its permitted subtypes.
public sealed class Triangle extends Shape
    permits EquilateralTriangle, IsoscelesTriangle {

    protected final double side1;
    protected final double side2;
    protected final double side3;

    public Triangle(double side1, double side2, double side3) {
        this.side1 = side1;
        this.side2 = side2;
        this.side3 = side3;
    }

    @Override
    public double area() {
        // Heron's formula for triangle area
        double s = (side1 + side2 + side3) / 2;
        return Math.sqrt(s * (s - side1) * (s - side2) * (s - side3));
    }

    @Override
    public String describe() {
        return "This is a Triangle with sides " + side1 + ", " + side2 + ", " + side3;
    }
}
```

**6. `src/main/java/com/example/shapes/EquilateralTriangle.java`**
```java
package com.example.shapes;

// EquilateralTriangle is final, extending the sealed Triangle.
public final class EquilateralTriangle extends Triangle {
    public EquilateralTriangle(double side) {
        super(side, side, side);
    }

    @Override
    public String describe() {
        return "This is an Equilateral Triangle with side " + side1;
    }
}
```

**7. `src/main/java/com/example/shapes/IsoscelesTriangle.java`**
```java
package com.example.shapes;

// IsoscelesTriangle is final, extending the sealed Triangle.
public final class IsoscelesTriangle extends Triangle {
    public IsoscelesTriangle(double base, double leg) {
        super(base, leg, leg);
    }

    @Override
    public String describe() {
        return "This is an Isosceles Triangle with base " + side1 + " and legs " + side2;
    }
}
```

**8. `src/main/java/com/example/Main.java`**
```java
package com.example;

import com.example.shapes.*;

public class Main {
    public static void main(String[] args) {
        Shape circle = new Circle(5.0);
        Shape rectangle = new Rectangle(4.0, 6.0);
        Shape square = new Square(5.0); // Allowed because Rectangle is non-sealed
        Shape triangle = new EquilateralTriangle(7.0);
        Shape isoscelesTriangle = new IsoscelesTriangle(5.0, 8.0);

        System.out.println(circle.describe() + ", Area: " + circle.area());
        System.out.println(rectangle.describe() + ", Area: " + rectangle.area());
        System.out.println(square.describe() + ", Area: " + square.area());
        System.out.println(triangle.describe() + ", Area: " + triangle.area());
        System.out.println(isoscelesTriangle.describe() + ", Area: " + isoscelesTriangle.area());

        System.out.println("\n--- Using switch expression with Shape ---");
        printShapeInfo(circle);
        printShapeInfo(square);
        printShapeInfo(isoscelesTriangle);

        // --- Demonstrating compiler error for non-permitted extension (UNCOMMENT TO SEE ERROR) ---
        // class InvalidShape extends Shape { // Compile-time error: sealed class not permitted
        //     @Override public double area() { return 0; }
        //     @Override public String describe() { return "Invalid"; }
        // }
        // Shape invalid = new InvalidShape();
    }

    public static void printShapeInfo(Shape shape) {
        String info = switch (shape) {
            case Circle c -> "It's a Circle with radius " + c.getRadius();
            case Rectangle r -> "It's a " + (r instanceof Square ? "Square" : "Rectangle") + " (W:" + r.getWidth() + ", H:" + r.getHeight() + ")";
            case EquilateralTriangle et -> "It's an Equilateral Triangle with side " + et.side1;
            case IsoscelesTriangle it -> "It's an Isosceles Triangle (Base:" + it.side1 + ", Leg:" + it.side2 + ")";
            // Note: Triangle itself is abstract and sealed, so it won't be instantiated directly.
            // The compiler knows all possible direct subtypes (Circle, Rectangle, Triangle)
            // and then for Triangle, it knows its subtypes (EquilateralTriangle, IsoscelesTriangle).
            // A 'default' case or a catch-all 'Triangle t' is not strictly required IF all concrete sub-types are covered.
            // However, a 'Triangle t' case would handle EquilateralTriangle and IsoscelesTriangle as well.
            // For exhaustive switch, we must cover all concrete leaf nodes, or their non-final parents.
            // Here, we cover Circle, Rectangle (which includes Square), EquilateralTriangle, IsoscelesTriangle.
        };
        System.out.println(info + " - Area: " + shape.area());
    }
}
```

**Compilation and Execution:**

1.  **Compile:** Navigate to the `src/main/java` directory.
    ```bash
    javac --enable-preview --release 17 com/example/shapes/*.java com/example/Main.java
    ```
2.  **Run:** From the `src/main/java` directory.
    ```bash
    java --enable-preview --enable-native-access=ALL-UNNAMED com.example.Main
    ```
    *(Note: `--enable-native-access=ALL-UNNAMED` might be required in some environments if you encounter issues, though less common for sealed classes. `--enable-preview` is essential for features that were in preview, even if finalized, for older JDKs, or if you compile with an older JDK and run with Java 17. For pure Java 17, `java com.example.Main` might suffice if `--enable-preview` was used during `javac` and the feature is finalized.)*

**Expected Output:**

```
This is a Circle with radius 5.0, Area: 78.53981633974483
This is a Rectangle with width 4.0 and height 6.0, Area: 24.0
This is a Square with side 5.0, Area: 25.0
This is an Equilateral Triangle with side 7.0, Area: 21.217621935619424
This is an Isosceles Triangle with base 5.0 and legs 8.0, Area: 19.364916731037085

--- Using switch expression with Shape ---
It's a Circle with radius 5.0 - Area: 78.53981633974483
It's a Square - Area: 25.0
It's an Isosceles Triangle (Base:5.0, Leg:8.0) - Area: 19.364916731037085
```

---

### Example 2: Sealed Interface with Records and Exhaustive Switch

This example demonstrates using a sealed interface with Java Records (which are implicitly final, making them good candidates for `final` permitted subtypes). It also highlights the exhaustive `switch` expression benefit.

**File Structure:**
```
.
├── src
│   ├── main
│   │   ├── java
│   │   │   ├── com
│   │   │   │   ├── example
│   │   │   │   │   ├── expressions
│   │   │   │   │   │   ├── Constant.java
│   │   │   │   │   │   ├── Expression.java
│   │   │   │   │   │   ├── Minus.java
│   │   │   │   │   │   └── Plus.java
│   │   │   │   │   └── Main.java
```

**1. `src/main/java/com/example/expressions/Expression.java`**
```java
package com.example.expressions;

// Expression is a sealed interface, permitting only these specific records.
public sealed interface Expression permits Constant, Plus, Minus {
    double evaluate();
}
```

**2. `src/main/java/com/example/expressions/Constant.java`**
```java
package com.example.expressions;

// Records are implicitly final, so they don't need a final modifier here.
public record Constant(double value) implements Expression {
    @Override
    public double evaluate() {
        return value;
    }
}
```

**3. `src/main/java/com/example/expressions/Plus.java`**
```java
package com.example.expressions;

public record Plus(Expression left, Expression right) implements Expression {
    @Override
    public double evaluate() {
        return left.evaluate() + right.evaluate();
    }
}
```

**4. `src/main/java/com/example/expressions/Minus.java`**
```java
package com.example.expressions;

public record Minus(Expression left, Expression right) implements Expression {
    @Override
    public double evaluate() {
        return left.evaluate() - right.evaluate();
    }
}
```

**5. `src/main/java/com/example/Main.java`**
```java
package com.example;

import com.example.expressions.*;

public class Main {
    public static void main(String[] args) {
        // Represents: (10 + 5) - 2
        Expression expr1 = new Minus(
                                new Plus(
                                    new Constant(10),
                                    new Constant(5)
                                ),
                                new Constant(2)
                            );

        // Represents: (20 - 7)
        Expression expr2 = new Minus(
                                new Constant(20),
                                new Constant(7)
                            );

        // Represents: 42
        Expression expr3 = new Constant(42);

        System.out.println("Expression 1: " + evaluateAndDescribe(expr1)); // Expected: 13.0
        System.out.println("Expression 2: " + evaluateAndDescribe(expr2)); // Expected: 13.0
        System.out.println("Expression 3: " + evaluateAndDescribe(expr3)); // Expected: 42.0

        System.out.println("\n--- Demonstrating Exhaustive Switch ---");
        // Example of an exhaustive switch (no default needed)
        // If you were to add a new permitted type to Expression (e.g., Multiply)
        // and didn't update this switch, the compiler would give an error.
        System.out.println("Value of expr1: " + processExpression(expr1));
        System.out.println("Value of expr2: " + processExpression(expr2));
        System.out.println("Value of expr3: " + processExpression(expr3));
    }

    public static String evaluateAndDescribe(Expression expr) {
        String description = switch (expr) {
            case Constant c -> "Constant(" + c.value() + ")";
            case Plus p -> "Plus(" + evaluateAndDescribe(p.left()) + ", " + evaluateAndDescribe(p.right()) + ")";
            case Minus m -> "Minus(" + evaluateAndDescribe(m.left()) + ", " + evaluateAndDescribe(m.right()) + ")";
            // No default needed here because all permitted subtypes are covered
            // and the compiler guarantees exhaustiveness.
        };
        return description + " = " + expr.evaluate();
    }

    public static double processExpression(Expression expr) {
        return switch (expr) {
            case Constant(double value) -> value; // Deconstruction pattern
            case Plus(Expression left, Expression right) -> left.evaluate() + right.evaluate();
            case Minus(Expression left, Expression right) -> left.evaluate() - right.evaluate();
        };
        // Again, no default needed. If you comment out one case (e.g., 'case Plus'),
        // the compiler will produce an error because the switch is no longer exhaustive
        // for the sealed type Expression.
    }
}
```

**Compilation and Execution:**

1.  **Compile:** Navigate to the `src/main/java` directory.
    ```bash
    javac --enable-preview --release 17 com/example/expressions/*.java com/example/Main.java
    ```
2.  **Run:** From the `src/main/java` directory.
    ```bash
    java --enable-preview com.example.Main
    ```

**Expected Output:**

```
Expression 1: Minus(Plus(Constant(10.0), Constant(5.0)), Constant(2.0)) = 13.0
Expression 2: Minus(Constant(20.0), Constant(7.0)) = 13.0
Expression 3: Constant(42.0) = 42.0

--- Demonstrating Exhaustive Switch ---
Value of expr1: 13.0
Value of expr2: 13.0
Value of expr3: 42.0
```

---

### Example 3: Demonstrating `non-sealed` and `sealed` permitting `sealed`

This example specifically focuses on how different permitted subtypes continue the hierarchy.

**File Structure:**
```
.
├── src
│   ├── main
│   │   ├── java
│   │   │   ├── com
│   │   │   │   ├── example
│   │   │   │   │   ├── vehicles
│   │   │   │   │   │   ├── Car.java
│   │   │   │   │   │   ├── Bike.java
│   │   │   │   │   │   ├── Motorbike.java
│   │   │   │   │   │   ├── RoadBike.java
│   │   │   │   │   │   ├── MountainBike.java
│   │   │   │   │   │   └── Vehicle.java
│   │   │   │   │   └── Main.java
```

**1. `src/main/java/com/example/vehicles/Vehicle.java`**
```java
package com.example.vehicles;

// Vehicle is sealed, permitting Car (final), Bike (non-sealed), and Motorbike (sealed).
public sealed interface Vehicle permits Car, Bike, Motorbike {
    String getType();
    double getSpeed();
}
```

**2. `src/main/java/com/example/vehicles/Car.java`**
```java
package com.example.vehicles;

// Car is final, terminating this branch of the hierarchy.
public final class Car implements Vehicle {
    private final String model;
    private final double speed;

    public Car(String model, double speed) {
        this.model = model;
        this.speed = speed;
    }

    @Override
    public String getType() {
        return "Car (" + model + ")";
    }

    @Override
    public double getSpeed() {
        return speed;
    }
}
```

**3. `src/main/java/com/example/vehicles/Bike.java`**
```java
package com.example.vehicles;

// Bike is non-sealed, allowing any class to extend it.
public non-sealed class Bike implements Vehicle {
    protected final String type;
    protected final double speed;

    public Bike(String type, double speed) {
        this.type = type;
        this.speed = speed;
    }

    @Override
    public String getType() {
        return "Bike (" + type + ")";
    }

    @Override
    public double getSpeed() {
        return speed;
    }
}
```

**4. `src/main/java/com/example/vehicles/RoadBike.java`**
```java
package com.example.vehicles;

// RoadBike can extend Bike because Bike is non-sealed.
// No specific modifier (final, sealed, non-sealed) is required for RoadBike
// because it's not a direct permitted subtype of a sealed type.
public class RoadBike extends Bike {
    public RoadBike(double speed) {
        super("Road", speed);
    }
}
```

**5. `src/main/java/com/example/vehicles/Motorbike.java`**
```java
package com.example.vehicles;

// Motorbike is sealed, meaning it will also define its permitted subtypes.
public sealed class Motorbike implements Vehicle
    permits MountainBike { // For simplicity, only one permitted type here
    private final String engineType;
    private final double speed;

    public Motorbike(String engineType, double speed) {
        this.engineType = engineType;
        this.speed = speed;
    }

    @Override
    public String getType() {
        return "Motorbike (" + engineType + ")";
    }

    @Override
    public double getSpeed() {
        return speed;
    }
}
```

**6. `src/main/java/com/example/vehicles/MountainBike.java`**
```java
package com.example.vehicles;

// MountainBike is final, extending the sealed Motorbike.
public final class MountainBike extends Motorbike {
    public MountainBike(double speed) {
        super("Off-road", speed);
    }

    @Override
    public String getType() {
        return "Mountain Bike";
    }
}
```

**7. `src/main/java/com/example/Main.java`**
```java
package com.example;

import com.example.vehicles.*;

public class Main {
    public static void main(String[] args) {
        Vehicle car = new Car("Sedan", 120.0);
        Vehicle roadBike = new RoadBike(30.0); // Allowed: Bike is non-sealed
        Vehicle mountainBike = new MountainBike(50.0); // Allowed: Motorbike is sealed, and MountainBike is permitted

        System.out.println(car.getType() + " at " + car.getSpeed() + " km/h");
        System.out.println(roadBike.getType() + " at " + roadBike.getSpeed() + " km/h");
        System.out.println(mountainBike.getType() + " at " + mountainBike.getSpeed() + " km/h");

        System.out.println("\n--- Processing Vehicles ---");
        processVehicle(car);
        processVehicle(roadBike);
        processVehicle(mountainBike);

        // --- Demonstrating compile-time errors (UNCOMMENT TO SEE ERRORS) ---

        // Attempt to extend a 'final' class:
        // class SportCar extends Car { // Compile-time error: cannot inherit from final class
        //     public SportCar() { super("Sport", 200); }
        // }

        // Attempt to extend a 'sealed' class without being permitted:
        // class Scooter extends Motorbike { // Compile-time error: Scooter not permitted
        //    public Scooter() { super("Electric", 40); }
        // }

        // Attempt to implement a 'sealed' interface without being permitted:
        // class Skateboard implements Vehicle { // Compile-time error: Skateboard not permitted
        //    @Override public String getType() { return "Skateboard"; }
        //    @Override public double getSpeed() { return 15; }
        // }
    }

    public static void processVehicle(Vehicle vehicle) {
        String message = switch (vehicle) {
            case Car c -> "Driving a " + c.getType();
            case RoadBike rb -> "Riding a " + rb.getType();
            case MountainBike mb -> "Riding an adventurous " + mb.getType();
            case Bike b -> "Just cycling on a " + b.getType(); // Catches generic Bike, but specific RoadBike will be matched first.
            // Note: If you remove 'case Bike b', the compiler will still be happy
            // because RoadBike is covered, and Bike itself is not instantiated directly here.
            case Motorbike m -> "Riding a powerful " + m.getType(); // Catches generic Motorbike, but specific MountainBike will be matched first.
        };
        System.out.println(message + " at " + vehicle.getSpeed() + " km/h");
    }
}
```

**Compilation and Execution:**

1.  **Compile:** Navigate to the `src/main/java` directory.
    ```bash
    javac --enable-preview --release 17 com/example/vehicles/*.java com/example/Main.java
    ```
2.  **Run:** From the `src/main/java` directory.
    ```bash
    java --enable-preview com.example.Main
    ```

**Expected Output:**

```
Car (Sedan) at 120.0 km/h
Bike (Road) at 30.0 km/h
Mountain Bike at 50.0 km/h

--- Processing Vehicles ---
Driving a Car (Sedan) at 120.0 km/h
Riding a Bike (Road) at 30.0 km/h
Riding an adventurous Mountain Bike at 50.0 km/h
```

---

## 7. Conclusion

Sealed classes and interfaces in Java 17 are a powerful addition for creating robust and maintainable type hierarchies. They provide explicit control over inheritance and implementation, which is invaluable for designing APIs, modeling complex domains, and ensuring the exhaustiveness of `switch` expressions with pattern matching. By clearly defining the boundaries of your type hierarchies, you can write safer, more predictable, and easier-to-understand code.