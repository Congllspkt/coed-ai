The `java.util.stream.Collectors.collectingAndThen()` method is a powerful utility in the Java Stream API that allows you to perform a final transformation on the result of another `Collector`. It essentially combines two operations: a collection phase followed by a finishing transformation.

### `Collectors.collectingAndThen()` Method

**Purpose:**
To apply a finishing transformation function to the result produced by a *downstream* collector. This is particularly useful when you want to collect elements into an intermediate type and then convert that intermediate type into a different final type, often for immutability, formatting, or further processing.

**Method Signature:**

```java
public static <T, A, R, RR> Collector<T, A, RR> collectingAndThen(
    Collector<T, A, R> downstream, // The primary collector
    Function<R, RR> finisher       // The function to apply to the result of downstream
)
```

**Parameters:**

1.  **`downstream` (Type: `Collector<T, A, R>`):**
    *   This is the primary `Collector` that will first process the elements of the stream.
    *   `T`: The type of elements in the input stream.
    *   `A`: The intermediate accumulation type of the `downstream` collector.
    *   `R`: The result type produced by the `downstream` collector.

2.  **`finisher` (Type: `Function<R, RR>`):**
    *   This is a `Function` that will be applied to the result (`R`) obtained from the `downstream` collector.
    *   `R`: The input type for this function (which is the output type of the `downstream` collector).
    *   `RR`: The final result type produced by this function, and thus, the final result type of `collectingAndThen()`.

**How it Works:**

1.  Elements from the stream are fed into the `downstream` collector.
2.  The `downstream` collector accumulates and eventually produces an intermediate result of type `R`.
3.  The `finisher` `Function` is then invoked with this `R` result as its input.
4.  The `finisher` transforms `R` into `RR`.
5.  `RR` is the final value returned by the `collect()` operation.

**Why Use It? (Common Use Cases):**

