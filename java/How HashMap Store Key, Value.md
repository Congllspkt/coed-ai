`HashMap` in Java is one of the most fundamental and widely used data structures. It implements the `Map` interface and provides a way to store data in `key-value` pairs. It uses a technique called **hashing** for efficient storage and retrieval of elements.

Let's dive into the details of how `HashMap` stores key-value pairs.

## How HashMap Stores Key, Value Pairs

At its core, `HashMap` uses an **array of `Node` objects** (historically, `Entry` objects). Each `Node` represents a single key-value pair and also contains information to handle collisions.

Here's a breakdown of the internal structure and working mechanism:

### 1. The Core Data Structure: `Node` Array (Buckets)

*   `HashMap` maintains an internal array, often called `table` or `buckets`. Each index in this array is a "bucket."
*   Each `Node` in the `HashMap` essentially stores:
    *   `hash`: The hash code of the key. This is pre-computed and stored to avoid recomputing it during comparisons.
    *   `key`: The actual key object.
    *   `value`: The value associated with the key.
    *   `next`: A reference to the next `Node` in case of a **collision** (forming a linked list).

    *(In Java 8+, if a bucket's linked list becomes too long (e.g., more than 8 nodes), it converts the linked list into a **Red-Black Tree** for better performance in the worst-case scenario, achieving O(log n) lookup instead of O(n) for a long linked list.)*

### 2. The `put(key, value)` Operation

When you call `map.put(key, value)`, here's what happens:

1.  **Calculate Hash Code:**
    *   The `hashCode()` method of the `key` object is called. This method returns an integer hash code for the key.
    *   `HashMap` then performs some internal "scrambling" on this hash code (using a `hash()` function) to further reduce collisions and distribute keys more evenly, even if the key's `hashCode()` implementation isn't ideal.

2.  **Calculate Array Index (Bucket):**
    *   The scrambled hash code is then used to determine the index (or "bucket") in the internal `Node` array where this key-value pair should be stored.
    *   This is typically done using the formula: `index = (table.length - 1) & hash`. This ensures the index is always within the bounds of the array.

3.  **Collision Check and Storage:**

    *   **Scenario A: No Collision (Empty Bucket):** If the calculated index points to an empty bucket, a new `Node` (containing the key, value, and hash) is created and placed directly at that index.

    *   **Scenario B: Collision (Occupied Bucket):** If the calculated index already contains a `Node` (meaning another key has hashed to the same bucket), `HashMap` needs to handle this collision:
        *   **Iterate and Check for Equality:** It traverses the linked list (or Red-Black Tree) starting from the `Node` at that bucket. For each `Node` in the list/tree, it performs two checks:
            1.  **Hash Equality:** Is the `hash` stored in the current `Node` equal to the `hash` of the new key? (This is a quick pre-check).
            2.  **Key Equality:** If hashes match, it then calls the `equals()` method on the current `Node's` key and the new key (`newKey.equals(existingKey)`). This is the definitive check.
        *   **Key Found:** If both the hash and `equals()` methods return `true`, it means the new key is *identical* to an existing key. In this case, the `value` associated with that key is updated with the new value, and the old value is returned.
        *   **Key Not Found:** If the new key is not found (i.e., it's a *different* key but happens to hash to the same bucket, or the list is exhausted without a match), a new `Node` is created and appended to the end of the linked list (or inserted into the Red-Black Tree) at that bucket.

### 3. The `get(key)` Operation

When you call `map.get(key)`, here's what happens:

1.  **Calculate Hash Code and Index:**
    *   The `hashCode()` of the provided `key` is calculated and "scrambled" in the same way as during `put()`.
    *   The same index calculation `(table.length - 1) & hash` is performed to find the relevant bucket.

2.  **Search the Bucket:**
    *   `HashMap` goes to the calculated bucket in its internal `Node` array.
    *   It then traverses the linked list (or Red-Black Tree) at that bucket.
    *   For each `Node` in the list/tree, it performs the same two checks as in `put()`:
        1.  **Hash Equality:** Is the `hash` stored in the `Node` equal to the hash of the key we are searching for?
        2.  **Key Equality:** If hashes match, does `searchedKey.equals(currentNode.key)` return `true`?

3.  **Return Value:**
    *   If both checks pass, the `value` associated with that `Node` is returned.
    *   If the end of the linked list/tree is reached without finding a matching key, `null` is returned.

### 4. Important Concepts: `hashCode()` and `equals()`

The correct functioning and performance of `HashMap` *heavily depend* on the correct implementation of `hashCode()` and `equals()` methods for the objects used as keys.

*   **`hashCode()` Contract:**
    *   If two objects are equal according to the `equals(Object)` method, then calling the `hashCode()` method on each of the two objects *must* produce the same integer result.
    *   If two objects are unequal according to the `equals(Object)` method, it is *not required* that calling the `hashCode()` method on each of the two objects produce distinct integer results. However, different hash codes for unequal objects can improve the performance of hash tables.

*   **`equals()` Contract:**
    *   **Reflexive:** For any non-null reference value `x`, `x.equals(x)` should return `true`.
    *   **Symmetric:** For any non-null reference values `x` and `y`, `x.equals(y)` should return `true` if and only if `y.equals(x)` returns `true`.
    *   **Transitive:** For any non-null reference values `x`, `y`, and `z`, if `x.equals(y)` returns `true` and `y.equals(z)` returns `true`, then `x.equals(z)` should return `true`.
    *   **Consistent:** For any non-null reference values `x` and `y`, multiple invocations of `x.equals(y)` consistently return `true` or consistently return `false`, provided no information used in `equals` comparisons on the objects is modified.
    *   For any non-null reference value `x`, `x.equals(null)` should return `false`.

**Consequences of Poor Implementations:**

*   **Incorrect `hashCode()`:** If `equals()` returns `true` but `hashCode()` returns different values for two objects, `HashMap` might store them in different buckets. Then, `get()` might not find the object even if it's logically present, because it will look in the wrong bucket.
*   **Incorrect `equals()`:** If `hashCode()` is good but `equals()` is bad, `HashMap` might incorrectly consider two distinct keys as the same, leading to data loss (overwriting) or inability to retrieve the correct value.
*   **Mutable Keys:** If a key's fields that are used in `hashCode()` or `equals()` change *after* it's been put into the `HashMap`, its hash code might change. This means `HashMap` will look for it in the wrong bucket when you try to `get()` it, effectively making the key unretrievable. Immutable keys (like `String`, `Integer`, `Boolean`) are highly recommended.

### 5. Load Factor and Rehashing

*   **Load Factor:** This is a threshold (default: 0.75) that dictates when the `HashMap` should resize itself.
*   **Threshold:** `capacity * loadFactor`. When the number of entries in the `HashMap` exceeds this threshold, `HashMap` performs **rehashing**.
*   **Rehashing:** A new, larger array (typically double the size) is created. All existing `Node`s from the old array are then re-calculated for their new bucket index in the new array and re-distributed. This is an expensive operation (O(n)) but ensures that the average O(1) performance for `put` and `get` is maintained by keeping the number of elements per bucket low.

## Example: Storing `Student` Objects in `HashMap`

Let's illustrate with a custom `Student` class.

```java
import java.util.HashMap;
import java.util.Objects;

// Custom Class to be used as Key
class Student {
    private int id;
    private String name;

    public Student(int id, String name) {
        this.id = id;
        this.name = name;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    // IMPORTANT: Override hashCode() and equals() for correct HashMap behavior
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Student student = (Student) o;
        // Two students are considered equal if their IDs are the same
        return id == student.id;
    }

    @Override
    public int hashCode() {
        // The hash code is based only on the ID, consistent with equals()
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "Student{" +
               "id=" + id +
               ", name='" + name + '\'' +
               '}';
    }
}

public class HashMapStorageExample {

    public static void main(String[] args) {
        // Create a HashMap to store Student objects (as keys) and their grades (as values)
        HashMap<Student, String> studentGrades = new HashMap<>();

        System.out.println("--- Putting elements into HashMap ---");

        // Input 1: Put Student 1
        Student s1 = new Student(101, "Alice Smith");
        studentGrades.put(s1, "A+");
        System.out.println("Put: " + s1 + " -> A+");
        System.out.println("HashMap after put: " + studentGrades);
        // Expected internal: (s1.hashCode() & capacity-1) -> Node(s1, "A+")

        System.out.println("\n---");

        // Input 2: Put Student 2 (different ID, different hash, different bucket)
        Student s2 = new Student(102, "Bob Johnson");
        studentGrades.put(s2, "B");
        System.out.println("Put: " + s2 + " -> B");
        System.out.println("HashMap after put: " + studentGrades);
        // Expected internal: (s2.hashCode() & capacity-1) -> Node(s2, "B")

        System.out.println("\n---");

        // Input 3: Put Student 3 (different ID, different hash, different bucket)
        Student s3 = new Student(103, "Charlie Brown");
        studentGrades.put(s3, "C");
        System.out.println("Put: " + s3 + " -> C");
        System.out.println("HashMap after put: " + studentGrades);

        System.out.println("\n--- Testing key collision scenario (same ID, different name) ---");

        // Input 4: Put Student 4 (same ID as s1, but different name)
        // Since equals() only checks 'id', this Student object will be considered equal to s1
        Student s4 = new Student(101, "Alicia Jones"); // Same ID as s1
        studentGrades.put(s4, "A-"); // This will OVERWRITE the value for s1
        System.out.println("Put: " + s4 + " -> A- (same ID as Alice)");
        System.out.println("HashMap after put (s1's value should be updated): " + studentGrades);
        // Internal: s4.hashCode() will be same as s1.hashCode().
        // It will go to the same bucket.
        // Then s4.equals(s1) will return true.
        // So, value for s1 (which is now effectively s4) will be updated from "A+" to "A-".

        System.out.println("\n--- Retrieving elements ---");

        // Input 5: Get Student 1
        Student searchS1 = new Student(101, "Random Name"); // Only ID matters for search
        String gradeS1 = studentGrades.get(searchS1);
        System.out.println("Get grade for " + searchS1 + ": " + gradeS1);
        // Internal: searchS1.hashCode() will be used to find the bucket.
        // Then searchS1.equals(existingNode.key) will be used to find the exact match.
        // It should retrieve "A-" as that's the updated value.

        // Input 6: Get Student 2
        String gradeS2 = studentGrades.get(s2);
        System.out.println("Get grade for " + s2 + ": " + gradeS2);

        // Input 7: Get a non-existent student
        Student nonExistentStudent = new Student(999, "Non Existent");
        String gradeNonExistent = studentGrades.get(nonExistentStudent);
        System.out.println("Get grade for " + nonExistentStudent + ": " + gradeNonExistent); // Should be null

        System.out.println("\n--- Checking for key existence ---");
        System.out.println("Does HashMap contain student with ID 102? " + studentGrades.containsKey(new Student(102, "Any Name")));
        System.out.println("Does HashMap contain student with ID 999? " + studentGrades.containsKey(new Student(999, "Any Name")));
    }
}
```

### Output:

```
--- Putting elements into HashMap ---
Put: Student{id=101, name='Alice Smith'} -> A+
HashMap after put: {Student{id=101, name='Alice Smith'}=A+}

---
Put: Student{id=102, name='Bob Johnson'} -> B
HashMap after put: {Student{id=102, name='Bob Johnson'}=B, Student{id=101, name='Alice Smith'}=A+}

---
Put: Student{id=103, name='Charlie Brown'} -> C
HashMap after put: {Student{id=103, name='Charlie Brown'}=C, Student{id=102, name='Bob Johnson'}=B, Student{id=101, name='Alice Smith'}=A+}

--- Testing key collision scenario (same ID, different name) ---
Put: Student{id=101, name='Alicia Jones'} -> A- (same ID as Alice)
HashMap after put (s1's value should be updated): {Student{id=103, name='Charlie Brown'}=C, Student{id=102, name='Bob Johnson'}=B, Student{id=101, name='Alicia Jones'}=A-}

--- Retrieving elements ---
Get grade for Student{id=101, name='Random Name'}: A-
Get grade for Student{id=102, name='Bob Johnson'}: B
Get grade for Student{id=999, name='Non Existent'}: null

--- Checking for key existence ---
Does HashMap contain student with ID 102? true
Does HashMap contain student with ID 999? false
```

### Explanation of Output with Internal Logic:

1.  **`Put: Student{id=101, name='Alice Smith'} -> A+`**:
    *   `s1.hashCode()` is calculated (based on `id=101`).
    *   An index is determined.
    *   A `Node(hash_s1, s1, "A+", null)` is created and placed at that index.

2.  **`Put: Student{id=102, name='Bob Johnson'} -> B`**:
    *   `s2.hashCode()` is calculated (based on `id=102`). This will likely result in a different hash than `s1`.
    *   A different index is determined.
    *   A `Node(hash_s2, s2, "B", null)` is created and placed at that index.

3.  **`Put: Student{id=103, name='Charlie Brown'} -> C`**:
    *   Similar process for `s3`, placed in its respective bucket.

4.  **`Put: Student{id=101, name='Alicia Jones'} -> A-`**:
    *   A *new* `Student` object `s4` is created with `id=101` but `name="Alicia Jones"`.
    *   `s4.hashCode()` is calculated. Since its `id` is 101, its `hashCode()` will be the *same* as `s1`'s `hashCode()`.
    *   `HashMap` goes to the *same bucket* as `s1`.
    *   It finds the `Node` containing `s1`.
    *   It checks `s4.equals(s1)`. Since our `equals()` method only compares `id`, `s4.equals(s1)` returns `true`.
    *   Because the keys are considered equal, `HashMap` **overwrites** the value associated with `s1` (which is now represented by `s4` in the map's context) from "A+" to "A-". Notice in the `HashMap after put` output, `Student{id=101, name='Alicia Jones'}=A-` is now visible, replacing the previous entry.

5.  **`Get grade for Student{id=101, name='Random Name'}: A-`**:
    *   A new `Student` object `searchS1` is created with `id=101`.
    *   `searchS1.hashCode()` is calculated, which is the same as `s1` and `s4`.
    *   `HashMap` goes to the same bucket.
    *   It finds the `Node` for `Student{id=101, name='Alicia Jones'}`.
    *   `searchS1.equals(Node's_key)` is `true`.
    *   The value "A-" is returned.

This detailed example clearly demonstrates how `HashMap` uses `hashCode()` for initial bucket placement and `equals()` for definitive key identification and collision resolution, leading to efficient storage and retrieval of key-value pairs.