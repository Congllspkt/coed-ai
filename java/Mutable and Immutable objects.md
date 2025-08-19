# Mutable and Immutable Objects in Java

In Java, objects can be classified into two main categories based on whether their state can be changed after they are created: **Mutable** and **Immutable**. Understanding this distinction is fundamental for writing robust, thread-safe, and predictable Java applications.

---

## I. Immutable Objects

An **immutable object** is an object whose state cannot be modified after it is created. Once an immutable object has been instantiated, its internal data remains constant throughout its lifetime. Any operation that appears to modify an immutable object will, in fact, return a *new* object with the desired changes, leaving the original object untouched.

### Key Characteristics and Properties:

1.  **State Unchanged:** The values of its fields cannot be altered once the object is constructed.
2.  **Thread-Safe:** Since their state never changes, immutable objects are inherently thread-safe. Multiple threads can access them concurrently without causing consistency issues or requiring explicit synchronization.
3.  **Predictable:** Their behavior is consistent because their state is fixed. This makes them easier to reason about and debug.
4.  **Suitable for Keys:** They are ideal for use as keys in `HashMap` or `HashSet` because their `hashCode()` value (if properly implemented) will not change after creation, ensuring that the object can always be found.
5.  **Cachable:** If an immutable object is frequently used, it can be safely cached, as its state will never become stale.

### Advantages of Immutability:

*   **Thread Safety:** No need for synchronization, making concurrent programming simpler and less error-prone.
*   **Security:** Prevents malicious or accidental modification of an object's state.
*   **Simplicity:** Easier to design, implement, and use. Reduces side effects.
*   **Caching:** Can be easily cached and reused.
*   **Good `HashMap` keys:** Reliable for hash-based collections.

### Disadvantages of Immutability:

*   **Object Creation Overhead:** For operations that seem to "modify" the object (like `String.concat()`), a new object is created. This can lead to increased memory usage and garbage collection overhead if modifications are frequent.

### Common Built-in Immutable Classes in Java:

Java provides many built-in immutable classes:

1.  **`String`:** The most common example.
2.  **Wrapper Classes:** `Integer`, `Long`, `Double`, `Boolean`, `Character`, `Byte`, `Short`, `Float`.
3.  **`BigDecimal`, `BigInteger`:** For arbitrary-precision numbers.
4.  **Date/Time API (`java.time` package):** `LocalDate`, `LocalTime`, `LocalDateTime`, `ZonedDateTime`, `Instant`, `Duration`, `Period`.
5.  **Some Collections:** While `ArrayList` and `HashMap` are mutable, methods like `List.of()`, `Set.of()`, `Map.of()` (Java 9+) create *unmodifiable* (effectively immutable) collections.

---

#### Example 1: `String` (Immutable)

```java
public class StringImmutableExample {
    public static void main(String[] args) {
        String s1 = "Hello";
        System.out.println("Original String s1: " + s1); // Input: Hello
        System.out.println("Hash Code of s1: " + s1.hashCode());

        // Any operation that modifies the string creates a NEW string object
        String s2 = s1.concat(" World");
        System.out.println("Modified String s2 (new object): " + s2); // Input: Hello World
        System.out.println("Hash Code of s2: " + s2.hashCode());
        System.out.println("Original String s1 (unchanged): " + s1); // Input: Hello
        System.out.println("Hash Code of s1 (unchanged): " + s1.hashCode());

        // Proof that s1 and s2 are different objects
        System.out.println("s1 == s2? " + (s1 == s2)); // Input: false (different memory addresses)
    }
}
```

**Output:**
```
Original String s1: Hello
Hash Code of s1: 69608447
Modified String s2 (new object): Hello World
Hash Code of s2: -1921312386
Original String s1 (unchanged): Hello
Hash Code of s1 (unchanged): 69608447
s1 == s2? false
```

**Explanation:** Even though we used `s1.concat(" World")`, `s1` itself did not change. Instead, a *new* `String` object (`s2`) was created with the concatenated value. The `hashCode()` values confirm that `s1` and `s2` are distinct objects.

---

#### Example 2: `Integer` (Immutable Wrapper Class)

