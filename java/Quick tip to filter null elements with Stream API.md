Here's a quick tip to filter `null` elements from a Java Stream, presented in Markdown format with details and examples.

---

# Quick Tip: Filtering Null Elements with Java Stream API

When working with collections that might contain `null` elements, you often want to process only the non-null ones. The Java Stream API provides an elegant way to achieve this using the `filter()` intermediate operation.

---

## The Quick Tip

Use `stream().filter(Objects::nonNull)` to efficiently remove all `null` elements from your stream.

## Detail

The `filter()` method takes a `Predicate` as an argument. A `Predicate` is a functional interface that represents a boolean-valued function of one argument. It returns `true` if the element should be kept, and `false` if it should be discarded.

`Objects::nonNull` is a method reference to the static `nonNull` method of the `java.util.Objects` class. This method simply returns `true` if the given object is not `null`, and `false` otherwise. This makes it a perfect `Predicate` for filtering out `null` elements.

### Why `Objects::nonNull`?

*   **Readability:** It clearly expresses the intent: "keep elements that are not null."
*   **Conciseness:** It's more compact than a lambda expression like `element -> element != null`.
*   **Safety:** It's a standard utility method, robust and reliable.

## Example

Let's say you have a list of strings, some of which are `null`:

### Input

```java
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

public class NullFilterExample {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", null, "Bob", "Charlie", null, "David", null, "Eve");

        System.out.println("Original List: " + names);
    }
}
```

**Output of Input Code:**

```
Original List: [Alice, null, Bob, Charlie, null, David, null, Eve]
```

### Filtering Code

Now, let's filter out the `null` elements:

```java
import java.util.Arrays;
import java.util.List;
import java.util.Objects; // Import Objects class
import java.util.stream.Collectors;

public class NullFilterExample {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", null, "Bob", "Charlie", null, "David", null, "Eve");

        // Filter out null elements
        List<String> nonNullNames = names.stream()
                                         .filter(Objects::nonNull) // The magic happens here!
                                         .collect(Collectors.toList());

        System.out.println("Original List: " + names);
        System.out.println("Filtered List (non-null): " + nonNullNames);
    }
}
```

### Output

```
Original List: [Alice, null, Bob, Charlie, null, David, null, Eve]
Filtered List (non-null): [Alice, Bob, Charlie, David, Eve]
```

As you can see, all `null` elements have been successfully removed, and only the valid string names remain in the `nonNullNames` list.

---

## Alternative (Lambda Expression)

While `Objects::nonNull` is preferred for its clarity and conciseness, you can also achieve the same result using a lambda expression:

```java
List<String> nonNullNamesLambda = names.stream()
                                       .filter(name -> name != null) // Equivalent lambda
                                       .collect(Collectors.toList());
```

Both approaches yield the same result, but `Objects::nonNull` is generally considered more idiomatic for this specific filtering task.

---