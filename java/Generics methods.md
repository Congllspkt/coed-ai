Generic methods in Java are a powerful feature that allows you to write methods that can operate on objects of various types in a type-safe manner, without having to write separate methods for each type. They introduce their own type parameters, distinct from any type parameters declared by the enclosing class.

### Why Use Generic Methods?

1.  **Type Safety:** They provide compile-time type checking, eliminating the need for explicit casts and reducing the risk of `ClassCastException` at runtime.
2.  **Code Reusability:** You can write a single method that works for multiple data types, leading to more concise and maintainable code.
3.  **Flexibility:** They allow you to define algorithms that are applicable to various types.

### Syntax of Generic Methods

The syntax for declaring a generic method involves placing the type parameter (or parameters) *before* the method's return type.

```java
public <T> void methodName(T parameter) {
    // Method body
}
```

*   **`<T>`**: This is the type parameter declaration. `T` is a common convention for "Type," but you can use any valid identifier (e.g., `E` for Element, `K` for Key, `V` for Value, `N` for Number, etc.).
*   **`T` (return type)**: This indicates that the method might return an object of the type specified by the `T` parameter. It could also be `void`, `List<T>`, or any other type.
*   **`T` (parameter type)**: This indicates that the method accepts a parameter of the type specified by the `T` parameter.

### Key Concepts

*   **Type Inference:** When you call a generic method, the Java compiler usually has enough information to infer the actual type argument (e.g., `Integer`, `String`). You don't often need to explicitly specify it.
*   **Bounded Type Parameters:** You can restrict the types that can be used as type arguments for a generic method. This is done using the `extends` keyword. For example, `<T extends Number>` means `T` can be `Number` or any subclass of `Number`. `<T extends Comparable<T>>` means `T` must implement the `Comparable` interface, allowing comparison operations.

---

## Examples of Generic Methods

Let's explore some common use cases with examples.

### Example 1: Simple Generic Method to Print an Array

This method can print the elements of an array of any type (`Integer`, `String`, `Double`, etc.).

```java
// File: GenericMethodExample1.java

public class GenericMethodExample1 {

    /**
     * A generic method to print all elements of an array of any type.
     * The type parameter <T> is declared before the return type 'void'.
     *
     * @param <T>   The type of elements in the array.
     * @param array The array to be printed.
     */
    public static <T> void printArray(T[] array) {
        System.out.print("Array Elements: [");
        for (int i = 0; i < array.length; i++) {
            System.out.print(array[i]);
            if (i < array.length - 1) {
                System.out.print(", ");
            }
        }
        System.out.println("]");
    }

    public static void main(String[] args) {
        // --- Input 1: Integer Array ---
        Integer[] intArray = {1, 2, 3, 4, 5};
        System.out.println("Calling printArray with Integer Array:");
        printArray(intArray); // Type T is inferred as Integer

        System.out.println("\n--------------------\n");

        // --- Input 2: Double Array ---
        Double[] doubleArray = {1.1, 2.2, 3.3, 4.4};
        System.out.println("Calling printArray with Double Array:");
        printArray(doubleArray); // Type T is inferred as Double

        System.out.println("\n--------------------\n");

        // --- Input 3: String Array ---
        String[] stringArray = {"Hello", "World", "Generics"};
        System.out.println("Calling printArray with String Array:");
        printArray(stringArray); // Type T is inferred as String
    }
}
```

**Input (Implicit in `main` method calls):**

```java
Integer[] intArray = {1, 2, 3, 4, 5};
Double[] doubleArray = {1.1, 2.2, 3.3, 4.4};
String[] stringArray = {"Hello", "World", "Generics"};
```

**Output:**

```
Calling printArray with Integer Array:
Array Elements: [1, 2, 3, 4, 5]

--------------------

Calling printArray with Double Array:
Array Elements: [1.1, 2.2, 3.3, 4.4]

--------------------

Calling printArray with String Array:
Array Elements: [Hello, World, Generics]
```

### Example 2: Generic Method with Bounded Type Parameter (Finding Maximum)

To find the maximum element in an array, the elements must be comparable. We use a bounded type parameter `T extends Comparable<T>` to enforce this.