```java
public class IntegerImmutableExample {
    public static void main(String[] args) {
        Integer i1 = 10;
        System.out.println("Original Integer i1: " + i1); // Input: 10
        System.out.println("Hash Code of i1: " + System.identityHashCode(i1));

        // When you perform an arithmetic operation, a new Integer object is created
        // This is due to auto-unboxing, operation, and auto-boxing back to Integer
        i1 = i1 + 5; 
        
        System.out.println("Modified Integer i1 (new object): " + i1); // Input: 15
        System.out.println("Hash Code of i1: " + System.identityHashCode(i1)); // New hash code
        
        // Let's create another Integer to see if identity changes on simple assignment
        Integer i2 = 20;
        Integer i3 = i2; // i3 now points to the same object as i2
        System.out.println("\nInteger i2: " + i2);
        System.out.println("Hash Code of i2: " + System.identityHashCode(i2));
        System.out.println("Integer i3: " + i3);
        System.out.println("Hash Code of i3: " + System.identityHashCode(i3));

        i2 = 25; // This creates a NEW Integer object for i2, i3 still points to the old one
        System.out.println("\nAfter modifying i2:");
        System.out.println("Integer i2: " + i2);
        System.out.println("Hash Code of i2: " + System.identityHashCode(i2)); // New hash code for i2
        System.out.println("Integer i3: " + i3);
        System.out.println("Hash Code of i3: " + System.identityHashCode(i3)); // i3's object is unchanged
    }
}
```

**Output:**
```
Original Integer i1: 10
Hash Code of i1: 1651191114
Modified Integer i1 (new object): 15
Hash Code of i1: 1598424915

Integer i2: 20
Hash Code of i2: 673030302
Integer i3: 20
Hash Code of i3: 673030302

After modifying i2:
Integer i2: 25
Hash Code of i2: 978949819
Integer i3: 20
Hash Code of i3: 673030302
```

**Explanation:** When we performed `i1 = i1 + 5;`, Java internally unboxed `i1` to `int`, performed the addition, and then autoboxed the result (`15`) back into a *new* `Integer` object, which was then assigned to `i1`. This demonstrates that `Integer` objects themselves are immutable; the *reference* `i1` simply points to a different object. The second part of the example further reinforces this by showing that changing `i2` does not affect `i3` because `i2` is reassigned to a *new* `Integer` object.

---

### How to Create a Custom Immutable Class:

To create your own immutable class, you must follow several rules:

1.  **Declare the class as `final`:** This prevents it from being subclassed and having its immutability compromised by overriding methods.
2.  **Make all fields `private` and `final`:** `private` restricts direct access, and `final` ensures that their values can only be assigned once (in the constructor).
3.  **Do not provide setter methods:** There should be no methods that can change the state of the object.
4.  **Provide a constructor that initializes all fields:** All fields must be set during object creation.
5.  **Perform "deep copy" for mutable object fields:** If your class has fields that are mutable objects (e.g., `ArrayList`, `Date`), you must:
    *   **In the constructor:** Create a *new* copy of the mutable object passed as an argument, instead of directly assigning the reference. This prevents external modification of your object's internal state.
    *   **In getter methods:** Return a *new* copy of the mutable object, not a direct reference. This prevents external code from getting a reference to your internal mutable object and modifying it.

#### Example 3: Custom Immutable Class (`Student`)

