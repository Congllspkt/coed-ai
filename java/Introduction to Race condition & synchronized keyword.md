# Introduction to Race Conditions & `synchronized` Keyword in Java

In the world of concurrent programming, where multiple parts of a program execute simultaneously, managing shared resources becomes crucial. Failure to do so can lead to subtle and hard-to-debug issues. This document will explore two fundamental concepts in Java concurrency: Race Conditions and the `synchronized` keyword.

---

## 1. Introduction to Concurrency and Shared Resources

Modern applications often leverage multiple threads to improve performance, responsiveness, and resource utilization. Threads share the same memory space, which means they can access the same variables and objects. While this sharing allows for efficient data exchange, it also introduces potential problems when multiple threads try to read and modify the same data concurrently.

---

## 2. What is a Race Condition?

A **Race Condition** occurs when multiple threads try to access and modify shared data simultaneously, and the final outcome depends on the unpredictable order in which these threads execute. If the order of execution can change the result, you have a race condition.

### Analogy: The Bank Account

Imagine a bank account with a balance.

*   **Initial Balance:** $1000
*   **Thread A (Deposit):** Wants to deposit $200.
    1.  Reads balance: $1000
    2.  Calculates new balance: $1000 + $200 = $1200
    3.  Writes new balance: $1200
*   **Thread B (Withdrawal):** Wants to withdraw $500.
    1.  Reads balance: $1000 (at the same time Thread A reads it)
    2.  Calculates new balance: $1000 - $500 = $500
    3.  Writes new balance: $500

**Possible Execution Order (Race Condition):**

1.  Thread A reads balance ($1000).
2.  Thread B reads balance ($1000).
3.  Thread A calculates new balance ($1200).
4.  **Context Switch** (Thread A pauses, Thread B resumes).
5.  Thread B calculates new balance ($500).
6.  Thread B writes new balance ($500).
7.  **Context Switch** (Thread B pauses, Thread A resumes).
8.  Thread A writes new balance ($1200).

**Final Balance:** $1200 (Incorrect! It should have been $1000 + $200 - $500 = $700)

The problem arises because the operations (read, modify, write) are not **atomic** (indivisible). If one thread is interrupted after reading but before writing, another thread can step in and mess up the state.

### Example: Counter Increment (Without Synchronization)

Let's create a simple `Counter` class that increments a value, and then run multiple threads to increment it concurrently.

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

// 1. The Shared Resource
class Counter {
    private int count = 0;

    public void increment() {
        // This operation (read-modify-write) is NOT atomic
        // 1. Read 'count'
        // 2. Increment 'count' in memory
        // 3. Write 'count' back to memory
        count++;
    }

    public int getCount() {
        return count;
    }
}

// 2. The Main Program Demonstrating Race Condition
public class RaceConditionDemo {

    public static void main(String[] args) throws InterruptedException {
        Counter counter = new Counter();
        int numberOfThreads = 100;
        int incrementsPerThread = 100;
        int totalExpectedCount = numberOfThreads * incrementsPerThread;

        // Using ExecutorService for managing threads
        ExecutorService executor = Executors.newFixedThreadPool(numberOfThreads);

        long startTime = System.currentTimeMillis();

        for (int i = 0; i < numberOfThreads; i++) {
            executor.submit(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    counter.increment();
                }
            });
        }

        // Shut down the executor and wait for all tasks to complete
        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.MINUTES); // Wait for tasks to finish

        long endTime = System.currentTimeMillis();

        System.out.println("--- Race Condition Example (Without Synchronization) ---");
        System.out.println("Total expected count: " + totalExpectedCount);
        System.out.println("Final count:          " + counter.getCount());
        System.out.println("Time taken:           " + (endTime - startTime) + " ms");

        if (counter.getCount() != totalExpectedCount) {
            System.out.println("\n!!! RACE CONDITION DETECTED: Final count is NOT as expected !!!");
            System.out.println("This is because multiple threads interfered with each other during increment operations.");
        } else {
            System.out.println("\n(Rarely, the count might be correct due to chance, but rerun to see the issue.)");
        }
    }
}
```

### Input:
To run this example, save the code as `RaceConditionDemo.java` and `Counter.java` in the same directory, compile, and execute:
```bash
javac RaceConditionDemo.java
java RaceConditionDemo
```

### Example Output (will vary slightly on each run, but typically less than 10000):

```
--- Race Condition Example (Without Synchronization) ---
Total expected count: 10000
Final count:          9876
Time taken:           15 ms

