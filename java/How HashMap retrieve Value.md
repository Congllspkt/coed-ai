To understand how `HashMap` retrieves a value in Java, you need to grasp its internal structure and the role of `hashCode()` and `equals()` methods.

---

# How HashMap Retrieves Value in Java

`HashMap` is a part of Java's Collections Framework that implements the `Map` interface. It stores data in key-value pairs. It provides an average time complexity of **O(1)** for basic operations like `get()`, `put()`, `remove()`, and `containsKey()`, assuming a good hash function and minimal collisions. In the worst-case scenario (many collisions, poor hash function), it can degrade to **O(n)**.

## Core Concepts

Before diving into retrieval, let's understand the fundamental concepts:

1.  **Hashing:** The process of converting a given key into an integer value (hash code). This hash code is then used to determine the storage location (bucket) for the key-value pair.
2.  **Buckets (Bins):** `HashMap` internally uses an array of `Node` objects (or `Entry` in older Java versions). Each index in this array is called a "bucket."
3.  **Collision:** When two different keys produce the same hash code or map to the same bucket index, it's called a collision.
4.  **Collision Resolution:** `HashMap` resolves collisions primarily using:
    *   **Linked Lists:** If multiple entries map to the same bucket, they are stored as a linked list within that bucket.
    *   **Red-Black Trees (Java 8+):** If a linked list in a bucket becomes too long (typically > 8 nodes), `HashMap` converts it into a Red-Black Tree for better performance (O(log n) instead of O(n) for traversal within that bucket). This is called "treefication."
5.  **`hashCode()` Method:** Defined in `Object` class. It returns an integer hash code for the object. `HashMap` uses this to find the initial bucket.
    *   **Contract:** If two objects are equal according to the `equals()` method, then calling the `hashCode()` method on each of the two objects *must* produce the same integer result.
6.  **`equals()` Method:** Defined in `Object` class. It determines if two objects are logically equal. `HashMap` uses this to compare keys within a bucket to find the exact match.
    *   **Contract:** If two objects are equal according to `equals()`, their hash codes *must* be equal. If their hash codes are different, they *cannot* be equal.

## How `get()` Method Works in HashMap

When you call `map.get(key)`:

1.  **Calculate Hash of the Key:**
    *   The `get()` method first takes the `key` you provide and calls its `hashCode()` method.
    *   `HashMap` then performs an internal `hash()` function (which typically involves XORing the hash code with its higher bits) on the result from `key.hashCode()`. This is done to improve the distribution of hash values and reduce collisions, especially for poorly designed `hashCode()` implementations.

    ```java
    // Simplified internal hash function logic (actual is more complex)
    static final int hash(Object key) {
        int h;
        return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
    }
    ```

2.  **Determine the Bucket Index:**
    *   The resulting `hash` value is then used to calculate the index of the bucket in the internal array (`table`). This is typically done using a bitwise AND operation: `(table.length - 1) & hash`. This is an optimized way to perform a modulo operation (`hash % table.length`) when the `table.length` is always a power of 2.

    ```java
    // Simplified index calculation
    int index = (table.length - 1) & hash;
    ```

3.  **Navigate to the Bucket and Traverse:**
    *   The `HashMap` goes to the `index` calculated in the previous step.
    *   It retrieves the `Node` (or `Entry`) at that bucket.

4.  **Key Comparison (Handling Collisions):**
    *   **Check for `null` key:** If the `key` passed to `get()` is `null`, it's a special case. `null` keys always map to bucket `0`.
    *   **Traverse the Chain/Tree:** If the bucket is not empty, `HashMap` iterates through the elements (nodes) in that bucket.
        *   **Linked List Scenario:** If the bucket contains a linked list, it traverses each `Node` in the list. For each `Node`, it performs a two-step check:
            1.  **Hash Match:** It first checks if the `hash` value of the current `Node` matches the `hash` calculated for the target `key`. This is a fast preliminary check.
            2.  **Key Equality (`equals()`):** If the hashes match, it then performs a full key comparison using the `equals()` method: `(currentKey == targetKey || targetKey.equals(currentKey))`.
                *   `currentKey == targetKey`: Checks for reference equality (same object in memory).
                *   `targetKey.equals(currentKey)`: Checks for logical equality if they are different objects but represent the same value.
        *   **Red-Black Tree Scenario:** If the bucket has "treefied" into a Red-Black Tree (due to many collisions), the retrieval traverses the tree (which is faster than a long linked list) using the hash and `compareTo()` or `equals()` method to find the correct node.

5.  **Return Value:**
    *   If a matching `key` is found (both hash and `equals()` return true), the `value` associated with that `Node` is returned.
    *   If the iteration/traversal completes without finding a matching key, `null` is returned, indicating the key is not present in the map.

## Internal Data Structure Visualization

