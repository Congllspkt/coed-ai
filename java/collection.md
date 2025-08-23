# Java Collections Framework

The Java Collections Framework (JCF) is a set of interfaces and classes that represent groups of objects as a single unit. It provides a unified architecture for storing and manipulating collections of objects, offering various data structures and algorithms.

Located primarily in the `java.util` package, the JCF offers high-performance, reusable data structures that are essential for any Java application.

## 1. Core Concepts

*   **Interfaces:** Define the abstract data types (e.g., `List`, `Set`, `Queue`, `Map`).
*   **Implementations:** Concrete classes that implement the interfaces (e.g., `ArrayList`, `HashSet`, `HashMap`).
*   **Algorithms:** Static methods that perform useful operations on collections (e.g., sorting, searching, shuffling), provided by the `Collections` utility class.
*   **Generics:** Allow you to specify the type of objects that a collection will hold, providing compile-time type safety and preventing `ClassCastException` at runtime.

### Why use the Collections Framework?

*   **Reduced Development Effort:** No need to write your own data structures.
*   **Increased Performance:** Optimized, high-performance implementations are provided.
*   **Standard API:** Makes it easier to learn and use new APIs.
*   **Interoperability:** Different parts of your application can interact seamlessly using standard collection types.

## 2. The `Collection` Interface (Root of Many)

The `java.util.Collection` interface is the root interface in the collection hierarchy. It represents a group of objects known as its elements. All the other interfaces like `List`, `Set`, and `Queue` extend this `Collection` interface. `Map` is separate but considered part of the framework.

**Common methods in `Collection`:**

*   `add(E element)`: Adds an element to the collection.
*   `remove(Object element)`: Removes an element from the collection.
*   `contains(Object element)`: Checks if an element is in the collection.
*   `size()`: Returns the number of elements.
*   `isEmpty()`: Checks if the collection is empty.
*   `clear()`: Removes all elements.
*   `iterator()`: Returns an `Iterator` over the elements.

## 3. Key Interfaces and Implementations

Let's dive into the most commonly used interfaces and their primary implementations.

### 3.1. `List` Interface

*   **Characteristics:**
    *   **Ordered:** Elements maintain their insertion order (or a specific order based on index).
    *   **Allows Duplicates:** You can store the same element multiple times.
    *   **Index-based Access:** Elements can be accessed by their integer index.

*   **Common Implementations:**
    *   **`ArrayList`:** Implements `List` using a dynamic array.
        *   **Pros:** Fast random access (`get(index)`), good for iteration.
        *   **Cons:** Slower insertions/deletions in the middle (requires shifting elements).
    *   **`LinkedList`:** Implements `List` using a doubly-linked list.
        *   **Pros:** Fast insertions/deletions at any position.
        *   **Cons:** Slower random access (`get(index)`), as it has to traverse from the beginning or end.
    *   **`Vector`:** Similar to `ArrayList` but synchronized (thread-safe), making it generally slower for single-threaded use. `Stack` extends `Vector`.

---

#### `List` Example with `ArrayList`

**Scenario:** Managing a list of favorite movies.

```java
import java.util.ArrayList;
import java.util.List;

public class ArrayListExample {
    public static void main(String[] args) {
        // 1. Create an ArrayList of Strings
        List<String> favoriteMovies = new ArrayList<>();
        System.out.println("Initial list: " + favoriteMovies); // Output: []
        System.out.println("Is list empty? " + favoriteMovies.isEmpty()); // Output: true

        // 2. Add elements
        System.out.println("\n--- Adding Movies ---");
        favoriteMovies.add("The Shawshank Redemption");
        favoriteMovies.add("The Godfather");
        favoriteMovies.add("The Dark Knight");
        favoriteMovies.add("Pulp Fiction");
        favoriteMovies.add("The Godfather"); // Adding a duplicate
        System.out.println("After adding: " + favoriteMovies);
        System.out.println("List size: " + favoriteMovies.size());

        // 3. Access elements by index
        System.out.println("\n--- Accessing Movies ---");
        System.out.println("Movie at index 0: " + favoriteMovies.get(0));
        System.out.println("Movie at index 3: " + favoriteMovies.get(3));

        // 4. Update an element
        System.out.println("\n--- Updating Movie ---");
        favoriteMovies.set(2, "Inception"); // Replace "The Dark Knight" with "Inception"
        System.out.println("After updating index 2: " + favoriteMovies);

        // 5. Check if an element exists
        System.out.println("\n--- Checking for Movies ---");
        System.out.println("Contains 'Pulp Fiction'? " + favoriteMovies.contains("Pulp Fiction"));
        System.out.println("Contains 'Titanic'? " + favoriteMovies.contains("Titanic"));

        // 6. Remove elements
        System.out.println("\n--- Removing Movies ---");
        favoriteMovies.remove("The Godfather"); // Removes the first occurrence
        System.out.println("After removing 'The Godfather' (first): " + favoriteMovies);

        favoriteMovies.remove(0); // Removes element at index 0 ("The Shawshank Redemption")
        System.out.println("After removing at index 0: " + favoriteMovies);

        // 7. Iterating through the list
        System.out.println("\n--- Iterating through the list ---");
        for (String movie : favoriteMovies) {
            System.out.println("  - " + movie);
        }

        // 8. Clear the list
        System.out.println("\n--- Clearing the list ---");
        favoriteMovies.clear();
        System.out.println("After clearing: " + favoriteMovies);
        System.out.println("Is list empty now? " + favoriteMovies.isEmpty());
    }
}
```

