This document provides a detailed explanation of Stack and Queue data structures in Java, including their principles, core operations, Java implementations, and practical examples with input and output.

---

# Stack and Queue in Java

## Table of Contents

1.  [Introduction to Data Structures](#introduction-to-data-structures)
2.  [Stack](#stack)
    *   [Definition](#stack-definition)
    *   [Analogy](#stack-analogy)
    *   [Core Operations](#stack-core-operations)
    *   [Java Implementation: `java.util.Stack`](#java-implementation-javautilstack)
        *   [Example Code](#stack-example-code)
        *   [Input & Output](#stack-input--output)
    *   [Modern Approach: `Deque` as a Stack](#modern-approach-deque-as-a-stack)
    *   [Use Cases](#stack-use-cases)
3.  [Queue](#queue)
    *   [Definition](#queue-definition)
    *   [Analogy](#queue-analogy)
    *   [Core Operations](#queue-core-operations)
    *   [Java Implementation: `java.util.Queue` (with `LinkedList`)](#java-implementation-javautilqueue-with-linkedlist)
        *   [Example Code](#queue-example-code)
        *   [Input & Output](#queue-input--output)
    *   [Modern Approach: `ArrayDeque` as a Queue](#modern-approach-arraydeque-as-a-queue)
    *   [Use Cases](#queue-use-cases)
4.  [Stack vs. Queue: A Comparison](#stack-vs-queue-a-comparison)
5.  [Conclusion](#conclusion)

---

## 1. Introduction to Data Structures

Data structures are fundamental ways of organizing and storing data in a computer so that it can be accessed and modified efficiently. Stack and Queue are two of the most basic and widely used linear data structures. They both manage elements in a specific order, but differ in the principle of adding and removing elements.

## 2. Stack

### Stack Definition

A **Stack** is a linear data structure that follows the **Last-In, First-Out (LIFO)** principle. This means the last element added to the stack is the first one to be removed.

### Stack Analogy

Think of a stack of plates:
*   You add new plates on top. (Push)
*   You remove plates from the top. (Pop)
*   You can only access the top-most plate.

### Stack Core Operations

| Operation | Description                                     | `java.util.Stack` Method | `java.util.Deque` Method (for Stack behavior) |
| :-------- | :---------------------------------------------- | :----------------------- | :-------------------------------------------- |
| **Push**  | Adds an element to the top of the stack.        | `push(E item)`           | `push(E e)` or `addFirst(E e)`                |
| **Pop**   | Removes and returns the top element.            | `pop()`                  | `pop()` or `removeFirst()`                    |
| **Peek**  | Returns the top element without removing it.    | `peek()`                 | `peek()` or `peekFirst()`                     |
| **isEmpty** | Checks if the stack is empty.                   | `isEmpty()`              | `isEmpty()`                                   |
| **Search** | Returns the 1-based position of an element from the top. Returns -1 if not found. | `search(Object o)`       | (No direct equivalent, but can iterate)       |
| **Size**  | Returns the number of elements in the stack.    | `size()`                 | `size()`                                      |

### Java Implementation: `java.util.Stack`

In Java, the `java.util.Stack` class is a legacy class that extends `Vector` (which is a synchronized and dynamic array). While it works, it's generally **discouraged for new code** due to its legacy nature and the performance overhead of `Vector`'s synchronization. For modern Java, the `Deque` interface (implemented by `ArrayDeque` or `LinkedList`) is preferred for stack functionality.

#### Stack Example Code

```java
import java.util.Stack;
import java.util.EmptyStackException; // To catch specific exceptions

public class StackExample {
    public static void main(String[] args) {
        // 1. Create a Stack
        Stack<String> cardStack = new Stack<>();
        System.out.println("Initial Stack: " + cardStack); // Output: []
        System.out.println("Is stack empty? " + cardStack.isEmpty()); // Output: true

        // 2. Push elements onto the stack
        System.out.println("\n--- PUSH OPERATIONS ---");
        cardStack.push("Ace of Spades");
        cardStack.push("King of Hearts");
        cardStack.push("Queen of Diamonds");
        System.out.println("Stack after pushes: " + cardStack);
        System.out.println("Top element (peek): " + cardStack.peek()); // Queen of Diamonds
        System.out.println("Is stack empty? " + cardStack.isEmpty()); // Output: false
        System.out.println("Stack size: " + cardStack.size());

        // 3. Pop elements from the stack
        System.out.println("\n--- POP OPERATIONS ---");
        String poppedCard1 = cardStack.pop(); // Queen of Diamonds
        System.out.println("Popped: " + poppedCard1);
        System.out.println("Stack after first pop: " + cardStack);
        System.out.println("Top element (peek): " + cardStack.peek()); // King of Hearts

        String poppedCard2 = cardStack.pop(); // King of Hearts
        System.out.println("Popped: " + poppedCard2);
        System.out.println("Stack after second pop: " + cardStack);

        // 4. Search for an element
        System.out.println("\n--- SEARCH OPERATION ---");
        // search returns 1-based position from the top, or -1 if not found
        System.out.println("'Ace of Spades' position: " + cardStack.search("Ace of Spades")); // 1
        System.out.println("'Joker' position: " + cardStack.search("Joker")); // -1

        // 5. Pop all remaining elements
        System.out.println("\n--- FINAL POPS ---");
        cardStack.pop(); // Ace of Spades
        System.out.println("Stack after last pop: " + cardStack);
        System.out.println("Is stack empty? " + cardStack.isEmpty()); // Output: true

        // 6. Attempt to pop from an empty stack (will throw EmptyStackException)
        try {
            cardStack.pop();
        } catch (EmptyStackException e) {
            System.out.println("Error: Tried to pop from an empty stack! " + e.getMessage());
        }

        // 7. Attempt to peek from an empty stack (will throw EmptyStackException)
        try {
            cardStack.peek();
        } catch (EmptyStackException e) {
            System.out.println("Error: Tried to peek from an empty stack! " + e.getMessage());
        }
    }
}
```

#### Stack Input & Output

**Input:** (Implicitly defined by the code, no user input required)

**Output:**
```
Initial Stack: []
Is stack empty? true

--- PUSH OPERATIONS ---
Stack after pushes: [Ace of Spades, King of Hearts, Queen of Diamonds]
Top element (peek): Queen of Diamonds
Is stack empty? false
Stack size: 3

--- POP OPERATIONS ---
Popped: Queen of Diamonds
Stack after first pop: [Ace of Spades, King of Hearts]
Top element (peek): King of Hearts
Popped: King of Hearts
Stack after second pop: [Ace of Spades]

--- SEARCH OPERATION ---
'Ace of Spades' position: 1
'Joker' position: -1

--- FINAL POPS ---
Stack after last pop: []
Is stack empty? true
Error: Tried to pop from an empty stack! 
Error: Tried to peek from an empty stack! 
```

### Modern Approach: `Deque` as a Stack

For better performance and a more consistent API, it's recommended to use the `Deque` interface (Double-Ended Queue) and its implementations like `ArrayDeque` or `LinkedList` to act as a Stack. `ArrayDeque` is generally preferred as it's more efficient than `LinkedList` for most queue/stack operations and doesn't incur the overhead of a linked list's nodes.

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class DequeAsStackExample {
    public static void main(String[] args) {
        Deque<String> stack = new ArrayDeque<>(); // or new LinkedList<>();

        stack.push("Item 1"); // Adds to the "top"
        stack.push("Item 2");
        stack.push("Item 3");

        System.out.println("Deque acting as Stack: " + stack); // [Item 3, Item 2, Item 1] (implementation detail, conceptual top is left)
        System.out.println("Top element: " + stack.peek()); // Item 3

        String popped = stack.pop(); // Removes Item 3
        System.out.println("Popped: " + popped);
        System.out.println("Deque after pop: " + stack); // [Item 2, Item 1]
    }
}
```

### Stack Use Cases

*   **Function Call Stack:** When a method is called, its state (local variables, return address) is pushed onto a stack. When it returns, its state is popped.
*   **Undo/Redo Functionality:** Each action can be pushed onto an "undo" stack. When undoing, actions are popped. Redo functionality uses a similar concept.
*   **Expression Evaluation:** Converting infix to postfix expressions, and evaluating postfix expressions.
*   **Backtracking Algorithms:** Used in algorithms like Depth-First Search (DFS) or finding paths in a maze to remember the path taken and backtrack when a dead end is reached.
*   **Browser History:** Stores URLs visited, allowing "back" button functionality.

## 3. Queue

### Queue Definition

A **Queue** is a linear data structure that follows the **First-In, First-Out (FIFO)** principle. This means the first element added to the queue is the first one to be removed.

### Queue Analogy

Think of a waiting line (a "queue" in British English) at a bank or a supermarket:
*   People join the line at the back. (Enqueue / Offer / Add)
*   People leave the line from the front. (Dequeue / Poll / Remove)
*   The person at the front is the next to be served.

### Queue Core Operations

The `java.util.Queue` interface defines several methods for adding, removing, and examining elements. It offers two forms for each operation: one that throws an exception on failure and one that returns a special value (e.g., `null` or `false`). It's generally recommended to use the "special value" operations (`offer`, `poll`, `peek`) as they are more robust in scenarios where the queue might be bounded or empty.

| Operation   | Description                                     | `Queue` Method (Throws Exception) | `Queue` Method (Returns Special Value) |
| :---------- | :---------------------------------------------- | :-------------------------------- | :--------------------------------------- |
| **Enqueue** | Adds an element to the rear (tail) of the queue. | `add(E e)`                        | `offer(E e)`                             |
| **Dequeue** | Removes and returns the element from the front (head) of the queue. | `remove()`                        | `poll()`                                 |
| **Peek**    | Returns the element at the front without removing it. | `element()`                       | `peek()`                                 |
| **isEmpty** | Checks if the queue is empty.                   | N/A                               | `isEmpty()`                              |
| **Size**    | Returns the number of elements in the queue.    | N/A                               | `size()`                                 |

### Java Implementation: `java.util.Queue` (with `LinkedList`)

The `java.util.Queue` is an interface in Java, not a concrete class. Common implementations include:
*   `java.util.LinkedList`: Implements both `List` and `Deque` interfaces, making it suitable for both Queue and Stack behavior.
*   `java.util.ArrayDeque`: More efficient than `LinkedList` for most Queue operations, especially when used as a pure FIFO queue.
*   `java.util.PriorityQueue`: A specialized queue where elements are ordered according to their natural ordering or a custom `Comparator`. It's not a strict FIFO queue.

For a general-purpose FIFO queue, `LinkedList` or `ArrayDeque` are typically used. We'll use `LinkedList` for this example.

#### Queue Example Code

```java
import java.util.LinkedList;
import java.util.Queue;
import java.util.NoSuchElementException; // To catch specific exceptions

public class QueueExample {
    public static void main(String[] args) {
        // 1. Create a Queue using LinkedList
        // Declare as Queue interface type, instantiate with LinkedList
        Queue<String> customerQueue = new LinkedList<>();
        System.out.println("Initial Queue: " + customerQueue); // Output: []
        System.out.println("Is queue empty? " + customerQueue.isEmpty()); // Output: true

        // 2. Enqueue elements (add/offer)
        System.out.println("\n--- ENQUEUE OPERATIONS ---");
        customerQueue.offer("Alice"); // Recommended for non-blocking add
        customerQueue.offer("Bob");
        customerQueue.add("Charlie"); // Also works, but throws exception on capacity violation
        System.out.println("Queue after enqueues: " + customerQueue);
        System.out.println("Front element (peek): " + customerQueue.peek()); // Alice
        System.out.println("Is queue empty? " + customerQueue.isEmpty()); // Output: false
        System.out.println("Queue size: " + customerQueue.size());

        // 3. Dequeue elements (poll/remove)
        System.out.println("\n--- DEQUEUE OPERATIONS ---");
        String servedCustomer1 = customerQueue.poll(); // Recommended for non-blocking remove
        System.out.println("Served: " + servedCustomer1); // Alice
        System.out.println("Queue after first dequeue: " + customerQueue);
        System.out.println("Front element (peek): " + customerQueue.peek()); // Bob

        String servedCustomer2 = customerQueue.remove(); // Also works, but throws exception if empty
        System.out.println("Served: " + servedCustomer2); // Bob
        System.out.println("Queue after second dequeue: " + customerQueue);

        // 4. Check status
        System.out.println("\n--- STATUS CHECKS ---");
        System.out.println("Current front element (element()): " + customerQueue.element()); // Charlie
        System.out.println("Current queue size: " + customerQueue.size());

        // 5. Dequeue all remaining elements
        System.out.println("\n--- FINAL DEQUEUES ---");
        while (!customerQueue.isEmpty()) {
            System.out.println("Served: " + customerQueue.poll());
        }
        System.out.println("Queue after all dequeues: " + customerQueue);
        System.out.println("Is queue empty? " + customerQueue.isEmpty()); // Output: true

        // 6. Attempt to poll/peek from an empty queue (will return null)
        System.out.println("\n--- EMPTY QUEUE OPERATIONS ---");
        System.out.println("Attempting to poll from empty queue: " + customerQueue.poll()); // null
        System.out.println("Attempting to peek from empty queue: " + customerQueue.peek()); // null

        // 7. Attempt to remove/element from an empty queue (will throw NoSuchElementException)
        try {
            customerQueue.remove();
        } catch (NoSuchElementException e) {
            System.out.println("Error: Tried to remove from an empty queue! " + e.getMessage());
        }

        try {
            customerQueue.element();
        } catch (NoSuchElementException e) {
            System.out.println("Error: Tried to element from an empty queue! " + e.getMessage());
        }
    }
}
```

#### Queue Input & Output

**Input:** (Implicitly defined by the code, no user input required)

**Output:**
```
Initial Queue: []
Is queue empty? true

--- ENQUEUE OPERATIONS ---
Queue after enqueues: [Alice, Bob, Charlie]
Front element (peek): Alice
Is queue empty? false
Queue size: 3

--- DEQUEUE OPERATIONS ---
Served: Alice
Queue after first dequeue: [Bob, Charlie]
Front element (peek): Bob
Served: Bob
Queue after second dequeue: [Charlie]

--- STATUS CHECKS ---
Current front element (element()): Charlie
Current queue size: 1

--- FINAL DEQUEUES ---
Served: Charlie
Queue after all dequeues: []
Is queue empty? true

--- EMPTY QUEUE OPERATIONS ---
Attempting to poll from empty queue: null
Attempting to peek from empty queue: null
Error: Tried to remove from an empty queue! No such element
Error: Tried to element from an empty queue! No such element
```

### Modern Approach: `ArrayDeque` as a Queue

`ArrayDeque` is often the preferred choice for implementing a queue (or stack) in Java because it's generally more efficient than `LinkedList` for add/remove operations at both ends, especially for large collections, as it avoids the overhead of creating and linking node objects.

```java
import java.util.ArrayDeque;
import java.util.Queue;

public class ArrayDequeAsQueueExample {
    public static void main(String[] args) {
        Queue<String> messageQueue = new ArrayDeque<>();

        messageQueue.offer("Message 1");
        messageQueue.offer("Message 2");
        messageQueue.offer("Message 3");

        System.out.println("ArrayDeque acting as Queue: " + messageQueue); // [Message 1, Message 2, Message 3]
        System.out.println("Next message: " + messageQueue.peek()); // Message 1

        String processed = messageQueue.poll();
        System.out.println("Processed: " + processed); // Message 1
        System.out.println("Queue after processing: " + messageQueue); // [Message 2, Message 3]
    }
}
```

### Queue Use Cases

*   **Task Scheduling:** Managing tasks in a multi-threaded environment where tasks are processed in the order they arrive.
*   **Message Queues:** In distributed systems, messages are often queued for asynchronous processing.
*   **Breadth-First Search (BFS):** Graph traversal algorithm where nodes are visited level by level.
*   **Printer Queues:** Documents are printed in the order they are sent to the printer.
*   **Buffer for Streaming Data:** Data arriving from a stream is buffered in a queue before processing.

## 4. Stack vs. Queue: A Comparison

| Feature             | Stack                               | Queue                               |
| :------------------ | :---------------------------------- | :---------------------------------- |
| **Principle**       | Last-In, First-Out (LIFO)           | First-In, First-Out (FIFO)          |
| **Primary Operations** | Push (add to top), Pop (remove from top) | Enqueue (add to rear), Dequeue (remove from front) |
| **Analogy**         | Stack of plates, Call stack         | Waiting line, Printer queue         |
| **Insertion Point** | Top (or Front)                      | Rear (or Tail)                      |
| **Deletion Point**  | Top (or Front)                      | Front (or Head)                     |
| **`java.util` Class** | `java.util.Stack` (Legacy)          | `java.util.Queue` (Interface)       |
| **Recommended Java Impl.** | `java.util.Deque` (e.g., `ArrayDeque` or `LinkedList`) | `java.util.Queue` (e.g., `ArrayDeque` or `LinkedList`) |
| **Common Use Cases** | Undo/Redo, Function calls, DFS, Expression parsing | Task scheduling, BFS, Message passing, Printer spooling |

## 5. Conclusion

Stack and Queue are fundamental data structures with distinct ordering principles (LIFO for Stack, FIFO for Queue). While Java provides a `Stack` class, it's generally recommended to use the more modern and efficient `Deque` interface (`ArrayDeque` or `LinkedList`) for both stack and queue implementations in new code. Understanding their behavior and appropriate use cases is crucial for designing efficient and robust algorithms and systems.