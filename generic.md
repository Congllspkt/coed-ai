# Java Generics - Detailed Explanation with Examples

Java Generics, introduced in Java 5, are a powerful feature that allows you to write type-safe code while enhancing code reusability. They enable classes, interfaces, and methods to operate on objects of various types without losing type safety.

---

## Table of Contents

1.  [Introduction](#1-introduction)
2.  [Why Use Generics?](#2-why-use-generics)
    *   [Before Generics (The Problem)](#before-generics-the-problem)
    *   [With Generics (The Solution)](#with-generics-the-solution)
3.  [Generic Classes](#3-generic-classes)
4.  [Generic Interfaces](#4-generic-interfaces)
5.  [Generic Methods](#5-generic-methods)
6.  [Generic Wildcards](#6-generic-wildcards)
    *   [Unbounded Wildcard (`<?>`)](#unbounded-wildcard-)
    *   [Upper Bounded Wildcard (`<? extends T>`)](#upper-bounded-wildcard--extends-t)
    *   [Lower Bounded Wildcard (`<? super T>`)](#lower-bounded-wildcard--super-t)
    *   [PECS Principle (Producer Extends, Consumer Super)](#pecs-principle-producer-extends-consumer-super)
7.  [Type Erasure](#7-type-erasure)
8.  [Limitations of Generics](#8-limitations-of-generics)
9.  [Conclusion](#9-conclusion)

---

## 1. Introduction

Generics allow you to define classes, interfaces, and methods with *type parameters*. These parameters act as placeholders for actual types that are specified when the class, interface, or method is used. The primary goal is to provide compile-time type checking and remove the need for explicit type casts.

## 2. Why Use Generics?

### Before Generics (The Problem)

Before Java 5, collections like `ArrayList` stored objects of type `Object`. This meant you could add any type of object to a collection, leading to potential `ClassCastException` at runtime if you weren't careful.

**Example: Without Generics**

```java
// RawListExample.java
import java.util.ArrayList;
import java.util.List;

public class RawListExample {
    public static void main(String[] args) {
        List list = new ArrayList(); // Raw type list
        list.add("Hello");         // Add a String
        list.add(123);             // Add an Integer - No compile-time error here!
        list.add(true);            // Add a Boolean

        for (Object obj : list) {
            // This cast might fail at runtime if the element is not a String
            String s = (String) obj; 
            System.out.println(s.toUpperCase());
        }
    }
}
```

**Input:** (None, run directly)

**Output:**

```text
HELLO
Exception in thread "main" java.lang.ClassCastException: class java.lang.Integer cannot be cast to class java.lang.String (java.lang.Integer and java.lang.String are in module java.base of loader 'bootstrap')
	at RawListExample.main(RawListExample.java:13)
```

As you can see, the error occurs at runtime, which is late and can be hard to debug in large applications.

### With Generics (The Solution)

Generics enforce type safety at *compile time*. If you try to add an incorrect type to a generic collection, the compiler will flag it as an error immediately.

**Example: With Generics**

```java
// GenericListExample.java
import java.util.ArrayList;
import java.util.List;

public class GenericListExample {
    public static void main(String[] args) {
        List<String> stringList = new ArrayList<>(); // Type-safe list for Strings
        stringList.add("Hello");
        stringList.add("World");
        // stringList.add(123); // Compile-time error: Incompatible types!
        
        // No explicit cast needed, type is known at compile time
        for (String s : stringList) {
            System.out.println(s.toUpperCase());
        }
    }
}
```

**Input:** (None, run directly)

**Output:**

```text
HELLO
WORLD
```

**Benefits of Generics:**

1.  **Compile-time Type Checking:** Catches errors early in the development cycle.
2.  **Elimination of Casts:** Reduces boilerplate code and improves readability.
3.  **Code Reusability:** Allows a single class, interface, or method to work with different types without duplication.

---

## 3. Generic Classes

A generic class is a class that is declared with one or more type parameters. These type parameters are placeholders for actual types that will be provided when the class is instantiated.

**Syntax:**

```java
class ClassName<T1, T2, ..., Tn> { /* ... */ }
```

Where `T1, T2, ... Tn` are type parameters (commonly single uppercase letters like `T` for Type, `E` for Element, `K` for Key, `V` for Value, etc.).

**Example: `Box` Class**

Let's create a generic `Box` class that can hold an object of any type.

```java
// Box.java
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

    public void printContentType() {
        System.out.println("Content type: " + content.getClass().getName());
    }
}
```

**Using the `Box` Class**

```java
// GenericClassExample.java
public class GenericClassExample {
    public static void main(String[] args) {
        // Create a Box to hold a String
        Box<String> stringBox = new Box<>("Hello Generics!");
        String text = stringBox.getContent(); // No cast needed
        System.out.println("String Box Content: " + text);
        stringBox.printContentType();

        System.out.println("--------------------");

        // Create a Box to hold an Integer
        Box<Integer> integerBox = new Box<>(12345);
        int number = integerBox.getContent(); // No cast needed
        System.out.println("Integer Box Content: " + number);
        integerBox.printContentType();

        System.out.println("--------------------");
        
        // You cannot put an Integer into a Box<String>
        // stringBox.setContent(100); // Compile-time error!
    }
}
```

**Input:** (None, run directly)

**Output:**

```text
String Box Content: Hello Generics!
Content type: java.lang.String
--------------------
Integer Box Content: 12345
Content type: java.lang.Integer
--------------------
```

---

## 4. Generic Interfaces

Similar to generic classes, you can define generic interfaces that operate on a type parameter.

**Syntax:**

```java
interface InterfaceName<T> { /* ... */ }
```

**Example: `Container` Interface**

```java
// Container.java
public interface Container<T> {
    void put(T item);
    T get();
    boolean isEmpty();
}
```

**Implementing a Generic Interface**

You can implement a generic interface by either specifying the type parameter directly or by making the implementing class generic itself.

**1. Implementing with a Specific Type**

```java
// StringContainer.java
public class StringContainer implements Container<String> {
    private String data;

    @Override
    public void put(String item) {
        this.data = item;
    }

    @Override
    public String get() {
        return data;
    }

    @Override
    public boolean isEmpty() {
        return data == null || data.isEmpty();
    }
}
```

**2. Implementing with a Generic Type (The implementing class is also generic)**

```java
// GenericContainer.java
public class GenericContainer<T> implements Container<T> {
    private T data;

    @Override
    public void put(T item) {
        this.data = item;
    }

    @Override
    public T get() {
        return data;
    }

    @Override
    public boolean isEmpty() {
        return data == null; // Simple check, depends on type T
    }
}
```

**Using Generic Interfaces**

```java
// GenericInterfaceExample.java
public class GenericInterfaceExample {
    public static void main(String[] args) {
        System.out.println("--- Using StringContainer ---");
        Container<String> stringCont = new StringContainer();
        stringCont.put("Java Generics");
        System.out.println("Content: " + stringCont.get());
        System.out.println("Is Empty: " + stringCont.isEmpty());

        System.out.println("\n--- Using GenericContainer with Integer ---");
        Container<Integer> integerCont = new GenericContainer<>();
        integerCont.put(42);
        System.out.println("Content: " + integerCont.get());
        System.out.println("Is Empty: " + integerCont.isEmpty());

        System.out.println("\n--- Using GenericContainer with Double ---");
        Container<Double> doubleCont = new GenericContainer<>();
        doubleCont.put(3.14159);
        System.out.println("Content: " + doubleCont.get());
        System.out.println("Is Empty: " + doubleCont.isEmpty());
    }
}
```

**Input:** (None, run directly)

**Output:**

```text
--- Using StringContainer ---
Content: Java Generics
Is Empty: false

--- Using GenericContainer with Integer ---
Content: 42
Is Empty: false

--- Using GenericContainer with Double ---
Content: 3.14159
Is Empty: false
```

---

## 5. Generic Methods

You can write generic methods that can be called with arguments of different types. The type parameter for a generic method is declared *before* the return type of the method.

**Syntax:**

```java
public <T> T methodName(T param) { /* ... */ }
```

**Example: Generic Utility Methods**

```java
// GenericMethodExample.java
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

public class GenericMethodExample {

    // A generic method to print elements of an array of any type
    public static <T> void printArray(T[] array) {
        System.out.print("Array elements: ");
        for (T element : array) {
            System.out.print(element + " ");
        }
        System.out.println();
    }

    // A generic method to return the first element of a List of any type
    public static <E> E getFirstElement(List<E> list) {
        if (list == null || list.isEmpty()) {
            return null;
        }
        return list.get(0);
    }

    // A generic method to check if an element is present in an array
    public static <T> boolean contains(T[] array, T elementToFind) {
        for (T element : array) {
            if (element != null && element.equals(elementToFind)) {
                return true;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        // Using printArray with Integer array
        Integer[] intArray = {1, 2, 3, 4, 5};
        printArray(intArray); // Type argument inferred as Integer

        // Using printArray with String array
        String[] stringArray = {"apple", "banana", "cherry"};
        printArray(stringArray); // Type argument inferred as String

        System.out.println("--------------------");

        // Using getFirstElement with List of Strings
        List<String> fruits = new ArrayList<>(Arrays.asList("Mango", "Orange", "Grape"));
        String firstFruit = getFirstElement(fruits); // Type argument inferred as String
        System.out.println("First fruit: " + firstFruit);

        // Using getFirstElement with List of Doubles
        List<Double> temperatures = new ArrayList<>(Arrays.asList(98.6, 100.1, 99.5));
        Double firstTemp = getFirstElement(temperatures); // Type argument inferred as Double
        System.out.println("First temperature: " + firstTemp);
        
        System.out.println("--------------------");

        // Using contains
        System.out.println("Int array contains 3: " + contains(intArray, 3));
        System.out.println("Int array contains 9: " + contains(intArray, 9));
        System.out.println("String array contains \"banana\": " + contains(stringArray, "banana"));
        System.out.println("String array contains \"kiwi\": " + contains(stringArray, "kiwi"));
    }
}
```

**Input:** (None, run directly)

**Output:**

```text
Array elements: 1 2 3 4 5 
Array elements: apple banana cherry 
--------------------
First fruit: Mango
First temperature: 98.6
--------------------
Int array contains 3: true
Int array contains 9: false
String array contains "banana": true
String array contains "kiwi": false
```

---

## 6. Generic Wildcards

Wildcards (`?`) are a special type of type argument that can be used in generic code. They provide more flexibility in how generic types can be used.

### Unbounded Wildcard (`<?>`)

*   **Meaning:** Represents an unknown type.
*   **Use Case:** When the type doesn't matter, or you can only read `Object` methods. You *cannot* add elements (except `null`) to a collection declared with `<?>` because the specific type is unknown.
*   **Scenario:** Useful for methods that operate on generic types where the specific type of elements is not relevant, such as printing the contents of a list.

**Example:**

```java
// UnboundedWildcardExample.java
import java.util.ArrayList;
import java.util.List;

public class UnboundedWildcardExample {

    // Method to print elements of a list of any type
    public static void printList(List<?> list) {
        System.out.print("List elements: ");
        for (Object elem : list) { // Elements are read as Object
            System.out.print(elem + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        List<Integer> intList = new ArrayList<>();
        intList.add(10);
        intList.add(20);
        printList(intList); // Works with List<Integer>

        List<String> stringList = new ArrayList<>();
        stringList.add("Apple");
        stringList.add("Banana");
        printList(stringList); // Works with List<String>

        // You cannot add elements to a List<?> (except null)
        // List<?> mysteryList = new ArrayList<>();
        // mysteryList.add("something"); // Compile-time error!
        // mysteryList.add(123);        // Compile-time error!
    }
}
```

**Input:** (None, run directly)

**Output:**

```text
List elements: 10 20 
List elements: Apple Banana 
```

### Upper Bounded Wildcard (`<? extends T>`)

*   **Meaning:** Represents an unknown type that is either `T` or a subtype of `T`.
*   **Use Case:** When you want to *read* (consume) data from a generic structure. You *cannot* add elements (except `null`) to a collection declared with `<? extends T>` because you don't know the exact subtype.
*   **Scenario:** Useful for methods that process lists where the elements are `T` or a more specific type (e.g., a list of `Number` or any of its subclasses like `Integer`, `Double`, etc.).

**Example:**

```java
// UpperBoundedWildcardExample.java
import java.util.ArrayList;
import java.util.List;

public class UpperBoundedWildcardExample {

    // Method to sum numbers from a list where elements are Number or its subtypes
    public static double sumOfNumbers(List<? extends Number> numbers) {
        double sum = 0.0;
        for (Number number : numbers) { // Can read elements as Number
            sum += number.doubleValue();
        }
        // numbers.add(new Integer(10)); // Compile-time error! Cannot add.
        // numbers.add(new Double(5.0)); // Compile-time error! Cannot add.
        return sum;
    }

    public static void main(String[] args) {
        List<Integer> integers = new ArrayList<>();
        integers.add(1);
        integers.add(2);
        integers.add(3);
        System.out.println("Sum of integers: " + sumOfNumbers(integers));

        List<Double> doubles = new ArrayList<>();
        doubles.add(10.5);
        doubles.add(20.5);
        System.out.println("Sum of doubles: " + sumOfNumbers(doubles));

        List<Number> numbers = new ArrayList<>();
        numbers.add(100);
        numbers.add(50.5);
        System.out.println("Sum of mixed numbers: " + sumOfNumbers(numbers));
        
        // List<String> strings = new ArrayList<>();
        // strings.add("abc");
        // sumOfNumbers(strings); // Compile-time error: String is not a subtype of Number
    }
}
```

**Input:** (None, run directly)

**Output:**

```text
Sum of integers: 6.0
Sum of doubles: 31.0
Sum of mixed numbers: 150.5
```

### Lower Bounded Wildcard (`<? super T>`)

*   **Meaning:** Represents an unknown type that is either `T` or a supertype of `T`.
*   **Use Case:** When you want to *write* (produce) data into a generic structure. You can add `T` or any subtype of `T` to a collection declared with `<? super T>`. You can only read elements as `Object`.
*   **Scenario:** Useful for methods that add elements to a list, where the list can accept elements of type `T` or any of its superclasses (e.g., a list that can hold `Integer`s, `Number`s, or `Object`s).

**Example:**

```java
// LowerBoundedWildcardExample.java
import java.util.ArrayList;
import java.util.List;

public class LowerBoundedWildcardExample {

    // Method to add integers to a list that can hold Integer or its supertypes
    public static void addIntegers(List<? super Integer> list) {
        list.add(10); // Can add Integer
        list.add(20); // Can add Integer
        list.add(new Integer(30)); // Can add Integer
        // list.add(new Double(5.0)); // Compile-time error! Cannot add Double
    }
    
    // Method to read from a <? super T> list (elements are read as Object)
    public static void printListContents(List<?> list) { // Using unbounded for printing
        System.out.print("List contents: ");
        for (Object o : list) {
            System.out.print(o + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        List<Integer> integers = new ArrayList<>();
        addIntegers(integers); // List<Integer> is <? super Integer>
        printListContents(integers);

        List<Number> numbers = new ArrayList<>();
        addIntegers(numbers); // List<Number> is <? super Integer>
        printListContents(numbers);

        List<Object> objects = new ArrayList<>();
        addIntegers(objects); // List<Object> is <? super Integer>
        printListContents(objects);

        // List<Double> doubles = new ArrayList<>();
        // addIntegers(doubles); // Compile-time error: Double is not a supertype of Integer
    }
}
```

**Input:** (None, run directly)

**Output:**

```text
List contents: 10 20 30 
List contents: 10 20 30 
List contents: 10 20 30 
```

### PECS Principle (Producer Extends, Consumer Super)

This is a mnemonic to remember when to use `extends` and `super` wildcards:

*   **P**roducer **E**xtends: If your collection is primarily for *producing* (reading) values, use `<? extends T>`. (e.g., `List<? extends Number>`). You can iterate over it and get `T` or its subtypes.
*   **C**onsumer **S**uper: If your collection is primarily for *consuming* (writing) values, use `<? super T>`. (e.g., `List<? super Integer>`). You can add `T` or its subtypes to it.

---

## 7. Type Erasure

Java Generics are implemented using a technique called **type erasure**. This means that generic type information (like `<String>`, `<Integer>`) is only present at compile time. At runtime, all generic type parameters are replaced with their bounds or with `Object` if no bounds are specified.

**How it works:**

*   `List<String>` becomes `List` (raw type).
*   `T` in `Box<T>` becomes `Object`.
*   `T` in `Box<T extends Number>` becomes `Number`.

**Implications:**

1.  **No `new T()`:** You cannot create instances of type parameters at runtime because `T` is erased to `Object` or its bound.
2.  **No `T instanceof`:** You cannot use `instanceof` with a type parameter. `if (obj instanceof T)` is invalid.
3.  **No primitive types:** You cannot use primitive types (like `int`, `char`, `double`) as type arguments. You must use their wrapper classes (e.g., `Integer`, `Character`, `Double`).
4.  **Runtime type information loss:** You cannot determine the exact generic type at runtime. `new ArrayList<String>().getClass()` and `new ArrayList<Integer>().getClass()` will both return `java.util.ArrayList`.

**Example of Erasure:**

```java
// TypeErasureExample.java
import java.util.ArrayList;
import java.util.List;

public class TypeErasureExample {
    public static void main(String[] args) {
        List<String> stringList = new ArrayList<>();
        List<Integer> integerList = new ArrayList<>();

        // At runtime, both stringList and integerList are seen as plain ArrayList
        System.out.println("Class of stringList: " + stringList.getClass());
        System.out.println("Class of integerList: " + integerList.getClass());
        System.out.println("Are their classes the same? " + (stringList.getClass() == integerList.getClass()));
    }
}
```

**Input:** (None, run directly)

**Output:**

```text
Class of stringList: class java.util.ArrayList
Class of integerList: class java.util.ArrayList
Are their classes the same? true
```

---

## 8. Limitations of Generics

Due to type erasure, there are certain things you cannot do with generics:

1.  **Cannot Instantiate Type Parameters:**
    ```java
    // public class MyClass<T> { T instance = new T(); } // Compile-time error!
    ```
    Workaround: Pass a `Class<T>` object to the constructor, e.g., `new T[size]` also invalid.

2.  **Cannot Create Arrays of Parameterized Types:**
    ```java
    // List<Integer>[] arrayOfLists = new List<Integer>[10]; // Compile-time error!
    ```
    Workaround: Use raw types with unchecked cast if absolutely necessary, but generally avoid.

3.  **Cannot Use `instanceof` with Type Parameters:**
    ```java
    // public <T> void check(Object obj) { if (obj instanceof T) { ... } } // Compile-time error!
    ```
    Workaround: Pass a `Class<T>` object and use `isInstance()`.

4.  **Cannot Create Static Fields of Type Parameters:**
    ```java
    // public class MyClass<T> { static T myStaticField; } // Compile-time error!
    ```
    Static fields belong to the class itself, not to a specific instantiation of the class.

5.  **Cannot Use Primitive Types as Type Arguments:**
    ```java
    // List<int> numbers = new ArrayList<>(); // Compile-time error!
    ```
    Always use wrapper classes (e.g., `Integer`, `Boolean`, `Double`).

6.  **Generic Exception Classes:** A generic class cannot extend `Throwable` or `Exception`.
    ```java
    // class MyGenericException<T> extends Exception {} // Compile-time error!
    ```

---

## 9. Conclusion

Java Generics are a fundamental feature for writing robust, type-safe, and reusable code. By enforcing type checks at compile time, they help catch errors early, eliminate the need for verbose casting, and make your code more readable and maintainable. While understanding type erasure and its limitations is important, the benefits of using generics in modern Java development far outweigh these considerations. Master generics, especially wildcards, to write more flexible and powerful Java applications.