**Input:**
(No direct user input for this example. The input is hardcoded within the `main` method.)

**Output:**
```
Initial list: []
Is list empty? true

--- Adding Movies ---
After adding: [The Shawshank Redemption, The Godfather, The Dark Knight, Pulp Fiction, The Godfather]
List size: 5

--- Accessing Movies ---
Movie at index 0: The Shawshank Redemption
Movie at index 3: Pulp Fiction

--- Updating Movie ---
After updating index 2: [The Shawshank Redemption, The Godfather, Inception, Pulp Fiction, The Godfather]

--- Checking for Movies ---
Contains 'Pulp Fiction'? true
Contains 'Titanic'? false

--- Removing Movies ---
After removing 'The Godfather' (first): [The Shawshank Redemption, Inception, Pulp Fiction, The Godfather]
After removing at index 0: [Inception, Pulp Fiction, The Godfather]

--- Iterating through the list ---
  - Inception
  - Pulp Fiction
  - The Godfather

--- Clearing the list ---
After clearing: []
Is list empty now? true
```

---

### 3.2. `Set` Interface

*   **Characteristics:**
    *   **No Duplicates:** Each element must be unique. If you try to add a duplicate, the `add()` method will return `false` and the set will not change.
    *   **Unordered (generally):** The order of elements is not guaranteed unless specified by the implementation.
    *   **No Index-based Access:** You cannot access elements by index.

*   **Common Implementations:**
    *   **`HashSet`:** Implements `Set` using a hash table.
        *   **Pros:** Best performance (constant time for `add`, `remove`, `contains`) but offers no guarantee regarding the order of elements.
        *   **Cons:** Unordered.
    *   **`LinkedHashSet`:** Extends `HashSet` but also uses a doubly-linked list to maintain insertion order.
        *   **Pros:** Maintains insertion order while still providing good performance.
        *   **Cons:** Slightly slower than `HashSet` due to maintaining the linked list.
    *   **`TreeSet`:** Implements `SortedSet` (which extends `Set`) using a Red-Black tree.
        *   **Pros:** Stores elements in natural sorted order (or by a custom `Comparator`).
        *   **Cons:** Slower performance (`O(log n)`) for basic operations compared to `HashSet`.

---

#### `Set` Example with `HashSet`

**Scenario:** Storing unique names of attendees at an event.

```java
import java.util.HashSet;
import java.util.Set;

public class HashSetExample {
    public static void main(String[] args) {
        // 1. Create a HashSet of Strings
        Set<String> attendees = new HashSet<>();
        System.out.println("Initial set: " + attendees); // Output: []
        System.out.println("Is set empty? " + attendees.isEmpty()); // Output: true

        // 2. Add elements
        System.out.println("\n--- Adding Attendees ---");
        attendees.add("Alice");
        attendees.add("Bob");
        attendees.add("Charlie");
        System.out.println("After adding initial attendees: " + attendees);
        System.out.println("Set size: " + attendees.size());

        boolean addedDuplicate = attendees.add("Bob"); // Adding a duplicate
        System.out.println("Tried to add 'Bob' again. Was it added? " + addedDuplicate); // Output: false
        System.out.println("After adding 'Bob' again: " + attendees); // Set remains unchanged
        System.out.println("Set size: " + attendees.size());

        attendees.add("David");
        System.out.println("After adding 'David': " + attendees);

        // 3. Check if an element exists
        System.out.println("\n--- Checking for Attendees ---");
        System.out.println("Contains 'Charlie'? " + attendees.contains("Charlie"));
        System.out.println("Contains 'Eve'? " + attendees.contains("Eve"));

        // 4. Remove elements
        System.out.println("\n--- Removing Attendees ---");
        attendees.remove("Bob");
        System.out.println("After removing 'Bob': " + attendees);
        System.out.println("Set size: " + attendees.size());

        // 5. Iterating through the set (order is not guaranteed for HashSet)
        System.out.println("\n--- Iterating through the set ---");
        for (String name : attendees) {
            System.out.println("  - " + name);
        }

        // 6. Clear the set
        System.out.println("\n--- Clearing the set ---");
        attendees.clear();
        System.out.println("After clearing: " + attendees);
        System.out.println("Is set empty now? " + attendees.isEmpty());
    }
}
```

