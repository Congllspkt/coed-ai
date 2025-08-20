The `LinkedHashMap` in Java is a fascinating and highly useful data structure that combines the best features of a `HashMap` and a `LinkedList`.

Let's dive into its details.

---

## LinkedHashMap in Java

### 1. Introduction

`LinkedHashMap` is a part of the Java Collections Framework and belongs to the `java.util` package. It extends `HashMap` and implements the `Map` interface.

The primary difference between `HashMap` and `LinkedHashMap` lies in **iteration order**:

*   **`HashMap`**: Does not guarantee any order for its elements; the order can even change over time.
*   **`LinkedHashMap`**: Maintains a **doubly-linked list** running through all of its entries. This means it preserves the order in which elements were inserted, or the order in which they were last accessed (depending on its configuration).

This combination provides the fast lookups of a hash table (`O(1)` on average for `get`, `put`, `remove`) while also offering predictable iteration order.

### 2. Key Features

*   **Order Guarantee**: Guarantees iteration order. By default, it maintains **insertion order**. It can also be configured to maintain **access order**.
*   **Performance**: Like `HashMap`, it provides `O(1)` (average time) performance for basic operations like `get`, `put`, `containsKey`, and `remove`.
*   **Nulls**: Allows one `null` key and multiple `null` values.
*   **Non-Synchronized**: It is not thread-safe. If multiple threads access a `LinkedHashMap` concurrently, and at least one of the threads modifies the map, it must be synchronized externally.
*   **Space Overhead**: It consumes more memory than a `HashMap` because of the additional overhead of the doubly-linked list used to maintain order.
*   **Inheritance**: Extends `java.util.HashMap`.

### 3. Internal Structure

`LinkedHashMap` maintains two data structures internally:

1.  **Hash Table (Array of Buckets)**: Inherited from `HashMap`, this is used for fast lookups based on hash codes.
2.  **Doubly-Linked List**: This list connects all the `Map.Entry` objects in the order they were inserted (or accessed). Each `Entry` object has `before` and `after` pointers in addition to the `key`, `value`, and `next` (for collision resolution in hash table) pointers.

### 4. Constructors

`LinkedHashMap` provides several constructors to allow different configurations:

1.  **`LinkedHashMap()`**:
    *   Constructs an empty `LinkedHashMap` with the default initial capacity (16) and load factor (0.75).
    *   Maintains **insertion order**.

    ```java
    LinkedHashMap<String, Integer> map = new LinkedHashMap<>();
    ```

2.  **`LinkedHashMap(int initialCapacity)`**:
    *   Constructs an empty `LinkedHashMap` with the specified initial capacity and the default load factor (0.75).
    *   Maintains **insertion order**.

    ```java
    LinkedHashMap<String, Integer> map = new LinkedHashMap<>(32);
    ```

3.  **`LinkedHashMap(int initialCapacity, float loadFactor)`**:
    *   Constructs an empty `LinkedHashMap` with the specified initial capacity and load factor.
    *   Maintains **insertion order**.

    ```java
    LinkedHashMap<String, Integer> map = new LinkedHashMap<>(32, 0.8f);
    ```

4.  **`LinkedHashMap(Map<? extends K, ? extends V> m)`**:
    *   Constructs a new `LinkedHashMap` with the same mappings as the specified `Map`.
    *   Maintains **insertion order**.

    ```java
    HashMap<String, Integer> otherMap = new HashMap<>();
    otherMap.put("A", 1);
    LinkedHashMap<String, Integer> map = new LinkedHashMap<>(otherMap);
    ```

5.  **`LinkedHashMap(int initialCapacity, float loadFactor, boolean accessOrder)`**:
    *   This is the most important constructor for `LinkedHashMap`'s unique behavior.
    *   Constructs an empty `LinkedHashMap` with the specified initial capacity, load factor, and **ordering mode**.
    *   If `accessOrder` is `true`, it maintains **access order** (LRU-like behavior).
    *   If `accessOrder` is `false`, it maintains **insertion order**.

    ```java
    // For insertion order (same as default behavior)
    LinkedHashMap<String, Integer> insertionOrderMap = new LinkedHashMap<>(16, 0.75f, false);

    // For access order (useful for LRU caches)
    LinkedHashMap<String, Integer> accessOrderMap = new LinkedHashMap<>(16, 0.75f, true);
    ```

### 5. Common Methods

