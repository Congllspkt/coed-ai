# Wrapper Classes in Java

Wrapper classes in Java provide a way to use primitive data types (like `int`, `char`, `boolean`, etc.) as objects. This is essential because many Java APIs, especially the Collections Framework, are designed to work only with objects.

## 1. What are Wrapper Classes?

In Java, we have two main categories of data types:

1.  **Primitive Data Types:** `byte`, `short`, `int`, `long`, `float`, `double`, `boolean`, `char`. These store the actual value directly in memory. They are not objects and do not have methods.
2.  **Reference (Object) Data Types:** Instances of classes, arrays, interfaces. These store references to objects in memory.

Wrapper classes essentially "wrap" a primitive value inside an object. For every primitive type, Java provides a corresponding wrapper class:

| Primitive Type | Wrapper Class (from `java.lang` package) |
| :------------- | :--------------------------------------- |
| `byte`         | `Byte`                                   |
| `short`        | `Short`                                  |
| `int`          | `Integer`                                |
| `long`         | `Long`                                   |
| `float`        | `Float`                                  |
| `double`       | `Double`                                 |
| `boolean`      | `Boolean`                                |
| `char`         | `Character`                              |
| `void`         | `Void` (less common for practical boxing) |

## 2. Key Characteristics of Wrapper Classes

*   **Immutability:** Like `String`, all wrapper class objects are immutable. Once created, their internal value cannot be changed.
*   **Final:** Wrapper classes are `final`, meaning they cannot be subclassed.
*   **`Number` Class:** All numeric wrapper classes (`Byte`, `Short`, `Integer`, `Long`, `Float`, `Double`) inherit from the abstract class `java.lang.Number`. This class provides methods like `intValue()`, `doubleValue()`, `longValue()`, etc., to convert the object's value into different primitive types.
*   **`Comparable` Interface:** All wrapper classes implement the `Comparable` interface, allowing their objects to be compared.
*   **Utility Methods:** They provide useful static methods for converting strings to primitive types (`parseInt()`, `valueOf()`), and other operations.

## 3. Autoboxing and Unboxing (Since Java 5)

Before Java 5, converting between primitives and wrapper objects was a manual process, which was tedious. Java 5 introduced **autoboxing** and **unboxing** to automate this conversion, making the code much cleaner and easier to read.

### 3.1. Autoboxing

*   **Definition:** The automatic conversion of a primitive data type into its corresponding wrapper class object.
*   **When it happens:**
    *   When a primitive value is assigned to a wrapper class variable.
    *   When a primitive value is passed as an argument to a method that expects an object of the wrapper class.

**Example of Autoboxing:**

```java
public class AutoboxingExample {
    public static void main(String[] args) {
        int primitiveInt = 100;
        // Autoboxing: primitiveInt (int) is automatically converted to an Integer object
        Integer wrapperInt = primitiveInt; 
        
        char primitiveChar = 'A';
        // Autoboxing: primitiveChar (char) is automatically converted to a Character object
        Character wrapperChar = primitiveChar; 
        
        System.out.println("Primitive int: " + primitiveInt);
        System.out.println("Wrapper Integer: " + wrapperInt);
        System.out.println("Primitive char: " + primitiveChar);
        System.out.println("Wrapper Character: " + wrapperChar);
        
        // Autoboxing in method calls
        printInteger(25); // 25 (int) is autoboxed to Integer
    }
    
    public static void printInteger(Integer num) {
        System.out.println("Received Integer object: " + num);
    }
}
```

**Input:** (No explicit input needed, values are hardcoded)

**Output:**
```
Primitive int: 100
Wrapper Integer: 100
Primitive char: A
Wrapper Character: A
Received Integer object: 25
```

### 3.2. Unboxing

*   **Definition:** The automatic conversion of a wrapper class object into its corresponding primitive data type.
*   **When it happens:**
    *   When a wrapper object is assigned to a primitive variable.
    *   When a wrapper object is passed as an argument to a method that expects a primitive type.
    *   When an arithmetic operation is performed on a wrapper object.

**Example of Unboxing:**

```java
public class UnboxingExample {
    public static void main(String[] args) {
        Integer wrapperInteger = 500;
        // Unboxing: wrapperInteger (Integer object) is automatically converted to an int primitive
        int primitiveInt = wrapperInteger; 
        
        Double wrapperDouble = 99.99;
        // Unboxing: wrapperDouble (Double object) is automatically converted to a double primitive
        double primitiveDouble = wrapperDouble;
        
        System.out.println("Wrapper Integer: " + wrapperInteger);
        System.out.println("Primitive int: " + primitiveInt);
        System.out.println("Wrapper Double: " + wrapperDouble);
        System.out.println("Primitive double: " + primitiveDouble);
        
        // Unboxing for arithmetic operations
        Integer num1 = 10;
        Integer num2 = 20;
        int sum = num1 + num2; // num1 and num2 are unboxed, then added
        System.out.println("Sum of wrapper integers: " + sum);
        
        // Unboxing in method calls
        printPrimitive(wrapperInteger); // wrapperInteger (Integer) is unboxed to int
    }
    
    public static void printPrimitive(int num) {
        System.out.println("Received primitive int: " + num);
    }
}
```