!!! RACE CONDITION DETECTED: Final count is NOT as expected !!!
This is because multiple threads interfered with each other during increment operations.
```

### Explanation of the Problem:

The `count++` operation, while seemingly simple, is actually a three-step process:
1.  Read the current value of `count`.
2.  Increment that value.
3.  Write the new value back to `count`.

If Thread A reads `count` as `50`, and then before it can write back `51`, Thread B also reads `count` as `50`, both threads will then calculate `51`. When they both write `51` back, one increment is lost. This happens repeatedly, leading to a final count less than the expected `10000`.

---

## 3. The `synchronized` Keyword

The `synchronized` keyword in Java is a fundamental mechanism for achieving thread safety. It provides a way to control access to shared resources by allowing only one thread to execute a specific block of code or method at any given time.

### How it Works (Intrinsic Locks/Monitors)

Every Java object has an associated **intrinsic lock** (also known as a **monitor lock**). When a thread enters a `synchronized` method or block, it attempts to acquire the lock for the object.
*   If the lock is available, the thread acquires it and proceeds.
*   If the lock is already held by another thread, the current thread enters a `BLOCKED` state until the lock becomes available.
*   Once the thread exits the `synchronized` method or block (either normally or due to an exception), it releases the lock, allowing other waiting threads to acquire it.

This mechanism ensures that only one thread can execute the `synchronized` code protected by that specific lock at any given time, thus preventing race conditions.

### Types of `synchronized` Constructs:

#### 3.1. Synchronized Methods (Instance Methods)

When you make an instance method `synchronized`, the lock used is the **object instance** on which the method is called (`this`).

**Syntax:**

```java
public synchronized void methodName() {
    // This code block is synchronized
    // Only one thread can execute this method on the SAME object instance at a time.
}
```

**Example (Corrected Counter):**

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

// 1. The Shared Resource (NOW Synchronized)
class SynchronizedCounter {
    private int count = 0;

    // The 'synchronized' keyword ensures that only one thread
    // can execute this increment method on THIS SynchronizedCounter object at a time.
    public synchronized void increment() {
        count++;
    }

    public int getCount() {
        return count;
    }
}

// 2. The Main Program Demonstrating Synchronization
public class SynchronizedDemo {

    public static void main(String[] args) throws InterruptedException {
        SynchronizedCounter counter = new SynchronizedCounter();
        int numberOfThreads = 100;
        int incrementsPerThread = 100;
        int totalExpectedCount = numberOfThreads * incrementsPerThread;

        ExecutorService executor = Executors.newFixedThreadPool(numberOfThreads);

        long startTime = System.currentTimeMillis();

        for (int i = 0; i < numberOfThreads; i++) {
            executor.submit(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    counter.increment(); // Call to the synchronized method
                }
            });
        }

        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.MINUTES);

        long endTime = System.currentTimeMillis();

        System.out.println("--- Synchronized Method Example ---");
        System.out.println("Total expected count: " + totalExpectedCount);
        System.out.println("Final count:          " + counter.getCount());
        System.out.println("Time taken:           " + (endTime - startTime) + " ms");

        if (counter.getCount() == totalExpectedCount) {
            System.out.println("\nSUCCESS: Final count is as expected due to synchronization!");
        } else {
            System.out.println("\nERROR: Something went wrong even with synchronization (unlikely with this simple example).");
        }
    }
}
```

### Input:
To run this example, save the code as `SynchronizedDemo.java` and `SynchronizedCounter.java` in the same directory, compile, and execute:
```bash
javac SynchronizedDemo.java
java SynchronizedDemo
```

### Example Output (will consistently be 10000):

```
--- Synchronized Method Example ---
Total expected count: 10000
Final count:          10000
Time taken:           28 ms

SUCCESS: Final count is as expected due to synchronization!
```

