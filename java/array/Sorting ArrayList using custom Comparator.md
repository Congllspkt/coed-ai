Sorting an `ArrayList` in Java using a custom `Comparator` is a fundamental skill. While `Collections.sort()` can sort lists of objects that implement the `Comparable` interface (natural ordering), a `Comparator` gives you the flexibility to define *any* sorting logic, including sorting by multiple fields, in reverse order, or based on specific business rules.

---

## Sorting an ArrayList using a Custom Comparator in Java

### 1. Introduction

Java's `java.util.Collections` class provides a `sort()` method that can sort a `List`.
*   The simpler `Collections.sort(List<T> list)` overload requires the elements in the list to implement the `Comparable<T>` interface, providing a "natural" order.
*   The more flexible `Collections.sort(List<T> list, Comparator<? super T> c)` overload allows you to provide a custom `Comparator` instance to define the sorting logic on the fly. This is what we'll focus on.

### 2. Why Use a Custom Comparator?

You would use a custom `Comparator` when:

*   **Your objects do not have a natural order:** Or you don't want to enforce one via `Comparable`.
*   **You need multiple sorting criteria:** For example, sort by name, and if names are the same, then sort by age.
*   **You need different sorting orders:** Ascending vs. Descending for the same field.
*   **You are sorting objects from a third-party library:** Where you cannot modify their classes to implement `Comparable`.

### 3. The `Comparator` Interface

The `Comparator` interface is a functional interface (meaning it has a single abstract method) defined as:

```java
public interface Comparator<T> {
    int compare(T o1, T o2);

    // Other default and static methods (Java 8+)
}
```

The `compare(T o1, T o2)` method is the heart of the `Comparator`. It defines the comparison logic between two objects, `o1` and `o2`.

**Return Values of `compare(o1, o2)`:**

*   **Negative integer:** If `o1` should come *before* `o2`. (`o1 < o2`)
*   **Zero:** If `o1` and `o2` are considered *equal* for sorting purposes. (`o1 == o2`)
*   **Positive integer:** If `o1` should come *after* `o2`. (`o1 > o2`)

**Important Note for Primitives:**
When comparing primitive integers (like `int` or `long`), it's generally safer and clearer to use `Integer.compare(int x, int y)` or `Long.compare(long x, long y)` instead of `x - y` to avoid potential integer overflow issues for very large differences.

### 4. Step-by-Step Guide

1.  **Define your Data Class:** Create the class for the objects you want to sort. Ensure it has relevant fields and potentially a `toString()` method for easy printing.
2.  **Create your `ArrayList`:** Populate it with instances of your data class.
3.  **Implement the `Comparator` Interface:** Create a new class (or use an anonymous inner class/lambda expression in Java 8+) that implements `Comparator<YourClass>` and overrides the `compare()` method.
4.  **Call `Collections.sort()`:** Pass your `ArrayList` and an instance of your custom `Comparator` to this method.

### 5. Examples

Let's use a `Person` class for our examples:

```java
// Person.java
public class Person {
    private String name;
    private int age;
    private String city;

    public Person(String name, int age, String city) {
        this.name = name;
        this.age = age;
        this.city = city;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    public String getCity() {
        return city;
    }

    @Override
    public String toString() {
        return "Person [Name: " + name + ", Age: " + age + ", City: " + city + "]";
    }
}
```

---

#### Example 1: Sorting by a Single Field (Age Ascending)

We want to sort a list of `Person` objects based on their `age` in ascending order.

**1. Create the `AgeComparator` class:**

```java
// AgeComparator.java
import java.util.Comparator;

public class AgeComparator implements Comparator<Person> {
    @Override
    public int compare(Person p1, Person p2) {
        // Compares ages. Integer.compare is safe and recommended.
        // Returns negative if p1.age < p2.age
        // Returns zero if p1.age == p2.age
        // Returns positive if p1.age > p2.age
        return Integer.compare(p1.getAge(), p2.getAge());
    }
}
```

**2. Main Program:**

```java
// PersonSortingExample1.java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class PersonSortingExample1 {
    public static void main(String[] args) {
        // Input: Create an ArrayList of Person objects
        List<Person> people = new ArrayList<>();
        people.add(new Person("Alice", 30, "New York"));
        people.add(new Person("Bob", 25, "Los Angeles"));
        people.add(new Person("Charlie", 35, "Chicago"));
        people.add(new Person("David", 25, "Houston")); // Same age as Bob

        System.out.println("--- Before Sorting (by Age Ascending) ---");
        for (Person p : people) {
            System.out.println(p);
        }

        // Sort the list using our custom AgeComparator
        Collections.sort(people, new AgeComparator());

        System.out.println("\n--- After Sorting (by Age Ascending) ---");
        // Output: Print the sorted list
        for (Person p : people) {
            System.out.println(p);
        }
    }
}
```