```
+----------------+
|  HashMap Array |
|   (Buckets)    |
+----------------+
| [0]            | ---> null (or Node if null key is present)
+----------------+
| [1]            | ---> Node1 (hash1, key1, value1) -> null
+----------------+
| [2]            | ---> Node2 (hash2, key2, value2)
|                |      |
|                |      V
|                |   Node3 (hash3, key3, value3)  -- Collision! (Linked List)
|                |      |
|                |      V
|                |   Node4 (hash4, key4, value4)  -- Collision!
+----------------+
| ...            |
+----------------+
| [N-1]          | ---> NodeX (hashX, keyX, valueX) -> RedBlackTreeNode... (Treefied)
+----------------+
```

## Importance of `hashCode()` and `equals()`

*   **Correctness:** If you use custom objects as keys in a `HashMap`, you *must* correctly override both `hashCode()` and `equals()`.
    *   If `equals()` says two objects are equal but `hashCode()` returns different values, `HashMap` might store them in different buckets, leading to `get()` failing to retrieve a value that *is* present.
    *   If you only override `equals()` but not `hashCode()`, `HashMap` will use the default `hashCode()` (often based on memory address), causing the same issue.
*   **Performance:** A good `hashCode()` distributes keys evenly across buckets, minimizing collisions and keeping operations close to O(1). A poor `hashCode()` (e.g., one that always returns a constant value) will put all keys into one bucket, degenerating `HashMap` into a linked list (or tree), making operations O(n) or O(log n).

---

## Example (Input, Output)

Let's illustrate with a simple Java example.

```java
import java.util.HashMap;
import java.util.Map;

public class HashMapRetrievalExample {

    public static void main(String[] args) {

        // 1. Create a HashMap
        Map<String, Integer> fruitPrices = new HashMap<>();

        // 2. Populate the HashMap (Input Data)
        System.out.println("--- Populating the HashMap ---");
        fruitPrices.put("Apple", 100);
        System.out.println("Added: Key='Apple', Value=100");
        fruitPrices.put("Banana", 50);
        System.out.println("Added: Key='Banana', Value=50");
        fruitPrices.put("Orange", 75);
        System.out.println("Added: Key='Orange', Value=75");
        fruitPrices.put("Grape", 120);
        System.out.println("Added: Key='Grape', Value=120");
        fruitPrices.put(null, 0); // Demonstrating null key
        System.out.println("Added: Key=null, Value=0");

        System.out.println("\n--- Retrieving Values ---");

        // 3. Retrieve values using the get() method
        // Retrieval 1: Existing key "Apple"
        String key1 = "Apple";
        Integer price1 = fruitPrices.get(key1);
        System.out.println("Input: get(\"" + key1 + "\")");
        System.out.println("Output: Price of " + key1 + ": " + price1); // Expected: 100

        // Retrieval 2: Existing key "Orange"
        String key2 = "Orange";
        Integer price2 = fruitPrices.get(key2);
        System.out.println("\nInput: get(\"" + key2 + "\")");
        System.out.println("Output: Price of " + key2 + ": " + price2); // Expected: 75

        // Retrieval 3: Non-existing key "Mango"
        String key3 = "Mango";
        Integer price3 = fruitPrices.get(key3);
        System.out.println("\nInput: get(\"" + key3 + "\")");
        System.out.println("Output: Price of " + key3 + ": " + price3); // Expected: null

        // Retrieval 4: Null key
        Integer price4 = fruitPrices.get(null);
        System.out.println("\nInput: get(null)");
        System.out.println("Output: Price for null key: " + price4); // Expected: 0

        // Retrieval 5: Another existing key "Banana"
        String key5 = new String("Banana"); // A new String object, but logically equal to the one put in.
        Integer price5 = fruitPrices.get(key5);
        System.out.println("\nInput: get(new String(\"Banana\"))");
        System.out.println("Output: Price of " + key5 + ": " + price5); // Expected: 50
        System.out.println("Explanation: Even though 'new String(\"Banana\")' creates a different object instance,");
        System.out.println("             String's hashCode() and equals() methods ensure correct retrieval.");
    }
}
```

### Input (Code Execution)

You would compile and run the `HashMapRetrievalExample.java` file.

```bash
javac HashMapRetrievalExample.java
java HashMapRetrievalExample
```

### Output (Console)

```
--- Populating the HashMap ---
Added: Key='Apple', Value=100
Added: Key='Banana', Value=50
Added: Key='Orange', Value=75
Added: Key='Grape', Value=120
Added: Key=null, Value=0

--- Retrieving Values ---
Input: get("Apple")
Output: Price of Apple: 100

Input: get("Orange")
Output: Price of Orange: 75

Input: get("Mango")
Output: Price of Mango: null

Input: get(null)
Output: Price for null key: 0

Input: get(new String("Banana"))
Output: Price of Banana: 50
Explanation: Even though 'new String("Banana")' creates a different object instance,
             String's hashCode() and equals() methods ensure correct retrieval.
```

---

This detailed explanation covers the internal mechanics of `HashMap` retrieval, the roles of `hashCode()` and `equals()`, and provides a practical example with clear input and output.