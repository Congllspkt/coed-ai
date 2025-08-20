The `Stream.filter()` method is a powerful and fundamental operation in Java Streams API, allowing you to select elements from a stream that satisfy a given condition. It's an **intermediate operation**, meaning it returns another `Stream` and can be chained with other stream operations.

---

# Demo: Java Stream's `filter()` Method

## 1. Introduction to `Stream.filter()`

The `filter()` method is used to create a new stream consisting of elements from the current stream that match a given `Predicate`. A `Predicate` is a functional interface that represents a boolean-valued function, essentially taking an argument and returning `true` or `false`.

**Purpose:** To narrow down a collection of data to only include items that meet specific criteria.

## 2. Method Signature

```java
Stream<T> filter(Predicate<? super T> predicate)
```

*   **`T`**: The type of elements in the stream.
*   **`predicate`**: A `Predicate` (a functional interface) that is applied to each element in the stream.
    *   If `predicate.test(element)` returns `true`, the element is included in the new stream.
    *   If `predicate.test(element)` returns `false`, the element is excluded.
*   **Returns**: A new `Stream<T>` containing only the elements that passed the predicate.

## 3. How it Works (Conceptual Flow)

1.  A stream of elements is generated (e.g., from a `List`, `Set`, `Array`).
2.  The `filter()` operation takes a `Predicate` as an argument.
3.  Each element from the source stream is passed to the `test()` method of the `Predicate`.
4.  If `test()` returns `true`, the element is allowed to pass through to the next stage of the stream pipeline.
5.  If `test()` returns `false`, the element is discarded.
6.  The result is a new stream containing only the filtered elements.

## 4. Key Characteristics

*   **Intermediate Operation:** Returns a new `Stream`. It does not perform any actual computation until a **terminal operation** (like `collect()`, `forEach()`, `count()`) is invoked.
*   **Stateless:** The operation for one element does not depend on the processing of previous elements.
*   **Non-Interfering:** Does not modify the underlying data source.
*   **Lazy Evaluation:** Elements are processed only when a terminal operation is called, and only as many as necessary.

---

## 5. Examples

Let's explore `filter()` with various data types and scenarios.

### Example 1: Filtering Integers (Even Numbers)

This example demonstrates how to filter a list of integers to keep only the even numbers.

**Input:** A `List` of `Integer` objects.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamFilterExample1 {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        System.out.println("Original Numbers: " + numbers);

        // Filter for even numbers
        List<Integer> evenNumbers = numbers.stream()
                                            .filter(n -> n % 2 == 0) // Predicate: n is even
                                            .collect(Collectors.toList());

        System.out.println("Even Numbers: " + evenNumbers);
    }
}
```

**Output:**

```
Original Numbers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Even Numbers: [2, 4, 6, 8, 10]
```

### Example 2: Filtering Strings (Starts with 'A' and Length > 3)

Here, we'll filter a list of names to find those that start with the letter 'A' AND have a length greater than 3. This demonstrates combining conditions within the predicate.

**Input:** A `List` of `String` objects.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamFilterExample2 {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "Bob", "Anna", "Charlie", "Adam", "David", "Ann");

        System.out.println("Original Names: " + names);

        // Filter names that start with 'A' and have a length greater than 3
        List<String> filteredNames = names.stream()
                                            .filter(name -> name.startsWith("A") && name.length() > 3)
                                            .collect(Collectors.toList());

        System.out.println("Names starting with 'A' and length > 3: " + filteredNames);
    }
}
```

**Output:**

```
Original Names: [Alice, Bob, Anna, Charlie, Adam, David, Ann]
Names starting with 'A' and length > 3: [Alice, Anna, Adam]
```

### Example 3: Filtering Custom Objects (Employees by Age and Salary)

This is a very common use case: filtering a list of custom objects based on their properties.

First, let's define a simple `Employee` class:

