# Introduction to TreeMap in Java

## Table of Contents
1.  [What is TreeMap?](#1-what-is-treemap)
2.  [Key Characteristics](#2-key-characteristics)
3.  [When to Use TreeMap](#3-when-to-use-treemap)
4.  [When Not to Use TreeMap](#4-when-not-to-use-treemap)
5.  [Constructors](#5-constructors)
6.  [Common Methods and Examples](#6-common-methods-and-examples)
    *   `put()`
    *   `get()`
    *   `containsKey()`
    *   `remove()`
    *   `size()` & `isEmpty()`
    *   `keySet()`, `values()`, `entrySet()`
    *   `firstKey()`, `lastKey()`
    *   `floorKey()`, `ceilingKey()`, `lowerKey()`, `higherKey()`
    *   `headMap()`, `tailMap()`, `subMap()`
7.  [Iterating Through TreeMap](#7-iterating-through-treemap)
8.  [Custom Sorting with Comparator](#8-custom-sorting-with-comparator)
9.  [TreeMap vs. HashMap](#9-treemap-vs-hashmap)
10. [Conclusion](#10-conclusion)

---

## 1. What is TreeMap?

In Java, `TreeMap` is a class that implements the `NavigableMap` interface, which in turn extends the `SortedMap` and `Map` interfaces. It is a **key-value pair collection** where the elements are **sorted by their keys** in natural ascending order or by a custom `Comparator` provided at the time of its creation.

`TreeMap` is backed by a **Red-Black Tree** data structure, which ensures logarithmic time performance for most operations like `put`, `get`, `remove`, and `containsKey`.

## 2. Key Characteristics

*   **Sorted Order:** The primary feature of `TreeMap` is that it stores elements in a **sorted order based on the keys**. By default, it uses the natural ordering of the keys. If the keys don't have a natural ordering (i.e., they don't implement `Comparable`) or you want a different order, you must provide a `Comparator`.
*   **No Null Keys:** `TreeMap` **does not allow `null` keys**. Attempting to insert a `null` key will result in a `NullPointerException`.
*   **Null Values Allowed:** `TreeMap` **allows `null` values**. You can associate a `null` value with any non-null key.
*   **Performance:** Operations like `put`, `get`, `remove`, and `containsKey` have a time complexity of **O(log n)**, where 'n' is the number of elements in the map. This is due to the balanced binary tree structure (Red-Black Tree).
*   **`NavigableMap` Features:** As it implements `NavigableMap`, it provides methods for navigating the map, such as `firstKey()`, `lastKey()`, `floorKey()`, `ceilingKey()`, `higherKey()`, `lowerKey()`, and sub-map views like `headMap()`, `tailMap()`, and `subMap()`.
*   **Not Synchronized:** `TreeMap` is **not thread-safe**. If multiple threads access a `TreeMap` concurrently and at least one thread modifies the map, it must be synchronized externally. This is typically done by wrapping it with `Collections.synchronizedSortedMap()` or by using a `ConcurrentSkipListMap` (which is thread-safe and also provides sorted order).

## 3. When to Use TreeMap

*   **When you need sorted data:** The most common use case is when you need your key-value pairs to be stored and retrieved in a specific order based on the keys.
*   **Range-based operations:** When you need to retrieve a subset of the map based on a key range (e.g., all entries with keys between X and Y).
*   **Finding nearest elements:** When you need to find the element just greater than or less than a given key.
*   **Natural ordering:** When your keys naturally implement `Comparable` and you want them sorted this way.
*   **Custom ordering:** When you need to define a specific sorting logic for your keys using a `Comparator`.

## 4. When Not to Use TreeMap

*   **When insertion/lookup speed is paramount and order doesn't matter:** If `O(1)` average time complexity for basic operations (like `HashMap` offers) is more critical than sorted order, `HashMap` is a better choice.
*   **When insertion order needs to be preserved:** If you need to maintain the order in which elements were inserted, consider `LinkedHashMap`.
*   **When `null` keys are required:** Since `TreeMap` does not allow `null` keys, `HashMap` would be suitable if you need to store a `null` key.
*   **For very small datasets:** The overhead of maintaining the Red-Black Tree might make it slightly slower than `HashMap` for very small numbers of elements, though the difference is usually negligible.

## 5. Constructors

`TreeMap` offers several constructors:

1.  **`TreeMap()`:** Constructs a new, empty tree map, ordered according to the natural ordering of its keys. The keys must implement the `Comparable` interface.
    ```java
    TreeMap<Integer, String> treeMap1 = new TreeMap<>();
    ```

2.  **`TreeMap(Comparator<? super K> comparator)`:** Constructs a new, empty tree map, ordered according to the given comparator.
    ```java
    // Example: Order strings by length
    TreeMap<String, Integer> treeMap2 = new TreeMap<>(
        (s1, s2) -> Integer.compare(s1.length(), s2.length())
    );
    ```

3.  **`TreeMap(Map<? extends K, ? extends V> m)`:** Constructs a new tree map containing the same mappings as the given map, ordered according to the natural ordering of its keys.
    ```java
    import java.util.HashMap;
    import java.util.Map;

    Map<Integer, String> hashMap = new HashMap<>();
    hashMap.put(3, "C");
    hashMap.put(1, "A");
    hashMap.put(2, "B");

    TreeMap<Integer, String> treeMap3 = new TreeMap<>(hashMap);
    // treeMap3 will contain {1=A, 2=B, 3=C}
    ```

4.  **`TreeMap(SortedMap<K, ? extends V> m)`:** Constructs a new tree map containing the same mappings and using the same ordering as the specified sorted map.
    ```java
    import java.util.SortedMap;
    import java.util.TreeMap;

    SortedMap<Integer, String> existingSortedMap = new TreeMap<>();
    existingSortedMap.put(10, "Ten");
    existingSortedMap.put(20, "Twenty");

    TreeMap<Integer, String> treeMap4 = new TreeMap<>(existingSortedMap);
    // treeMap4 will contain {10=Ten, 20=Twenty} and use the same comparator if any
    ```

## 6. Common Methods and Examples

Let's illustrate the most commonly used `TreeMap` methods with Java code examples.

### `put()`
Associates the specified value with the specified key in this map.

```java
import java.util.TreeMap;

public class TreeMapPutExample {
    public static void main(String[] args) {
        TreeMap<Integer, String> students = new TreeMap<>();

        System.out.println("Initial TreeMap: " + students);

        // put elements
        students.put(101, "Alice");
        students.put(103, "Charlie");
        students.put(102, "Bob");
        students.put(100, "David"); // Will be first due to sorted order

        System.out.println("TreeMap after puts: " + students);

        // Putting an existing key updates the value
        students.put(101, "Alicia");
        System.out.println("TreeMap after updating 101: " + students);

        // Put null value (allowed)
        students.put(104, null);
        System.out.println("TreeMap after putting null value for 104: " + students);

        // Attempting to put null key (throws NullPointerException)
        try {
            students.put(null, "Invalid");
        } catch (NullPointerException e) {
            System.out.println("Caught exception for null key: " + e.getMessage());
        }
    }
}
```

**Input:** (Implicit in code)
```
Initial TreeMap: {}
TreeMap after puts: {100=David, 101=Alice, 102=Bob, 103=Charlie}
TreeMap after updating 101: {100=David, 101=Alicia, 102=Bob, 103=Charlie}
TreeMap after putting null value for 104: {100=David, 101=Alicia, 102=Bob, 103=Charlie, 104=null}
Caught exception for null key: null
```

### `get()`
Returns the value to which the specified key is mapped, or `null` if this map contains no mapping for the key.

```java
import java.util.TreeMap;

public class TreeMapGetExample {
    public static void main(String[] args) {
        TreeMap<Integer, String> scores = new TreeMap<>();
        scores.put(85, "Alice");
        scores.put(92, "Bob");
        scores.put(78, "Charlie");

        System.out.println("TreeMap: " + scores);

        String student1 = scores.get(92);
        System.out.println("Score 92 maps to: " + student1);

        String student2 = scores.get(100); // Key not present
        System.out.println("Score 100 maps to: " + student2);
    }
}
```

**Input:** (Implicit in code)
```
TreeMap: {78=Charlie, 85=Alice, 92=Bob}
Score 92 maps to: Bob
Score 100 maps to: null
```

### `containsKey()`
Returns `true` if this map contains a mapping for the specified key.

```java
import java.util.TreeMap;

public class TreeMapContainsKeyExample {
    public static void main(String[] args) {
        TreeMap<String, String> capitals = new TreeMap<>();
        capitals.put("USA", "Washington D.C.");
        capitals.put("France", "Paris");
        capitals.put("Japan", "Tokyo");

        System.out.println("TreeMap: " + capitals);

        boolean hasUSA = capitals.containsKey("USA");
        System.out.println("Does TreeMap contain USA? " + hasUSA);

        boolean hasGermany = capitals.containsKey("Germany");
        System.out.println("Does TreeMap contain Germany? " + hasGermany);
    }
}
```

**Input:** (Implicit in code)
```
TreeMap: {France=Paris, Japan=Tokyo, USA=Washington D.C.}
Does TreeMap contain USA? true
Does TreeMap contain Germany? false
```

### `remove()`
Removes the mapping for the specified key from this map if it is present.

```java
import java.util.TreeMap;

public class TreeMapRemoveExample {
    public static void main(String[] args) {
        TreeMap<String, Integer> productStocks = new TreeMap<>();
        productStocks.put("Laptop", 10);
        productStocks.put("Mouse", 50);
        productStocks.put("Keyboard", 25);
        productStocks.put("Monitor", 15);

        System.out.println("Initial TreeMap: " + productStocks);

        Integer removedStock1 = productStocks.remove("Mouse");
        System.out.println("Removed stock for Mouse: " + removedStock1);
        System.out.println("TreeMap after removing Mouse: " + productStocks);

        Integer removedStock2 = productStocks.remove("Webcam"); // Key not present
        System.out.println("Removed stock for Webcam: " + removedStock2);
        System.out.println("TreeMap after removing Webcam: " + productStocks);
    }
}
```

**Input:** (Implicit in code)
```
Initial TreeMap: {Keyboard=25, Laptop=10, Monitor=15, Mouse=50}
Removed stock for Mouse: 50
TreeMap after removing Mouse: {Keyboard=25, Laptop=10, Monitor=15}
Removed stock for Webcam: null
TreeMap after removing Webcam: {Keyboard=25, Laptop=10, Monitor=15}
```

### `size()` & `isEmpty()`
`size()` returns the number of key-value mappings in this map.
`isEmpty()` returns `true` if this map contains no key-value mappings.

```java
import java.util.TreeMap;

public class TreeMapSizeEmptyExample {
    public static void main(String[] args) {
        TreeMap<String, Double> prices = new TreeMap<>();

        System.out.println("Is prices map empty? " + prices.isEmpty());
        System.out.println("Size of prices map: " + prices.size());

        prices.put("Apple", 1.50);
        prices.put("Banana", 0.75);

        System.out.println("Is prices map empty after adding elements? " + prices.isEmpty());
        System.out.println("Size of prices map after adding elements: " + prices.size());

        prices.clear(); // Removes all mappings
        System.out.println("Is prices map empty after clear? " + prices.isEmpty());
        System.out.println("Size of prices map after clear: " + prices.size());
    }
}
```

**Input:** (Implicit in code)
```
Is prices map empty? true
Size of prices map: 0
Is prices map empty after adding elements? false
Size of prices map after adding elements: 2
Is prices map empty after clear? true
Size of prices map after clear: 0
```

### `keySet()`, `values()`, `entrySet()`
These methods provide different views of the map's contents:
*   `keySet()`: Returns a `Set` view of the keys contained in this map.
*   `values()`: Returns a `Collection` view of the values contained in this map.
*   `entrySet()`: Returns a `Set` view of the mappings contained in this map. Each element in the set is a `Map.Entry<K, V>`.

```java
import java.util.TreeMap;
import java.util.Set;
import java.util.Collection;
import java.util.Map;

public class TreeMapViewsExample {
    public static void main(String[] args) {
        TreeMap<Integer, String> students = new TreeMap<>();
        students.put(101, "Alice");
        students.put(103, "Charlie");
        students.put(102, "Bob");

        System.out.println("TreeMap: " + students);

        // Get keys
        Set<Integer> studentIds = students.keySet();
        System.out.println("Keys (student IDs): " + studentIds);

        // Get values
        Collection<String> studentNames = students.values();
        System.out.println("Values (student names): " + studentNames);

        // Get entries
        Set<Map.Entry<Integer, String>> entries = students.entrySet();
        System.out.println("Entries (key-value pairs): " + entries);
    }
}
```

**Input:** (Implicit in code)
```
TreeMap: {101=Alice, 102=Bob, 103=Charlie}
Keys (student IDs): [101, 102, 103]
Values (student names): [Alice, Bob, Charlie]
Entries (key-value pairs): [101=Alice, 102=Bob, 103=Charlie]
```

### `firstKey()`, `lastKey()`
Returns the first (lowest) and last (highest) key currently in this map.

```java
import java.util.TreeMap;

public class TreeMapFirstLastKeyExample {
    public static void main(String[] args) {
        TreeMap<Integer, String> ranks = new TreeMap<>();
        ranks.put(5, "Gold");
        ranks.put(1, "Bronze");
        ranks.put(10, "Diamond");
        ranks.put(3, "Silver");

        System.out.println("TreeMap: " + ranks);

        System.out.println("First key (lowest rank): " + ranks.firstKey());
        System.out.println("Last key (highest rank): " + ranks.lastKey());

        // You can also get the corresponding entry:
        System.out.println("First entry: " + ranks.firstEntry());
        System.out.println("Last entry: " + ranks.lastEntry());
    }
}
```

**Input:** (Implicit in code)
```
TreeMap: {1=Bronze, 3=Silver, 5=Gold, 10=Diamond}
First key (lowest rank): 1
Last key (highest rank): 10
First entry: 1=Bronze
Last entry: 10=Diamond
```

### `floorKey()`, `ceilingKey()`, `lowerKey()`, `higherKey()`
These methods are part of the `NavigableMap` interface and are very useful for finding keys relative to a given key.

*   **`floorKey(K key)`:** Returns the greatest key less than or equal to `key`, or `null` if there is no such key.
*   **`ceilingKey(K key)`:** Returns the least key greater than or equal to `key`, or `null` if there is no such key.
*   **`lowerKey(K key)`:** Returns the greatest key strictly less than `key`, or `null` if there is no such key.
*   **`higherKey(K key)`:** Returns the least key strictly greater than `key`, or `null` if there is no such key.

```java
import java.util.TreeMap;

public class TreeMapNavigableKeysExample {
    public static void main(String[] args) {
        TreeMap<Integer, String> map = new TreeMap<>();
        map.put(10, "A");
        map.put(20, "B");
        map.put(30, "C");
        map.put(40, "D");

        System.out.println("TreeMap: " + map);

        // Using 25 as the search key
        System.out.println("\nSearching around key 25:");
        System.out.println("floorKey(25): " + map.floorKey(25));   // Greatest key <= 25 (20)
        System.out.println("ceilingKey(25): " + map.ceilingKey(25)); // Least key >= 25 (30)
        System.out.println("lowerKey(25): " + map.lowerKey(25));   // Greatest key < 25 (20)
        System.out.println("higherKey(25): " + map.higherKey(25)); // Least key > 25 (30)

        // Using 20 (an existing key) as the search key
        System.out.println("\nSearching around key 20 (existing):");
        System.out.println("floorKey(20): " + map.floorKey(20));   // Greatest key <= 20 (20)
        System.out.println("ceilingKey(20): " + map.ceilingKey(20)); // Least key >= 20 (20)
        System.out.println("lowerKey(20): " + map.lowerKey(20));   // Greatest key < 20 (10)
        System.out.println("higherKey(20): " + map.higherKey(20)); // Least key > 20 (30)

        // Edge cases
        System.out.println("\nEdge cases:");
        System.out.println("floorKey(5): " + map.floorKey(5));     // No key <= 5 (null)
        System.out.println("ceilingKey(45): " + map.ceilingKey(45)); // No key >= 45 (null)
        System.out.println("lowerKey(10): " + map.lowerKey(10));   // No key < 10 (null)
        System.out.println("higherKey(40): " + map.higherKey(40)); // No key > 40 (null)
    }
}
```

**Input:** (Implicit in code)
```
TreeMap: {10=A, 20=B, 30=C, 40=D}

Searching around key 25:
floorKey(25): 20
ceilingKey(25): 30
lowerKey(25): 20
higherKey(25): 30

Searching around key 20 (existing):
floorKey(20): 20
ceilingKey(20): 20
lowerKey(20): 10
higherKey(20): 30

Edge cases:
floorKey(5): null
ceilingKey(45): null
lowerKey(10): null
higherKey(40): null
```

### `headMap()`, `tailMap()`, `subMap()`
These methods return `SortedMap` or `NavigableMap` views of portions of this map. Changes to the returned map are reflected in the original map, and vice versa.

*   **`headMap(K toKey)` / `headMap(K toKey, boolean inclusive)`:** Returns a view of the portion of this map whose keys are strictly less than (or less than or equal to, if inclusive is true) `toKey`.
*   **`tailMap(K fromKey)` / `tailMap(K fromKey, boolean inclusive)`:** Returns a view of the portion of this map whose keys are greater than or equal to (or strictly greater than, if inclusive is false) `fromKey`.
*   **`subMap(K fromKey, K toKey)` / `subMap(K fromKey, boolean fromInclusive, K toKey, boolean toInclusive)`:** Returns a view of the portion of this map whose keys range from `fromKey` to `toKey`. The `fromKey` is inclusive, and `toKey` is exclusive by default (or can be controlled by `inclusive` booleans).

```java
import java.util.TreeMap;
import java.util.NavigableMap;
import java.util.SortedMap;

public class TreeMapSubMapExample {
    public static void main(String[] args) {
        TreeMap<Integer, String> grades = new TreeMap<>();
        grades.put(95, "Alice");
        grades.put(88, "Bob");
        grades.put(72, "Charlie");
        grades.put(90, "David");
        grades.put(75, "Eve");
        grades.put(80, "Frank");

        System.out.println("Original TreeMap: " + grades); // {72=Charlie, 75=Eve, 80=Frank, 88=Bob, 90=David, 95=Alice}

        // 1. headMap() - keys strictly less than 85
        SortedMap<Integer, String> below85 = grades.headMap(85);
        System.out.println("Students with grades < 85: " + below85);

        // headMap() - keys less than or equal to 88
        NavigableMap<Integer, String> belowOrEq88 = grades.headMap(88, true);
        System.out.println("Students with grades <= 88: " + belowOrEq88);

        // 2. tailMap() - keys greater than or equal to 90
        SortedMap<Integer, String> aboveOrEq90 = grades.tailMap(90);
        System.out.println("Students with grades >= 90: " + aboveOrEq90);

        // tailMap() - keys strictly greater than 88
        NavigableMap<Integer, String> strictlyAbove88 = grades.tailMap(88, false);
        System.out.println("Students with grades > 88: " + strictlyAbove88);

        // 3. subMap() - keys from 75 (inclusive) to 90 (exclusive)
        SortedMap<Integer, String> between75and90Exclusive = grades.subMap(75, 90);
        System.out.println("Students with grades [75, 90): " + between75and90Exclusive);

        // subMap() - keys from 75 (inclusive) to 90 (inclusive)
        NavigableMap<Integer, String> between75and90Inclusive = grades.subMap(75, true, 90, true);
        System.out.println("Students with grades [75, 90]: " + between75and90Inclusive);

        // Modifying a sub-map affects the original map
        System.out.println("\nModifying sub-map...");
        between75and90Inclusive.remove(88); // Remove Bob
        System.out.println("Original TreeMap after sub-map remove: " + grades);
    }
}
```

**Input:** (Implicit in code)
```
Original TreeMap: {72=Charlie, 75=Eve, 80=Frank, 88=Bob, 90=David, 95=Alice}
Students with grades < 85: {72=Charlie, 75=Eve, 80=Frank}
Students with grades <= 88: {72=Charlie, 75=Eve, 80=Frank, 88=Bob}
Students with grades >= 90: {90=David, 95=Alice}
Students with grades > 88: {90=David, 95=Alice}
Students with grades [75, 90): {75=Eve, 80=Frank, 88=Bob}
Students with grades [75, 90]: {75=Eve, 80=Frank, 88=Bob, 90=David}

Modifying sub-map...
Original TreeMap after sub-map remove: {72=Charlie, 75=Eve, 80=Frank, 90=David, 95=Alice}
```

## 7. Iterating Through TreeMap

You can iterate over a `TreeMap` using its `entrySet()`, `keySet()`, or `values()` methods, typically with a for-each loop. The iteration will always follow the sorted order of the keys.

```java
import java.util.TreeMap;
import java.util.Map;

public class TreeMapIterationExample {
    public static void main(String[] args) {
        TreeMap<String, String> phoneBook = new TreeMap<>();
        phoneBook.put("Charlie", "555-1111");
        phoneBook.put("Alice", "555-2222");
        phoneBook.put("Bob", "555-3333");

        System.out.println("--- Iterating by Entry (Key-Value Pairs) ---");
        for (Map.Entry<String, String> entry : phoneBook.entrySet()) {
            System.out.println("Name: " + entry.getKey() + ", Phone: " + entry.getValue());
        }

        System.out.println("\n--- Iterating by Keys Only ---");
        for (String name : phoneBook.keySet()) {
            System.out.println("Name: " + name);
        }

        System.out.println("\n--- Iterating by Values Only ---");
        for (String phoneNumber : phoneBook.values()) {
            System.out.println("Phone: " + phoneNumber);
        }
    }
}
```

**Input:** (Implicit in code)
```
--- Iterating by Entry (Key-Value Pairs) ---
Name: Alice, Phone: 555-2222
Name: Bob, Phone: 555-3333
Name: Charlie, Phone: 555-1111

--- Iterating by Keys Only ---
Name: Alice
Name: Bob
Name: Charlie

--- Iterating by Values Only ---
Phone: 555-2222
Phone: 555-3333
Phone: 555-1111
```

## 8. Custom Sorting with Comparator

If the keys of your `TreeMap` do not implement `Comparable` or you want a different sorting order than the natural one, you can provide a `Comparator` object to the `TreeMap` constructor.

```java
import java.util.Comparator;
import java.util.TreeMap;

public class TreeMapCustomSortingExample {

    // Custom Comparator to sort strings by length (shortest first),
    // then alphabetically if lengths are equal
    static class StringLengthComparator implements Comparator<String> {
        @Override
        public int compare(String s1, String s2) {
            int lengthCompare = Integer.compare(s1.length(), s2.length());
            if (lengthCompare != 0) {
                return lengthCompare;
            }
            // If lengths are equal, sort alphabetically
            return s1.compareTo(s2);
        }
    }

    public static void main(String[] args) {
        // Create a TreeMap with the custom comparator
        TreeMap<String, Integer> wordCounts = new TreeMap<>(new StringLengthComparator());

        wordCounts.put("Apple", 5);
        wordCounts.put("Banana", 3);
        wordCounts.put("Cat", 8);
        wordCounts.put("Dog", 10);
        wordCounts.put("Zoo", 1);
        wordCounts.put("Elephant", 2);
        wordCounts.put("Bird", 7);
        wordCounts.put("Ape", 6); // Same length as Cat, Dog, Zoo, Bird, Ape. Sorted alphabetically among them.

        System.out.println("TreeMap sorted by custom StringLengthComparator:");
        for (Map.Entry<String, Integer> entry : wordCounts.entrySet()) {
            System.out.println(entry.getKey() + " (length: " + entry.getKey().length() + ") => " + entry.getValue());
        }

        System.out.println("\n--- Alternative: Using a Lambda Comparator ---");
        // Using a lambda expression for sorting strings by reverse alphabetical order
        TreeMap<String, Integer> reverseOrderMap = new TreeMap<>((s1, s2) -> s2.compareTo(s1));

        reverseOrderMap.put("Zebra", 1);
        reverseOrderMap.put("Apple", 2);
        reverseOrderMap.put("Banana", 3);
        reverseOrderMap.put("Cat", 4);

        System.out.println("TreeMap sorted by reverse alphabetical order:");
        for (Map.Entry<String, Integer> entry : reverseOrderMap.entrySet()) {
            System.out.println(entry.getKey() + " => " + entry.getValue());
        }
    }
}
```

**Input:** (Implicit in code)
```
TreeMap sorted by custom StringLengthComparator:
Ape (length: 3) => 6
Bird (length: 4) => 7
Cat (length: 3) => 8
Dog (length: 3) => 10
Zoo (length: 3) => 1
Apple (length: 5) => 5
Banana (length: 6) => 3
Elephant (length: 8) => 2

--- Alternative: Using a Lambda Comparator ---
TreeMap sorted by reverse alphabetical order:
Zebra => 1
Cat => 4
Banana => 3
Apple => 2
```
**Note:** In the `StringLengthComparator` example, notice how "Cat", "Dog", "Zoo", "Ape", "Bird" (all length 3 or 4) are then sorted alphabetically *among themselves* because of the `s1.compareTo(s2)` fallback.

## 9. TreeMap vs. HashMap

Here's a quick comparison to help you choose between `TreeMap` and `HashMap`:

| Feature             | `HashMap`                                        | `TreeMap`                                         |
| :------------------ | :----------------------------------------------- | :------------------------------------------------ |
| **Order**           | No guaranteed order; elements are not sorted.    | **Sorted by keys** (natural or custom comparator). |
| **Null Keys**       | Allows one `null` key.                           | **Does not allow `null` keys**.                   |
| **Null Values**     | Allows multiple `null` values.                   | Allows multiple `null` values.                    |
| **Performance**     | **O(1)** average for `put`, `get`, `remove`.     | **O(log n)** for `put`, `get`, `remove`.          |
| **Underlying Data Structure** | Hash Table                                       | Red-Black Tree (a self-balancing Binary Search Tree) |
| **Memory**          | Generally uses less memory per entry (no tree nodes). | Slightly more memory overhead due to tree nodes. |
| **Interface**       | Implements `Map`                                 | Implements `NavigableMap` (extends `SortedMap`, `Map`) |
| **Use Cases**       | Fast lookups, when order doesn't matter.         | When sorted order is essential, range queries, finding nearest keys. |
| **Thread Safety**   | Not synchronized (use `ConcurrentHashMap` for concurrent access). | Not synchronized (use `ConcurrentSkipListMap` for concurrent access or `Collections.synchronizedSortedMap`). |

## 10. Conclusion

`TreeMap` is a powerful and versatile data structure in Java, particularly useful when the sorted order of keys is a fundamental requirement of your application. While it incurs a logarithmic performance cost compared to the constant time average performance of `HashMap`, its unique capabilities for ordered iteration, range views, and navigational operations often justify this trade-off. Understanding its underlying Red-Black Tree implementation helps appreciate its balanced performance characteristics.