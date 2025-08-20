This Markdown document provides a detailed explanation and examples of the `groupingBy()` and `partitioningBy()` methods available in Java Streams' `Collectors` class.

---

# Demo of Streams `groupingBy()` and `partitioningBy()` Methods in Java

Java 8 introduced Streams, a powerful API for processing collections of data in a declarative way. Along with streams, the `java.util.stream.Collectors` class provides various terminal operations, among which `groupingBy()` and `partitioningBy()` are two of the most versatile for transforming a stream into a `Map`.

Both methods are used to categorize elements of a stream based on certain criteria and collect them into a `Map`. The key difference lies in the nature of the categorization.

---

## 1. `groupingBy()` Method

The `groupingBy()` collector is used for grouping objects by a common attribute. It collects elements of a stream into a `Map`, where the keys represent the grouped categories, and the values are lists of elements belonging to that category (or the result of a further downstream collector).

### Purpose
To group elements of a stream into a `Map` where keys are derived from the elements themselves, and values are collections of elements that share the same key.

### Signatures

`groupingBy()` has three main overloads:

1.  `static <T, K> Collector<T, ?, Map<K, List<T>>> groupingBy(Function<? super T, ? extends K> classifier)`
    *   **Parameters:**
        *   `classifier`: A `Function` that extracts the key (the grouping criterion) from each element.
    *   **Return Type:** A `Collector` that accumulates elements into a `Map<K, List<T>>`. The values are `List`s containing elements belonging to that key.

2.  `static <T, K, A, D> Collector<T, ?, Map<K, D>> groupingBy(Function<? super T, ? extends K> classifier, Collector<? super T, A, D> downstream)`
    *   **Parameters:**
        *   `classifier`: Same as above.
        *   `downstream`: A `Collector` that processes the elements within each group. This allows you to collect something other than a `List` (e.g., count, sum, average, a `Set`, etc.).
    *   **Return Type:** A `Collector` that accumulates elements into a `Map<K, D>`, where `D` is the result type of the `downstream` collector.

3.  `static <T, K, M extends Map<K, D>, A, D> Collector<T, ?, M> groupingBy(Function<? super T, ? extends K> classifier, Supplier<M> mapFactory, Collector<? super T, A, D> downstream)`
    *   **Parameters:**
        *   `classifier`: Same as above.
        *   `mapFactory`: A `Supplier` that constructs a new empty `Map` into which the results are inserted. This allows you to specify the type of `Map` (e.g., `TreeMap`, `LinkedHashMap`).
        *   `downstream`: Same as above.
    *   **Return Type:** A `Collector` that accumulates elements into a `Map` of type `M`.

### Example Data Model

Let's use a `Product` class for our examples:

```java
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.DoubleSummaryStatistics;
import java.util.Arrays;
import java.util.function.Function;
import java.util.stream.Collectors;

class Product {
    String name;
    String category;
    double price;

    public Product(String name, String category, double price) {
        this.name = name;
        this.category = category;
        this.price = price;
    }

    public String getName() { return name; }
    public String getCategory() { return category; }
    public double getPrice() { return price; }

    @Override
    public String toString() {
        return "Product{" +
               "name='" + name + '\'' +
               ", category='" + category + '\'' +
               ", price=" + String.format("%.2f", price) +
               '}';
    }
}
```

### Examples of `groupingBy()`

#### Example 1: Basic Grouping (using `groupingBy(classifier)`)

Group products by their `category`.

```java
public class GroupingByDemo {
    public static void main(String[] args) {
        List<Product> products = Arrays.asList(
            new Product("Laptop", "Electronics", 1200.00),
            new Product("Keyboard", "Electronics", 75.00),
            new Product("Mouse", "Electronics", 25.00),
            new Product("Desk Chair", "Furniture", 150.00),
            new Product("Table", "Furniture", 250.00),
            new Product("Monitor", "Electronics", 300.00),
            new Product("Coffee Mug", "Kitchen", 15.00),
            new Product("Blender", "Kitchen", 80.00)
        );

        // --- Example 1: Basic Grouping ---
        System.out.println("--- Example 1: Basic Grouping by Category ---");
        Map<String, List<Product>> productsByCategory = 
            products.stream()
                    .collect(Collectors.groupingBy(Product::getCategory));

        productsByCategory.forEach((category, productList) -> {
            System.out.println("Category: " + category);
            productList.forEach(product -> System.out.println("  " + product));
        });
    }
}
```

**Input Data:**

```
[
    Product{name='Laptop', category='Electronics', price=1200.00},
    Product{name='Keyboard', category='Electronics', price=75.00},
    Product{name='Mouse', category='Electronics', price=25.00},
    Product{name='Desk Chair', category='Furniture', price=150.00},
    Product{name='Table', category='Furniture', price=250.00},
    Product{name='Monitor', category='Electronics', price=300.00},
    Product{name='Coffee Mug', category='Kitchen', price=15.00},
    Product{name='Blender', category='Kitchen', price=80.00}
]
```

**Output:**

