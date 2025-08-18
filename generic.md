# Generics in Java

Generics were introduced in Java 5 to provide type safety and code reusability. Before generics, collections in Java (like `ArrayList` or `HashMap`) stored elements of type `Object`. This meant that you could add any type of object to a collection, but when retrieving them, you had to explicitly cast them back to their original type. This process was error-prone and could lead to `ClassCastException` at runtime.

Generics solve this problem by allowing you to define classes, interfaces, and methods with *type parameters*. These type parameters act as placeholders for the actual types that will be used when the class, interface, or method is instantiated or called.

---

## Table of Contents

1.  [Why Generics? (The Problem They Solve)](#1-why-generics-the-problem-they-solve)
2.  [Core Concepts](#2-core-concepts)
    *   [Generic Classes](#generic-classes)
    *   [Generic Methods](#generic-methods)
    *   [Generic Interfaces](#generic-interfaces)
3.  [Advanced Concepts](#3-advanced-concepts)
    *   [Bounded Type Parameters](#bounded-type-parameters)
    *   [Wildcards](#wildcards)
        *   [Unbounded Wildcard (`<?>`)](#unbounded-wildcard-)
        *   [Upper Bounded Wildcard (`<? extends T>`)](#upper-bounded-wildcard-extends-t)
        *   [Lower Bounded Wildcard (`<? super T>`)](#lower-bounded-wildcard-super-t)
    *   [PECS Principle (Producer Extends, Consumer Super)](#pecs-principle-producer-extends-consumer-super)
4.  [Behind the Scenes: Type Erasure](#4-behind-the-scenes-type-erasure)
5.  [Benefits of Generics](#5-benefits-of-generics)
6.  [Limitations of Generics](#6-limitations-of-generics)
7.  [Best Practices](#7-best-practices)
8.  [Conclusion](#8-conclusion)

---

## 1. Why Generics? (The Problem They Solve)

Consider an `ArrayList` before Java 5:

```java
import java.util.ArrayList;
import java.util.List;

public class PreGenericsExample {
    public static void main(String[] args) {
        List myList = new ArrayList(); // No type specified (raw type)

        myList.add("Hello"); // Adding a String
        myList.add(123);     // Adding an Integer (autoboxed)
        myList.add(true);    // Adding a Boolean (autoboxed)

        // Problem: We need to cast and assume the type
        String s = (String) myList.get(0); // Works
        System.out.println(s);

        // This will compile, but throw ClassCastException at runtime!
        try {
            Integer i = (Integer) myList.get(1); // Works
            System.out.println(i);

            Boolean b = (Boolean) myList.get(2); // Works
            System.out.println(b);

            // This is where the runtime error happens
            String anotherString = (String) myList.get(1); // Casting Integer to String
            System.out.println(anotherString);
        } catch (ClassCastException e) {
            System.out.println("Runtime Error: " + e.getMessage());
        }
    }
}
```

This example clearly shows the `ClassCastException` at runtime. Generics prevent this by enforcing type checks at **compile time**.

With generics, the same example becomes:

```java
import java.util.ArrayList;
import java.util.List;

public class WithGenericsExample {
    public static void main(String[] args) {
        List<String> stringList = new ArrayList<>(); // Type specified: String

        stringList.add("Hello");
        stringList.add("World");
        // stringList.add(123); // COMPILE-TIME ERROR: Incompatible types!

        String s1 = stringList.get(0); // No cast needed
        String s2 = stringList.get(1); // No cast needed
        System.out.println(s1 + " " + s2);
    }
}
```
This is much safer and easier to read.

---

## 2. Core Concepts

### Generic Classes

A generic class is a class that can operate on data of various types, but the type itself is specified during the object creation.

**Syntax:**
```java
class MyClass<T> {
    // T is a type parameter
}
```
Commonly used type parameter names:
*   `E` - Element (used extensively by Java Collections Framework)
*   `K` - Key
*   `V` - Value
*   `N` - Number
*   `T` - Type
*   `S`, `U`, `V` etc. - for second, third, fourth types

**Example: A Generic `Box` Class**

```java
public class Box<T> { // T is the type parameter
    private T content;

    public Box(T content) {
        this.content = content;
    }

    public T getContent() {
        return content;
    }

    public void setContent(T content) {
        this.content = content;
    }

    public static void main(String[] args) {
        // Create a Box for Integers
        Box<Integer> integerBox = new Box<>(123);
        System.out.println("Integer Box Content: " + integerBox.getContent());
        // integerBox.setContent("Hello"); // COMPILE-TIME ERROR: Incompatible types!

        // Create a Box for Strings
        Box<String> stringBox = new Box<>("Generic Hello");
        System.out.println("String Box Content: " + stringBox.getContent());

        // Create a Box for custom objects
        Box<Box<String>> nestedBox = new Box<>(stringBox);
        System.out.println("Nested Box Content: " + nestedBox.getContent().getContent());
    }
}
```

### Generic Methods

Generic methods are methods that introduce their own type parameters, independent of the class they are defined in. This allows them to be used with different types each time they are called.

**Syntax:**
```java
public <T> T myGenericMethod(T parameter) {
    // ...
}
```
The `<T>` before the return type indicates that this is a generic method with a type parameter `T`.

**Example: A Generic `printArray` Method**

```java
public class GenericMethodExample {

    // A generic method to print elements of any array type
    public static <E> void printArray(E[] inputArray) {
        for (E element : inputArray) {
            System.out.printf("%s ", element);
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Integer[] intArray = {1, 2, 3, 4, 5};
        Double[] doubleArray = {1.1, 2.2, 3.3, 4.4};
        Character[] charArray = {'H', 'E', 'L', 'L', 'O'};

        System.out.print("Integer Array: ");
        printArray(intArray); // Type argument inferred as Integer

        System.out.print("Double Array: ");
        printArray(doubleArray); // Type argument inferred as Double

        System.out.print("Character Array: ");
        printArray(charArray); // Type argument inferred as Character
    }
}
```

### Generic Interfaces

Like classes, interfaces can also be generic, allowing their implementing classes to define the specific type.

**Syntax:**
```java
interface MyInterface<T> {
    T process(T data);
}
```

**Example: A Generic `Processor` Interface**

```java
public interface Processor<T> {
    T process(T data);
}

public class StringProcessor implements Processor<String> {
    @Override
    public String process(String data) {
        return data.toUpperCase();
    }

    public static void main(String[] args) {
        Processor<String> processor = new StringProcessor();
        String result = processor.process("hello world");
        System.out.println("Processed String: " + result);

        // You could also have an IntegerProcessor, etc.
        // Processor<Integer> integerProcessor = new IntegerProcessor();
    }
}
```

---

## 3. Advanced Concepts

### Bounded Type Parameters

Sometimes you want to restrict the types that can be used as type arguments for a generic class or method. This is done using **bounded type parameters**.

**Syntax:**
*   ` <T extends UpperBound> `: `T` must be `UpperBound` or a subclass of `UpperBound`. (Can be a class or an interface).
*   ` <T extends Interface1 & Interface2> `: `T` must implement all specified interfaces (and optionally extend a class if listed first).

**Example: A `NumericBox` that only holds numbers**

```java
public class NumericBox<T extends Number> { // T must be Number or a subclass of Number
    private T number;

    public NumericBox(T number) {
        this.number = number;
    }

    public double doubleValue() {
        return number.doubleValue(); // Can call Number methods
    }

    public static <U extends Number> double sum(U num1, U num2) {
        return num1.doubleValue() + num2.doubleValue(); // Can call Number methods
    }

    public static void main(String[] args) {
        NumericBox<Integer> integerBox = new NumericBox<>(10);
        System.out.println("Integer Box Double Value: " + integerBox.doubleValue());

        NumericBox<Double> doubleBox = new NumericBox<>(15.5);
        System.out.println("Double Box Double Value: " + doubleBox.doubleValue());

        // NumericBox<String> stringBox = new NumericBox<>("hello"); // COMPILE-TIME ERROR: String is not a Number!

        System.out.println("Sum of 5 and 7: " + NumericBox.sum(5, 7));
        System.out.println("Sum of 2.5 and 3.5: " + NumericBox.sum(2.5, 3.5));
    }
}
```

### Wildcards

Wildcards (`?`) are used in generic code to relax the restrictions on type parameters. They are primarily used in method signatures, especially for arguments that are collections.

#### Unbounded Wildcard (`<?>`)

Represents an unknown type. It means "any type." It's useful when the methods in the generic class don't depend on the type parameter, or when you are reading data from a generic collection that could contain any type.

**Use cases:**
*   When you can write a method that operates on `Object` functionality.
*   When you are consuming data that could be of any type.

**Example:**
```java
import java.util.List;
import java.util.ArrayList;

public class UnboundedWildcardExample {

    // Method that can print a list of any type
    public static void printList(List<?> list) { // List of unknown type
        for (Object elem : list) { // Elements are treated as Object
            System.out.print(elem + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        List<Integer> intList = new ArrayList<>();
        intList.add(1);
        intList.add(2);
        printList(intList); // Prints 1 2

        List<String> stringList = new ArrayList<>();
        stringList.add("Hello");
        stringList.add("World");
        printList(stringList); // Prints Hello World

        // What you CANNOT do:
        // list.add(new Object()); // COMPILE-TIME ERROR: Cannot add to List<?> as type is unknown!
        // The compiler doesn't know what type '?' represents, so it cannot guarantee type safety if you add.
    }
}
```

#### Upper Bounded Wildcard (`<? extends T>`)

Represents `T` or any subclass of `T`. It means "an unknown type that is `T` or a subtype of `T`". Useful for methods that read (get) values from a generic collection.

**Use cases:**
*   When you need to read from a generic collection. (Producer)
*   When you want to operate on `T` or its subtypes.

**Example:**
```java
import java.util.List;
import java.util.ArrayList;

class Animal {}
class Dog extends Animal {}
class GermanShepherd extends Dog {}
class Cat extends Animal {}

public class UpperBoundedWildcardExample {

    // Method to print details of animals or their subclasses
    public static void printAnimals(List<? extends Animal> animals) {
        for (Animal a : animals) { // Elements are guaranteed to be Animal or its subtype
            System.out.println("Animal: " + a.getClass().getSimpleName());
        }
        // animals.add(new Dog()); // COMPILE-TIME ERROR! Cannot add because '?' could be Cat,
                               // and adding a Dog would violate type safety.
                               // You can't add anything (except null) to a <? extends T> list.
    }

    public static void main(String[] args) {
        List<Animal> animalList = new ArrayList<>();
        animalList.add(new Animal());
        animalList.add(new Dog());
        printAnimals(animalList);

        List<Dog> dogList = new ArrayList<>();
        dogList.add(new Dog());
        dogList.add(new GermanShepherd());
        printAnimals(dogList); // Works because Dog extends Animal

        // List<String> stringList = new ArrayList<>();
        // printAnimals(stringList); // COMPILE-TIME ERROR! String does not extend Animal
    }
}
```

#### Lower Bounded Wildcard (`<? super T>`)

Represents `T` or any superclass of `T`. It means "an unknown type that is `T` or a supertype of `T`". Useful for methods that write (add) values to a generic collection.

**Use cases:**
*   When you need to add to a generic collection. (Consumer)
*   When you want to operate on `T` or its supertypes.

**Example:**
```java
import java.util.List;
import java.util.ArrayList;

class Vehicle {}
class Car extends Vehicle {}
class Sedan extends Car {}

public class LowerBoundedWildcardExample {

    // Method to add Sedan objects to a list that can hold Sedan or its supertypes
    public static void addSedansToList(List<? super Sedan> list) {
        list.add(new Sedan()); // This is safe. A Sedan can always be added to a list of Sedan, Car, or Vehicle.
        // list.add(new Car()); // COMPILE-TIME ERROR: A Car might not be a Sedan (if '?' is Sedan)
                               // Only T itself (Sedan) or its subtypes (none in this case) can be added.
        
        // When retrieving, you only know it's an Object (or '?'s lower bound, which is Sedan here)
        Object obj = list.get(0); // Safe, but not very useful
        // Sedan sedan = list.get(0); // COMPILE-TIME ERROR: Cannot cast Object to Sedan without explicit cast
    }

    public static void main(String[] args) {
        List<Sedan> sedans = new ArrayList<>();
        addSedansToList(sedans); // Adds a Sedan to the list of Sedans
        System.out.println("Sedans list size: " + sedans.size());

        List<Car> cars = new ArrayList<>();
        addSedansToList(cars);   // Adds a Sedan to the list of Cars
        System.out.println("Cars list size: " + cars.size());

        List<Vehicle> vehicles = new ArrayList<>();
        addSedansToList(vehicles); // Adds a Sedan to the list of Vehicles
        System.out.println("Vehicles list size: " + vehicles.size());

        List<Object> objects = new ArrayList<>();
        addSedansToList(objects); // Adds a Sedan to the list of Objects
        System.out.println("Objects list size: " + objects.size());
    }
}
```

### PECS Principle (Producer Extends, Consumer Super)

This is a widely used mnemonic to remember when to use `extends` and when to use `super` with wildcards.

*   **P**roducer **E**xtends: If your generic method or class is going to *produce* (read) instances of `T`, use `<? extends T>`.
    *   Example: `void printAnimals(List<? extends Animal> animals)` - `animals` list produces `Animal` objects.
*   **C**onsumer **S**uper: If your generic method or class is going to *consume* (write/add) instances of `T`, use `<? super T>`.
    *   Example: `void addSedansToList(List<? super Sedan> list)` - `list` consumes `Sedan` objects.

---

## 4. Behind the Scenes: Type Erasure

Generics in Java are implemented using a technique called **type erasure**. This means that generic type information is only present at compile time and is removed during the compilation process (converted to bytecode). The JVM does not know anything about generic types.

**How it works:**
1.  **Generic types replaced with raw types:** All generic type parameters are replaced with their upper bounds (or `Object` if no explicit bound is given).
    *   `List<String>` becomes `List` (internally, the elements are treated as `Object`).
    *   `Box<T>` becomes `Box` (and `T` inside the class becomes `Object`).
    *   `NumericBox<T extends Number>` becomes `NumericBox` (and `T` inside the class becomes `Number`).
2.  **Casts inserted:** The compiler inserts necessary type casts to ensure type safety.
    *   `String s = stringList.get(0);` becomes `String s = (String) stringList.get(0);`
3.  **Bridge methods generated:** For overriding generic methods, the compiler might generate special synthetic methods called "bridge methods" to maintain polymorphism and compatibility with pre-generics code.

**Implications of Type Erasure:**

*   You cannot use primitive types as type arguments (e.g., `List<int>`). You must use their wrapper classes (`List<Integer>`).
*   You cannot create instances of type parameters directly: `new T()` is forbidden.
*   You cannot create arrays of type parameters: `new T[size]` is forbidden (e.g., `new T[10]` is not allowed inside a `Box<T>`).
*   You cannot use `instanceof` with type parameters: `object instanceof T` is forbidden.
*   Generic type information is not available at runtime. So, `new ArrayList<String>().getClass() == new ArrayList<Integer>().getClass()` evaluates to `true`. Both return `java.util.ArrayList`.

---

## 5. Benefits of Generics

*   **Type Safety:** Catches common programming errors (like `ClassCastException`) at compile time instead of runtime.
*   **Code Reusability:** Write generic algorithms once and apply them to different types. (e.g., `Collections.sort()`).
*   **Elimination of Casts:** Reduces boilerplate code and makes it cleaner to read.
*   **Improved Readability:** The type parameters make the intent of the code clearer (e.g., `List<String>` immediately tells you it holds strings).
*   **Performance:** While not a direct performance gain from generics themselves, eliminating explicit casts can sometimes lead to minor performance improvements by reducing runtime overhead.

---

## 6. Limitations of Generics

Due to type erasure, generics in Java have certain limitations:

*   **No Primitive Types:** You cannot use primitive types (`int`, `char`, `boolean`, etc.) as type arguments. You must use their corresponding wrapper classes (`Integer`, `Character`, `Boolean`, etc.).
    ```java
    // List<int> intList = new ArrayList<>(); // COMPILE-TIME ERROR
    List<Integer> integerList = new ArrayList<>(); // Correct
    ```
*   **Cannot Instantiate Type Parameters:** You cannot create an instance of a type parameter directly using `new T()`.
    ```java
    // public class MyClass<T> { T data = new T(); } // COMPILE-TIME ERROR
    ```
    (Workarounds involve passing a `Class<T>` object or using reflection).
*   **Cannot Use `instanceof` with Type Parameters:** Due to type erasure, `T` doesn't exist at runtime, so `obj instanceof T` doesn't make sense.
    ```java
    // public boolean isInstanceOfT(Object obj, T type) { return obj instanceof T; } // COMPILE-TIME ERROR
    ```
*   **Cannot Create Arrays of Type Parameters:** You cannot create arrays like `new T[size]`.
    ```java
    // T[] myArray = new T[10]; // COMPILE-TIME ERROR
    ```
    (Workarounds involve creating `Object[]` and casting, or using `java.lang.reflect.Array.newInstance()`).
*   **No Static Fields/Methods with Class Type Parameters:** A generic class cannot have static fields or methods that use the class's type parameters directly. Static members belong to the class itself, not to specific instances parameterized by a type.
    ```java
    // public class MyClass<T> { public static T staticField; } // COMPILE-TIME ERROR
    ```
    (Static generic methods are allowed, as their type parameter is defined at the method level).
*   **No Checked Exceptions with Generic Types:** You cannot catch generic exception types.
    ```java
    // public class MyException<T> extends Exception {}
    // try { ... } catch (MyException<String> e) { ... } // COMPILE-TIME ERROR
    ```
*   **No Overloading Based Solely on Type Parameters:** Due to type erasure, the JVM cannot distinguish between methods that differ only in their generic type parameters.
    ```java
    // public void print(List<String> list) {}
    // public void print(List<Integer> list) {} // COMPILE-TIME ERROR (erased to print(List) in both cases)
    ```

---

## 7. Best Practices

*   **Use Meaningful Type Parameter Names:** Stick to conventions (`T`, `E`, `K`, `V`, `N`, `S`, `U`).
*   **Adhere to PECS (Producer Extends, Consumer Super):** This principle guides the correct use of wildcards for better flexibility and safety.
*   **Avoid Raw Types:** Always specify type arguments when using generic classes (e.g., `List<String>` instead of `List`). Using raw types bypasses compile-time type checking and reintroduces the problems generics were designed to solve.
*   **Understand Type Erasure:** Knowing how generics are implemented helps you understand their limitations and avoid common pitfalls.
*   **Leverage Type Inference:** In Java 7 and later, the diamond operator (`<>`) can often be used when creating instances, letting the compiler infer the type arguments, making code cleaner.
    ```java
    List<String> list = new ArrayList<>(); // Java 7+
    ```
*   **Consider `@SafeVarargs`:** For generic methods that take a variable number of arguments (`varargs`) of a generic type, using `@SafeVarargs` (on non-final, static, or constructor methods) can suppress warnings when the compiler determines the usage is safe, but care must be taken.
*   **Use `Comparable` and `Comparator`:** For sorting and comparing generic types, leverage these interfaces with appropriate bounds.

---

## 8. Conclusion

Generics are a fundamental and powerful feature in modern Java. They significantly enhance the type safety, readability, and reusability of your code by moving many type-related errors from runtime to compile time. While type erasure introduces some limitations, understanding these underlying mechanisms and adhering to best practices allows you to write robust and efficient generic code. Mastering generics is essential for working effectively with the Java Collections Framework and for designing flexible and extensible APIs.