**Output:**

```
--- Before Sorting (by Age Ascending) ---
Person [Name: Alice, Age: 30, City: New York]
Person [Name: Bob, Age: 25, City: Los Angeles]
Person [Name: Charlie, Age: 35, City: Chicago]
Person [Name: David, Age: 25, City: Houston]

--- After Sorting (by Age Ascending) ---
Person [Name: Bob, Age: 25, City: Los Angeles]
Person [Name: David, Age: 25, City: Houston]
Person [Name: Alice, Age: 30, City: New York]
Person [Name: Charlie, Age: 35, City: Chicago]
```
*Note: Bob and David (both age 25) maintain their relative order because the comparator returns 0, indicating equality for sorting purposes. The `Collections.sort` algorithm is stable.*

---

#### Example 2: Sorting by Multiple Fields (Name Ascending, then Age Ascending)

We want to sort by `name` first. If names are the same, then sort by `age`.

**1. Create the `NameAgeComparator` class:**

```java
// NameAgeComparator.java
import java.util.Comparator;

public class NameAgeComparator implements Comparator<Person> {
    @Override
    public int compare(Person p1, Person p2) {
        // 1. Compare by Name
        int nameComparison = p1.getName().compareTo(p2.getName());

        // If names are different, return the result of name comparison
        if (nameComparison != 0) {
            return nameComparison;
        }

        // If names are the same, then compare by Age
        return Integer.compare(p1.getAge(), p2.getAge());
    }
}
```

**2. Main Program:**

```java
// PersonSortingExample2.java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class PersonSortingExample2 {
    public static void main(String[] args) {
        // Input: Create an ArrayList of Person objects
        List<Person> people = new ArrayList<>();
        people.add(new Person("Alice", 30, "New York"));
        people.add(new Person("Bob", 25, "Los Angeles"));
        people.add(new Person("Charlie", 35, "Chicago"));
        people.add(new Person("Alice", 28, "San Francisco")); // Another Alice
        people.add(new Person("David", 25, "Houston"));

        System.out.println("--- Before Sorting (by Name then Age) ---");
        for (Person p : people) {
            System.out.println(p);
        }

        // Sort the list using our custom NameAgeComparator
        Collections.sort(people, new NameAgeComparator());

        System.out.println("\n--- After Sorting (by Name then Age) ---");
        // Output: Print the sorted list
        for (Person p : people) {
            System.out.println(p);
        }
    }
}
```

**Output:**

```
--- Before Sorting (by Name then Age) ---
Person [Name: Alice, Age: 30, City: New York]
Person [Name: Bob, Age: 25, City: Los Angeles]
Person [Name: Charlie, Age: 35, City: Chicago]
Person [Name: Alice, Age: 28, City: San Francisco]
Person [Name: David, Age: 25, City: Houston]

--- After Sorting (by Name then Age) ---
Person [Name: Alice, Age: 28, City: San Francisco]
Person [Name: Alice, Age: 30, City: New York]
Person [Name: Bob, Age: 25, City: Los Angeles]
Person [Name: Charlie, Age: 35, City: Chicago]
Person [Name: David, Age: 25, City: Houston]
```
*Note: The two "Alice" entries are now sorted correctly by age.*

---

#### Example 3: Sorting in Reverse Order (Age Descending)

We want to sort by `age` in descending order.

**1. Create the `AgeDescendingComparator` class:**

```java
// AgeDescendingComparator.java
import java.util.Comparator;

public class AgeDescendingComparator implements Comparator<Person> {
    @Override
    public int compare(Person p1, Person p2) {
        // To sort in descending order, simply reverse the comparison.
        // p2.getAge() vs p1.getAge()
        return Integer.compare(p2.getAge(), p1.getAge());
    }
}
```

**2. Main Program:**

```java
// PersonSortingExample3.java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class PersonSortingExample3 {
    public static void main(String[] args) {
        // Input: Create an ArrayList of Person objects
        List<Person> people = new ArrayList<>();
        people.add(new Person("Alice", 30, "New York"));
        people.add(new Person("Bob", 25, "Los Angeles"));
        people.add(new Person("Charlie", 35, "Chicago"));
        people.add(new Person("David", 28, "Houston"));

        System.out.println("--- Before Sorting (by Age Descending) ---");
        for (Person p : people) {
            System.out.println(p);
        }

        // Sort the list using our custom AgeDescendingComparator
        Collections.sort(people, new AgeDescendingComparator());

        System.out.println("\n--- After Sorting (by Age Descending) ---");
        // Output: Print the sorted list
        for (Person p : people) {
            System.out.println(p);
        }
    }
}
```