**Input:**
(No direct user input.)

**Output:**
```
Initial set: []
Is set empty? true

--- Adding Attendees ---
After adding initial attendees: [Charlie, Bob, Alice] // Order can vary
Set size: 3
Tried to add 'Bob' again. Was it added? false
After adding 'Bob' again: [Charlie, Bob, Alice] // Order can vary
Set size: 3
After adding 'David': [Charlie, Bob, David, Alice] // Order can vary

--- Checking for Attendees ---
Contains 'Charlie'? true
Contains 'Eve'? false

--- Removing Attendees ---
After removing 'Bob': [Charlie, David, Alice] // Order can vary
Set size: 3

--- Iterating through the set ---
  - Charlie
  - David
  - Alice
  
--- Clearing the set ---
After clearing: []
Is set empty now? true
```
*(Note: The exact order of elements when printing a `HashSet` may vary across different runs or JVM versions, as `HashSet` does not guarantee order.)*

---

### 3.3. `Queue` Interface

*   **Characteristics:**
    *   **Ordered for Processing:** Elements are typically processed in a specific order (e.g., FIFO - First-In, First-Out, or by priority).
    *   **Allows Duplicates:** Generally, queues allow duplicates.
    *   **Head/Tail Operations:** Designed for operations at the head (retrieval/removal) and tail (insertion).

*   **Common Implementations:**
    *   **`LinkedList`:** Can be used as a `Queue` (and `Deque` - Double Ended Queue).
        *   **Pros:** Good for basic FIFO operations.
    *   **`PriorityQueue`:** Stores elements based on their natural order or a custom `Comparator`.
        *   **Pros:** Elements are retrieved based on their priority (smallest element first by default).
        *   **Cons:** Not good for random access.

---

#### `Queue` Example with `PriorityQueue`

**Scenario:** A task scheduler where tasks are processed based on their priority (represented by an integer, lower number means higher priority).

```java
import java.util.PriorityQueue;
import java.util.Queue;

public class PriorityQueueExample {
    public static void main(String[] args) {
        // 1. Create a PriorityQueue of Integers
        // By default, PriorityQueue orders elements in natural ascending order.
        Queue<Integer> taskQueue = new PriorityQueue<>();
        System.out.println("Initial queue: " + taskQueue); // Output: []
        System.out.println("Is queue empty? " + taskQueue.isEmpty()); // Output: true

        // 2. Add elements (offer)
        System.out.println("\n--- Adding Tasks (Priorities) ---");
        taskQueue.offer(5); // Low priority
        taskQueue.offer(1); // High priority
        taskQueue.offer(10); // Very low priority
        taskQueue.offer(3); // Medium priority
        taskQueue.offer(1); // Another high priority task
        System.out.println("After offering tasks: " + taskQueue); // Internal representation, not necessarily sorted

        System.out.println("Queue size: " + taskQueue.size());

        // 3. Peek at the head (element with highest priority/smallest value)
        System.out.println("\n--- Peeking at Head ---");
        System.out.println("Next task to process (peek): " + taskQueue.peek()); // Should be 1

        // 4. Poll elements (retrieve and remove the head)
        System.out.println("\n--- Processing Tasks ---");
        System.out.println("Processing task: " + taskQueue.poll()); // Removes 1
        System.out.println("Queue after poll: " + taskQueue);
        System.out.println("Next task to process (peek): " + taskQueue.peek()); // Should be 1 (the other one)

        System.out.println("Processing task: " + taskQueue.poll()); // Removes 1
        System.out.println("Queue after poll: " + taskQueue);
        System.out.println("Next task to process (peek): " + taskQueue.peek()); // Should be 3

        System.out.println("Processing task: " + taskQueue.poll()); // Removes 3
        System.out.println("Processing task: " + taskQueue.poll()); // Removes 5
        System.out.println("Processing task: " + taskQueue.poll()); // Removes 10
        System.out.println("Queue after all tasks processed: " + taskQueue);

        // 5. Try to peek/poll from an empty queue
        System.out.println("\n--- Empty Queue Operations ---");
        System.out.println("Next task on empty queue (peek): " + taskQueue.peek()); // Output: null
        System.out.println("Processing task on empty queue (poll): " + taskQueue.poll()); // Output: null

        System.out.println("Is queue empty now? " + taskQueue.isEmpty());
    }
}
```

