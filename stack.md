# The Stack Data Structure in Java

## Introduction

A **Stack** is a linear data structure that follows a particular order in which operations are performed. The order is **LIFO (Last In, First Out)**. This means the last element added to the stack is the first one to be removed.

Think of a stack of plates:
*   You add new plates on top.
*   You remove plates from the top.
*   The plate you put on last is the first one you take off.

## Java's `Stack` Class

Java provides a `Stack` class as part of its `java.util` package.

*   **Hierarchy:** `java.lang.Object` -> `java.util.Vector` -> `java.util.Stack`
*   **Legacy Class:** The `Stack` class extends `Vector`, which means it's a legacy class and is synchronized (thread-safe). While thread-safety might seem good, it introduces overhead even in single-threaded environments. For new code, it's generally recommended to use the `Deque` interface (pronounced "deck") with implementations like `ArrayDeque` or `LinkedList` if you need stack-like behavior, as `Deque` provides a more robust and efficient API for both stack and queue operations.

### Key Characteristics of `java.util.Stack`:

1.  **LIFO Principle:** Strictly adheres to Last-In, First-Out.
2.  **Inherits from `Vector`:** This means it's a dynamic array that can grow or shrink. It also inherits all methods of `Vector`, including those not typically associated with a stack (e.g., `add(index, element)`, `get(index)`), which can lead to misuse.
3.  **Synchronized:** All its methods are synchronized, making it thread-safe. This can be a performance bottleneck in single-threaded applications.
4.  **`EmptyStackException`:** Methods like `pop()` and `peek()` throw this exception if the stack is empty.

## Common `Stack` Operations (Methods)

The `Stack` class provides several specific methods for its LIFO behavior:

1.  ### `push(E item)`
    *   **Purpose:** Inserts an element onto the top of the stack.
    *   **Returns:** The `item` pushed.
    *   **Example:** `myStack.push("Apple");`

2.  ### `pop()`
    *   **Purpose:** Removes the element at the top of the stack and returns that element.
    *   **Returns:** The element at the top of the stack.
    *   **Throws:** `EmptyStackException` if the stack is empty.
    *   **Example:** `String removedItem = myStack.pop();`

3.  ### `peek()`
    *   **Purpose:** Returns the element at the top of the stack without removing it.
    *   **Returns:** The element at the top of the stack.
    *   **Throws:** `EmptyStackException` if the stack is empty.
    *   **Example:** `String topItem = myStack.peek();`

4.  ### `empty()`
    *   **Purpose:** Tests if the stack is empty.
    *   **Returns:** `true` if the stack contains no elements, `false` otherwise.
    *   **Example:** `if (myStack.empty()) { ... }`

5.  ### `search(Object o)`
    *   **Purpose:** Returns the 1-based position where an object is on this stack. The topmost item is at distance 1.
    *   **Returns:** The 1-based position from the top of the stack where the object is located; returns -1 if the object is not found.
    *   **Note:** This method is often discouraged as it violates the typical stack abstraction (where you only interact with the top).
    *   **Example:** `int position = myStack.search("Orange");`

## Constructor

*   `Stack()`: Creates an empty Stack.

## Example Usage of `java.util.Stack`

```java
import java.util.Stack;
import java.util.EmptyStackException;

public class StackExample {

    public static void main(String[] args) {

        // 1. Create a Stack
        Stack<String> fruits = new Stack<>();
        System.out.println("Initial stack: " + fruits);
        System.out.println("Is stack empty? " + fruits.empty());
        System.out.println("Stack size: " + fruits.size());

        System.out.println("\n--- Pushing Elements ---");
        // 2. Push elements onto the stack
        fruits.push("Apple");
        fruits.push("Banana");
        fruits.push("Cherry");
        System.out.println("Stack after pushes: " + fruits); // Output: [Apple, Banana, Cherry]
        System.out.println("Stack size: " + fruits.size()); // Output: 3

        System.out.println("\n--- Peeking Element ---");
        // 3. Peek at the top element without removing it
        try {
            String topFruit = fruits.peek();
            System.out.println("Top element (peek): " + topFruit); // Output: Cherry
            System.out.println("Stack after peek: " + fruits); // Output: [Apple, Banana, Cherry]
            System.out.println("Stack size after peek: " + fruits.size()); // Output: 3
        } catch (EmptyStackException e) {
            System.out.println("Cannot peek, stack is empty.");
        }

        System.out.println("\n--- Popping Elements ---");
        // 4. Pop elements from the stack
        try {
            String poppedFruit1 = fruits.pop();
            System.out.println("Popped: " + poppedFruit1); // Output: Cherry
            System.out.println("Stack after 1 pop: " + fruits); // Output: [Apple, Banana]

            String poppedFruit2 = fruits.pop();
            System.out.println("Popped: " + popped2Fruit); // Output: Banana
            System.out.println("Stack after 2 pops: " + fruits); // Output: [Apple]

            System.out.println("Is stack empty now? " + fruits.empty()); // Output: false

        } catch (EmptyStackException e) {
            System.out.println("Cannot pop, stack is empty.");
        }

        System.out.println("\n--- Searching Elements ---");
        // 5. Search for an element (1-based position from top)
        fruits.push("Grape"); // Add Grape back
        fruits.push("Kiwi");  // Add Kiwi
        System.out.println("Stack for search: " + fruits); // Output: [Apple, Grape, Kiwi]

        int posGrape = fruits.search("Grape");
        System.out.println("'Grape' found at position: " + posGrape); // Output: 2 (Kiwi is 1, Grape is 2)

        int posApple = fruits.search("Apple");
        System.out.println("'Apple' found at position: " + posApple); // Output: 3

        int posMango = fruits.search("Mango");
        System.out.println("'Mango' found at position: " + posMango); // Output: -1 (Not found)

        System.out.println("\n--- Emptying the Stack ---");
        // 6. Pop all remaining elements
        while (!fruits.empty()) {
            System.out.println("Popping: " + fruits.pop());
        }
        System.out.println("Stack after all pops: " + fruits);
        System.out.println("Is stack empty? " + fruits.empty()); // Output: true

        System.out.println("\n--- Handling EmptyStackException ---");
        // 7. Attempting to pop from an empty stack
        try {
            fruits.pop(); // This will throw EmptyStackException
        } catch (EmptyStackException e) {
            System.out.println("Caught EmptyStackException: " + e.getMessage());
        }
    }
}
```