**Input:** (No explicit input needed)

**Output:**
```
Wrapper Integer: 500
Primitive int: 500
Wrapper Double: 99.99
Primitive double: 99.99
Sum of wrapper integers: 30
Received primitive int: 500
```

## 4. Why Use Wrapper Classes? (Use Cases and Advantages)

### 4.1. Collections Framework

The Java Collections Framework (e.g., `ArrayList`, `HashMap`, `HashSet`) can only store objects, not primitive types. Wrapper classes enable you to store primitive values in collections.

**Example:**

```java
import java.util.ArrayList;
import java.util.List;

public class CollectionExample {
    public static void main(String[] args) {
        // You cannot do ArrayList<int>
        List<Integer> ages = new ArrayList<>();
        
        // Autoboxing happens here: 25, 30, 22 are converted to Integer objects
        ages.add(25); 
        ages.add(30);
        ages.add(22);
        
        System.out.println("Ages in ArrayList: " + ages);
        
        // Unboxing happens when retrieving if assigned to a primitive
        int firstAge = ages.get(0); 
        System.out.println("First age (unboxed): " + firstAge);
    }
}
```

**Input:** (None)

**Output:**
```
Ages in ArrayList: [25, 30, 22]
First age (unboxed): 25
```

### 4.2. Generics

Generics in Java also work only with objects. If you want to use generic types that represent primitive values, you must use their corresponding wrapper classes.

**Example:**

```java
// A generic class that holds a value
class Box<T> {
    private T value;

    public Box(T value) {
        this.value = value;
    }

    public T getValue() {
        return value;
    }
}

public class GenericsExample {
    public static void main(String[] args) {
        // You cannot do Box<int>
        Box<Integer> integerBox = new Box<>(123); // Autoboxing
        Box<Boolean> booleanBox = new Box<>(true); // Autoboxing

        int unboxedInt = integerBox.getValue(); // Unboxing
        boolean unboxedBoolean = booleanBox.getValue(); // Unboxing

        System.out.println("Integer Box Value: " + unboxedInt);
        System.out.println("Boolean Box Value: " + unboxedBoolean);
    }
}
```

**Input:** (None)

**Output:**
```
Integer Box Value: 123
Boolean Box Value: true
```

### 4.3. Handling Null Values

Primitive types cannot be `null`. Wrapper classes, being objects, can hold a `null` value. This is useful when a numeric or boolean value is optional or unknown (e.g., retrieved from a database where a column might be `NULL`).

**Example:**

```java
public class NullWrapperExample {
    public static void main(String[] args) {
        Integer score = null; // A wrapper can be null
        // int primitiveScore = null; // Compile-time error!
        
        System.out.println("Score: " + score);
        
        // Use with caution, as unboxing a null wrapper leads to NullPointerException
        // int actualScore = score; // This would throw NullPointerException if score is null
    }
}
```

**Input:** (None)

**Output:**
```
Score: null
```

### 4.4. Utility Methods

Wrapper classes provide a variety of useful static methods for type conversion, parsing, and other operations.

**Example:**

```java
public class UtilityMethodsExample {
    public static void main(String[] args) {
        // 1. Parsing a String to a primitive
        String numStr = "12345";
        int parsedInt = Integer.parseInt(numStr);
        System.out.println("Parsed int from string: " + parsedInt);

        // 2. Creating a wrapper object from a String
        String doubleStr = "98.76";
        Double wrapperDouble = Double.valueOf(doubleStr);
        System.out.println("Wrapper Double from string: " + wrapperDouble);

        // 3. Converting wrapper/primitive to String
        Integer myInt = 789;
        String intToStr = myInt.toString();
        String anotherIntToStr = String.valueOf(555); // Can also use String.valueOf()
        System.out.println("Integer to String: " + intToStr);
        System.out.println("Primitive int to String: " + anotherIntToStr);

        // 4. Constants (e.g., min/max values)
        System.out.println("Max value of Integer: " + Integer.MAX_VALUE);
        System.out.println("Min value of Character: " + (int)Character.MIN_VALUE); // Cast char to int to see numeric value
    }
}
```

**Input:** (None)

**Output:**
```
Parsed int from string: 12345
Wrapper Double from string: 98.76
Integer to String: 789
Primitive int to String: 555
Max value of Integer: 2147483647
Min value of Character: 0
```

