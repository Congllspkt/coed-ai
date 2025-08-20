# Demo of Constructor Reference in Java

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Prerequisites](#2-prerequisites)
    *   [Functional Interfaces](#21-functional-interfaces)
    *   [Lambda Expressions](#22-lambda-expressions)
    *   [Method References (Briefly)](#23-method-references-briefly)
3.  [What is a Constructor Reference?](#3-what-is-a-constructor-reference)
    *   [Syntax](#31-syntax)
    *   [How it Works](#32-how-it-works)
4.  [Benefits](#4-benefits)
5.  [Examples](#5-examples)
    *   [Example 1: Constructor Reference for a No-Argument Constructor](#example-1-constructor-reference-for-a-no-argument-constructor)
    *   [Example 2: Constructor Reference for a Parameterized Constructor](#example-2-constructor-reference-for-a-parameterized-constructor)
6.  [Conclusion](#6-conclusion)

---

## 1. Introduction

In Java 8, a powerful feature called **Method References** was introduced, allowing you to refer to methods or constructors without executing them. They provide a compact, readable syntax for lambda expressions that perform a single method call or constructor invocation.

A **Constructor Reference** is a specific type of method reference that refers to a class's constructor. It's used when you want to create an instance of a class and the functional interface's abstract method matches the signature of a constructor.

## 2. Prerequisites

To understand constructor references, it's essential to have a basic grasp of the following concepts:

### 2.1. Functional Interfaces

A functional interface is an interface that has exactly one abstract method. It can have multiple default or static methods, but only one abstract method. They are marked with the `@FunctionalInterface` annotation (optional but recommended for clarity and compile-time checking).

**Example:**
```java
@FunctionalInterface
interface MyFactory {
    Object create(); // Single Abstract Method (SAM)
}
```

### 2.2. Lambda Expressions

Lambda expressions provide a concise way to represent an anonymous function (a function without a name). They are often used to implement the abstract method of a functional interface.

**Example:**
```java
MyFactory factory = () -> new Object(); // Lambda expression implementing MyFactory
```

### 2.3. Method References (Briefly)

Method references are a shorthand for lambda expressions that simply call an existing method. They come in several forms:
*   Static Method Reference: `ClassName::staticMethodName`
*   Instance Method Reference (on a specific object): `object::instanceMethodName`
*   Instance Method Reference (on an arbitrary object of a particular type): `ClassName::instanceMethodName`
*   **Constructor Reference:** `ClassName::new`

## 3. What is a Constructor Reference?

A constructor reference is a special type of method reference that points to a constructor. It's used to create new instances of a class.

### 3.1. Syntax

The syntax for a constructor reference is:

```java
ClassName::new
```

*   `ClassName`: The name of the class whose constructor you want to reference.
*   `new`: A keyword indicating that it's a reference to a constructor.

### 3.2. How it Works

A constructor reference `ClassName::new` can be assigned to a functional interface whose abstract method signature matches the signature of one of `ClassName`'s constructors.

Specifically:
1.  The **return type** of the functional interface's abstract method must be `ClassName` (or a supertype of `ClassName`).
2.  The **parameters** of the functional interface's abstract method must match the parameters of the constructor you intend to reference, in type and order.

When the abstract method of the functional interface is invoked, the corresponding constructor of `ClassName` will be called, and a new instance will be returned.

## 4. Benefits

*   **Conciseness:** Reduces boilerplate code compared to full lambda expressions.
*   **Readability:** Can make code more readable by clearly indicating that an instance is being created.
*   **Clarity:** Directly points to the constructor, making the intent clear.

## 5. Examples

Let's illustrate constructor references with practical examples.

---

### Example 1: Constructor Reference for a No-Argument Constructor

In this example, we'll create a `Person` class with a no-argument constructor and a functional interface that can create a `Person` object.

**File: `ConstructorRefDemo1.java`**

```java
// 1. Define a Class
class Person {
    String name;

    // No-argument constructor
    public Person() {
        this.name = "Unknown";
        System.out.println("Person (no-arg) constructor called.");
    }

    public Person(String name) {
        this.name = name;
        System.out.println("Person (string-arg) constructor called for: " + name);
    }

    public String getName() {
        return name;
    }
}

// 2. Define a Functional Interface
@FunctionalInterface
interface PersonFactory {
    // This abstract method returns a Person object and takes no arguments,
    // matching the signature of Person's no-arg constructor.
    Person create();
}

public class ConstructorRefDemo1 {
    public static void main(String[] args) {

        System.out.println("--- Using Lambda Expression (No-Arg) ---");
        // Using a lambda expression to implement PersonFactory
        PersonFactory lambdaFactory = () -> new Person();
        Person p1 = lambdaFactory.create();
        System.out.println("Person created by lambda: " + p1.getName());

        System.out.println("\n--- Using Constructor Reference (No-Arg) ---");
        // Using a constructor reference to implement PersonFactory
        // Person::new refers to the no-argument constructor of the Person class.
        PersonFactory constructorRefFactory = Person::new;
        Person p2 = constructorRefFactory.create();
        System.out.println("Person created by constructor reference: " + p2.getName());
    }
}
```

#### Explanation:
1.  **`Person` Class:** Has a default no-argument constructor and another constructor with a `String` argument.
2.  **`PersonFactory` Interface:** This is a functional interface with a single abstract method `create()`. Its signature (`Person create()`) perfectly matches the no-argument constructor of the `Person` class (which takes no arguments and effectively "returns" a `Person` object).
3.  **Lambda Expression:** `() -> new Person()` is a classic lambda implementation.
4.  **Constructor Reference:** `Person::new` directly refers to the no-argument constructor of `Person`. When `constructorRefFactory.create()` is called, it's equivalent to calling `new Person()`.

#### Input & Output:

**Input (Compile and Run):**
```bash
javac ConstructorRefDemo1.java
java ConstructorRefDemo1
```

**Output:**
```
--- Using Lambda Expression (No-Arg) ---
Person (no-arg) constructor called.
Person created by lambda: Unknown

--- Using Constructor Reference (No-Arg) ---
Person (no-arg) constructor called.
Person created by constructor reference: Unknown
```

---

### Example 2: Constructor Reference for a Parameterized Constructor

Now, let's extend the concept to a constructor that takes arguments.

**File: `ConstructorRefDemo2.java`**

```java
// 1. Define a Class
class Product {
    String name;
    double price;

    // Parameterized constructor
    public Product(String name, double price) {
        this.name = name;
        this.price = price;
        System.out.println("Product constructor called for: " + name);
    }

    public String getDetails() {
        return "Product: " + name + ", Price: $" + String.format("%.2f", price);
    }
}

// 2. Define a Functional Interface
@FunctionalInterface
interface ProductCreator {
    // This abstract method takes two arguments (String, double) and returns a Product object,
    // matching the signature of Product's parameterized constructor.
    Product create(String name, double price);
}

public class ConstructorRefDemo2 {
    public static void main(String[] args) {

        System.out.println("--- Using Lambda Expression (Parameterized) ---");
        // Using a lambda expression to implement ProductCreator
        ProductCreator lambdaCreator = (n, p) -> new Product(n, p);
        Product laptop = lambdaCreator.create("Laptop", 1200.50);
        System.out.println("Product created by lambda: " + laptop.getDetails());

        System.out.println("\n--- Using Constructor Reference (Parameterized) ---");
        // Using a constructor reference to implement ProductCreator
        // Product::new refers to the constructor of the Product class that
        // matches the (String, double) signature.
        ProductCreator constructorRefCreator = Product::new;
        Product keyboard = constructorRefCreator.create("Mechanical Keyboard", 85.99);
        System.out.println("Product created by constructor reference: " + keyboard.getDetails());

        Product mouse = constructorRefCreator.create("Gaming Mouse", 49.99);
        System.out.println("Another product by constructor reference: " + mouse.getDetails());
    }
}
```

#### Explanation:
1.  **`Product` Class:** Has a constructor `Product(String name, double price)`.
2.  **`ProductCreator` Interface:** This functional interface has an abstract method `create(String name, double price)`. Its signature (`Product create(String, double)`) perfectly matches the parameterized constructor of the `Product` class.
3.  **Lambda Expression:** `(n, p) -> new Product(n, p)` is a concise way to create a `Product` instance using the provided arguments.
4.  **Constructor Reference:** `Product::new` here refers to the *parameterized* constructor of `Product`. The Java compiler infers which constructor to use based on the `ProductCreator` interface's method signature. When `constructorRefCreator.create("...", ...)` is called, it's equivalent to calling `new Product("...", ...)`.

#### Input & Output:

**Input (Compile and Run):**
```bash
javac ConstructorRefDemo2.java
java ConstructorRefDemo2
```

**Output:**
```
--- Using Lambda Expression (Parameterized) ---
Product constructor called for: Laptop
Product created by lambda: Product: Laptop, Price: $1200.50

--- Using Constructor Reference (Parameterized) ---
Product constructor called for: Mechanical Keyboard
Product created by constructor reference: Product: Mechanical Keyboard, Price: $85.99
Product constructor called for: Gaming Mouse
Another product by constructor reference: Product: Gaming Mouse, Price: $49.99
```

---

## 6. Conclusion

Constructor references (`ClassName::new`) are a powerful and elegant feature in Java 8+ that enhance code readability and conciseness when dealing with functional interfaces that create new objects. They are a syntactic sugar over specific lambda expressions, making your code cleaner and more expressive, especially in scenarios involving factory patterns or streaming API operations where object creation is a common task. Remember, the key is always the **matching signature** between the functional interface's abstract method and the target constructor.