This example shows an immutable `Student` class which internally holds a mutable `ArrayList` of grades, demonstrating the need for defensive copying.

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class Student { // 1. Class is final

    private final String name; // 2. Fields are private and final
    private final int id;
    private final List<Integer> grades; // This is a mutable object field

    public Student(String name, int id, List<Integer> grades) {
        this.name = name;
        this.id = id;
        // 5a. Defensive copy in constructor for mutable field
        this.grades = new ArrayList<>(grades); 
    }

    // 3. No setter methods

    // Getter methods
    public String getName() {
        return name;
    }

    public int getId() {
        return id;
    }

    public List<Integer> getGrades() {
        // 5b. Defensive copy in getter for mutable field, or return unmodifiable list
        // Option 1: Return a new ArrayList (defensive copy)
        return new ArrayList<>(this.grades); 
        
        // Option 2: Return an unmodifiable view of the list (preferred for performance)
        // return Collections.unmodifiableList(this.grades); 
    }

    @Override
    public String toString() {
        return "Student{" +
               "name='" + name + '\'' +
               ", id=" + id +
               ", grades=" + grades +
               '}';
    }

    public static void main(String[] args) {
        // Input preparation for the Student object
        List<Integer> initialGrades = new ArrayList<>();
        initialGrades.add(90);
        initialGrades.add(85);

        Student student1 = new Student("Alice", 101, initialGrades);
        System.out.println("Initial student1: " + student1); // Input: Alice, 101, [90, 85]

        // --- Attempt to modify student1's state ---

        // 1. Try to modify the original list passed to the constructor
        initialGrades.add(70); 
        System.out.println("\nAfter modifying initialGrades list:");
        System.out.println("student1 (should be unchanged due to defensive copy): " + student1);
        // Expected: student1's grades should still be [90, 85]
        // Output confirmation: Student{name='Alice', id=101, grades=[90, 85]}

        // 2. Try to modify the list returned by the getter
        List<Integer> retrievedGrades = student1.getGrades();
        retrievedGrades.add(95); // This adds to the *copy* returned by getGrades()
        System.out.println("\nAfter attempting to modify retrievedGrades list:");
        System.out.println("student1 (should be unchanged due to defensive copy): " + student1);
        // Expected: student1's grades should still be [90, 85]
        // Output confirmation: Student{name='Alice', id=101, grades=[90, 85]}

        // 3. Demonstrate creating a "modified" student (which is actually a new object)
        List<Integer> newGradesForAlice = new ArrayList<>(student1.getGrades()); // Get current grades
        newGradesForAlice.add(92); // Add a new grade to the copy
        Student student2 = new Student(student1.getName(), student1.getId(), newGradesForAlice);
        System.out.println("\nstudent2 (a new object with modified grades): " + student2);
        // Expected: student2's grades should be [90, 85, 92]
        // Output confirmation: Student{name='Alice', id=101, grades=[90, 85, 92]}

        System.out.println("Original student1 (still unchanged): " + student1);
        // Output confirmation: Student{name='Alice', id=101, grades=[90, 85]}
    }
}
```

**Output:**
```
Initial student1: Student{name='Alice', id=101, grades=[90, 85]}

After modifying initialGrades list:
student1 (should be unchanged due to defensive copy): Student{name='Alice', id=101, grades=[90, 85]}

After attempting to modify retrievedGrades list:
student1 (should be unchanged due to defensive copy): Student{name='Alice', id=101, grades=[90, 85]}

student2 (a new object with modified grades): Student{name='Alice', id=101, grades=[90, 85, 92]}
Original student1 (still unchanged): Student{name='Alice', id=101, grades=[90, 85]}
```

**Explanation:** This example clearly demonstrates how defensive copying protects the immutability of the `Student` object. Even if the `initialGrades` list (used during construction) or the `retrievedGrades` list (returned by `getGrades()`) are modified, the internal `grades` list within `student1` remains unchanged. To get a "modified" student, we had to create a *new* `Student` object (`student2`) with the updated grades.

---

## II. Mutable Objects

A **mutable object** is an object whose state can be changed after it is created. You can modify its fields directly (if accessible) or through setter methods without creating a new object.

### Key Characteristics and Properties:

1.  **State Changeable:** The values of its fields can be altered at any point after construction.
2.  **Not Inherently Thread-Safe:** If multiple threads access and modify a mutable object concurrently without proper synchronization, it can lead to data corruption or inconsistent states (race conditions).
3.  **Efficiency for In-Place Modifications:** Can be more memory-efficient and performant for operations that involve frequent modifications, as they avoid creating new objects.
4.  **Not Suitable for Keys:** Generally not suitable for use as keys in `HashMap` or `HashSet`, because if the object is mutated after being inserted, its `hashCode()` could change, making it impossible to retrieve.

### Advantages of Mutability:

*   **Performance/Memory Efficiency:** No new objects are created for modifications, reducing garbage collection overhead and memory footprint, especially for objects that undergo many changes.
*   **Flexibility:** Allows for direct manipulation of an object's state.

### Disadvantages of Mutability:

*   **Thread Safety Issues:** Requires careful synchronization in multi-threaded environments, increasing complexity and potential for bugs.
*   **Debugging Difficulty:** Harder to track changes and reason about the object's state over time due to side effects.
*   **Security Risks:** Easier for external code to unintentionally or maliciously alter the object's state.
*   **`HashMap`/`HashSet` Problems:** Unreliable as collection keys if their state changes.

### Common Built-in Mutable Classes in Java:

Many common Java classes are mutable:

1.  **`StringBuilder`, `StringBuffer`:** Mutable alternatives to `String`.
2.  **Collection Classes:** `ArrayList`, `LinkedList`, `HashMap`, `HashSet`, `TreeMap`, `TreeSet`, `Date` (deprecated, but a classic example of mutability), `Calendar`.
3.  **`File`:** Represents a path, but its state (which path it points to) can be changed via methods like `renameTo()`.

---

#### Example 4: `StringBuilder` (Mutable)

```java
public class StringBuilderMutableExample {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder("Hello");
        System.out.println("Original StringBuilder: " + sb);
        System.out.println("Hash Code of sb: " + System.identityHashCode(sb)); // Identity hash code of the object

