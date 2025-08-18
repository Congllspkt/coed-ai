A **Queue** is a fundamental linear data structure that follows the **First-In, First-Out (FIFO)** principle. This means the first element added to the queue will be the first one to be removed. Think of a real-world queue, like people waiting in line at a bank or items waiting to be printed on a printer – the person who arrives first gets served first, and the document submitted first gets printed first.

In Java, the `Queue` is an **interface** located in the `java.util` package, defining the basic operations of a queue. It extends the `Collection` interface.

---

## `Queue` Interface in Java

The `Queue` interface provides methods for inserting, removing, and examining elements. These methods come in two forms:

1.  **Throwing an exception:** If the operation fails.
2.  **Returning a special value:** (e.g., `null` or `false`) if the operation fails.

It's generally recommended to use the "special value" methods (`offer`, `poll`, `peek`) in most applications, as they provide a more graceful way to handle failures without resorting to `try-catch` blocks for common scenarios like an empty queue.

Here's a breakdown of the core methods:

| Method                 | Throws Exception             | Returns Special Value         | Description                                                          |
| :--------------------- | :--------------------------- | :---------------------------- | :------------------------------------------------------------------- |
| `boolean add(E e)`     | `IllegalStateException`      | -                             | Inserts the specified element into the queue. Throws exception if full. |
| `boolean offer(E e)`   | -                            | `true` (success), `false` (failure) | Inserts the specified element into the queue. Returns `false` if full. |
| `E remove()`           | `NoSuchElementException`     | -                             | Retrieves and removes the head of this queue. Throws exception if empty. |
| `E poll()`             | -                            | `null` (if empty)             | Retrieves and removes the head of this queue. Returns `null` if empty. |
| `E element()`          | `NoSuchElementException`     | -                             | Retrieves, but does not remove, the head of this queue. Throws exception if empty. |
| `E peek()`             | -                            | `null` (if empty)             | Retrieves, but does not remove, the head of this queue. Returns `null` if empty. |
| `int size()`           | -                            | -                             | Returns the number of elements in this queue.                        |
| `boolean isEmpty()`    | -                            | -                             | Returns `true` if this queue contains no elements.                   |

---

## Common `Queue` Implementations

Since `Queue` is an interface, you cannot instantiate it directly. You need to use one of its concrete implementations. The most common ones are:

1.  **`LinkedList`**:
    *   A `LinkedList` implements the `Deque` interface, which in turn extends the `Queue` interface.
    *   It's a good general-purpose choice for implementing a queue.
    *   Offers good performance for adding and removing elements from both ends (`O(1)`).

2.  **`ArrayDeque`**:
    *   Also implements the `Deque` interface.
    *   Often preferred over `LinkedList` when a queue is needed, as it's typically faster (because it avoids the overhead of linked nodes) and more memory-efficient than `LinkedList` for most queue operations.
    *   It's a resizable array implementation.

3.  **`PriorityQueue`**:
    *   **Important Note:** A `PriorityQueue` does *not* follow the strict FIFO principle. Instead, elements are dequeued based on their *priority* (natural order or a custom `Comparator`).
    *   It's implemented using a min-heap, meaning the smallest element (highest priority) is always at the head.
    *   Useful when you need elements to be processed based on some ranking, not just their arrival order.

4.  **`ConcurrentLinkedQueue`**:
    *   A thread-safe, unbounded `Queue` implementation.
    *   Useful in multi-threaded environments where multiple threads might add or remove elements concurrently.

---

## Examples of `Queue` in Java

### 1. Basic `LinkedList` as a Queue

This example demonstrates how to use `LinkedList` to implement a FIFO queue.

```java
import java.util.LinkedList;
import java.util.Queue;

public class LinkedListQueueExample {
    public static void main(String[] args) {
        // 1. Declare and initialize a Queue using LinkedList
        // It's good practice to declare the variable as the interface type (Queue)
        // and instantiate it with the concrete class (LinkedList).
        Queue<String> queue = new LinkedList<>();

        System.out.println("Is queue empty initially? " + queue.isEmpty()); // true

        // 2. Add elements to the queue (enqueue) using offer()
        queue.offer("Alice");
        queue.offer("Bob");
        queue.offer("Charlie");
        queue.offer("David");

        System.out.println("Queue after adding elements: " + queue); // Output: [Alice, Bob, Charlie, David]
        System.out.println("Size of queue: " + queue.size());      // Output: 4

        // 3. Peek at the head of the queue (without removing)
        String headElement = queue.peek();
        System.out.println("Head of the queue (peek): " + headElement); // Output: Alice
        System.out.println("Queue after peek: " + queue);               // Output: [Alice, Bob, Charlie, David] (unchanged)

        // 4. Remove elements from the queue (dequeue) using poll()
        String removedElement1 = queue.poll();
        System.out.println("Removed element (poll): " + removedElement1); // Output: Alice
        System.out.println("Queue after first poll: " + queue);         // Output: [Bob, Charlie, David]

        String removedElement2 = queue.remove(); // Using remove() method
        System.out.println("Removed element (remove): " + removedElement2); // Output: Bob
        System.out.println("Queue after second remove: " + queue);      // Output: [Charlie, David]

        // 5. Iterate through the remaining elements (order is preserved)
        System.out.println("Iterating through queue:");
        for (String person : queue) {
            System.out.println(person);
        }

        // 6. Empty the queue
        while (!queue.isEmpty()) {
            System.out.println("Polling: " + queue.poll());
        }

        System.out.println("Queue after emptying: " + queue);         // Output: []
        System.out.println("Is queue empty now? " + queue.isEmpty()); // true

        // 7. Attempting to poll from an empty queue
        String resultFromEmptyPoll = queue.poll();
        System.out.println("Polling from empty queue: " + resultFromEmptyPoll); // Output: null

        // 8. Attempting to remove from an empty queue (will throw NoSuchElementException)
        // String resultFromEmptyRemove = queue.remove(); // Uncomment to see the exception
        // System.out.println(resultFromEmptyRemove);
    }
}
```

