# Creating Immutable Maps in Java

Immutable maps are collections that, once created, cannot be modified. This means you cannot add, remove, or update entries in the map after its creation. Java provides several ways to create immutable maps, ranging from older utility classes to modern factory methods introduced in Java 9 and 10.

## Why Use Immutable Maps?

Using immutable maps offers several significant advantages:

1.  **Thread Safety:** Immutable objects are inherently thread-safe. Since their state cannot change, multiple threads can access them concurrently without needing synchronization, eliminating common concurrency bugs.
2.  **Predictability:** The content of an immutable map is guaranteed to remain the same throughout its lifecycle, making your code easier to reason about and debug.
3.  **Safer Sharing:** You can pass immutable maps around your application or even across different parts of a system without worrying about them being accidentally modified by other components. This is crucial for defensive programming.
4.  **Used as Map Keys:** If you need to use a `Map` as a key in another `Map` or as an element in a `Set`, it should ideally be immutable, as its `hashCode()` and `equals()` contract must remain stable.
5.  **Caching:** Immutable objects are excellent candidates for caching, as their hash code never changes, and their content is stable.

## Methods to Create Immutable Maps

Let's explore the primary ways to create immutable maps in Java, along with detailed examples.

---

### 1. `Collections.unmodifiableMap()` (Legacy but Still Useful)

This method wraps an existing mutable `Map` and returns an unmodifiable *view* of it. Any attempt to modify the returned map will result in an `UnsupportedOperationException`.

**Important Note:** The "immutability" provided by `Collections.unmodifiableMap()` is a **view-only immutability**. If the *original* underlying map is modified, the unmodifiable view will reflect those changes. This means it's not truly immutable unless the original map is also no longer referenced or accessible.

**Example:**

```java
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class UnmodifiableMapExample {

    public static void main(String[] args) {

        // --- Input: Create a mutable HashMap ---
        System.out.println("--- Using Collections.unmodifiableMap() ---");
        Map<String, Integer> mutableMap = new HashMap<>();
        mutableMap.put("Apple", 10);
        mutableMap.put("Banana", 20);
        mutableMap.put("Orange", 30);
        System.out.println("Original Mutable Map: " + mutableMap);

        // --- Create an unmodifiable view ---
        Map<String, Integer> unmodifiableMap = Collections.unmodifiableMap(mutableMap);
        System.out.println("Unmodifiable View: " + unmodifiableMap);

        // --- Output: Attempting to modify the unmodifiable view ---
        System.out.println("\nAttempting to add to unmodifiableMap...");
        try {
            unmodifiableMap.put("Grape", 40); // This will throw an exception
        } catch (UnsupportedOperationException e) {
            System.out.println("Caught Expected Exception: " + e.getMessage());
        }
        System.out.println("Unmodifiable View after failed add: " + unmodifiableMap);

        System.out.println("\nAttempting to remove from unmodifiableMap...");
        try {
            unmodifiableMap.remove("Apple"); // This will throw an exception
        } catch (UnsupportedOperationException e) {
            System.out.println("Caught Expected Exception: " + e.getMessage());
        }
        System.out.println("Unmodifiable View after failed remove: " + unmodifiableMap);

        // --- Output: Demonstrating the "view-only" nature ---
        System.out.println("\n--- Modifying the original mutable map ---");
        mutableMap.put("Pineapple", 50); // Modify the original map
        mutableMap.remove("Banana");      // Modify the original map
        System.out.println("Original Mutable Map after modification: " + mutableMap);
        System.out.println("Unmodifiable View reflects changes: " + unmodifiableMap); // Unmodifiable view also changes!

        // --- Accessing elements ---
        System.out.println("\nAccessing elements from unmodifiableMap:");
        System.out.println("Orange count: " + unmodifiableMap.get("Orange"));
        System.out.println("Pineapple count: " + unmodifiableMap.get("Pineapple"));
        System.out.println("Banana count (removed): " + unmodifiableMap.get("Banana")); // Will be null
    }
}
```

**Output:**