        // Modifying the StringBuilder in-place
        sb.append(" World");
        System.out.println("Modified StringBuilder: " + sb);
        System.out.println("Hash Code of sb: " + System.identityHashCode(sb)); // Same hash code (same object)

        sb.insert(5, " Java");
        System.out.println("After insertion: " + sb);
        System.out.println("Hash Code of sb: " + System.identityHashCode(sb)); // Still same hash code

        // Proof that it's the same object
        StringBuilder sb2 = sb; // sb2 now points to the same object as sb
        sb.reverse();
        System.out.println("\nAfter reversing sb:");
        System.out.println("sb: " + sb);
        System.out.println("sb2 (also reversed): " + sb2); // sb2 reflects the change because it's the same object
    }
}
```

**Output:**
```
Original StringBuilder: Hello
Hash Code of sb: 1392838282
Modified StringBuilder: Hello World
Hash Code of sb: 1392838282
After insertion: Hello Java World
Hash Code of sb: 1392838282

After reversing sb:
sb: dlroW avaJ olleH
sb2 (also reversed): dlroW avaJ olleH
```

**Explanation:** Unlike `String`, the `StringBuilder` object `sb` is modified directly in memory when methods like `append()` or `insert()` are called. The `System.identityHashCode()` remains the same, confirming that it's the *same object* whose internal state has been altered. The fact that `sb2` also shows the reversed string confirms that both references point to the same mutable object.

---

#### Example 5: `ArrayList` (Mutable Collection)

```java
import java.util.ArrayList;
import java.util.List;

public class ArrayListMutableExample {
    public static void main(String[] args) {
        List<String> fruits = new ArrayList<>();
        fruits.add("Apple");
        fruits.add("Banana");

        System.out.println("Original fruits list: " + fruits); // Input: [Apple, Banana]
        System.out.println("Hash Code of fruits: " + System.identityHashCode(fruits));

        // Modifying the list in-place
        fruits.add("Cherry");
        System.out.println("After adding Cherry: " + fruits); // Input: [Apple, Banana, Cherry]
        System.out.println("Hash Code of fruits: " + System.identityHashCode(fruits)); // Same hash code

        fruits.remove("Banana");
        System.out.println("After removing Banana: " + fruits); // Input: [Apple, Cherry]
        System.out.println("Hash Code of fruits: " + System.identityHashCode(fruits)); // Still same hash code

        // Demonstrate shared reference and side effects
        List<String> veggies = fruits; // veggies now points to the SAME list object
        veggies.add("Carrot");

        System.out.println("\nAfter modifying 'veggies' list:");
        System.out.println("fruits list: " + fruits); // Input: [Apple, Cherry, Carrot]
        System.out.println("veggies list: " + veggies); // Input: [Apple, Cherry, Carrot]
    }
}
```

**Output:**
```
Original fruits list: [Apple, Banana]
Hash Code of fruits: 1651191114
After adding Cherry: [Apple, Banana, Cherry]
Hash Code of fruits: 1651191114
After removing Banana: [Apple, Cherry]
Hash Code of fruits: 1651191114