## When to Use `Stack` (and When Not To)

*   **Avoid using `java.util.Stack` for new code:** Due to its legacy nature, synchronization overhead, and inheriting non-stack methods from `Vector`, it's generally not the best choice.
*   **Preferred Alternative:** For implementing a stack, the `Deque` interface is the recommended approach in modern Java. `Deque` stands for "Double Ended Queue" and supports element insertion and removal at both ends.

    *   `ArrayDeque`: Recommended for most cases as it's more efficient than `LinkedList` for stack operations and is not synchronized.
    *   `LinkedList`: Can also implement `Deque`, but might have slightly more overhead due to its linked-list nature.

## Implementing Stack using `Deque`

The `Deque` interface provides methods that map directly to stack operations:

*   `push(E e)`: Adds an element to the front (top of the stack).
*   `pop()`: Removes and returns the element from the front (top of the stack). Throws `NoSuchElementException` if empty.
*   `peek()`: Returns the element from the front (top of the stack) without removing it. Returns `null` if empty.
*   `addFirst(E e)` / `removeFirst()` / `peekFirst()`: Equivalent to `push`/`pop`/`peek` for stack behavior.

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.NoSuchElementException;

public class DequeAsStackExample {

    public static void main(String[] args) {

        // Use Deque as a Stack
        Deque<String> browserHistory = new ArrayDeque<>();

        System.out.println("Initial browser history (stack): " + browserHistory);
        System.out.println("Is history empty? " + browserHistory.isEmpty()); // Deque uses isEmpty() instead of empty()

        System.out.println("\n--- Navigating (Pushing) ---");
        browserHistory.push("google.com");
        browserHistory.push("youtube.com");
        browserHistory.push("github.com");
        System.out.println("Current history: " + browserHistory); // Output: [github.com, youtube.com, google.com] (ArrayDeque often prints newest first)
                                                                 // Note: The internal representation might show "github.com" as the first element in the deque's array,
                                                                 // but it's the conceptual "top" of the stack.

        System.out.println("\n--- Current Page (Peek) ---");
        try {
            String currentPage = browserHistory.peek();
            System.out.println("Currently on: " + currentPage); // Output: github.com
            System.out.println("History after peek: " + browserHistory);
        } catch (NoSuchElementException e) {
            System.out.println("No pages in history.");
        }

        System.out.println("\n--- Going Back (Popping) ---");
        try {
            String lastPage = browserHistory.pop();
            System.out.println("Went back from: " + lastPage); // Output: github.com
            System.out.println("History after 1 back: " + browserHistory); // Output: [youtube.com, google.com]

            lastPage = browserHistory.pop();
            System.out.println("Went back from: " + lastPage); // Output: youtube.com
            System.out.println("History after 2 backs: " + browserHistory); // Output: [google.com]

        } catch (NoSuchElementException e) {
            System.out.println("Cannot go back, no more pages in history.");
        }

        System.out.println("\n--- Handling Empty State ---");
        // Pop the last element
        browserHistory.pop();
        System.out.println("History after all pops: " + browserHistory);
        System.out.println("Is history empty? " + browserHistory.isEmpty()); // Output: true

        // Attempt to pop from an empty deque
        try {
            browserHistory.pop();
        } catch (NoSuchElementException e) {
            System.out.println("Caught NoSuchElementException: Cannot go back, history is empty.");
        }
    }
}
```

## Summary

*   A Stack is a LIFO (Last In, First Out) data structure.
*   Java provides `java.util.Stack`, but it's a legacy class (extends `Vector`) and is synchronized, making it less ideal for modern, high-performance code.
*   For new code, it's highly recommended to use the `Deque` interface (e.g., `ArrayDeque` or `LinkedList`) to implement stack behavior. `Deque` offers `push()`, `pop()`, and `peek()` methods that provide the standard stack operations more efficiently and without the overhead of `java.util.Stack`.
*   Both `Stack` and `Deque` implementations are valuable tools for solving problems that inherently follow the LIFO principle, such as parsing expressions, managing function call stacks, or implementing browser history.