*   **Immutability:** Convert a mutable collection (e.g., `ArrayList`) produced by a `Collectors.toList()` into an unmodifiable or immutable collection (e.g., `Collections.unmodifiableList()`, Guava's `ImmutableList`).
*   **Type Conversion:** Transform the collected result into a more specific or convenient type (e.g., `Long` count to `Integer`, `Optional` to its contained value or a default).
*   **Formatting:** Take a numeric aggregate (like an average or sum) and format it into a `String`.
*   **Applying Business Logic:** Perform a final calculation or validation on the collected data.
*   **Combining Aggregates:** For instance, if you get an `Optional<T>` from `maxBy` or `minBy`, you can use `collectingAndThen` to unwrap it or provide a default value if empty.

---

### Examples

Let's illustrate `collectingAndThen()` with detailed examples.

---

### Example 1: Creating an Unmodifiable List

**Scenario:** You want to collect all elements from a stream into a `List`, but you want the resulting list to be unmodifiable to prevent accidental modification later.

```java
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

public class CollectingAndThenExample1 {

    public static void main(String[] args) {
        // Input: A list of names
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");

        System.out.println("--- Example 1: Creating an Unmodifiable List ---");
        System.out.println("Input names: " + names);

        // Using collectingAndThen to create an unmodifiable list
        List<String> immutableNames = names.stream()
            .collect(Collectors.collectingAndThen(
                Collectors.toList(),                 // Downstream: Collect into a mutable List
                Collections::unmodifiableList        // Finisher: Make the List unmodifiable
            ));

        System.out.println("Output (Unmodifiable List): " + immutableNames);

        // Attempt to modify the unmodifiable list (will throw UnsupportedOperationException)
        try {
            immutableNames.add("Eve");
            System.out.println("Attempted to add 'Eve'. (This line should not be reached)");
        } catch (UnsupportedOperationException e) {
            System.out.println("Successfully caught exception when trying to modify: " + e.getMessage());
        }
    }
}
```

**Input:**
```
[Alice, Bob, Charlie, David]
```

**Output:**
```
--- Example 1: Creating an Unmodifiable List ---
Input names: [Alice, Bob, Charlie, David]
Output (Unmodifiable List): [Alice, Bob, Charlie, David]
Successfully caught exception when trying to modify: add
```

**Explanation:**
The `Collectors.toList()` collector first gathers all names into a standard `ArrayList`. Then, `Collections::unmodifiableList` (the finisher function) takes this `ArrayList` and returns an unmodifiable view of it. Any subsequent attempt to modify `immutableNames` will result in an `UnsupportedOperationException`.

---

### Example 2: Calculating Average and Formatting as a String

**Scenario:** You have a list of prices and you want to calculate their average, then format that average into a user-friendly string (e.g., with currency symbol and two decimal places).

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class CollectingAndThenExample2 {

    public static void main(String[] args) {
        // Input: A list of product prices
        List<Double> productPrices = Arrays.asList(15.99, 20.50, 10.00, 5.75, 30.25);

        System.out.println("\n--- Example 2: Calculating Average and Formatting ---");
        System.out.println("Input product prices: " + productPrices);

        // Using collectingAndThen to get average and format it
        String formattedAveragePrice = productPrices.stream()
            .collect(Collectors.collectingAndThen(
                Collectors.averagingDouble(Double::doubleValue), // Downstream: Calculate the average (double)
                avg -> String.format("Average Price: $%.2f", avg) // Finisher: Format the double into a string
            ));

        System.out.println("Output (Formatted Average Price): " + formattedAveragePrice);
    }
}
```

**Input:**
```
[15.99, 20.50, 10.00, 5.75, 30.25]
```

**Output:**
```
--- Example 2: Calculating Average and Formatting ---
Input product prices: [15.99, 20.50, 10.00, 5.75, 30.25]
Output (Formatted Average Price): Average Price: $16.50
```

**Explanation:**
First, `Collectors.averagingDouble(Double::doubleValue)` calculates the average of the `productPrices`, which results in a `double` value (16.50). Then, the lambda expression `avg -> String.format("Average Price: $%.2f", avg)` is applied to this `double` value, formatting it into the desired string `Average Price: $16.50`.

---

### Example 3: Grouping and then Transforming Grouped Values

**Scenario:** You have a list of items and you want to group them by a certain characteristic (e.g., length of string), but for each group, you don't just want the items themselves, but some aggregated or transformed value (e.g., the *count* of items in that group, converted to an `Integer` instead of `Long`).

```java
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class CollectingAndThenExample3 {

    static class Item {
        String name;
        int weight;

        public Item(String name, int weight) {
            this.name = name;
            this.weight = weight;
        }

        public String getName() { return name; }
        public int getWeight() { return weight; }

        @Override
        public String toString() { return name + "(" + weight + "kg)"; }
    }

    public static void main(String[] args) {
        // Input: A list of Item objects
        List<Item> items = Arrays.asList(
            new Item("Apple", 100),
            new Item("Banana", 150),
            new Item("Orange", 100),
            new Item("Grape", 50),
            new Item("Melon", 500)
        );

        System.out.println("\n--- Example 3: Grouping by Weight and then Counting (Integer) ---");
        System.out.println("Input items: " + items);

        // Grouping items by weight and then counting how many items are in each weight group
        Map<Integer, Integer> weightCounts = items.stream()
            .collect(Collectors.groupingBy(
                Item::getWeight, // Classifier: Group by item weight
                Collectors.collectingAndThen( // Downstream collector for groupingBy
                    Collectors.counting(), // Downstream in collectingAndThen: Count elements (returns Long)
                    Long::intValue         // Finisher: Convert Long count to Integer
                )
            ));

        System.out.println("Output (Item counts by weight): " + weightCounts);
    }
}
```

**Input:**
```
[Apple(100kg), Banana(150kg), Orange(100kg), Grape(50kg), Melon(500kg)]
```

**Output:**
```
--- Example 3: Grouping by Weight and then Counting (Integer) ---
Input items: [Apple(100kg), Banana(150kg), Orange(100kg), Grape(50kg), Melon(500kg)]
Output (Item counts by weight): {50=1, 100=2, 150=1, 500=1}
```

**Explanation:**
In this example, `collectingAndThen` is used as the *downstream collector* for `groupingBy`.
*   `Collectors.groupingBy(Item::getWeight, ...)` groups the items by their `weight`.
*   For each group, `Collectors.counting()` is applied, which counts the number of items in that specific weight group. `Collectors.counting()` returns a `Long`.
*   The `Long::intValue` finisher then converts this `Long` count into an `Integer`.
This results in a `Map<Integer, Integer>` where keys are weights and values are the integer counts of items for that weight.

---

### Conclusion

`Collectors.collectingAndThen()` is a highly versatile method that allows for fine-grained control over the final result of a collection operation. It promotes cleaner, more expressive code by chaining transformations directly within the `collect()` call, making it ideal for tasks like ensuring immutability, formatting data, or performing final type conversions.