```
--- Example 1: Basic Grouping by Category ---
Category: Furniture
  Product{name='Desk Chair', category='Furniture', price=150.00}
  Product{name='Table', category='Furniture', price=250.00}
Category: Kitchen
  Product{name='Coffee Mug', category='Kitchen', price=15.00}
  Product{name='Blender', category='Kitchen', price=80.00}
Category: Electronics
  Product{name='Laptop', category='Electronics', price=1200.00}
  Product{name='Keyboard', category='Electronics', price=75.00}
  Product{name='Mouse', category='Electronics', price=25.00}
  Product{name='Monitor', category='Electronics', price=300.00}
```

#### Example 2: Grouping with a Downstream Collector (using `groupingBy(classifier, downstream)`)

a) **Count products per category:**

```java
        // --- Example 2a: Count products per category ---
        System.out.println("\n--- Example 2a: Count products per category ---");
        Map<String, Long> productCountByCategory = 
            products.stream()
                    .collect(Collectors.groupingBy(
                        Product::getCategory, 
                        Collectors.counting()
                    ));

        productCountByCategory.forEach((category, count) -> 
            System.out.println("Category: " + category + ", Count: " + count)
        );
```

**Output:**

```
--- Example 2a: Count products per category ---
Category: Furniture, Count: 2
Category: Kitchen, Count: 2
Category: Electronics, Count: 4
```

b) **Calculate average price per category:**

```java
        // --- Example 2b: Calculate average price per category ---
        System.out.println("\n--- Example 2b: Average price per category ---");
        Map<String, Double> averagePriceByCategory = 
            products.stream()
                    .collect(Collectors.groupingBy(
                        Product::getCategory, 
                        Collectors.averagingDouble(Product::getPrice)
                    ));

        averagePriceByCategory.forEach((category, avgPrice) -> 
            System.out.println("Category: " + category + ", Avg Price: " + String.format("%.2f", avgPrice))
        );
```

**Output:**

```
--- Example 2b: Average price per category ---
Category: Furniture, Avg Price: 200.00
Category: Kitchen, Avg Price: 47.50
Category: Electronics, Avg Price: 400.00
```

c) **Get a set of product names per category:**

```java
        // --- Example 2c: Get product names per category as a Set ---
        System.out.println("\n--- Example 2c: Product names per category (Set) ---");
        Map<String, Set<String>> productNamesByCategory =
            products.stream()
                    .collect(Collectors.groupingBy(
                        Product::getCategory,
                        Collectors.mapping(Product::getName, Collectors.toSet())
                    ));

        productNamesByCategory.forEach((category, names) -> {
            System.out.println("Category: " + category + ", Product Names: " + names);
        });
```

**Output:**

```
--- Example 2c: Product names per category (Set) ---
Category: Furniture, Product Names: [Table, Desk Chair]
Category: Kitchen, Product Names: [Blender, Coffee Mug]
Category: Electronics, Product Names: [Keyboard, Monitor, Mouse, Laptop]
```

#### Example 3: Grouping with a Custom Map Factory and Downstream Collector (using `groupingBy(classifier, mapFactory, downstream)`)

Store the grouped results in a `TreeMap` (which keeps keys sorted) and calculate sum of prices per category.

```java
        // --- Example 3: Grouping into a TreeMap with sum of prices ---
        System.out.println("\n--- Example 3: Grouping into a TreeMap with sum of prices ---");
        Map<String, Double> totalPricesByCategorySorted = 
            products.stream()
                    .collect(Collectors.groupingBy(
                        Product::getCategory,
                        TreeMap::new, // Custom Map Factory: TreeMap
                        Collectors.summingDouble(Product::getPrice)
                    ));

        totalPricesByCategorySorted.forEach((category, totalPrice) -> 
            System.out.println("Category: " + category + ", Total Price: " + String.format("%.2f", totalPrice))
        );
```

**Output:**

```
--- Example 3: Grouping into a TreeMap with sum of prices ---
Category: Electronics, Total Price: 1600.00
Category: Furniture, Total Price: 400.00
Category: Kitchen, Total Price: 95.00
```
Notice that "Electronics" comes before "Furniture" and "Kitchen" due to `TreeMap`'s natural ordering of keys.

---

## 2. `partitioningBy()` Method

The `partitioningBy()` collector is a specialized version of `groupingBy()`. It partitions elements into exactly two groups based on a `Predicate`: one for elements that satisfy the predicate (`true`), and one for elements that don't (`false`).

### Purpose
To divide elements of a stream into two distinct groups based on whether they match a given boolean condition. The resulting `Map` will always have `Boolean` keys (`true` and `false`).

### Signatures

`partitioningBy()` has two main overloads:

1.  `static <T> Collector<T, ?, Map<Boolean, List<T>>> partitioningBy(Predicate<? super T> predicate)`
    *   **Parameters:**
        *   `predicate`: A `Predicate` (a function that returns a boolean) used to classify elements.
    *   **Return Type:** A `Collector` that accumulates elements into a `Map<Boolean, List<T>>`. The values are `List`s.