```
--- Using Collections.unmodifiableMap() ---
Original Mutable Map: {Apple=10, Banana=20, Orange=30}
Unmodifiable View: {Apple=10, Banana=20, Orange=30}

Attempting to add to unmodifiableMap...
Caught Expected Exception: null
Unmodifiable View after failed add: {Apple=10, Banana=20, Orange=30}

Attempting to remove from unmodifiableMap...
Caught Expected Exception: null
Unmodifiable View after failed remove: {Apple=10, Banana=20, Orange=30}

--- Modifying the original mutable map ---
Original Mutable Map after modification: {Apple=10, Orange=30, Pineapple=50}
Unmodifiable View reflects changes: {Apple=10, Orange=30, Pineapple=50}

Accessing elements from unmodifiableMap:
Orange count: 30
Pineapple count: 50
Banana count (removed): null
```

---

### 2. `Map.of()` and `Map.ofEntries()` (Java 9+)

Introduced in Java 9, these static factory methods create truly immutable maps. The maps created by these methods are optimized for memory and performance.

*   `Map.of()`: Convenient for creating maps with a small number of key-value pairs (up to 10 pairs).
*   `Map.ofEntries()`: Used for maps with more than 10 key-value pairs, or when you want to build the map dynamically using `Map.entry()`.

**Key Characteristics:**
*   Truly immutable: Cannot be modified after creation.
*   Do not allow `null` keys or `null` values. Attempting to use them will result in a `NullPointerException`.
*   Optimized for small maps.

**Example:**

```java
import java.util.Map;
import java.util.Map.Entry; // For Map.entry()

public class MapOfExample {

    public static void main(String[] args) {

        System.out.println("--- Using Map.of() ---");
        // --- Input: Create an immutable map using Map.of() ---
        Map<String, String> mapOfColors = Map.of(
            "Red", "#FF0000",
            "Green", "#00FF00",
            "Blue", "#0000FF"
        );
        System.out.println("Map.of() created map: " + mapOfColors);

        // --- Output: Attempting to modify Map.of() map ---
        System.out.println("\nAttempting to add to mapOfColors...");
        try {
            mapOfColors.put("Yellow", "#FFFF00"); // This will throw an exception
        } catch (UnsupportedOperationException e) {
            System.out.println("Caught Expected Exception: " + e.getMessage());
        }
        System.out.println("Map after failed add: " + mapOfColors);

        // --- Output: Demonstrating null key/value restriction ---
        System.out.println("\nAttempting to create Map.of() with null key...");
        try {
            Map<String, String> mapWithNullKey = Map.of("Null", "Value", null, "AnotherValue");
        } catch (NullPointerException e) {
            System.out.println("Caught Expected Exception: " + e.getMessage());
        }

        System.out.println("\nAttempting to create Map.of() with null value...");
        try {
            Map<String, String> mapWithNullValue = Map.of("Key", "Value", "AnotherKey", null);
        } catch (NullPointerException e) {
            System.out.println("Caught Expected Exception: " + e.getMessage());
        }

        System.out.println("\n--- Using Map.ofEntries() ---");
        // --- Input: Create an immutable map using Map.ofEntries() ---
        Map<String, Integer> mapOfScores = Map.ofEntries(
            Map.entry("Alice", 95),
            Map.entry("Bob", 88),
            Map.entry("Charlie", 92),
            Map.entry("David", 78),
            Map.entry("Eve", 100),
            Map.entry("Frank", 85),
            Map.entry("Grace", 90),
            Map.entry("Heidi", 97),
            Map.entry("Ivan", 80),
            Map.entry("Judy", 93),
            Map.entry("Kyle", 75) // More than 10 entries, Map.ofEntries is suitable
        );
        System.out.println("Map.ofEntries() created map: " + mapOfScores);

        // --- Output: Attempting to modify Map.ofEntries() map ---
        System.out.println("\nAttempting to add to mapOfScores...");
        try {
            mapOfScores.put("Liam", 89); // This will throw an exception
        } catch (UnsupportedOperationException e) {
            System.out.println("Caught Expected Exception: " + e.getMessage());
        }
        System.out.println("Map after failed add: " + mapOfScores);

        // --- Accessing elements ---
        System.out.println("\nAccessing elements from mapOfColors:");
        System.out.println("Red: " + mapOfColors.get("Red"));
        System.out.println("\nAccessing elements from mapOfScores:");
        System.out.println("Alice's score: " + mapOfScores.get("Alice"));
        System.out.println("Kyle's score: " + mapOfScores.get("Kyle"));
    }
}
```