**Output:**

```
--- Before Sorting (by Age Descending) ---
Person [Name: Alice, Age: 30, City: New York]
Person [Name: Bob, Age: 25, City: Los Angeles]
Person [Name: Charlie, Age: 35, City: Chicago]
Person [Name: David, Age: 28, City: Houston]

--- After Sorting (by Age Descending) ---
Person [Name: Charlie, Age: 35, City: Chicago]
Person [Name: Alice, Age: 30, City: New York]
Person [Name: David, Age: 28, City: Houston]
Person [Name: Bob, Age: 25, City: Los Angeles]
```

---

### 6. Modern Java (Java 8+) - Lambdas and `Comparator.comparing()`

Java 8 introduced lambda expressions and new static/default methods in the `Comparator` interface, making custom sorting much more concise and readable.

#### 6.1. Using Lambda Expressions

For simple comparisons, you can define the `Comparator` directly as a lambda expression:

```java
// Sort by Age Ascending using Lambda
Collections.sort(people, (p1, p2) -> Integer.compare(p1.getAge(), p2.getAge()));

// Sort by Age Descending using Lambda
Collections.sort(people, (p1, p2) -> Integer.compare(p2.getAge(), p1.getAge()));
```

#### 6.2. Using `Comparator.comparing()` and `thenComparing()`

These methods are incredibly powerful for creating comparators based on getter methods.

**1. Sorting by a single field (Age Ascending):**

```java
import java.util.Comparator; // Don't forget this import

// ... inside your main method ...

// Input: Same as previous examples
List<Person> people = new ArrayList<>();
people.add(new Person("Alice", 30, "New York"));
people.add(new Person("Bob", 25, "Los Angeles"));
people.add(new Person("Charlie", 35, "Chicago"));
people.add(new Person("David", 25, "Houston"));

System.out.println("--- Before Sorting ---");
people.forEach(System.out::println);

// Sort using Comparator.comparing()
Collections.sort(people, Comparator.comparing(Person::getAge)); 
// Or if you prefer lambda syntax: Comparator.comparing(p -> p.getAge())

System.out.println("\n--- After Sorting (Age Ascending - Java 8) ---");
people.forEach(System.out::println);
```

**2. Sorting by multiple fields (Name Ascending, then Age Ascending):**

```java
// ... inside your main method ...

// Input: Same as previous examples, with duplicate names for test
List<Person> people = new ArrayList<>();
people.add(new Person("Alice", 30, "New York"));
people.add(new Person("Bob", 25, "Los Angeles"));
people.add(new Person("Charlie", 35, "Chicago"));
people.add(new Person("Alice", 28, "San Francisco"));
people.add(new Person("David", 25, "Houston"));

System.out.println("--- Before Sorting ---");
people.forEach(System.out::println);

// Sort using Comparator.comparing() and thenComparing()
Collections.sort(people, Comparator.comparing(Person::getName)
                                  .thenComparing(Person::getAge));

System.out.println("\n--- After Sorting (Name then Age - Java 8) ---");
people.forEach(System.out::println);
```

**3. Sorting in Reverse Order (Age Descending):**

```java
// ... inside your main method ...

// Input: Same as previous examples
List<Person> people = new ArrayList<>();
people.add(new Person("Alice", 30, "New York"));
people.add(new Person("Bob", 25, "Los Angeles"));
people.add(new Person("Charlie", 35, "Chicago"));
people.add(new Person("David", 28, "Houston"));

System.out.println("--- Before Sorting ---");
people.forEach(System.out::println);

// Sort using Comparator.comparing() and reversed()
Collections.sort(people, Comparator.comparing(Person::getAge).reversed());

System.out.println("\n--- After Sorting (Age Descending - Java 8) ---");
people.forEach(System.out::println);
```

You can even chain `thenComparing` for more complex criteria and use `reversed()` at any point in the chain:

```java
// Sort by Name Asc, then Age Desc, then City Asc
Collections.sort(people, 
    Comparator.comparing(Person::getName)
              .thenComparing(Comparator.comparing(Person::getAge).reversed()) // Age descending
              .thenComparing(Person::getCity));
```

### Conclusion

Using a custom `Comparator` with `Collections.sort()` provides immense flexibility for ordering `ArrayList` elements based on specific, dynamic, or multi-faceted criteria. With Java 8 and newer, lambda expressions and `Comparator.comparing()` methods have significantly streamlined the process, making custom sorting code much more concise and readable.