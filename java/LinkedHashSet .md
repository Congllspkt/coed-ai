# LinkedHashSet in Java

## Introduction

The `LinkedHashSet` class in Java is a part of the Java Collections Framework and belongs to the `java.util` package. It's a unique data structure that combines the features of both `HashSet` and `LinkedList`.

At its core, `LinkedHashSet` is a `Set`, which means it **does not allow duplicate elements**. What makes it special is that, unlike `HashSet`, it **maintains the insertion order** of elements. This means when you iterate over a `LinkedHashSet`, the elements will be returned in the order in which they were added.

It achieves this by using a hash table for storage (like `HashSet`) and a doubly-linked list to maintain the order of elements (like `LinkedList` or `LinkedHashMap`).

## Key Characteristics / Features

1.  **No Duplicate Elements:** Like any other `Set` implementation, `LinkedHashSet` ensures that all its elements are unique. If you try to add a duplicate element, the `add()` method will return `false`, and the set will remain unchanged.
2.  **Maintains Insertion Order:** This is its primary distinguishing feature. When you iterate through a `LinkedHashSet`, the elements are returned in the order they were inserted.
3.  **Non-Synchronized:** `LinkedHashSet` is not thread-safe. If multiple threads access a `LinkedHashSet` concurrently and at least one of the threads modifies the set, it must be synchronized externally. This is typically done by wrapping the set with `Collections.synchronizedSet()`.
4.  **Permits One `null` Element:** A `LinkedHashSet` can store one `null` element, just like `HashSet`.
5.  **Performance:**
    *   **Basic Operations (add, remove, contains, size):** On average, these operations perform in **O(1)** (constant time), assuming a good hash function and proper load factor. In the worst case (many collisions), it can degrade to O(n).
    *   **Iteration:** Iteration over `LinkedHashSet` is generally faster than `HashSet` because it iterates through the elements in the linked list, which is more predictable than traversing the hash table.

## How it Works Internally

`LinkedHashSet` is implemented using a **`LinkedHashMap`**.
*   Each element added to the `LinkedHashSet` becomes a key in the internal `LinkedHashMap`.
*   A dummy `Object` (or `Boolean`) is used as the value for these keys in the `LinkedHashMap`.
*   The `LinkedHashMap` itself maintains a doubly-linked list running through its entries. This linked list defines the iteration order, which is the order in which elements were inserted into the `LinkedHashSet`.

This internal structure allows it to provide fast operations (due to hashing) while preserving insertion order (due to the linked list).

## Constructors

`LinkedHashSet` provides several constructors:

1.  **`LinkedHashSet()`:**
    *   Constructs a new, empty linked hash set with the default initial capacity (16) and load factor (0.75).
    ```java
    LinkedHashSet<String> mySet = new LinkedHashSet<>();
    ```

2.  **`LinkedHashSet(int initialCapacity)`:**
    *   Constructs a new, empty linked hash set with the specified initial capacity and the default load factor (0.75).
    *   Useful for performance if you know approximately how many elements you'll store, as it reduces rehashing.
    ```java
    LinkedHashSet<Integer> capacitySet = new LinkedHashSet<>(100);
    ```

3.  **`LinkedHashSet(int initialCapacity, float loadFactor)`:**
    *   Constructs a new, empty linked hash set with the specified initial capacity and load factor.
    *   `loadFactor`: A measure of how full the hash table can get before it is rehashed (its capacity is increased). Default is 0.75.
    ```java
    LinkedHashSet<Double> preciseSet = new LinkedHashSet<>(50, 0.8f);
    ```

4.  **`LinkedHashSet(Collection<? extends E> c)`:**
    *   Constructs a new linked hash set with the same elements as the specified collection. The elements are added in the order they are returned by the collection's iterator.
    ```java
    List<String> fruitsList = Arrays.asList("Apple", "Banana", "Orange");
    LinkedHashSet<String> fruitsSet = new LinkedHashSet<>(fruitsList);
    // fruitsSet will contain "Apple", "Banana", "Orange" in that order
    ```

## Commonly Used Methods

`LinkedHashSet` inherits methods from `AbstractSet`, `Set`, and `Collection` interfaces.

*   `boolean add(E e)`: Adds the specified element to the set if it is not already present. Returns `true` if the element was added, `false` otherwise.
*   `boolean remove(Object o)`: Removes the specified element from the set if it is present. Returns `true` if the element was removed, `false` otherwise.
*   `boolean contains(Object o)`: Returns `true` if this set contains the specified element.
*   `int size()`: Returns the number of elements in this set.
*   `boolean isEmpty()`: Returns `true` if this set contains no elements.
*   `void clear()`: Removes all of the elements from this set.
*   `Iterator<E> iterator()`: Returns an iterator over the elements in this set, in insertion order.

