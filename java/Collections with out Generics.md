# Collections Without Generics in Java

Before Java 5 (released in 2004), the Java Collections Framework existed but without the concept of Generics. This meant that all collections stored elements as `java.lang.Object`. While this provided flexibility (you could store any type of object), it introduced significant drawbacks related to type safety and code readability.

## Key Characteristics of Non-Generic Collections

1.  **Lack of Compile-Time Type Safety:**
    *   The compiler could not verify the types of objects being stored in or retrieved from the collection.
    *   You could accidentally add a `String` to a collection intended for `Integer` objects, and the compiler wouldn't complain.

2.  **Runtime `ClassCastException` Risk:**
    *   Because elements were retrieved as `Object`, you had to explicitly cast them back to their original type.
    *   If you cast an object to the wrong type, a `java.lang.ClassCastException` would occur at runtime, leading to program crashes. This was a major source of bugs.

3.  **Verbosity and Boilerplate Code:**
    *   Every retrieval required a cast, making the code more verbose and harder to read.

4.  **No Type Information at Runtime (Pre-Generics):**
    *   At runtime, the collection itself had no specific type information about its elements beyond them being `Object`.

## Common Non-Generic Collections (and their Usage)

The core collection interfaces (`List`, `Set`, `Map`) and their common implementations (`ArrayList`, `LinkedList`, `HashSet`, `HashMap`) existed, but without type parameters.

Let's look at examples for some of these.

---

### Example 1: Non-Generic `ArrayList`

A non-generic `ArrayList` can store any type of object. Retrieving requires casting.

**Input Code (`NonGenericArrayListExample.java`):**

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Iterator;

public class NonGenericArrayListExample {

    public static void main(String[] args) {
        // 1. Creating a non-generic ArrayList
        // Notice there are no type parameters like <String> or <Integer>
        List myNonGenericList = new ArrayList();

        // 2. Adding different types of objects
        myNonGenericList.add("Hello, World!"); // String
        myNonGenericList.add(123);             // Integer
        myNonGenericList.add(3.14);            // Double
        myNonGenericList.add(new Object());    // Custom Object

        System.out.println("--- Non-Generic ArrayList Content ---");

        // 3. Retrieving elements and casting
        // This is where ClassCastException can occur if casting wrongly

        // Correct retrieval of a String
        String str = (String) myNonGenericList.get(0);
        System.out.println("First element (String): " + str);

        // Correct retrieval of an Integer
        Integer num = (Integer) myNonGenericList.get(1);
        System.out.println("Second element (Integer): " + num);

        // Incorrect retrieval leading to ClassCastException
        System.out.println("\n--- Demonstrating ClassCastException ---");
        try {
            // Attempt to cast an Integer (123) to a String
            String problematicStr = (String) myNonGenericList.get(1);
            System.out.println("This line will not be reached if exception occurs: " + problematicStr);
        } catch (ClassCastException e) {
            System.out.println("ERROR: Caught ClassCastException as expected!");
            System.out.println("Message: " + e.getMessage());
        }

        System.out.println("\n--- Iterating through Non-Generic ArrayList (Old Style) ---");
        // 4. Iterating through the collection using an Iterator
        // Note: The Iterator's next() method also returns Object, requiring a cast.
        Iterator it = myNonGenericList.iterator();
        while (it.hasNext()) {
            Object element = it.next(); // Element is always Object
            System.out.print("Element Type: " + element.getClass().getName() + ", Value: " + element);

            // You would typically use 'instanceof' before casting in real-world code
            if (element instanceof String) {
                String s = (String) element;
                System.out.println(" (Processed as String: " + s.toUpperCase() + ")");
            } else if (element instanceof Integer) {
                Integer i = (Integer) element;
                System.out.println(" (Processed as Integer: " + (i * 2) + ")");
            } else {
                System.out.println(" (Unhandled type)");
            }
        }

        System.out.println("\n--- Iterating through Non-Generic ArrayList (Enhanced For-Loop - Java 5+) ---");
        // Although the collection is non-generic, if running on Java 5+,
        // the enhanced for-loop can be used, but elements are still Object.
        for (Object element : myNonGenericList) {
             System.out.println("Element: " + element);
        }
    }
}
```

**Compilation and Execution:**
```bash
javac NonGenericArrayListExample.java
java NonGenericArrayListExample
```

**Output:**

```text
--- Non-Generic ArrayList Content ---
First element (String): Hello, World!
Second element (Integer): 123