```java
// Employee.java
public class Employee {
    private String name;
    private int age;
    private double salary;

    public Employee(String name, int age, double salary) {
        this.name = name;
        this.age = age;
        this.salary = salary;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    public double getSalary() {
        return salary;
    }

    @Override
    public String toString() {
        return "Employee{name='" + name + "', age=" + age + ", salary=" + salary + '}';
    }
}
```

Now, the filtering example:

**Input:** A `List` of `Employee` objects.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamFilterExample3 {
    public static void main(String[] args) {
        List<Employee> employees = Arrays.asList(
            new Employee("Alice", 30, 60000.0),
            new Employee("Bob", 25, 45000.0),
            new Employee("Charlie", 35, 75000.0),
            new Employee("David", 28, 50000.0),
            new Employee("Eve", 40, 90000.0)
        );

        System.out.println("Original Employees:");
        employees.forEach(System.out::println);

        // Filter employees who are older than 30 AND earn more than 50000
        List<Employee> seniorHighEarners = employees.stream()
                                                    .filter(e -> e.getAge() > 30 && e.getSalary() > 50000)
                                                    .collect(Collectors.toList());

        System.out.println("\nEmployees (Age > 30 AND Salary > 50000):");
        seniorHighEarners.forEach(System.out::println);
    }
}
```

**Output:**

```
Original Employees:
Employee{name='Alice', age=30, salary=60000.0}
Employee{name='Bob', age=25, salary=45000.0}
Employee{name='Charlie', age=35, salary=75000.0}
Employee{name='David', age=28, salary=50000.0}
Employee{name='Eve', age=40, salary=90000.0}

Employees (Age > 30 AND Salary > 50000):
Employee{name='Charlie', age=35, salary=75000.0}
Employee{name='Eve', age=40, salary=90000.0}
```

### Example 4: Chaining Multiple Filters and Other Operations

You can chain multiple `filter()` calls, or combine `filter()` with other intermediate operations like `map()` before a terminal operation. Each `filter()` step progressively narrows down the elements in the stream.

**Input:** A `List` of `Integer` objects.

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StreamFilterExample4 {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        System.out.println("Original Numbers: " + numbers);

        // 1. Filter numbers greater than 4
        // 2. Then, filter the remaining numbers to keep only odd ones
        // 3. Then, map (transform) each remaining number by multiplying it by 2
        // 4. Finally, collect the results into a new List
        List<Integer> processedNumbers = numbers.stream()
                                                .filter(n -> n > 4)    // Keep: 5, 6, 7, 8, 9, 10
                                                .filter(n -> n % 2 != 0) // Keep: 5, 7, 9 (from previous result)
                                                .map(n -> n * 2)       // Transform: 10, 14, 18
                                                .collect(Collectors.toList());

        System.out.println("Processed Numbers ( > 4, then Odd, then * 2): " + processedNumbers);
    }
}
```

**Output:**

```
Original Numbers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Processed Numbers ( > 4, then Odd, then * 2): [10, 14, 18]
```

---

## 6. Best Practices and Tips

*   **Keep Predicates Simple:** Write clear and concise predicates. For complex logic, consider extracting it into a named method or a separate `Predicate` object.
*   **Chain Filters:** For multiple filtering criteria, chaining `filter()` calls often leads to more readable code than combining many `&&` or `||` operators in a single predicate.
*   **Method References:** For simple checks (e.g., `String::isEmpty`), use method references for even more concise code.
*   **Performance:** `filter()` is highly optimized. Thanks to lazy evaluation, elements are only processed when needed, and short-circuiting might occur with certain terminal operations (though `filter` itself doesn't short-circuit the entire stream).

---

## 7. Conclusion

The `Stream.filter()` method is an indispensable tool in the Java Streams API for data processing. It allows you to express selection logic declaratively, leading to more readable, concise, and often more efficient code compared to traditional loop-based filtering. By understanding its behavior as an intermediate operation and how to construct effective `Predicate`s, you can powerfully transform and refine your data streams.