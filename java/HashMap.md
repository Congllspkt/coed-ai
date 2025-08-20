# HashMap in Java

`HashMap` is one of the most popular data structures in Java, part of the `java.util` package. It implements the `Map` interface, which means it stores data in **key-value pairs**. Each key is unique, and it maps to a specific value.

## 1. Core Concepts

### 1.1. Key-Value Pairs
At its heart, a `HashMap` is a collection of mappings from a unique key to a value.
*   **Key:** Used to identify and retrieve the associated value. Must be unique within the `HashMap`.
*   **Value:** The data associated with a specific key. Multiple keys can map to the same value.

### 1.2. How it Works (Under the Hood)
`HashMap` uses a concept called **hashing** to store and retrieve elements quickly.

1.  **Hashing:** When you put a key-value pair into a `HashMap`, the `hashCode()` method of the key object is called. This method returns an integer hash code.
2.  **Bucket/Bin:** This hash code is then used to determine the index (or "bucket") in an internal array where the key-value pair will be stored. The index is typically calculated as `hash_code % array_length`.
3.  **Collision Handling (Separate Chaining):** It's possible for two different keys to produce the same hash code, or for their hash codes to map to the same array index. This is called a **collision**. `HashMap` handles collisions using **separate chaining**. This means each bucket in the array actually points to a linked list (or a Red-Black tree in newer Java versions for performance). If a collision occurs, the new key-value pair is simply added to the linked list at that bucket.
4.  **Treeify Threshold (JDK 8+):** To prevent performance degradation when a linked list in a bucket becomes very long (due to many collisions), `HashMap` in JDK 8 and later automatically converts a linked list to a balanced Red-Black tree when the number of nodes in that bucket exceeds a certain threshold (default `TREEIFY_THRESHOLD = 8`). This improves worst-case lookup time from O(n) to O(log n). If the number of elements in a tree falls below a threshold (`UNTREEIFY_THRESHOLD = 6`), it converts back to a linked list.
5.  **Resizing (Rehashing):** When the number of elements in the `HashMap` exceeds `(capacity * load_factor)`, the internal array is resized (usually doubled), and all existing key-value pairs are rehashed into the new, larger array. This operation can be costly.

## 2. Key Characteristics

*   **Unordered:** `HashMap` does **not** guarantee any specific order of elements. The order can change over time, especially after operations like resizing. If you need insertion order, consider `LinkedHashMap`. If you need sorted order by key, consider `TreeMap`.
*   **Allows one `null` key:** A `HashMap` can have at most one `null` key.
*   **Allows multiple `null` values:** A `HashMap` can have multiple key-value pairs where the value is `null`.
*   **Not Synchronized:** `HashMap` is **not thread-safe**. If multiple threads access a `HashMap` concurrently and at least one of them modifies the map, it must be synchronized externally. Otherwise, it may lead to `ConcurrentModificationException` or other unpredictable behavior. For thread-safe alternatives, consider `ConcurrentHashMap` or `Collections.synchronizedMap()`.
*   **Performance:** Provides constant-time performance (O(1)) for basic operations like `get` and `put` on average, assuming a good hash function distributes elements evenly. In the worst case (e.g., all keys hash to the same bucket due to a poor hash function), performance degrades to O(n) for linked lists and O(log n) for trees.

## 3. Constructors

Commonly used constructors for `HashMap`:

*   `HashMap()`: Creates an empty `HashMap` with the default initial capacity (16) and load factor (0.75).
*   `HashMap(int initialCapacity)`: Creates an empty `HashMap` with the specified initial capacity and a default load factor of 0.75.
*   `HashMap(int initialCapacity, float loadFactor)`: Creates an empty `HashMap` with the specified initial capacity and load factor.
    *   **Initial Capacity:** The number of buckets in the internal array. Setting a higher initial capacity can reduce the need for rehashing if you know you'll store many elements.
    *   **Load Factor:** A measure of how full the `HashMap` can get before its capacity is automatically increased. A value of 0.75 means the map will be resized when it's 75% full. Lowering the load factor reduces collisions but increases space consumption; raising it saves space but increases collision probability.
