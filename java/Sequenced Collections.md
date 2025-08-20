In Java, `SequencedCollection` is a new interface introduced in **Java 21** as part of Project Loom's efforts to provide more robust and consistent APIs. It's designed to bring a unified way to access and manipulate elements at both ends of a collection, and to provide a consistent view of the collection in reverse order.

Before Java 21, if you wanted to get the first or last element, or add/remove elements from both ends, you had to rely on specific collection types (e.g., `Deque` for `LinkedList` and `ArrayDeque`, or `List` for `ArrayList`'s `get(0)` and `get(size-1)`). This led to inconsistent APIs and made it harder to write generic code that works across different sequential collections.

`SequencedCollection` aims to solve this by providing a common set of methods.

---

## Java's `SequencedCollection` (Java 21+)

### 1. What is `SequencedCollection`?

`SequencedCollection` is an interface that extends `java.util.Collection`. Its primary purpose is to define methods for accessing, adding, and removing elements at both the beginning and the end of a collection, and for obtaining a reversed view of the collection.

It unifies the "sequence" aspect that many collections inherently possess but lacked a common interface for manipulating.

### 2. Key Features and Concepts

*   **Defined Encounter Order:** Elements in a `SequencedCollection` have a predictable, well-defined order.
*   **Unified API for Ends:** Provides methods like `getFirst()`, `getLast()`, `addFirst()`, `addLast()`, `removeFirst()`, `removeLast()`.
*   **Reversed View:** Offers a `reversed()` method that returns another `SequencedCollection` representing a reverse-ordered view of the original. This is a *view*, meaning changes to the reversed collection are reflected in the original, and vice-versa.
*   **Polymorphism:** Allows you to write code that operates on `SequencedCollection` instances, without needing to know the specific underlying implementation (e.g., `ArrayList`, `LinkedList`, `LinkedHashSet`).

### 3. The `SequencedCollection` Interface Methods

`SequencedCollection<E>` extends `Collection<E>` and adds the following methods:

*   **`E getFirst()`**: Returns the first element in this collection. Throws `NoSuchElementException` if the collection is empty.
*   **`E getLast()`**: Returns the last element in this collection. Throws `NoSuchElementException` if the collection is empty.
*   **`void addFirst(E e)`**: Adds the given element to the beginning of this collection.
*   **`void addLast(E e)`**: Adds the given element to the end of this collection.
*   **`E removeFirst()`**: Removes and returns the first element from this collection. Throws `NoSuchElementException` if the collection is empty.
*   **`E removeLast()`**: Removes and returns the last element from this collection. Throws `NoSuchElementException` if the collection is empty.
*   **`SequencedCollection<E> reversed()`**: Returns a `SequencedCollection` which is a reverse-ordered view of this collection. Any modifications to the original collection are reflected in the reversed view, and vice-versa.

#### Implementations

In Java 21+, several existing collection classes have been updated to implement `SequencedCollection`:

*   `java.util.ArrayList`
*   `java.util.LinkedList`
*   `java.util.Vector`
*   `java.util.ArrayDeque`
*   `java.util.LinkedHashSet`
*   `java.util.Stack`
*   `java.util.concurrent.ConcurrentLinkedDeque`

### 4. Why Use `SequencedCollection`?

*   **Clarity and Readability:** Code becomes more explicit about its intent (e.g., `list.addFirst(element)` instead of `list.add(0, element)`).
*   **Consistency:** Provides a uniform API across different sequential collections, reducing the need for `instanceof` checks or casting.
*   **Easier API Discovery:** Developers don't have to guess which collection supports which "end-access" methods.
*   **Better Abstraction:** You can write methods that accept a `SequencedCollection` parameter, making them more general and reusable.
*   **Future-Proofing:** Code written against this interface will automatically benefit from any future optimizations or new implementations.

### 5. Examples

Let's demonstrate the usage of `SequencedCollection` with concrete examples.

#### Example 1: Basic Operations (`addFirst`, `addLast`, `getFirst`, `getLast`, `removeFirst`, `removeLast`)

This example uses `LinkedList` (which now implements `SequencedCollection`) to demonstrate adding, getting, and removing elements from both ends.

**`SequencedCollectionBasicOperations.java`**

```java
import java.util.LinkedList;
import java.util.SequencedCollection;
import java.util.NoSuchElementException;

public class SequencedCollectionBasicOperations {

    public static void main(String[] args) {

        System.out.println("--- Demonstrating SequencedCollection Basic Operations ---");

        // 1. Create a SequencedCollection (using LinkedList as an implementation)
        SequencedCollection<String> fruits = new LinkedList<>();

        // 2. Add elements using addLast and addFirst
        System.out.println("\nInitial state: " + fruits);
        fruits.addLast("Banana");  // Add to the end
        fruits.addLast("Orange");  // Add to the end
        System.out.println("After addLast(\"Banana\"), addLast(\"Orange\"): " + fruits); // [Banana, Orange]

        fruits.addFirst("Apple"); // Add to the beginning
        System.out.println("After addFirst(\"Apple\"): " + fruits); // [Apple, Banana, Orange]

        fruits.addFirst("Grape"); // Add another to the beginning
        System.out.println("After addFirst(\"Grape\"): " + fruits); // [Grape, Apple, Banana, Orange]

        // 3. Get first and last elements
        try {
            System.out.println("\nFirst element: " + fruits.getFirst()); // Grape
            System.out.println("Last element: " + fruits.getLast());   // Orange
        } catch (NoSuchElementException e) {
            System.out.println("Collection is empty.");
        }

        // 4. Remove elements from ends
        System.out.println("\nOriginal collection before removal: " + fruits); // [Grape, Apple, Banana, Orange]

        String removedFirst = fruits.removeFirst();
        System.out.println("Removed first element: " + removedFirst); // Grape
        System.out.println("Collection after removeFirst: " + fruits); // [Apple, Banana, Orange]

        String removedLast = fruits.removeLast();
        System.out.println("Removed last element: " + removedLast);   // Orange
        System.out.println("Collection after removeLast: " + fruits);  // [Apple, Banana]

        // 5. Demonstrate empty collection scenario
        System.out.println("\nClearing the collection...");
        fruits.removeFirst(); // Apple
        fruits.removeLast();  // Banana
        System.out.println("Collection after clearing: " + fruits); // []

        try {
            fruits.getFirst();
        } catch (NoSuchElementException e) {
            System.out.println("Attempted getFirst() on empty collection: " + e.getMessage());
        }

        try {
            fruits.removeLast();
        } catch (NoSuchElementException e) {
            System.out.println("Attempted removeLast() on empty collection: " + e.getMessage());
        }
    }
}
```

**Input:**
This code does not require specific console input. The input to the collection is hardcoded within the example.

**Output:**

```
--- Demonstrating SequencedCollection Basic Operations ---

Initial state: []
After addLast("Banana"), addLast("Orange"): [Banana, Orange]
After addFirst("Apple"): [Apple, Banana, Orange]
After addFirst("Grape"): [Grape, Apple, Banana, Orange]

First element: Grape
Last element: Orange

Original collection before removal: [Grape, Apple, Banana, Orange]
Removed first element: Grape
Collection after removeFirst: [Apple, Banana, Orange]
Removed last element: Orange
Collection after removeLast: [Apple, Banana]

Clearing the collection...
Collection after clearing: []
Attempted getFirst() on empty collection: No such element
Attempted removeLast() on empty collection: No such element
```

---

#### Example 2: `reversed()` View

This example demonstrates the `reversed()` method, showing that it returns a *view* and how modifications to the view affect the original collection. We'll use `ArrayList` here, which is now also a `SequencedCollection`.

**`SequencedCollectionReversedView.java`**

```java
import java.util.ArrayList;
import java.util.SequencedCollection;

public class SequencedCollectionReversedView {

    public static void main(String[] args) {

        System.out.println("--- Demonstrating SequencedCollection.reversed() ---");

        // 1. Create a SequencedCollection (using ArrayList)
        SequencedCollection<Integer> numbers = new ArrayList<>();
        numbers.addLast(10);
        numbers.addLast(20);
        numbers.addLast(30);
        numbers.addLast(40);
        System.out.println("\nOriginal Collection: " + numbers); // [10, 20, 30, 40]

        // 2. Get a reversed view
        SequencedCollection<Integer> reversedNumbers = numbers.reversed();
        System.out.println("Reversed View:     " + reversedNumbers); // [40, 30, 20, 10]

        // 3. Demonstrate accessing elements from the reversed view
        System.out.println("\nFirst element in reversed view: " + reversedNumbers.getFirst()); // 40
        System.out.println("Last element in reversed view:  " + reversedNumbers.getLast());  // 10

        // 4. Demonstrate modifications through the reversed view affecting the original
        System.out.println("\n--- Modifying through the reversed view ---");
        reversedNumbers.removeFirst(); // Removes 40 (which was the last in original)
        System.out.println("After removeFirst() on reversed view:");
        System.out.println("  Original Collection: " + numbers);       // [10, 20, 30]
        System.out.println("  Reversed View:     " + reversedNumbers); // [30, 20, 10]

        reversedNumbers.addLast(5); // Adds 5 to the end of reversed (which is the beginning of original)
        System.out.println("After addLast(5) on reversed view:");
        System.out.println("  Original Collection: " + numbers);       // [5, 10, 20, 30]
        System.out.println("  Reversed View:     " + reversedNumbers); // [30, 20, 10, 5]

        // 5. Demonstrate modifications to original affecting the reversed view
        System.out.println("\n--- Modifying the original collection ---");
        numbers.addFirst(0);
        System.out.println("After addFirst(0) on original collection:");
        System.out.println("  Original Collection: " + numbers);       // [0, 5, 10, 20, 30]
        System.out.println("  Reversed View:     " + reversedNumbers); // [30, 20, 10, 5, 0]

        numbers.removeLast();
        System.out.println("After removeLast() on original collection:");
        System.out.println("  Original Collection: " + numbers);       // [0, 5, 10, 20]
        System.out.println("  Reversed View:     " + reversedNumbers); // [20, 10, 5, 0]
    }
}
```

**Input:**
This code does not require specific console input. The collection elements and operations are defined programmatically.

**Output:**

```
--- Demonstrating SequencedCollection.reversed() ---

Original Collection: [10, 20, 30, 40]
Reversed View:     [40, 30, 20, 10]

First element in reversed view: 40
Last element in reversed view:  10

--- Modifying through the reversed view ---
After removeFirst() on reversed view:
  Original Collection: [10, 20, 30]
  Reversed View:     [30, 20, 10]
After addLast(5) on reversed view:
  Original Collection: [5, 10, 20, 30]
  Reversed View:     [30, 20, 10, 5]

--- Modifying the original collection ---
After addFirst(0) on original collection:
  Original Collection: [0, 5, 10, 20, 30]
  Reversed View:     [30, 20, 10, 5, 0]
After removeLast() on original collection:
  Original Collection: [0, 5, 10, 20]
  Reversed View:     [20, 10, 5, 0]
```

---

### 6. Important Considerations

*   **Java 21+ Required:** `SequencedCollection` is a new feature in Java 21. Your project must be compiled and run with Java 21 or later.
*   **`UnsupportedOperationException`**: Some underlying collection implementations might not support all `SequencedCollection` operations (e.g., an unmodifiable `SequencedCollection` would throw `UnsupportedOperationException` for `addFirst` or `removeLast`). This is similar to how `ArrayList`'s `add(index, element)` can be `O(n)`.
*   **`NoSuchElementException`**: `getFirst()`, `getLast()`, `removeFirst()`, and `removeLast()` will throw `NoSuchElementException` if called on an empty collection.
*   **Performance:** While `SequencedCollection` provides a unified API, the performance of these operations still depends on the underlying collection implementation. For instance, `addFirst()` on an `ArrayList` (which involves shifting all elements) will still be O(n), whereas on a `LinkedList` it will be O(1).
*   **`SequencedSet` and `SequencedMap`**: Along with `SequencedCollection`, Java 21 also introduced `SequencedSet` (which extends `SequencedCollection` and `Set`) and `SequencedMap` (a new interface for maps that maintain insertion order and allow end-access, like `LinkedHashMap`). This is part of a broader effort to standardize sequenced access across the Collections Framework.

### Conclusion

`SequencedCollection` is a valuable addition to the Java Collections Framework, bringing much-needed consistency and clarity to operations involving the ends of ordered collections. By providing a unified interface for these common tasks, it simplifies code, improves readability, and makes it easier to write more generic and robust Java applications. As you transition to Java 21 and beyond, adopting `SequencedCollection` and its related interfaces will be a good practice for modern Java development.