**Input:**
(No direct user input.)

**Output:**
```
Initial queue: []
Is queue empty? true

--- Adding Tasks (Priorities) ---
After offering tasks: [1, 1, 10, 5, 3] // Internal order, not visually sorted
Queue size: 5

--- Peeking at Head ---
Next task to process (peek): 1

--- Processing Tasks ---
Processing task: 1
Queue after poll: [1, 3, 10, 5]
Next task to process (peek): 1
Processing task: 1
Queue after poll: [3, 5, 10]
Next task to process (peek): 3
Processing task: 3
Processing task: 5
Processing task: 10
Queue after all tasks processed: []

--- Empty Queue Operations ---
Next task on empty queue (peek): null
Processing task on empty queue (poll): null
Is queue empty now? true
```
*(Note: The internal array representation of `PriorityQueue` when printed might not look sorted, but `peek()` and `poll()` always return the highest priority element.)*

---

### 3.4. `Map` Interface

**Note:** `Map` is technically *not* a sub-interface of `Collection`. It's a separate hierarchy but is considered part of the Java Collections Framework because it manages a collection of objects (keys and values).

*   **Characteristics:**
    *   **Key-Value Pairs:** Stores data as pairs, where each key maps to a single value.
    *   **Unique Keys:** Keys must be unique. If you try to put a value with an existing key, the old value will be replaced.
    *   **Values Can Be Duplicates:** Multiple keys can map to the same value.
    *   **No Iteration Order (generally):** The order of key-value pairs is not guaranteed unless specified by the implementation.

*   **Common Implementations:**
    *   **`HashMap`:** Implements `Map` using a hash table.
        *   **Pros:** Fastest for `put`, `get`, `remove` operations (constant time on average).
        *   **Cons:** No guaranteed order of key-value pairs.
    *   **`LinkedHashMap`:** Extends `HashMap` but maintains insertion order of key-value pairs.
        *   **Pros:** Preserves insertion order, good performance.
        *   **Cons:** Slightly slower than `HashMap`.
    *   **`TreeMap`:** Implements `SortedMap` (which extends `Map`) using a Red-Black tree.
        *   **Pros:** Stores key-value pairs in natural sorted order of keys (or by a custom `Comparator`).
        *   **Cons:** Slower performance (`O(log n)`) for basic operations compared to `HashMap`.
    *   **`Hashtable`:** Similar to `HashMap` but synchronized (thread-safe) and does not allow `null` keys or values. Generally superseded by `ConcurrentHashMap` for concurrent use.

---

#### `Map` Example with `HashMap`

**Scenario:** Storing employee IDs and their names.