## 5. Important Considerations and Pitfalls

### 5.1. Performance Overhead

Creating objects takes more memory and CPU cycles than simply using primitives. For computationally intensive tasks where performance is critical and only primitive values are needed, using primitives directly is more efficient. Autoboxing/unboxing incurs a slight overhead.

### 5.2. `NullPointerException` during Unboxing

Attempting to unbox a `null` wrapper object will result in a `NullPointerException` at runtime. This is a very common mistake.

**Example:**

```java
public class NullPointerExceptionExample {
    public static void main(String[] args) {
        Integer nullableInt = null;
        
        try {
            // This line will throw NullPointerException
            int primitiveValue = nullableInt; 
            System.out.println("Value: " + primitiveValue);
        } catch (NullPointerException e) {
            System.out.println("Caught NullPointerException: Cannot unbox a null Integer!");
        }
        
        // Always check for null before unboxing or using arithmetic operations
        if (nullableInt != null) {
            int safeValue = nullableInt;
            System.out.println("Safely unboxed: " + safeValue);
        } else {
            System.out.println("Cannot unbox, Integer is null.");
        }
    }
}
```

**Input:** (None)

**Output:**
```
Caught NullPointerException: Cannot unbox a null Integer!
Cannot unbox, Integer is null.
```

### 5.3. Object Identity (`==`) vs. Value Equality (`equals()`)

For primitive types, `==` compares values. For objects (including wrappers), `==` compares *references* (whether two variables point to the *exact same object* in memory). To compare the actual *values* of wrapper objects, you should almost always use the `equals()` method.

**Important Note for `Integer` and `Character` Caching:**
Java caches `Integer` objects for values between -128 and 127 (inclusive) and `Character` objects for values between 0 and 127. When you autobox a value within this range, you might get the same cached object, leading `==` to return `true`. For values outside this range, new objects are created, and `==` will likely return `false` even if the values are the same. This is an optimization and can be confusing. **Always use `equals()` for value comparison!**

**Example:**

```java
public class EqualityExample {
    public static void main(String[] args) {
        // Case 1: Primitives (== compares values)
        int p1 = 10;
        int p2 = 10;
        System.out.println("Primitive 10 == Primitive 10: " + (p1 == p2)); // true

        // Case 2: Wrappers within cache range (-128 to 127)
        Integer i1 = 100; // Autoboxed
        Integer i2 = 100; // Autoboxed, likely from cache
        System.out.println("Integer 100 == Integer 100 (using ==): " + (i1 == i2)); // true (due to caching)
        System.out.println("Integer 100 equals Integer 100 (using .equals()): " + i1.equals(i2)); // true (correct)

        // Case 3: Wrappers outside cache range
        Integer i3 = 200; // Autoboxed, new object
        Integer i4 = 200; // Autoboxed, new object
        System.out.println("Integer 200 == Integer 200 (using ==): " + (i3 == i4)); // false (different objects)
        System.out.println("Integer 200 equals Integer 200 (using .equals()): " + i3.equals(i4)); // true (correct)
        
        // Case 4: Mixing primitive and wrapper
        Integer i5 = 300;
        int p5 = 300;
        // i5 is unboxed to primitive 300 for comparison
        System.out.println("Integer 300 == Primitive 300: " + (i5 == p5)); // true (unboxing happens)

        // Case 5: Boolean and Float/Double (no caching)
        Boolean b1 = true;
        Boolean b2 = true;
        System.out.println("Boolean true == Boolean true: " + (b1 == b2)); // true (Boolean also has cached TRUE/FALSE instances)
        
        Float f1 = 1.0f;
        Float f2 = 1.0f;
        System.out.println("Float 1.0 == Float 1.0: " + (f1 == f2)); // false (Float/Double don't cache)
        System.out.println("Float 1.0 equals Float 1.0: " + f1.equals(f2)); // true
    }
}
```

**Input:** (None)

**Output:**
```
Primitive 10 == Primitive 10: true
Integer 100 == Integer 100 (using ==): true
Integer 100 equals Integer 100 (using .equals()): true
Integer 200 == Integer 200 (using ==): false
Integer 200 equals Integer 200 (using .equals()): true
Integer 300 == Primitive 300: true
Boolean true == Boolean true: true
Float 1.0 == Float 1.0: false
Float 1.0 equals Float 1.0: true
```

## Conclusion

Wrapper classes are fundamental in modern Java development, bridging the gap between primitive types and object-oriented programming. Autoboxing and unboxing have significantly simplified their usage, making code cleaner and more readable. While indispensable for frameworks like Collections and Generics, it's crucial to be aware of potential pitfalls like `NullPointerException` and the difference between `==` and `equals()` when working with them.