2.  `static <T, A, D> Collector<T, ?, Map<Boolean, D>> partitioningBy(Predicate<? super T> predicate, Collector<? super T, A, D> downstream)`
    *   **Parameters:**
        *   `predicate`: Same as above.
        *   `downstream`: A `Collector` that processes the elements within each partition.
    *   **Return Type:** A `Collector` that accumulates elements into a `Map<Boolean, D>`, where `D` is the result type of the `downstream` collector.

### Example Data Model

Let's use a `Student` class for our examples:

```java
import java.util.List;
import java.util.Map;
import java.util.Arrays;
import java.util.stream.Collectors;
import java.util.function.Predicate;

class Student {
    String name;
    int score;

    public Student(String name, int score) {
        this.name = name;
        this.score = score;
    }

    public String getName() { return name; }
    public int getScore() { return score; }

    @Override
    public String toString() {
        return "Student{" +
               "name='" + name + '\'' +
               ", score=" + score +
               '}';
    }
}
```

### Examples of `partitioningBy()`

#### Example 1: Basic Partitioning (using `partitioningBy(predicate)`)

Partition students into "passed" (score >= 60) and "failed" (score < 60) groups.

```java
public class PartitioningByDemo {
    public static void main(String[] args) {
        List<Student> students = Arrays.asList(
            new Student("Alice", 85),
            new Student("Bob", 55),
            new Student("Charlie", 92),
            new Student("David", 70),
            new Student("Eve", 48),
            new Student("Frank", 60)
        );

        // --- Example 1: Basic Partitioning ---
        System.out.println("--- Example 1: Partitioning Students by Passing Score (>=60) ---");
        Map<Boolean, List<Student>> studentPartitions = 
            students.stream()
                    .collect(Collectors.partitioningBy(s -> s.getScore() >= 60));

        System.out.println("Passed Students:");
        studentPartitions.get(true).forEach(s -> System.out.println("  " + s));

        System.out.println("Failed Students:");
        studentPartitions.get(false).forEach(s -> System.out.println("  " + s));
    }
}
```

**Input Data:**

```
[
    Student{name='Alice', score=85},
    Student{name='Bob', score=55},
    Student{name='Charlie', score=92},
    Student{name='David', score=70},
    Student{name='Eve', score=48},
    Student{name='Frank', score=60}
]
```

**Output:**

```
--- Example 1: Partitioning Students by Passing Score (>=60) ---
Passed Students:
  Student{name='Alice', score=85}
  Student{name='Charlie', score=92}
  Student{name='David', score=70}
  Student{name='Frank', score=60}
Failed Students:
  Student{name='Bob', score=55}
  Student{name='Eve', score=48}
```

#### Example 2: Partitioning with a Downstream Collector (using `partitioningBy(predicate, downstream)`)

Count the number of passed and failed students.

```java
        // --- Example 2: Partitioning with downstream collector (counting) ---
        System.out.println("\n--- Example 2: Counting Passed/Failed Students ---");
        Map<Boolean, Long> studentCounts = 
            students.stream()
                    .collect(Collectors.partitioningBy(
                        s -> s.getScore() >= 60, 
                        Collectors.counting()
                    ));

        System.out.println("Number of Passed Students: " + studentCounts.get(true));
        System.out.println("Number of Failed Students: " + studentCounts.get(false));
```

**Output:**

```
--- Example 2: Counting Passed/Failed Students ---
Number of Passed Students: 4
Number of Failed Students: 2
```

---

## 3. `groupingBy()` vs. `partitioningBy()` - When to Use Which?

| Feature             | `groupingBy()`                                | `partitioningBy()`                                |
| :------------------ | :-------------------------------------------- | :------------------------------------------------ |
| **Number of Groups**| Arbitrary (determined by classifier function) | Exactly two (`true` and `false`)                  |
| **Key Type**        | Any type `K` derived from the classifier `Function` | Always `Boolean`                                  |
| **Grouping Logic**  | Based on a `Function` that maps an element to a key | Based on a `Predicate` that evaluates to `true` or `false` |
| **Use Case**        | Categorizing data into multiple distinct groups (e.g., products by category, employees by department). | Dividing data into two dichotomous sets (e.g., passing/failing, adult/minor, even/odd). |
| **Flexibility**     | More general and flexible. Can be used for partitioning by returning `true`/`false` from `Function`. | More specialized. Ideal when you *know* you only need two groups. |

**Choose `partitioningBy()`** when you want to divide your data into **exactly two groups** based on a boolean condition.
**Choose `groupingBy()`** when you need to divide your data into **any number of groups** based on a common attribute. You can simulate `partitioningBy()` with `groupingBy()` by having your classifier function return a boolean, but `partitioningBy()` is more semantically clear for a binary split.

---

## Conclusion

`groupingBy()` and `partitioningBy()` are powerful tools in the Java Stream API for aggregating and structuring data. They enable concise and expressive code for common data processing patterns, transforming flat lists of objects into organized maps, which can then be further processed or consumed. Understanding their differences and appropriate use cases allows you to write more efficient and readable Java code.