```java
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class HashMapExample {
    public static void main(String[] args) {
        // 1. Create a HashMap with Integer keys (employee ID) and String values (employee name)
        Map<Integer, String> employeeMap = new HashMap<>();
        System.out.println("Initial map: " + employeeMap); // Output: {}
        System.out.println("Is map empty? " + employeeMap.isEmpty()); // Output: true

        // 2. Add key-value pairs (put)
        System.out.println("\n--- Adding Employees ---");
        employeeMap.put(101, "Alice Smith");
        employeeMap.put(102, "Bob Johnson");
        employeeMap.put(103, "Charlie Brown");
        System.out.println("After adding employees: " + employeeMap);
        System.out.println("Map size: " + employeeMap.size());

        // 3. Add an entry with an existing key (updates the value)
        String oldValue = employeeMap.put(102, "Robert Johnson"); // Bob's name changed
        System.out.println("Updated name for 102 from '" + oldValue + "' to 'Robert Johnson'");
        System.out.println("Map after update: " + employeeMap);
        System.out.println("Map size: " + employeeMap.size()); // Size remains 3

        // 4. Get value by key
        System.out.println("\n--- Getting Employee Names ---");
        System.out.println("Employee 101: " + employeeMap.get(101));
        System.out.println("Employee 103: " + employeeMap.get(103));
        System.out.println("Employee 105 (non-existent): " + employeeMap.get(105)); // Output: null

        // 5. Check if key or value exists
        System.out.println("\n--- Checking for Keys/Values ---");
        System.out.println("Contains key 101? " + employeeMap.containsKey(101));
        System.out.println("Contains key 105? " + employeeMap.containsKey(105));
        System.out.println("Contains value 'Charlie Brown'? " + employeeMap.containsValue("Charlie Brown"));
        System.out.println("Contains value 'Jane Doe'? " + employeeMap.containsValue("Jane Doe"));

        // 6. Remove an entry
        System.out.println("\n--- Removing Employee ---");
        String removedValue = employeeMap.remove(101);
        System.out.println("Removed employee 101: " + removedValue);
        System.out.println("Map after removing 101: " + employeeMap);
        System.out.println("Map size: " + employeeMap.size());

        // 7. Iterate through keys, values, or entries
        System.out.println("\n--- Iterating through the Map ---");

        // Iterate keys
        System.out.println("Employee IDs (Keys):");
        Set<Integer> employeeIds = employeeMap.keySet();
        for (Integer id : employeeIds) {
            System.out.println("  - " + id);
        }

        // Iterate values
        System.out.println("Employee Names (Values):");
        for (String name : employeeMap.values()) {
            System.out.println("  - " + name);
        }

        // Iterate entries (most common and efficient way)
        System.out.println("Employee Entries (Key-Value Pairs):");
        for (Map.Entry<Integer, String> entry : employeeMap.entrySet()) {
            System.out.println("  - ID: " + entry.getKey() + ", Name: " + entry.getValue());
        }

        // 8. Clear the map
        System.out.println("\n--- Clearing the map ---");
        employeeMap.clear();
        System.out.println("After clearing: " + employeeMap);
        System.out.println("Is map empty now? " + employeeMap.isEmpty());
    }
}
```

**Input:**
(No direct user input.)

**Output:**
```
Initial map: {}
Is map empty? true

--- Adding Employees ---
After adding employees: {101=Alice Smith, 102=Bob Johnson, 103=Charlie Brown} // Order can vary
Map size: 3
Updated name for 102 from 'Bob Johnson' to 'Robert Johnson'
Map after update: {101=Alice Smith, 102=Robert Johnson, 103=Charlie Brown} // Order can vary
Map size: 3

--- Getting Employee Names ---
Employee 101: Alice Smith
Employee 103: Charlie Brown
Employee 105 (non-existent): null

--- Checking for Keys/Values ---
Contains key 101? true
Contains key 105? false
Contains value 'Charlie Brown'? true
Contains value 'Jane Doe'? false

--- Removing Employee ---
Removed employee 101: Alice Smith
Map after removing 101: {102=Robert Johnson, 103=Charlie Brown} // Order can vary
Map size: 2

--- Iterating through the Map ---
Employee IDs (Keys):
  - 102
  - 103
Employee Names (Values):
  - Robert Johnson
  - Charlie Brown
Employee Entries (Key-Value Pairs):
  - ID: 102, Name: Robert Johnson
  - ID: 103, Name: Charlie Brown

--- Clearing the map ---
After clearing: {}
Is map empty now? true
```
*(Note: The exact order of elements when printing a `HashMap` or iterating through its `keySet()`, `values()`, or `entrySet()` may vary, as `HashMap` does not guarantee order.)*

---

## 4. The `Collections` Utility Class

It's crucial to distinguish `java.util.Collection` (the interface) from `java.util.Collections` (a utility class).

The `Collections` class provides static methods for operating on or returning collections. These include:

*   **Sorting:** `sort(List list)`
*   **Searching:** `binarySearch(List list, T key)`
*   **Shuffling:** `shuffle(List list)`
*   **Reversing:** `reverse(List list)`
*   **Finding min/max:** `min(Collection coll)`, `max(Collection coll)`
*   **Making collections unmodifiable:** `unmodifiableList()`, `unmodifiableSet()`, `unmodifiableMap()`
*   **Synchronizing (thread-safe) wrappers:** `synchronizedList()`, `synchronizedSet()`, `synchronizedMap()`

---

#### `Collections` Example