```java
// File: GenericMethodExample2.java

public class GenericMethodExample2 {

    /**
     * A generic method to find the maximum element in an array.
     * The type parameter <T> is bounded to ensure that elements can be compared.
     * T must implement the Comparable interface.
     *
     * @param <T>   The type of elements in the array, which must be comparable.
     * @param array The array to search for the maximum element.
     * @return The maximum element in the array, or null if the array is empty or null.
     */
    public static <T extends Comparable<T>> T findMax(T[] array) {
        if (array == null || array.length == 0) {
            return null; // No maximum in an empty or null array
        }

        T max = array[0];
        for (int i = 1; i < array.length; i++) {
            if (array[i] != null && array[i].compareTo(max) > 0) {
                max = array[i];
            }
        }
        return max;
    }

    public static void main(String[] args) {
        // --- Input 1: Integer Array ---
        Integer[] intArray = {5, 2, 8, 1, 9, 3};
        System.out.println("Finding max in Integer Array:");
        System.out.println("Input: " + java.util.Arrays.toString(intArray));
        Integer maxInt = findMax(intArray);
        System.out.println("Output (Max Integer): " + maxInt); // Output: 9

        System.out.println("\n--------------------\n");

        // --- Input 2: String Array ---
        String[] stringArray = {"apple", "orange", "banana", "grape"};
        System.out.println("Finding max in String Array (alphabetical):");
        System.out.println("Input: " + java.util.Arrays.toString(stringArray));
        String maxString = findMax(stringArray);
        System.out.println("Output (Max String): " + maxString); // Output: orange

        System.out.println("\n--------------------\n");

        // --- Input 3: Array with one element ---
        Double[] singleElementArray = {7.7};
        System.out.println("Finding max in single-element Double Array:");
        System.out.println("Input: " + java.util.Arrays.toString(singleElementArray));
        Double maxDouble = findMax(singleElementArray);
        System.out.println("Output (Max Double): " + maxDouble); // Output: 7.7

        System.out.println("\n--------------------\n");

        // --- Input 4: Empty Array ---
        Integer[] emptyArray = {};
        System.out.println("Finding max in Empty Array:");
        System.out.println("Input: " + java.util.Arrays.toString(emptyArray));
        Integer maxEmpty = findMax(emptyArray);
        System.out.println("Output (Max for Empty Array): " + maxEmpty); // Output: null
    }
}
```

**Input (Implicit in `main` method calls):**

```java
Integer[] intArray = {5, 2, 8, 1, 9, 3};
String[] stringArray = {"apple", "orange", "banana", "grape"};
Double[] singleElementArray = {7.7};
Integer[] emptyArray = {};
```

**Output:**

```
Finding max in Integer Array:
Input: [5, 2, 8, 1, 9, 3]
Output (Max Integer): 9

--------------------

Finding max in String Array (alphabetical):
Input: [apple, orange, banana, grape]
Output (Max String): orange

--------------------

Finding max in single-element Double Array:
Input: [7.7]
Output (Max Double): 7.7

--------------------

Finding max in Empty Array:
Input: []
Output (Max for Empty Array): null
```

### Example 3: Generic Method with Multiple Type Parameters

You can also define methods with multiple type parameters, useful for operations involving different but related types.

```java
// File: GenericMethodExample3.java

import java.util.AbstractMap.SimpleEntry;
import java.util.Map;

public class GenericMethodExample3 {

    /**
     * A generic method to create a simple key-value pair (Entry).
     * This method uses two different type parameters: K for Key and V for Value.
     *
     * @param <K> The type of the key.
     * @param <V> The type of the value.
     * @param key The key to store.
     * @param value The value to store.
     * @return A SimpleEntry object representing the key-value pair.
     */
    public static <K, V> Map.Entry<K, V> createPair(K key, V value) {
        return new SimpleEntry<>(key, value);
    }

    public static void main(String[] args) {
        // --- Input 1: String Key, Integer Value ---
        System.out.println("Creating a pair with String key and Integer value:");
        Map.Entry<String, Integer> pair1 = createPair("Age", 30);
        System.out.println("Input: Key='Age', Value=30");
        System.out.println("Output (Pair 1): Key = " + pair1.getKey() + ", Value = " + pair1.getValue());

        System.out.println("\n--------------------\n");

        // --- Input 2: Integer Key, String Value ---
        System.out.println("Creating a pair with Integer key and String value:");
        Map.Entry<Integer, String> pair2 = createPair(101, "Java");
        System.out.println("Input: Key=101, Value='Java'");
        System.out.println("Output (Pair 2): Key = " + pair2.getKey() + ", Value = " + pair2.getValue());

        System.out.println("\n--------------------\n");

        // --- Input 3: Double Key, Boolean Value ---
        System.out.println("Creating a pair with Double key and Boolean value:");
        Map.Entry<Double, Boolean> pair3 = createPair(3.14, true);
        System.out.println("Input: Key=3.14, Value=true");
        System.out.println("Output (Pair 3): Key = " + pair3.getKey() + ", Value = " + pair3.getValue());
    }
}
```

**Input (Implicit in `main` method calls):**

```java
createPair("Age", 30);
createPair(101, "Java");
createPair(3.14, true);
```

**Output:**

```
Creating a pair with String key and Integer value:
Input: Key='Age', Value=30
Output (Pair 1): Key = Age, Value = 30

--------------------

Creating a pair with Integer key and String value:
Input: Key=101, Value='Java'
Output (Pair 2): Key = 101, Value = Java

--------------------

Creating a pair with Double key and Boolean value:
Input: Key=3.14, Value=true
Output (Pair 3): Key = 3.14, Value = true
```

---

### When to Use Generic Methods vs. Generic Classes

*   **Generic Methods:**
    *   Use when the type parameter is specific to a *single method* and does not affect the entire class.
    *   Often used for utility methods (e.g., `java.util.Collections.sort`, `java.util.Arrays.asList`).
    *   The method can be `static` or non-`static`.

*   **Generic Classes:**
    *   Use when the type parameter affects *multiple methods* and fields within the class, defining the type of objects that the class instance will work with.
    *   E.g., `ArrayList<E>`, `HashMap<K, V>`.

In summary, generic methods are a powerful tool for writing flexible, reusable, and type-safe code in Java, especially for utility functions that need to operate on various data types.