--- Demonstrating ClassCastException ---
ERROR: Caught ClassCastException as expected!
Message: java.lang.Integer cannot be cast to java.lang.String

--- Iterating through Non-Generic ArrayList (Old Style) ---
Element Type: java.lang.String, Value: Hello, World! (Processed as String: HELLO, WORLD!)
Element Type: java.lang.Integer, Value: 123 (Processed as Integer: 246)
Element Type: java.lang.Double, Value: 3.14 (Unhandled type)
Element Type: java.lang.Object, Value: java.lang.Object@<hashcode> (Unhandled type)

--- Iterating through Non-Generic ArrayList (Enhanced For-Loop - Java 5+) ---
Element: Hello, World!
Element: 123
Element: 3.14
Element: java.lang.Object@<hashcode>
```
*(Note: `<hashcode>` will be a different memory address each time for the `Object` instance).*

---

### Example 2: Non-Generic `HashSet`

A non-generic `HashSet` also stores `Object`s and enforces uniqueness based on `hashCode()` and `equals()` of the `Object` type.

**Input Code (`NonGenericHashSetExample.java`):**

```java
import java.util.HashSet;
import java.util.Set;
import java.util.Iterator;

public class NonGenericHashSetExample {

    public static void main(String[] args) {
        // 1. Creating a non-generic HashSet
        Set myNonGenericSet = new HashSet();

        // 2. Adding different types of objects
        myNonGenericSet.add("Apple");
        myNonGenericSet.add(100);
        myNonGenericSet.add("Banana");
        myNonGenericSet.add(3.14);
        myNonGenericSet.add("Apple"); // Duplicate, will not be added

        System.out.println("--- Non-Generic HashSet Content ---");

        // 3. Iterating through the Set
        System.out.println("Elements in the set:");
        Iterator it = myNonGenericSet.iterator();
        while (it.hasNext()) {
            Object element = it.next();
            // Need to cast if we want to use specific methods of the original type
            if (element instanceof String) {
                String s = (String) element;
                System.out.println("  String: " + s.toUpperCase());
            } else if (element instanceof Integer) {
                Integer i = (Integer) element;
                System.out.println("  Integer: " + (i + 10));
            } else {
                System.out.println("  Other: " + element);
            }
        }

        // 4. Checking for presence (requires a type-consistent object for comparison)
        System.out.println("\nChecking for elements:");
        System.out.println("Contains 'Banana'? " + myNonGenericSet.contains("Banana"));
        System.out.println("Contains 100? " + myNonGenericSet.contains(100));
        System.out.println("Contains 50? " + myNonGenericSet.contains(50));
    }
}
```

**Compilation and Execution:**
```bash
javac NonGenericHashSetExample.java
java NonGenericHashSetExample
```

**Output:**

```text
--- Non-Generic HashSet Content ---
Elements in the set:
  Other: 3.14
  String: BANANA
  Integer: 110
  String: APPLE

Checking for elements:
Contains 'Banana'? true
Contains 100? true
Contains 50? false
```
*(Note: The order of elements in a HashSet is not guaranteed, so your output might show elements in a different sequence).*

---

### Example 3: Non-Generic `HashMap`

A non-generic `HashMap` stores key-value pairs, where both keys and values are stored as `Object`.

**Input Code (`NonGenericHashMapExample.java`):**

```java
import java.util.HashMap;
import java.util.Map;
import java.util.Iterator;
import java.util.Set;

public class NonGenericHashMapExample {