---

### 2. Using `ArrayDeque` as a Queue

`ArrayDeque` is often preferred for its performance benefits. The usage is identical to `LinkedList` when used as a simple queue.

```java
import java.util.ArrayDeque;
import java.util.Queue;

public class ArrayDequeQueueExample {
    public static void main(String[] args) {
        Queue<Integer> numbers = new ArrayDeque<>();

        // Add elements
        numbers.offer(10);
        numbers.offer(20);
        numbers.offer(30);
        System.out.println("Queue after adding: " + numbers); // Output: [10, 20, 30]

        // Peek
        System.out.println("Head element (peek): " + numbers.peek()); // Output: 10

        // Remove
        System.out.println("Removed element (poll): " + numbers.poll()); // Output: 10
        System.out.println("Queue after poll: " + numbers);             // Output: [20, 30]

        // Add more
        numbers.offer(40);
        System.out.println("Queue after adding more: " + numbers); // Output: [20, 30, 40]

        // Remove all
        while (!numbers.isEmpty()) {
            System.out.println("Polling: " + numbers.poll());
        }
        System.out.println("Queue after emptying: " + numbers); // Output: []
    }
}
```

---

### 3. Using `PriorityQueue`

This example shows how `PriorityQueue` behaves differently by ordering elements based on their values, not insertion order.

```java
import java.util.PriorityQueue;
import java.util.Queue;

public class PriorityQueueExample {
    public static void main(String[] args) {
        // PriorityQueue of Integers (natural ordering: ascending)
        Queue<Integer> pq = new PriorityQueue<>();

        pq.offer(30);
        pq.offer(10);
        pq.offer(50);
        pq.offer(20);
        pq.offer(40);

        System.out.println("PriorityQueue elements (insertion order doesn't dictate internal storage): " + pq);
        // Output might vary: [10, 20, 50, 30, 40] or similar, not necessarily sorted on print.
        // This reflects the heap structure, not the logical order for polling.

        System.out.println("Polling elements from PriorityQueue (smallest first):");
        while (!pq.isEmpty()) {
            System.out.println("Polling: " + pq.poll());
        }
        // Expected Output:
        // Polling: 10
        // Polling: 20
        // Polling: 30
        // Polling: 40
        // Polling: 50

        System.out.println("------------------------------------");

        // PriorityQueue with custom comparator (e.g., largest first)
        // Using a lambda expression for a custom comparator
        Queue<String> stringPQ = new PriorityQueue<>((s1, s2) -> s2.compareTo(s1)); // Descending order

        stringPQ.offer("Apple");
        stringPQ.offer("Banana");
        stringPQ.offer("Cherry");
        stringPQ.offer("Date");

        System.out.println("Polling elements from String PriorityQueue (largest first):");
        while (!stringPQ.isEmpty()) {
            System.out.println("Polling: " + stringPQ.poll());
        }
        // Expected Output:
        // Polling: Date
        // Polling: Cherry
        // Polling: Banana
        // Polling: Apple
    }
}
```

---

## When to Use a Queue?

Queues are ideal for scenarios where you need to process items in the order they were received or based on a specific priority. Common use cases include:

*   **Task Scheduling:** Managing tasks to be executed in a specific order (e.g., a print queue, background jobs).
*   **Breadth-First Search (BFS):** An algorithm for traversing or searching tree or graph data structures.
*   **Message Queues:** In distributed systems, messages are often placed in a queue for asynchronous processing.
*   **Buffers:** Acting as temporary storage for data streams, ensuring data is processed in the correct sequence.
*   **Call Centers:** People waiting for their turn to be served by an agent.
*   **Simulation:** Modeling real-world waiting lines.

---

## Conclusion

The `Queue` interface in Java provides a robust and flexible way to implement FIFO (and priority-based) data structures. By understanding its core methods and choosing the appropriate implementation (`LinkedList`, `ArrayDeque`, `PriorityQueue`, etc.), you can efficiently manage ordered collections of elements in a wide range of applications. Remember to differentiate between methods that throw exceptions and those that return special values for better error handling.