## When to Use `LinkedHashSet`

*   **When you need uniqueness and insertion order:** This is the primary use case. If you need to ensure no duplicates *and* preserve the order in which items were added, `LinkedHashSet` is the perfect choice.
*   **Caching with order:** If you are building a cache where the order of insertion matters (e.g., "recently used" items), and you need fast lookups/additions.
*   **Maintaining call history/log:** If you want to keep a unique history of operations or events in the order they occurred.
*   **Faster iteration over `HashSet` when order matters:** While `HashSet` offers average O(1) for basic operations, its iteration order is not guaranteed and can be slow if the underlying hash table is poorly distributed. `LinkedHashSet` iteration is generally faster for iterating *all* elements because it just traverses the linked list.

## When Not to Use `LinkedHashSet`

*   **When order doesn't matter and maximum raw performance is critical:** `HashSet` might offer slightly better performance for `add`, `remove`, and `contains` operations as it doesn't have the overhead of maintaining the linked list (though the difference is often negligible in practice).
*   **When you need elements to be sorted (natural order or custom comparator):** Use `TreeSet` instead, as it automatically sorts elements.
*   **When you need a key-value mapping:** Use `LinkedHashMap` if you need insertion-ordered key-value pairs, or `HashMap` if order doesn't matter.

## Examples

### Example 1: Basic Usage and Insertion Order

This example demonstrates how `LinkedHashSet` maintains insertion order and handles duplicates.

```java
import java.util.LinkedHashSet;

public class LinkedHashSetExample1 {
    public static void main(String[] args) {
        System.out.println("--- LinkedHashSet Basic Usage and Insertion Order ---");

        // 1. Create a LinkedHashSet
        LinkedHashSet<String> fruits = new LinkedHashSet<>();
        System.out.println("Initial set: " + fruits + " (size: " + fruits.size() + ")");

        // 2. Add elements
        System.out.println("\nAdding elements:");
        fruits.add("Apple");
        fruits.add("Banana");
        fruits.add("Cherry");
        System.out.println("After adding Apple, Banana, Cherry: " + fruits); // Insertion order maintained

        // 3. Try to add a duplicate element
        boolean addedDuplicate = fruits.add("Apple"); // Returns false
        System.out.println("Attempted to add 'Apple' again. Was it added? " + addedDuplicate);
        System.out.println("Set after attempting to add duplicate: " + fruits); // "Apple" is not added again, order unchanged

        fruits.add("Date"); // Add a new element
        System.out.println("After adding Date: " + fruits);

        // 4. Iterate over the elements (insertion order will be preserved)
        System.out.println("\nIterating over elements (insertion order):");
        for (String fruit : fruits) {
            System.out.println("  " + fruit);
        }

        // 5. Check size
        System.out.println("Current size of the set: " + fruits.size());

        // 6. Check if an element exists
        System.out.println("Does set contain 'Banana'? " + fruits.contains("Banana"));
        System.out.println("Does set contain 'Grape'? " + fruits.contains("Grape"));

        // 7. Remove an element
        System.out.println("\nRemoving 'Banana':");
        boolean removed = fruits.remove("Banana");
        System.out.println("Was 'Banana' removed? " + removed);
        System.out.println("Set after removing Banana: " + fruits); // Order of remaining elements is preserved

        // 8. Clear the set
        System.out.println("\nClearing the set:");
        fruits.clear();
        System.out.println("Set after clearing: " + fruits + " (size: " + fruits.size() + ")");
        System.out.println("Is set empty? " + fruits.isEmpty());
    }
}
```

**Input:** (None from user, controlled by code)

**Output:**
```
--- LinkedHashSet Basic Usage and Insertion Order ---
Initial set: [] (size: 0)

Adding elements:
After adding Apple, Banana, Cherry: [Apple, Banana, Cherry]
Attempted to add 'Apple' again. Was it added? false
Set after attempting to add duplicate: [Apple, Banana, Cherry]
After adding Date: [Apple, Banana, Cherry, Date]

Iterating over elements (insertion order):
  Apple
  Banana
  Cherry
  Date
Current size of the set: 4
Does set contain 'Banana'? true
Does set contain 'Grape'? false

Removing 'Banana':
Was 'Banana' removed? true
Set after removing Banana: [Apple, Cherry, Date]

Clearing the set:
Set after clearing: [] (size: 0)
Is set empty? true
```

### Example 2: Working with Custom Objects (Importance of `hashCode()` and `equals()`)