`LinkedHashMap` inherits most of its methods from `HashMap`. The key difference is how these methods interact with the internal doubly-linked list for maintaining order.

*   `V put(K key, V value)`: Inserts a key-value mapping. If the key already exists, its value is updated. In insertion order, the position doesn't change. In access order, the entry moves to the end of the list.
*   `V get(Object key)`: Returns the value associated with the key. In insertion order, this has no effect on position. In access order, calling `get` on an existing key moves that entry to the "most recently accessed" end of the list.
*   `V remove(Object key)`: Removes the mapping for the specified key.
*   `boolean containsKey(Object key)`: Checks if the map contains the specified key.
*   `int size()`: Returns the number of key-value mappings.
*   `void clear()`: Removes all mappings.
*   `Set<K> keySet()`: Returns a `Set` view of the keys. The iteration order of this set will match the map's order.
*   `Collection<V> values()`: Returns a `Collection` view of the values. The iteration order of this collection will match the map's order.
*   `Set<Map.Entry<K, V>> entrySet()`: Returns a `Set` view of the mappings. The iteration order of this set will match the map's order.

### 6. Order Types in Detail

#### a) Insertion Order (Default)

*   This is the default behavior when you don't specify `accessOrder = true`.
*   Elements are ordered by the sequence in which their keys were *first inserted*.
*   If you `put` an existing key with a new value, its position in the linked list does **not** change.

#### b) Access Order (LRU Cache Behavior)

*   Activated by passing `true` for the `accessOrder` parameter in the constructor: `new LinkedHashMap<>(initialCapacity, loadFactor, true)`.
*   Elements are ordered by the sequence in which they were *last accessed*.
*   An access operation is defined as calling `get`, `put` (if the key already exists), or `putAll`.
*   When an existing entry is accessed (via `get` or `put`), it is moved to the "most recently accessed" end of the internal doubly-linked list.
*   This makes `LinkedHashMap` an excellent foundation for building **Least Recently Used (LRU) caches** by overriding the `removeEldestEntry` method.

### 7. When to Use `LinkedHashMap`

*   **Maintaining Insertion Order**: When you need a map where the order of elements (for iteration purposes) must be the order in which they were added.
*   **Implementing LRU Caches**: When you need a cache that automatically discards the least recently used items. `LinkedHashMap` with `accessOrder = true` and an overridden `removeEldestEntry` method is ideal for this.
*   **Predictable Iteration**: When you require predictable iteration order, unlike `HashMap` which provides no guarantees.
*   **Serialization/Deserialization**: If you serialize a `LinkedHashMap` and then deserialize it, the order will be preserved.

### 8. Disadvantages

*   **Memory Overhead**: It uses more memory than a `HashMap` due to the additional doubly-linked list pointers.
*   **Slightly Slower**: While still `O(1)` on average, the constant factor for operations might be slightly higher than `HashMap` due to the overhead of maintaining the linked list (updating pointers).

---

### 9. Examples

#### Example 1: Basic Insertion Order

This example demonstrates how `LinkedHashMap` preserves the order in which elements are first added.

**Java Code:**

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class LinkedHashMapInsertionOrderExample {

    public static void main(String[] args) {
        // Create a LinkedHashMap with default insertion order
        LinkedHashMap<String, Integer> scores = new LinkedHashMap<>();

        // 1. Add elements in a specific order
        System.out.println("--- Adding elements ---");
        scores.put("Alice", 90);
        System.out.println("Added: Alice -> 90. Map: " + scores);
        scores.put("Bob", 85);
        System.out.println("Added: Bob -> 85. Map: " + scores);
        scores.put("Charlie", 92);
        System.out.println("Added: Charlie -> 92. Map: " + scores);
        scores.put("David", 78);
        System.out.println("Added: David -> 78. Map: " + scores);

        // 2. Update an existing element - note that its position doesn't change
        System.out.println("\n--- Updating an existing element ---");
        scores.put("Bob", 88); // Bob's score updated, but his position remains the same
        System.out.println("Updated: Bob -> 88. Map: " + scores);

        // 3. Iterate over the map - observe the insertion order
        System.out.println("\n--- Iterating over elements (insertion order) ---");
        for (Map.Entry<String, Integer> entry : scores.entrySet()) {
            System.out.println("Name: " + entry.getKey() + ", Score: " + entry.getValue());
        }

        // 4. Removing an element
        System.out.println("\n--- Removing an element ---");
        scores.remove("Charlie");
        System.out.println("Removed: Charlie. Map: " + scores);

        System.out.println("\n--- Iterating after removal ---");
        for (Map.Entry<String, Integer> entry : scores.entrySet()) {
            System.out.println("Name: " + entry.getKey() + ", Score: " + entry.getValue());
        }
    }
}
```

**Input:** (No direct input, the data is hardcoded in the program)

```
N/A
```

**Output:**

```
--- Adding elements ---
Added: Alice -> 90. Map: {Alice=90}
Added: Bob -> 85. Map: {Alice=90, Bob=85}
Added: Charlie -> 92. Map: {Alice=90, Bob=85, Charlie=92}
Added: David -> 78. Map: {Alice=90, Bob=85, Charlie=92, David=78}

