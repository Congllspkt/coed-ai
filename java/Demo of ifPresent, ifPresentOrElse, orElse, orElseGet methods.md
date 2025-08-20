This document provides a detailed explanation and examples of the `ifPresent`, `ifPresentOrElse`, `orElse`, and `orElseGet` methods available in Java's `java.util.Optional` class.

---

# Java `Optional` Methods: `ifPresent`, `ifPresentOrElse`, `orElse`, `orElseGet`

## Table of Contents
1.  [Introduction to `java.util.Optional`](#1-introduction-to-javautiloptional)
2.  [`ifPresent(Consumer<? super T> action)`](#2-ifpresentconsumer-super-t-action)
3.  [`ifPresentOrElse(Consumer<? super T> action, Runnable emptyAction)`](#3-ifpresentorelseconsumer-super-t-action-runnable-emptyaction)
4.  [`orElse(T other)`](#4-orelset-other)
5.  [`orElseGet(Supplier<? extends T> supplier)`](#5-orelsegetsupplier-extends-t-supplier)
6.  [Summary and Best Practices](#6-summary-and-best-practices)

---

## 1. Introduction to `java.util.Optional`

`java.util.Optional` is a container object introduced in Java 8 that may or may not contain a non-null value. It is primarily used to:
*   **Avoid `NullPointerException` (NPEs):** By forcing developers to explicitly deal with the absence of a value.
*   **Improve Code Readability:** Making it clear when a value might be absent, rather than relying on `null` checks.
*   **Promote Functional Programming Style:** By providing methods that allow operations to be chained.

**Creating `Optional` instances:**
*   `Optional.of(value)`: Creates an `Optional` with the given non-null value. Throws `NullPointerException` if `value` is `null`.
*   `Optional.ofNullable(value)`: Creates an `Optional` with the given value if it's non-null, or an empty `Optional` if `value` is `null`.
*   `Optional.empty()`: Creates an empty `Optional` instance.

Let's dive into the specific methods.

---

## 2. `ifPresent(Consumer<? super T> action)`

### Purpose
This method performs the given action if a value is present in the `Optional`. If the `Optional` is empty, nothing happens. It's often used for side effects, like printing a message or updating a state, only when a value exists.

### Method Signature
```java
public void ifPresent(Consumer<? super T> action)
```
*   `Consumer`: A functional interface that represents an operation that accepts a single input argument and returns no result.

### When to use
Use `ifPresent` when you want to execute a block of code *only* if the `Optional` contains a value, and you don't need an alternative action if the value is absent.

### Example

```java
import java.util.Optional;
import java.util.function.Consumer;

public class IfPresentDemo {

    public static void main(String[] args) {
        // --- Scenario 1: Optional contains a value ---
        Optional<String> userNamePresent = Optional.of("Alice");
        System.out.println("--- Scenario 1: Value is present ---");
        System.out.print("Input: Optional.of(\"Alice\") -> ");
        userNamePresent.ifPresent(name -> System.out.println("Hello, " + name + "!"));
        // This is equivalent to:
        // if (userNamePresent.isPresent()) {
        //     System.out.println("Hello, " + userNamePresent.get() + "!");
        // }

        System.out.println(); // Newline for clarity

        // --- Scenario 2: Optional is empty ---
        Optional<String> userNameEmpty = Optional.empty();
        System.out.println("--- Scenario 2: Value is empty ---");
        System.out.print("Input: Optional.empty() -> ");
        userNameEmpty.ifPresent(name -> System.out.println("Hello, " + name + "!"));
        // Nothing will be printed here because the Optional is empty.
        System.out.println("(No output from ifPresent block when Optional is empty)");

        System.out.println(); // Newline for clarity

        // --- Scenario 3: Using a separate Consumer ---
        Consumer<String> greetingConsumer = name -> System.out.println("Greetings, " + name + "!");
        Optional<String> userWithConsumer = Optional.of("Bob");
        System.out.println("--- Scenario 3: Using a Consumer object ---");
        System.out.print("Input: Optional.of(\"Bob\") -> ");
        userWithConsumer.ifPresent(greetingConsumer);

        Optional<String> emptyWithConsumer = Optional.empty();
        System.out.print("Input: Optional.empty() -> ");
        emptyWithConsumer.ifPresent(greetingConsumer);
        System.out.println("(No output from ifPresent block)");
    }
}
```

### Run this code:
Compile and run `IfPresentDemo.java`.

### Expected Output:
```
--- Scenario 1: Value is present ---
Input: Optional.of("Alice") -> Hello, Alice!

--- Scenario 2: Value is empty ---
Input: Optional.empty() -> (No output from ifPresent block when Optional is empty)

--- Scenario 3: Using a Consumer object ---
Input: Optional.of("Bob") -> Greetings, Bob!
Input: Optional.empty() -> (No output from ifPresent block)
```

---

## 3. `ifPresentOrElse(Consumer<? super T> action, Runnable emptyAction)`

### Purpose
This method performs the given `action` if a value is present; otherwise, it performs the given `emptyAction`. It's a convenient way to handle both the "value present" and "value absent" cases in a single line, without explicit `if/else` checks.

### Method Signature
```java
public void ifPresentOrElse(Consumer<? super T> action, Runnable emptyAction)
```
*   `Consumer`: (Same as above) For when a value is present.
*   `Runnable`: A functional interface that represents an operation that takes no arguments and returns no result. This is for the "empty" case.

### When to use
Use `ifPresentOrElse` when you need to perform one specific action if a value is present, and a *different* specific action if it's absent. This makes your code more concise and readable than a traditional `if (optional.isPresent()) { ... } else { ... }` block.

### Example

```java
import java.util.Optional;

public class IfPresentOrElseDemo {

    public static void main(String[] args) {
        // --- Scenario 1: Optional contains a value ---
        Optional<String> emailPresent = Optional.of("user@example.com");
        System.out.println("--- Scenario 1: Value is present ---");
        System.out.print("Input: Optional.of(\"user@example.com\") -> ");
        emailPresent.ifPresentOrElse(
            email -> System.out.println("Email address found: " + email),
            () -> System.out.println("No email address provided.")
        );

        System.out.println(); // Newline for clarity

        // --- Scenario 2: Optional is empty ---
        Optional<String> emailEmpty = Optional.empty();
        System.out.println("--- Scenario 2: Value is empty ---");
        System.out.print("Input: Optional.empty() -> ");
        emailEmpty.ifPresentOrElse(
            email -> System.out.println("Email address found: " + email),
            () -> System.out.println("No email address provided.")
        );

        System.out.println(); // Newline for clarity

        // --- Scenario 3: Optional with potentially null value ---
        String databaseValue = null; // Imagine this comes from a DB query
        Optional<String> userDescription = Optional.ofNullable(databaseValue);
        System.out.println("--- Scenario 3: Value from potentially null source ---");
        System.out.print("Input: Optional.ofNullable(null) -> ");
        userDescription.ifPresentOrElse(
            desc -> System.out.println("User description: " + desc),
            () -> System.out.println("User description not available.")
        );
    }
}
```

### Run this code:
Compile and run `IfPresentOrElseDemo.java`.

### Expected Output:
```
--- Scenario 1: Value is present ---
Input: Optional.of("user@example.com") -> Email address found: user@example.com

--- Scenario 2: Value is empty ---
Input: Optional.empty() -> No email address provided.

--- Scenario 3: Value from potentially null source ---
Input: Optional.ofNullable(null) -> User description not available.
```

---

## 4. `orElse(T other)`

### Purpose
This method returns the value if it is present; otherwise, it returns a specified default value (`other`).

### Method Signature
```java
public T orElse(T other)
```
*   `other`: The default value to be returned if the `Optional` is empty.

### When to use
Use `orElse` when you always need a value, and the default value is a **pre-computed literal** or a **cheaply available value** that doesn't involve heavy computation or side effects.

**Important Pitfall:** The `other` argument to `orElse` is **always evaluated**, regardless of whether the `Optional` contains a value or not. This can lead to performance issues if the default value creation is expensive.

### Example

```java
import java.util.Optional;

public class OrElseDemo {

    public static String getDefaultValue() {
        System.out.println(" (getDefaultValue() method called)"); // This will always print
        return "Default Item";
    }

    public static void main(String[] args) {
        // --- Scenario 1: Optional contains a value ---
        Optional<String> configValue = Optional.of("Enabled");
        System.out.println("--- Scenario 1: Value is present ---");
        System.out.print("Input: Optional.of(\"Enabled\") -> Result: ");
        String result1 = configValue.orElse(getDefaultValue());
        System.out.println(result1);
        // Notice: getDefaultValue() is still called, even though "Enabled" is returned.

        System.out.println(); // Newline for clarity

        // --- Scenario 2: Optional is empty ---
        Optional<String> configValueEmpty = Optional.empty();
        System.out.println("--- Scenario 2: Value is empty ---");
        System.out.print("Input: Optional.empty() -> Result: ");
        String result2 = configValueEmpty.orElse(getDefaultValue());
        System.out.println(result2);
        // Here, getDefaultValue() is called, and its result ("Default Item") is returned.

        System.out.println(); // Newline for clarity

        // --- Scenario 3: Simple literal default ---
        Optional<Integer> userPoints = Optional.ofNullable(null);
        System.out.println("--- Scenario 3: Simple literal default ---");
        System.out.print("Input: Optional.ofNullable(null) -> Result: ");
        int points = userPoints.orElse(0); // 0 is a simple literal, no performance issue here
        System.out.println("User points: " + points);
    }
}
```

### Run this code:
Compile and run `OrElseDemo.java`.

### Expected Output:
```
--- Scenario 1: Value is present ---
Input: Optional.of("Enabled") -> Result:  (getDefaultValue() method called)
Enabled

--- Scenario 2: Value is empty ---
Input: Optional.empty() -> Result:  (getDefaultValue() method called)
Default Item

--- Scenario 3: Simple literal default ---
Input: Optional.ofNullable(null) -> Result: User points: 0
```
**Observation for `orElse`:** In Scenario 1, even though `configValue` contains "Enabled", the `getDefaultValue()` method (which prints a message) is still executed. This highlights the eager evaluation of the `other` argument.

---

## 5. `orElseGet(Supplier<? extends T> supplier)`

### Purpose
This method returns the value if it is present; otherwise, it invokes the supplied `Supplier` to provide a default value and returns the result of that invocation.

### Method Signature
```java
public T orElseGet(Supplier<? extends T> supplier)
```
*   `Supplier`: A functional interface that represents a supplier of results. Its `get()` method is called to produce the default value.

### When to use
Use `orElseGet` when you always need a value, and the default value needs to be **computed lazily** (only if the `Optional` is empty) or involves an **expensive operation**. This avoids the performance pitfall of `orElse`.

### Example

```java
import java.util.Optional;
import java.util.function.Supplier;

public class OrElseGetDemo {

    public static String getExpensiveDefaultValue() {
        System.out.println(" (getExpensiveDefaultValue() method called - this is lazy)");
        // Simulate an expensive operation
        try {
            Thread.sleep(100); // Simulate network call or complex calculation
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return "Lazily Generated Default Item";
    }

    public static void main(String[] args) {
        // --- Scenario 1: Optional contains a value ---
        Optional<String> itemFromCache = Optional.of("Cached Item");
        System.out.println("--- Scenario 1: Value is present ---");
        System.out.print("Input: Optional.of(\"Cached Item\") -> Result: ");
        String result1 = itemFromCache.orElseGet(() -> getExpensiveDefaultValue());
        System.out.println(result1);
        // Notice: getExpensiveDefaultValue() is NOT called.

        System.out.println(); // Newline for clarity

        // --- Scenario 2: Optional is empty ---
        Optional<String> itemFromDB = Optional.empty();
        System.out.println("--- Scenario 2: Value is empty ---");
        System.out.print("Input: Optional.empty() -> Result: ");
        String result2 = itemFromDB.orElseGet(() -> getExpensiveDefaultValue());
        System.out.println(result2);
        // Here, getExpensiveDefaultValue() IS called, and its result is returned.

        System.out.println(); // Newline for clarity

        // --- Scenario 3: Using a separate Supplier object ---
        Supplier<String> defaultSupplier = () -> "Fallback Value from Supplier";
        Optional<String> setting = Optional.of("Enabled");
        System.out.println("--- Scenario 3: Using a Supplier object (value present) ---");
        System.out.print("Input: Optional.of(\"Enabled\") -> Result: ");
        String settingResult = setting.orElseGet(defaultSupplier);
        System.out.println(settingResult);

        Optional<String> emptySetting = Optional.empty();
        System.out.println("--- Scenario 4: Using a Supplier object (value empty) ---");
        System.out.print("Input: Optional.empty() -> Result: ");
        String emptySettingResult = emptySetting.orElseGet(defaultSupplier);
        System.out.println(emptySettingResult);
    }
}
```

### Run this code:
Compile and run `OrElseGetDemo.java`.

### Expected Output:
```
--- Scenario 1: Value is present ---
Input: Optional.of("Cached Item") -> Result: Cached Item

--- Scenario 2: Value is empty ---
Input: Optional.empty() -> Result:  (getExpensiveDefaultValue() method called - this is lazy)
Lazily Generated Default Item

--- Scenario 3: Using a Supplier object (value present) ---
Input: Optional.of("Enabled") -> Result: Enabled

--- Scenario 4: Using a Supplier object (value empty) ---
Input: Optional.empty() -> Result: Fallback Value from Supplier
```
**Observation for `orElseGet`:** In Scenario 1, when `itemFromCache` has a value, `getExpensiveDefaultValue()` is *not* called. This demonstrates the lazy evaluation, which is crucial for performance with expensive default value computations.

---

## 6. Summary and Best Practices

| Method            | Purpose                                                    | When to Use                                                                 | Key Characteristic           |
| :---------------- | :--------------------------------------------------------- | :-------------------------------------------------------------------------- | :--------------------------- |
| `ifPresent`       | Perform action if value is present; otherwise, do nothing. | For side effects when a value exists, no alternative action needed.         | Eager evaluation of action (if value present). |
| `ifPresentOrElse` | Perform one action if value present, another if absent.    | When distinct actions are required for both cases.                          | Clean alternative to `if/else`. |
| `orElse`          | Get value if present; otherwise, a **default value**.      | When default is a **pre-computed, cheap literal or object**.                | **Eagerly evaluates** the default value (even if value is present). |
| `orElseGet`       | Get value if present; otherwise, a **supplied default**.   | When default needs to be **computed lazily** or is **expensive to create**. | **Lazily evaluates** the default value (only if value is absent). |

**General Best Practices with `Optional`:**

*   **Avoid `isPresent()` followed by `get()`:** This is often an anti-pattern that defeats the purpose of `Optional` by reintroducing the need for explicit checks. Prefer `ifPresent`, `ifPresentOrElse`, `map`, `filter`, `orElse`, `orElseGet`, etc.
*   **Don't use `Optional` as a field or method parameter:** `Optional` is primarily designed as a return type for methods where the absence of a value is a legitimate and expected scenario. Using it as a field can make serialization difficult, and as a parameter can lead to confusing method signatures.
*   **Chain operations with `map`, `filter`, `flatMap`:** These methods allow you to transform or filter the contained value only if it's present, making fluent API calls possible.
*   **Prefer `orElseGet` over `orElse` for expensive defaults:** To avoid unnecessary computations.
*   **Return `Optional.empty()` instead of `null`:** When a method logically might not return a value.

By understanding and correctly applying these `Optional` methods, you can write more robust, readable, and efficient Java code that handles the absence of values gracefully.