**Scenario:** Sorting a list of numbers.

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class CollectionsUtilityExample {
    public static void main(String[] args) {
        List<Integer> numbers = new ArrayList<>();
        numbers.add(5);
        numbers.add(1);
        numbers.add(8);
        numbers.add(2);
        numbers.add(5);

        System.out.println("Original list: " + numbers);

        // 1. Sort the list
        Collections.sort(numbers);
        System.out.println("Sorted list: " + numbers);

        // 2. Reverse the list
        Collections.reverse(numbers);
        System.out.println("Reversed list: " + numbers);

        // 3. Find min and max
        System.out.println("Minimum element: " + Collections.min(numbers));
        System.out.println("Maximum element: " + Collections.max(numbers));

        // 4. Shuffle the list
        Collections.shuffle(numbers);
        System.out.println("Shuffled list: " + numbers);

        // 5. Create an unmodifiable list
        List<Integer> unmodifiableNumbers = Collections.unmodifiableList(numbers);
        System.out.println("\nUnmodifiable list: " + unmodifiableNumbers);
        try {
            unmodifiableNumbers.add(10); // This will throw an UnsupportedOperationException
        } catch (UnsupportedOperationException e) {
            System.out.println("Attempted to modify unmodifiable list: " + e.getMessage());
        }
    }
}
```

**Input:**
(No direct user input.)

**Output:**
```
Original list: [5, 1, 8, 2, 5]
Sorted list: [1, 2, 5, 5, 8]
Reversed list: [8, 5, 5, 2, 1]
Minimum element: 1
Maximum element: 8
Shuffled list: [5, 1, 8, 2, 5] // Order will be random each time

Unmodifiable list: [5, 1, 8, 2, 5] // Will reflect the last shuffled state
Attempted to modify unmodifiable list: null
```
*(Note: The output for "Shuffled list" will vary each time you run the program.)*

---

## 5. When to Use Which? (A Quick Guide)

| Feature / Need          | `List`                                 | `Set`                                        | `Queue`                                 | `Map`                                      |
| :---------------------- | :------------------------------------- | :------------------------------------------- | :-------------------------------------- | :----------------------------------------- |
| **Order**               | Insertion order (or indexed)           | No guaranteed order (usually)                | Processing order (e.g., FIFO, Priority) | No guaranteed order of entries (usually)   |
| **Duplicates**          | Allowed                                | Not allowed                                  | Allowed                                 | Keys unique, Values can be duplicated      |
| **Primary Use Case**    | Ordered sequence of elements           | Collection of unique elements                | Processing elements in a specific order | Storing key-value associations             |
| **Key Operations**      | `add()`, `get()`, `set()`, `remove()`  | `add()`, `remove()`, `contains()`            | `offer()`, `poll()`, `peek()`           | `put()`, `get()`, `remove()`, `containsKey()` |
| **Common Implementations** | `ArrayList`, `LinkedList`              | `HashSet`, `LinkedHashSet`, `TreeSet`        | `LinkedList`, `PriorityQueue`           | `HashMap`, `LinkedHashMap`, `TreeMap`      |
| **When to use `ArrayList`** | Need fast random access (by index)     | (Not applicable)                             | (Not applicable)                        | (Not applicable)                           |
| **When to use `LinkedList`** | Frequent insertions/deletions in middle | (Not applicable)                             | As a FIFO queue (`offer`, `poll`)       | (Not applicable)                           |
| **When to use `HashSet`** | Need fast unique storage, order doesn't matter | (Primary use)                                | (Not applicable)                        | (Not applicable)                           |
| **When to use `TreeSet`** | Need unique elements sorted naturally or customly | (Primary use for sorted unique elements)     | (Not applicable)                        | (Not applicable)                           |
| **When to use `PriorityQueue`** | (Not applicable)                       | (Not applicable)                             | Need elements ordered by priority       | (Not applicable)                           |
| **When to use `HashMap`** | (Not applicable)                       | (Not applicable)                             | (Not applicable)                        | Need fast key-value storage, order doesn't matter |
| **When to use `TreeMap`** | (Not applicable)                       | (Not applicable)                             | (Not applicable)                        | Need key-value pairs sorted by key         |

## 6. Conclusion

The Java Collections Framework is an incredibly powerful and versatile part of the Java language. By understanding its core interfaces (`List`, `Set`, `Queue`, `Map`) and their various implementations, you can choose the most appropriate data structure for your specific needs, leading to more efficient, readable, and maintainable code. Always remember to use generics to leverage type safety!