*   `HashMap(Map<? extends K, ? extends V> m)`: Creates a new `HashMap` with the same mappings as the specified `Map`.

## 4. Key Methods

Here are some of the most frequently used methods:

*   **`V put(K key, V value)`**: Associates the specified value with the specified key in this map. If the map previously contained a mapping for the key, the old value is replaced. Returns the previous value associated with `key`, or `null` if there was no mapping for `key`.
*   **`V get(Object key)`**: Returns the value to which the specified key is mapped, or `null` if this map contains no mapping for the key.
*   **`V remove(Object key)`**: Removes the mapping for the specified key from this map if it is present. Returns the value to which this map previously associated the key, or `null` if the map contained no mapping for the key.
*   **`boolean containsKey(Object key)`**: Returns `true` if this map contains a mapping for the specified key.
*   **`boolean containsValue(Object value)`**: Returns `true` if this map maps one or more keys to the specified value.
*   **`int size()`**: Returns the number of key-value mappings in this map.
*   **`boolean isEmpty()`**: Returns `true` if this map contains no key-value mappings.
*   **`void clear()`**: Removes all of the mappings from this map.
*   **`Set<K> keySet()`**: Returns a `Set` view of the keys contained in this map.
*   **`Collection<V> values()`**: Returns a `Collection` view of the values contained in this map.
*   **`Set<Map.Entry<K, V>> entrySet()`**: Returns a `Set` view of the mappings contained in this map. This is typically the most efficient way to iterate over a `HashMap`.

## 5. Performance (Big O Notation)

*   **`put(K key, V value)`**:
    *   Average Case: O(1)
    *   Worst Case: O(n) (if all elements collide and form a long linked list) or O(log n) (if treeified)
*   **`get(Object key)`**:
    *   Average Case: O(1)
    *   Worst Case: O(n) (if all elements collide and form a long linked list) or O(log n) (if treeified)
*   **`remove(Object key)`**:
    *   Average Case: O(1)
    *   Worst Case: O(n) (if all elements collide and form a long linked list) or O(log n) (if treeified)
*   **Iteration (over `keySet()`, `values()`, or `entrySet()`):**
    *   O(n + capacity) - because it needs to iterate through all buckets, and then all elements within those buckets.

## 6. When to Use `HashMap`

*   When you need to store data as key-value pairs.
*   When you need fast average-case lookup, insertion, and deletion times (O(1)).
*   When the order of elements does not matter.
*   When you need to allow `null` keys and `null` values.

## 7. When Not to Use `HashMap`

*   When you need the elements to be sorted by their keys (use `TreeMap`).
*   When you need the elements to maintain insertion order (use `LinkedHashMap`).
*   When you need a thread-safe map for concurrent access (use `ConcurrentHashMap` or `Collections.synchronizedMap()`).

## 8. Example Usage

This example demonstrates the common operations of a `HashMap` for managing a simple inventory (item name -> quantity).