**Output:**

```
--- Using Map.of() ---
Map.of() created map: {Blue=#0000FF, Red=#FF0000, Green=#00FF00}

Attempting to add to mapOfColors...
Caught Expected Exception: null
Map after failed add: {Blue=#0000FF, Red=#FF0000, Green=#00FF00}

Attempting to create Map.of() with null key...
Caught Expected Exception: null keys not allowed
Attempting to create Map.of() with null value...
Caught Expected Exception: null values not allowed

--- Using Map.ofEntries() ---
Map.ofEntries() created map: {Alice=95, Kyle=75, Frank=85, Ivan=80, Bob=88, Heidi=97, Judy=93, David=78, Charlie=92, Grace=90, Eve=100}

Attempting to add to mapOfScores...
Caught Expected Exception: null
Map after failed add: {Alice=95, Kyle=75, Frank=85, Ivan=80, Bob=88, Heidi=97, Judy=93, David=78, Charlie=92, Grace=90, Eve=100}

Accessing elements from mapOfColors:
Red: #FF0000

Accessing elements from mapOfScores:
Alice's score: 95
Kyle's score: 75
```

---

### 3. `Map.copyOf()` (Java 10+)

Introduced in Java 10, `Map.copyOf()` creates a truly immutable map containing all entries from a given map. This is useful when you have an existing map (mutable or immutable) and want to create an immutable snapshot of it.

**Key Characteristics:**
*   Creates a new, truly immutable map.
*   Does not allow `null` keys or `null` values in the source map. If the source map contains them, it will throw a `NullPointerException`.
*   Performs a **shallow copy**. If the values in the original map are mutable objects, those objects themselves can still be modified, even though the map structure (keys and their associated value *references*) cannot change.

**Example:**

```java
import java.util.HashMap;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;

public class MapCopyOfExample {

    public static void main(String[] args) {

        System.out.println("--- Using Map.copyOf() ---");

        // --- Input: Create a mutable map ---
        Map<String, Integer> mutableScores = new HashMap<>();
        mutableScores.put("StudentA", 85);
        mutableScores.put("StudentB", 92);
        System.out.println("Original Mutable Map: " + mutableScores);

        // --- Create an immutable copy using Map.copyOf() ---
        Map<String, Integer> immutableScores = Map.copyOf(mutableScores);
        System.out.println("Immutable Copy: " + immutableScores);

        // --- Output: Attempting to modify the immutable copy ---
        System.out.println("\nAttempting to add to immutableScores...");
        try {
            immutableScores.put("StudentC", 78); // This will throw an exception
        } catch (UnsupportedOperationException e) {
            System.out.println("Caught Expected Exception: " + e.getMessage());
        }
        System.out.println("Immutable Copy after failed add: " + immutableScores);

        // --- Output: Modifying the original mutable map (does NOT affect the copy) ---
        System.out.println("\n--- Modifying the original mutable map ---");
        mutableScores.put("StudentC", 78);
        mutableScores.remove("StudentA");
        System.out.println("Original Mutable Map after modification: " + mutableScores);
        System.out.println("Immutable Copy remains unchanged: " + immutableScores); // Immutable copy is separate

        // --- Demonstrating shallow copy ---
        System.out.println("\n--- Demonstrating shallow copy with mutable values ---");
        Map<String, List<String>> mutableListsMap = new HashMap<>();
        List<String> fruits = new ArrayList<>();
        fruits.add("Apple");
        fruits.add("Banana");
        mutableListsMap.put("Fruits", fruits);

        List<String> veggies = new ArrayList<>();
        veggies.add("Carrot");
        mutableListsMap.put("Veggies", veggies);
        System.out.println("Original Map with mutable list values: " + mutableListsMap);

        Map<String, List<String>> immutableListsMap = Map.copyOf(mutableListsMap);
        System.out.println("Immutable Copy of map (shallow): " + immutableListsMap);

        // Modify a list within the original mutable map's value
        fruits.add("Orange"); // This modifies the 'fruits' list
        System.out.println("\nModified original 'fruits' list directly:");
        System.out.println("Original Map: " + mutableListsMap);
        System.out.println("Immutable Copy: " + immutableListsMap); // Immutable copy's list reference points to the same modified list!

        // --- Output: Demonstrating null key/value restriction ---
        System.out.println("\nAttempting to create Map.copyOf() from map with null value...");
        Map<String, String> mapWithNull = new HashMap<>();
        mapWithNull.put("Key1", "Value1");
        mapWithNull.put("Key2", null); // Contains a null value
        try {
            Map<String, String> copyOfNullMap = Map.copyOf(mapWithNull);
        } catch (NullPointerException e) {
            System.out.println("Caught Expected Exception: " + e.getMessage());
        }

        // --- Accessing elements ---
        System.out.println("\nAccessing elements from immutableScores:");
        System.out.println("StudentB score: " + immutableScores.get("StudentB"));
    }
}
```