### Explanation of the Solution:

By adding `synchronized` to the `increment()` method, we ensure that:
1.  When Thread A calls `counter.increment()`, it acquires the intrinsic lock of the `counter` object.
2.  No other thread (e.g., Thread B) can acquire the lock for the *same `counter` object* until Thread A releases it (which happens when Thread A finishes executing `increment()`).
3.  This guarantees that the `count++` operation is atomic from the perspective of multiple threads accessing the *same `Counter` instance*, preventing the read-modify-write race condition.

#### 3.2. Synchronized Static Methods

When you make a `static` method `synchronized`, the lock used is the **Class object** itself (e.g., `SynchronizedStaticCounter.class`). This means only one thread can execute *any* synchronized static method of that class at a time, regardless of how many instances of the class exist.

**Syntax:**

```java
public static synchronized void staticMethodName() {
    // This code block is synchronized
    // Only one thread can execute this method on the CLASS itself at a time.
}
```

#### 3.3. Synchronized Blocks

Synchronized blocks provide more fine-grained control over locking. You can specify *any object* as the lock. This is useful when:
*   You only need to protect a small part of a method.
*   You need to protect different parts of the same object with different locks (less common, more complex).
*   You need to synchronize on an object that is not `this` or the `Class` object.

**Syntax:**

```java
public void someMethod() {
    // ... some non-synchronized code ...

    Object lockObject = new Object(); // Can be any object, often a private final field

    synchronized (lockObject) { // Or 'this', or 'MyClass.class'
        // This code block is synchronized
        // Only one thread can enter this block if it acquires the lock on 'lockObject'.
    }

    // ... more non-synchronized code ...
}
```

**Example (Synchronized Block in Counter):**

```java
// Using a synchronized block
class BlockSynchronizedCounter {
    private int count = 0;
    // It's good practice to use a dedicated, private, final lock object
    private final Object lock = new Object(); 

    public void increment() {
        // Only the critical section is synchronized
        synchronized (lock) { // Acquire the lock on the 'lock' object
            count++;
        } // Release the lock
    }

    public int getCount() {
        return count;
    }
}

// The main method would be very similar to SynchronizedDemo,
// just instantiate BlockSynchronizedCounter instead.
```

### Important Considerations when using `synchronized`:

1.  **Granularity:**
    *   **Too much synchronization:** Locking large portions of code or entire objects unnecessarily can reduce concurrency, making your application effectively single-threaded in those parts and hurting performance.
    *   **Too little synchronization:** Leads to race conditions and incorrect results.
    *   Find the sweet spot: Synchronize only the critical sections that access shared mutable state.

2.  **Performance Overhead:** Acquiring and releasing locks has a performance cost. For very high-throughput scenarios, other mechanisms (like `java.util.concurrent.atomic` classes) might be more efficient.

3.  **Deadlocks:** If threads need to acquire multiple locks, they can get into a **deadlock** situation where each thread holds a lock that the other needs, and neither can proceed. This is a common pitfall in concurrent programming.

4.  **Alternatives in `java.util.concurrent`:** Java's `java.util.concurrent` package offers more advanced and flexible concurrency utilities, such as:
    *   **`Atomic` classes:** (`AtomicInteger`, `AtomicLong`, `AtomicBoolean`, `AtomicReference`) for atomic operations on single variables without explicit locking. They use low-level CPU instructions (CAS - Compare-And-Swap).
    *   **`ReentrantLock`:** A more flexible and feature-rich lock mechanism compared to `synchronized`, allowing for fair locking, timed lock attempts, and interruptible locks.
    *   **`ReadWriteLock`:** Allows multiple readers to access a resource concurrently, but only one writer at a time.

---

## Conclusion

Race conditions are a common and often elusive problem in concurrent programming. The `synchronized` keyword in Java is a powerful and essential tool for preventing race conditions by enforcing exclusive access to shared resources. By understanding how `synchronized` works (via intrinsic locks) and applying it correctly (using synchronized methods or blocks with appropriate granularity), developers can write robust and thread-safe concurrent applications. For more complex or performance-critical scenarios, exploring the `java.util.concurrent` package is highly recommended.