```java
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class HashMapExample {

    public static void main(String[] args) {

        // 1. Creating a HashMap
        System.out.println("--- 1. Creating a HashMap ---");
        Map<String, Integer> inventory = new HashMap<>();
        System.out.println("Initial inventory map: " + inventory); // Output: {}
        System.out.println("Is inventory empty? " + inventory.isEmpty()); // Output: true
        System.out.println("Inventory size: " + inventory.size());     // Output: 0

        System.out.println("\n--- 2. Adding elements (put) ---");
        // Using put(key, value)
        inventory.put("Laptop", 10);
        inventory.put("Mouse", 50);
        inventory.put("Keyboard", 25);
        inventory.put("Monitor", 15);
        System.out.println("Inventory after adding items: " + inventory);
        // Example Output: {Mouse=50, Laptop=10, Monitor=15, Keyboard=25}
        // Note: Order is not guaranteed and might vary.

        // Adding an item that already exists (updates the value)
        System.out.println("\n--- 3. Updating an element (put) ---");
        Integer oldQuantity = inventory.put("Laptop", 8); // Laptop quantity was 10, now 8
        System.out.println("Updated quantity for Laptop. Old quantity: " + oldQuantity); // Output: 10
        System.out.println("Inventory after updating Laptop: " + inventory);
        // Example Output: {Mouse=50, Laptop=8, Monitor=15, Keyboard=25}

        // Adding a null key and null value
        System.out.println("\n--- 4. Adding null key and value ---");
        inventory.put(null, 999); // One null key allowed
        inventory.put("Charger", null); // Multiple null values allowed
        System.out.println("Inventory after adding nulls: " + inventory);
        // Example Output: {null=999, Mouse=50, Laptop=8, Monitor=15, Keyboard=25, Charger=null}

        System.out.println("\n--- 5. Retrieving elements (get) ---");
        // Using get(key)
        System.out.println("Quantity of Mouse: " + inventory.get("Mouse"));     // Output: 50
        System.out.println("Quantity of Monitor: " + inventory.get("Monitor"));   // Output: 15
        System.out.println("Quantity of null key: " + inventory.get(null));    // Output: 999
        System.out.println("Quantity of non-existent item (Speaker): " + inventory.get("Speaker")); // Output: null

        System.out.println("\n--- 6. Checking for existence (containsKey, containsValue) ---");
        // Using containsKey(key)
        System.out.println("Does inventory contain Keyboard? " + inventory.containsKey("Keyboard")); // Output: true
        System.out.println("Does inventory contain Tablet? " + inventory.containsKey("Tablet"));   // Output: false

        // Using containsValue(value)
        System.out.println("Does inventory contain item with quantity 50? " + inventory.containsValue(50)); // Output: true
        System.out.println("Does inventory contain item with quantity 100? " + inventory.containsValue(100)); // Output: false

        System.out.println("\n--- 7. Removing elements (remove) ---");
        // Using remove(key)
        Integer removedQuantity = inventory.remove("Keyboard");
        System.out.println("Removed Keyboard with quantity: " + removedQuantity); // Output: 25
        System.out.println("Inventory after removing Keyboard: " + inventory);
        // Example Output: {null=999, Mouse=50, Laptop=8, Monitor=15, Charger=null}

        Integer removedNonExistent = inventory.remove("Projector");
        System.out.println("Removed non-existent Projector: " + removedNonExistent); // Output: null

        System.out.println("\n--- 8. Size and isEmpty ---");
        System.out.println("Current inventory size: " + inventory.size()); // Output: 5 (Laptop, Mouse, Monitor, null, Charger)
        System.out.println("Is inventory empty? " + inventory.isEmpty());     // Output: false

        System.out.println("\n--- 9. Iterating through HashMap ---");

        // Option A: Using entrySet() (most efficient for both key and value)
        System.out.println("--- Iterating using entrySet() ---");
        for (Map.Entry<String, Integer> entry : inventory.entrySet()) {
            System.out.println("Item: " + entry.getKey() + ", Quantity: " + entry.getValue());
        }
        /* Example Output: (Order may vary)
        Item: null, Quantity: 999
        Item: Mouse, Quantity: 50
        Item: Laptop, Quantity: 8
        Item: Monitor, Quantity: 15
        Item: Charger, Quantity: null
        */

        // Option B: Using keySet() (if you only need keys, then get values)
        System.out.println("\n--- Iterating using keySet() ---");
        Set<String> itemNames = inventory.keySet();
        for (String itemName : itemNames) {
            System.out.println("Item: " + itemName + ", Quantity: " + inventory.get(itemName));
        }

        // Option C: Using values() (if you only need values)
        System.out.println("\n--- Iterating using values() ---");
        Collection<Integer> quantities = inventory.values();
        for (Integer quantity : quantities) {
            System.out.println("Quantity: " + quantity);
        }

        System.out.println("\n--- 10. Clearing the HashMap (clear) ---");
        inventory.clear();
        System.out.println("Inventory after clearing: " + inventory);     // Output: {}
        System.out.println("Is inventory empty? " + inventory.isEmpty()); // Output: true
        System.out.println("Inventory size: " + inventory.size());         // Output: 0
    }
}
```

### Input:
The input is implicitly defined by the Java code itself, as values are hardcoded into the `HashMap` operations. There's no external user input.