**Output:**

```
--- Using Map.copyOf() ---
Original Mutable Map: {StudentA=85, StudentB=92}
Immutable Copy: {StudentA=85, StudentB=92}

Attempting to add to immutableScores...
Caught Expected Exception: null
Immutable Copy after failed add: {StudentA=85, StudentB=92}

--- Modifying the original mutable map ---
Original Mutable Map after modification: {StudentB=92, StudentC=78}
Immutable Copy remains unchanged: {StudentA=85, StudentB=92}

--- Demonstrating shallow copy with mutable values ---
Original Map with mutable list values: {Fruits=[Apple, Banana], Veggies=[Carrot]}
Immutable Copy of map (shallow): {Fruits=[Apple, Banana], Veggies=[Carrot]}

Modified original 'fruits' list directly:
Original Map: {Fruits=[Apple, Banana, Orange], Veggies=[Carrot]}
Immutable Copy: {Fruits=[Apple, Banana, Orange], Veggies=[Carrot]}

Attempting to create Map.copyOf() from map with null value...
Caught Expected Exception: null values not allowed
```

---

## Choosing the Right Method

*   **`Collections.unmodifiableMap()`**:
    *   **Use when:** You need to return an unmodifiable *view* of an existing mutable map, but the underlying map might still be modified elsewhere.
    *   **Caveat:** Not truly immutable if the original map can be changed.
    *   **Nulls:** Allows null keys/values if the underlying map does.

*   **`Map.of()` / `Map.ofEntries()` (Java 9+)**:
    *   **Use when:** You want to create a new, small, truly immutable map from scratch.
    *   **Benefits:** Excellent performance and memory efficiency for small maps.
    *   **Caveat:** No `null` keys or values allowed. `Map.of()` has a limit of 10 key-value pairs.

*   **`Map.copyOf()` (Java 10+)**:
    *   **Use when:** You have an existing map (mutable or immutable) and want to create a *new, truly immutable snapshot* of its current state.
    *   **Benefits:** Creates a completely independent immutable map.
    *   **Caveats:** No `null` keys or values allowed in the source map. Performs a shallow copy, meaning mutable *values* inside the map can still be changed.

## Deep Immutability Considerations

All the standard Java immutable map methods (including `Map.copyOf()`, `Map.of()`, `Collections.unmodifiableMap()`) provide **shallow immutability**. This means the map itself cannot be modified (no adding/removing entries, no changing associations between keys and values), but if the *values* stored in the map are mutable objects (e.g., `ArrayList`, custom mutable classes), those objects can still be modified through their own methods.

If you need **deep immutability** (where the map *and* all its contained objects are immutable), you must ensure that:
1.  All keys are immutable.
2.  All values are immutable.
3.  If values contain other objects, those objects must also be immutable, and so on.

For complex deep immutability requirements, you might need to manually create defensive copies of mutable values when putting them into the map, or consider using third-party libraries like Google Guava's `ImmutableMap` which often provide more convenient builders and sometimes better performance characteristics for larger maps.