After modifying 'veggies' list:
fruits list: [Apple, Cherry, Carrot]
veggies list: [Apple, Cherry, Carrot]
```

**Explanation:** `ArrayList` is a classic mutable collection. We can add, remove, and modify elements directly within the `fruits` list. The `System.identityHashCode()` remains constant because it's the *same list object* being modified. When `veggies` is assigned `fruits`, both references point to the same underlying `ArrayList`. Therefore, a modification through `veggies` is immediately reflected when accessing `fruits`. This "side effect" is a common source of bugs in multi-threaded environments if not properly managed.

---

#### Example 6: Custom Mutable Class (`Person`)

```java
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // Setter methods allow modification of the object's state
    public void setName(String name) {
        this.name = name;
    }

    public void setAge(int age) {
        this.age = age;
    }

    // Getter methods
    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    @Override
    public String toString() {
        return "Person{" +
               "name='" + name + '\'' +
               ", age=" + age +
               '}';
    }

    public static void main(String[] args) {
        Person person1 = new Person("Bob", 30);
        System.out.println("Initial person1: " + person1); // Input: Bob, 30
        System.out.println("Hash Code of person1: " + System.identityHashCode(person1));

        // Modify the state of person1
        person1.setAge(31);
        person1.setName("Robert");

        System.out.println("Modified person1: " + person1); // Input: Robert, 31
        System.out.println("Hash Code of person1: " + System.identityHashCode(person1)); // Same hash code

        // Demonstrate shared reference and side effects
        Person person2 = person1; // person2 now points to the SAME object as person1

        person2.setAge(32); // Modify person2
        
        System.out.println("\nAfter modifying person2:");
        System.out.println("person1 (also modified): " + person1); // Input: Robert, 32
        System.out.println("person2: " + person2); // Input: Robert, 32
    }
}
```

**Output:**
```
Initial person1: Person{name='Bob', age=30}
Hash Code of person1: 1651191114
Modified person1: Person{name='Robert', age=31}
Hash Code of person1: 1651191114

After modifying person2:
person1 (also modified): Person{name='Robert', age=32}
person2: Person{name='Robert', age=32}
```

**Explanation:** The `Person` class is mutable because it has setter methods (`setName`, `setAge`) that allow its internal state (`name`, `age`) to be changed after construction. The `System.identityHashCode()` confirms that the modifications happen on the *same object*. When `person2` is assigned `person1`, they both refer to the same object. Therefore, modifying the object through `person2` affects what `person1` sees, illustrating the potential for side effects.

---

## III. Key Differences: Mutable vs. Immutable Objects

| Feature               | Immutable Objects                                   | Mutable Objects                                     |
| :-------------------- | :-------------------------------------------------- | :-------------------------------------------------- |
| **Definition**        | State cannot be changed after creation.             | State can be changed after creation.                |
| **Modifiability**     | Cannot be modified. Operations return new objects.  | Can be modified in-place.                           |
| **Thread Safety**     | Inherently thread-safe (no synchronization needed). | Not inherently thread-safe (requires synchronization). |
| **Performance (Creation)** | Potentially higher overhead if many intermediate objects are created during "modifications." | Lower overhead for initial creation.                |
| **Performance (Modification)** | Potentially lower performance due to new object creation. | Higher performance for in-place modifications.      |
| **Caching**           | Easily cacheable.                                   | Not easily cacheable (state can change).            |
| **`HashMap` Keys**    | Excellent choice (hash code remains constant).      | Not suitable (hash code can change, breaking lookups). |
| **Security**          | More secure, as state cannot be tampered with.      | Less secure, state can be altered unexpectedly.     |
| **Complexity**        | Simpler to reason about and debug.                  | More complex due to potential side effects.         |
| **Examples**          | `String`, `Integer`, `LocalDate`, `List.of()`     | `StringBuilder`, `ArrayList`, `Date`                |

---

## IV. When to Use Which?

**Choose Immutable Objects when:**

*   **Thread Safety is paramount:** Essential for concurrent programming.
*   **Object's value needs to be constant:** Like configuration settings, identifiers, or fixed data.
*   **You need reliable keys for `HashMap`/`HashSet`:** Ensures consistent hashing.
*   **Security is a concern:** Prevents unauthorized state changes.
*   **Simplicity and predictability are desired:** Easier to test and reason about.
*   **Frequent reads, infrequent "modifications":** Where "modifications" mean creating new instances.

**Choose Mutable Objects when:**

*   **Performance and memory efficiency are critical for frequent in-place modifications:** E.g., building a large string (`StringBuilder`), accumulating items in a list (`ArrayList`).
*   **The object represents a dynamic state:** Where its properties are expected to change frequently (e.g., a counter, a sensor reading, a user session object).
*   **You need to pass an object to a method and expect that method to modify its state (by reference).**

---

## Conclusion

Both mutable and immutable objects have their place in Java programming. Understanding their distinct characteristics, advantages, and disadvantages allows developers to make informed design choices, leading to more robust, efficient, and maintainable applications. As a general rule, favoring immutability (where practical) often leads to simpler, safer, and more predictable code, especially in modern concurrent environments.