### Output:
The output will be printed to the console as the program executes. Due to the unordered nature of `HashMap`, the exact order of elements in printed maps (e.g., `System.out.println("Inventory after adding items: " + inventory);`) might vary slightly across different runs or JVM versions, but the key-value pairs themselves will be consistent.

```text
--- 1. Creating a HashMap ---
Initial inventory map: {}
Is inventory empty? true
Inventory size: 0

--- 2. Adding elements (put) ---
Inventory after adding items: {Mouse=50, Laptop=10, Monitor=15, Keyboard=25}

--- 3. Updating an element (put) ---
Updated quantity for Laptop. Old quantity: 10
Inventory after updating Laptop: {Mouse=50, Laptop=8, Monitor=15, Keyboard=25}

--- 4. Adding null key and value ---
Inventory after adding nulls: {null=999, Mouse=50, Laptop=8, Monitor=15, Keyboard=25, Charger=null}

--- 5. Retrieving elements (get) ---
Quantity of Mouse: 50
Quantity of Monitor: 15
Quantity of null key: 999
Quantity of non-existent item (Speaker): null

--- 6. Checking for existence (containsKey, containsValue) ---
Does inventory contain Keyboard? true
Does inventory contain Tablet? false
Does inventory contain item with quantity 50? true
Does inventory contain item with quantity 100? false

--- 7. Removing elements (remove) ---
Removed Keyboard with quantity: 25
Inventory after removing Keyboard: {null=999, Mouse=50, Laptop=8, Monitor=15, Charger=null}
Removed non-existent Projector: null

--- 8. Size and isEmpty ---
Current inventory size: 5
Is inventory empty? false

--- 9. Iterating through HashMap ---
--- Iterating using entrySet() ---
Item: null, Quantity: 999
Item: Mouse, Quantity: 50
Item: Laptop, Quantity: 8
Item: Monitor, Quantity: 15
Item: Charger, Quantity: null

--- Iterating using keySet() ---
Item: null, Quantity: 999
Item: Mouse, Quantity: 50
Item: Laptop, Quantity: 8
Item: Monitor, Quantity: 15
Item: Charger, Quantity: null

--- Iterating using values() ---
Quantity: 999
Quantity: 50
Quantity: 8
Quantity: 15
Quantity: null

--- 10. Clearing the HashMap (clear) ---
Inventory after clearing: {}
Is inventory empty? true
Inventory size: 0
```

## 9. Best Practices and Tips

*   **Override `hashCode()` and `equals()`:** If you use custom objects as keys in a `HashMap`, you **must** override both the `hashCode()` and `equals()` methods.
    *   **`hashCode()`:** Ensures that equal objects produce the same hash code.
    *   **`equals()`:** Ensures that `HashMap` can correctly identify duplicate keys and retrieve values.
    *   **Contract:** The contract states: If two objects are equal according to the `equals(Object)` method, then calling the `hashCode` method on each of the two objects must produce the same integer result. It is not required that if two objects are unequal, then calling the `hashCode` method on each of the two objects must produce distinct integer results.
*   **Immutable Keys:** Using immutable objects (like `String`, `Integer`, `Double`, etc.) as keys is highly recommended. If a mutable object is used as a key and its state (which affects its `hashCode()`) changes *after* it's put into the map, you may lose the ability to retrieve the associated value.
*   **Initial Capacity and Load Factor:** For large `HashMaps` or performance-critical applications, fine-tuning the `initialCapacity` and `loadFactor` can minimize rehashing operations, which are expensive. If you know the approximate number of elements, set `initialCapacity` to `(expected_elements / load_factor) + 1`.
*   **Thread Safety:** Remember that `HashMap` is not thread-safe. If your application involves multiple threads accessing and modifying a `HashMap`, consider using `java.util.concurrent.ConcurrentHashMap` or using `Collections.synchronizedMap()`. `ConcurrentHashMap` is generally preferred for concurrent scenarios as it offers better scalability than `Collections.synchronizedMap()`.

## Conclusion

`HashMap` is a cornerstone data structure in Java, offering excellent performance for storing and retrieving key-value pairs. Its efficiency stems from its hashing mechanism. Understanding its internal workings, characteristics, and best practices is crucial for writing robust and performant Java applications.