When storing custom objects in a `LinkedHashSet` (or any hash-based collection like `HashSet`, `HashMap`), it's crucial to correctly override the `equals()` and `hashCode()` methods. If not, the `LinkedHashSet` might not correctly identify duplicates or find elements.

```java
import java.util.LinkedHashSet;
import java.util.Objects;

class Product {
    private String id;
    private String name;
    private double price;

    public Product(String id, String name, double price) {
        this.id = id;
        this.name = name;
        this.price = price;
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }

    @Override
    public String toString() {
        return "Product{id='" + id + "', name='" + name + "', price=" + price + '}';
    }

    // IMPORTANT: Override equals() and hashCode() for proper Set behavior
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Product product = (Product) o;
        return Objects.equals(id, product.id); // Products are equal if their IDs are the same
    }

    @Override
    public int hashCode() {
        return Objects.hash(id); // Hash code based on the ID
    }
}

public class LinkedHashSetExample2 {
    public static void main(String[] args) {
        System.out.println("--- LinkedHashSet with Custom Objects ---");

        LinkedHashSet<Product> productCatalog = new LinkedHashSet<>();

        Product p1 = new Product("P001", "Laptop", 1200.00);
        Product p2 = new Product("P002", "Mouse", 25.00);
        Product p3 = new Product("P003", "Keyboard", 75.00);
        Product p4_duplicate_id = new Product("P001", "Gaming Laptop", 1500.00); // Same ID as p1, different name/price
        Product p5 = new Product("P004", "Monitor", 300.00);

        System.out.println("Adding products:");
        productCatalog.add(p1);
        productCatalog.add(p2);
        productCatalog.add(p3);
        System.out.println("Catalog after adding P001, P002, P003:\n" + productCatalog);

        System.out.println("\nAttempting to add P001 again (but with different name/price): " + p4_duplicate_id);
        boolean addedDuplicate = productCatalog.add(p4_duplicate_id);
        System.out.println("Was the duplicate ID product added? " + addedDuplicate);
        // Note: The original P001 (Laptop) remains because of insertion order.
        // If it were a plain HashSet, the new P001 might replace the old one based on JVM's internal logic,
        // but LinkedHashSet will keep the *first* one encountered with that 'id'.
        System.out.println("Catalog after attempting to add duplicate:\n" + productCatalog);

        productCatalog.add(p5);
        System.out.println("\nCatalog after adding P004:\n" + productCatalog);

        System.out.println("\nIterating through the product catalog (insertion order):");
        for (Product product : productCatalog) {
            System.out.println("  " + product);
        }

        System.out.println("\nChecking if P002 (Mouse) is in catalog: " + productCatalog.contains(new Product("P002", "Dummy", 0.0))); // Only ID matters for equals()
        System.out.println("Checking if P005 (Non-existent) is in catalog: " + productCatalog.contains(new Product("P005", "Dummy", 0.0)));
    }
}
```

**Input:** (None from user, controlled by code)

**Output:**
```
--- LinkedHashSet with Custom Objects ---
Adding products:
Catalog after adding P001, P002, P003:
[Product{id='P001', name='Laptop', price=1200.0}, Product{id='P002', name='Mouse', price=25.0}, Product{id='P003', name='Keyboard', price=75.0}]

Attempting to add P001 again (but with different name/price): Product{id='P001', name='Gaming Laptop', price=1500.0}
Was the duplicate ID product added? false
Catalog after attempting to add duplicate:
[Product{id='P001', name='Laptop', price=1200.0}, Product{id='P002', name='Mouse', price=25.0}, Product{id='P003', name='Keyboard', price=75.0}]

Catalog after adding P004:
[Product{id='P001', name='Laptop', price=1200.0}, Product{id='P002', name='Mouse', price=25.0}, Product{id='P003', name='Keyboard', price=75.0}, Product{id='P004', name='Monitor', price=300.0}]

Iterating through the product catalog (insertion order):
  Product{id='P001', name='Laptop', price=1200.0}
  Product{id='P002', name='Mouse', price=25.0}
  Product{id='P003', name='Keyboard', price=75.0}
  Product{id='P004', name='Monitor', price=300.0}

Checking if P002 (Mouse) is in catalog: true
Checking if P005 (Non-existent) is in catalog: false
```

In this example, even though `p4_duplicate_id` has different `name` and `price`, its `id` (`P001`) is the same as `p1`. Because `equals()` and `hashCode()` are overridden to consider only the `id` for equality, the `LinkedHashSet` correctly identifies `p4_duplicate_id` as a duplicate of `p1` and does not add it. Furthermore, the order of `p1`, `p2`, `p3`, and `p5` is preserved as they were added.