--- Updating an existing element ---
Updated: Bob -> 88. Map: {Alice=90, Bob=88, Charlie=92, David=78}

--- Iterating over elements (insertion order) ---
Name: Alice, Score: 90
Name: Bob, Score: 88
Name: Charlie, Score: 92
Name: David, Score: 78

--- Removing an element ---
Removed: Charlie. Map: {Alice=90, Bob=88, David=78}

--- Iterating after removal ---
Name: Alice, Score: 90
Name: Bob, Score: 88
Name: David, Score: 78
```

#### Example 2: Access Order (Simulating LRU Cache Behavior)

This example demonstrates how `LinkedHashMap` reorders elements based on access (using `get` or `put` on an existing key).

**Java Code:**

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class LinkedHashMapAccessOrderExample {

    public static void main(String[] args) {
        // Create a LinkedHashMap with access order enabled (last parameter is true)
        LinkedHashMap<String, Integer> cache = new LinkedHashMap<>(16, 0.75f, true);

        // 1. Add elements
        System.out.println("--- Initial Additions (Order: A, B, C, D) ---");
        cache.put("A", 1);
        cache.put("B", 2);
        cache.put("C", 3);
        cache.put("D", 4);
        printCache("Current Cache State:", cache);

        // 2. Access 'B' - 'B' should move to the end (most recently accessed)
        System.out.println("\n--- Accessing 'B' ---");
        cache.get("B"); // Access 'B'
        printCache("After get('B'):", cache); // Expected: A, C, D, B

        // 3. Access 'A' - 'A' should move to the end
        System.out.println("\n--- Accessing 'A' ---");
        cache.get("A"); // Access 'A'
        printCache("After get('A'):", cache); // Expected: C, D, B, A

        // 4. Update 'C' - this also counts as an access, 'C' moves to the end
        System.out.println("\n--- Updating 'C' ---");
        cache.put("C", 30); // Update 'C'
        printCache("After put('C', 30):", cache); // Expected: D, B, A, C

        // 5. Add a new element 'E' - it goes to the end
        System.out.println("\n--- Adding new element 'E' ---");
        cache.put("E", 5);
        printCache("After put('E', 5):", cache); // Expected: D, B, A, C, E

        // 6. Access 'D' again - 'D' moves to the very end
        System.out.println("\n--- Accessing 'D' again ---");
        cache.get("D");
        printCache("After get('D'):", cache); // Expected: B, A, C, E, D
    }

    private static void printCache(String message, LinkedHashMap<String, Integer> cache) {
        System.out.print(message + " {");
        boolean first = true;
        for (Map.Entry<String, Integer> entry : cache.entrySet()) {
            if (!first) {
                System.out.print(", ");
            }
            System.out.print(entry.getKey() + "=" + entry.getValue());
            first = false;
        }
        System.out.println("}");
    }
}
```

**Input:** (No direct input, the data is hardcoded in the program)

```
N/A
```

**Output:**

```
--- Initial Additions (Order: A, B, C, D) ---
Current Cache State: {A=1, B=2, C=3, D=4}

--- Accessing 'B' ---
After get('B'): {A=1, C=3, D=4, B=2}

--- Accessing 'A' ---
After get('A'): {C=3, D=4, B=2, A=1}

--- Updating 'C' ---
After put('C', 30): {D=4, B=2, A=1, C=30}

--- Adding new element 'E' ---
After put('E', 5): {D=4, B=2, A=1, C=30, E=5}

--- Accessing 'D' again ---
After get('D'): {B=2, A=1, C=30, E=5, D=4}
```

---

This detailed overview and examples should give you a solid understanding of `LinkedHashMap` and its capabilities in Java.