    public static void main(String[] args) {
        // 1. Creating a non-generic HashMap
        Map myNonGenericMap = new HashMap();

        // 2. Adding different types of key-value pairs
        myNonGenericMap.put("Name", "Alice");       // String -> String
        myNonGenericMap.put(1, 100);                 // Integer -> Integer
        myNonGenericMap.put("Price", 99.99);         // String -> Double
        myNonGenericMap.put(true, "Boolean Key");    // Boolean -> String

        System.out.println("--- Non-Generic HashMap Content ---");

        // 3. Retrieving values (requires casting)
        String name = (String) myNonGenericMap.get("Name");
        System.out.println("Name: " + name);

        Integer number = (Integer) myNonGenericMap.get(1);
        System.out.println("Number: " + number);

        // Incorrect retrieval
        System.out.println("\n--- Demonstrating ClassCastException for Map Value ---");
        try {
            Double price = (Double) myNonGenericMap.get("Name"); // "Name" maps to a String, not Double
            System.out.println("This line won't be reached: " + price);
        } catch (ClassCastException e) {
            System.out.println("ERROR: Caught ClassCastException for value as expected!");
            System.out.println("Message: " + e.getMessage());
        }

        System.out.println("\n--- Iterating through Non-Generic HashMap (Old Style - EntrySet) ---");
        // 4. Iterating through the map's entry set
        // The Entry object itself is non-generic, so get methods return Object
        Set entrySet = myNonGenericMap.entrySet();
        Iterator entryIterator = entrySet.iterator();

        while (entryIterator.hasNext()) {
            Map.Entry entry = (Map.Entry) entryIterator.next(); // Cast to Map.Entry
            Object key = entry.getKey();   // Key is Object
            Object value = entry.getValue(); // Value is Object

            System.out.println("  Key Type: " + key.getClass().getName() +
                               ", Value Type: " + value.getClass().getName() +
                               " -> Key: " + key + ", Value: " + value);
        }
    }
}
```

**Compilation and Execution:**
```bash
javac NonGenericHashMapExample.java
java NonGenericHashMapExample
```

**Output:**

```text
--- Non-Generic HashMap Content ---
Name: Alice
Number: 100

--- Demonstrating ClassCastException for Map Value ---
ERROR: Caught ClassCastException for value as expected!
Message: java.lang.String cannot be cast to java.lang.Double

--- Iterating through Non-Generic HashMap (Old Style - EntrySet) ---
  Key Type: java.lang.Integer, Value Type: java.lang.Integer -> Key: 1, Value: 100
  Key Type: java.lang.String, Value Type: java.lang.String -> Key: Name, Value: Alice
  Key Type: java.lang.Boolean, Value Type: java.lang.String -> Key: true, Value: Boolean Key
  Key Type: java.lang.String, Value Type: java.lang.Double -> Key: Price, Value: 99.99
```
*(Note: The order of entries in a HashMap is not guaranteed).*

---

## Why Generics Were Introduced (Contrast)

Generics were introduced in Java 5 primarily to address the issues of type safety and verbosity in the Collections Framework.

**With Generics (`ArrayList<String>`):**

*   **Compile-time type safety:** `ArrayList<String>` can *only* hold `String` objects. The compiler enforces this.
*   **No `ClassCastException` at runtime:** When you retrieve an element using `myGenericList.get(0)`, it's already known to be a `String`, so no casting is needed, and `ClassCastException` for incorrect type is prevented at compile time.
*   **Cleaner code:** Less explicit casting makes code much more readable and maintainable.

**Example of a Generic `ArrayList` for comparison:**

```java
import java.util.ArrayList;
import java.util.List;

public class GenericArrayListExample {
    public static void main(String[] args) {
        // Generic ArrayList: only holds String objects
        List<String> myGenericList = new ArrayList<>();

        myGenericList.add("Hello");
        myGenericList.add("World");
        // myGenericList.add(123); // Compile-time error: The method add(String) is not applicable for the arguments (int)

        String s1 = myGenericList.get(0); // No cast needed
        System.out.println(s1);

        for (String s : myGenericList) { // Type-safe iteration
            System.out.println(s.toUpperCase());
        }
    }
}
```

## When You Might Encounter Non-Generic Collections

While you should **always prefer generics in new Java code**, you might still encounter non-generic collections in a few scenarios:

1.  **Legacy Codebases:** Older Java projects (pre-Java 5 or those not yet migrated) will extensively use non-generic collections.
2.  **Reflection:** When using Java Reflection to inspect or manipulate types at runtime, you often deal with `Object` and need to handle type casting manually.
3.  **Interoperability:** Occasionally, you might interact with very old libraries that return non-generic collection types.

## Conclusion

Non-generic collections in Java are a historical artifact from before Java 5. They expose fundamental weaknesses in type safety, leading to `ClassCastException` at runtime and verbose code. Generics were introduced specifically to solve these problems, providing compile-time type safety, eliminating the need for manual casting, and making code much more robust and readable.

**For any new Java development, always use generic collections.** They are a cornerstone of modern, safe, and efficient Java programming.