In Java, `wait()`, `notify()`, and `notifyAll()` are fundamental methods for inter-thread communication. They allow threads to coordinate their activities by pausing execution until a certain condition is met and then resuming when notified by another thread.

---

# `wait()`, `notify()`, `notifyAll()` in Java

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Prerequisites: The `synchronized` Keyword](#2-prerequisites-the-synchronized-keyword)
3.  [Detailed Explanation of `wait()`, `notify()`, `notifyAll()`](#3-detailed-explanation-of-wait-notify-notifyall)
    *   [`wait()`](#wait)
    *   [`notify()`](#notify)
    *   [`notifyAll()`](#notifyall)
4.  [Key Rules and Best Practices](#4-key-rules-and-best-practices)
5.  [Example: Producer-Consumer Problem](#5-example-producer-consumer-problem)
    *   [Problem Description](#problem-description)
    *   [Code Structure](#code-structure)
    *   [Full Code](#full-code)
    *   [How to Compile and Run (Input)](#how-to-compile-and-run-input)
    *   [Expected Output](#expected-output)
6.  [Summary](#6-summary)
7.  [Further Considerations](#7-further-considerations)

---

## 1. Introduction

`wait()`, `notify()`, and `notifyAll()` are methods defined in the `Object` class, meaning every Java object inherits them. They are crucial for implementing the "Guarded Suspension" pattern, where a thread waits for a certain condition to become true before proceeding, and other threads notify it when that condition might have changed.

They are used for communication between threads that share a common resource or monitor.

## 2. Prerequisites: The `synchronized` Keyword

Before discussing `wait()`, `notify()`, and `notifyAll()`, it's critical to understand their prerequisite: the `synchronized` keyword.

*   **Monitor (Lock):** In Java, every object has an intrinsic lock, also known as a monitor.
*   **`synchronized` Block/Method:** When a thread enters a `synchronized` block or method, it acquires the monitor for the object on which it's synchronizing. Only one thread can hold an object's monitor at any given time.
*   **Requirement:** `wait()`, `notify()`, and `notifyAll()` **must** be called from within a `synchronized` block or method. If called outside, they will throw an `IllegalMonitorStateException`. This is because these methods operate on the object's monitor. A thread must own the monitor to control its state (waiting or notifying others).

## 3. Detailed Explanation of `wait()`, `notify()`, `notifyAll()`

### `wait()`

*   **Signature:**
    *   `public final void wait() throws InterruptedException`
    *   `public final void wait(long timeout) throws InterruptedException`
    *   `public final void wait(long timeout, int nanos) throws InterruptedException`

*   **What it does:**
    1.  **Releases the Lock:** The calling thread **releases the monitor** (lock) of the object it's synchronized on. This is the key difference from `Thread.sleep()`.
    2.  **Goes to Waiting State:** The thread then enters the object's "waiting set" and transitions into a `WAITING` (or `TIMED_WAITING` if a timeout is specified) state. It effectively pauses its execution.
    3.  **Waits for Notification/Timeout:** The thread remains in the waiting state until:
        *   Another thread calls `notify()` or `notifyAll()` on the *same object*.
        *   The specified `timeout` expires (if `wait(long)` or `wait(long, int)` is used).
        *   The thread is `interrupted()`.
    4.  **Re-acquires Lock:** When notified (or timed out/interrupted), the thread becomes `RUNNABLE` but does *not* immediately resume execution. It must first **re-acquire the monitor** for the object. Only after successfully re-acquiring the lock does it resume execution from where it left off.

*   **Key Points:**
    *   **`IllegalMonitorStateException`:** Thrown if the current thread does not own the object's monitor.
    *   **`InterruptedException`:** Thrown if another thread interrupts the current thread while it is waiting.
    *   **Spurious Wakeups:** A thread can sometimes wake up from `wait()` even without a `notify()` or timeout. Therefore, `wait()` should always be called inside a `while` loop, checking the condition it's waiting for:
        ```java
        synchronized (sharedObject) {
            while (!conditionMet) { // IMPORTANT: Use a while loop!
                sharedObject.wait();
            }
            // Condition is now met, proceed
        }
        ```

### `notify()`

*   **Signature:**
    *   `public final void notify()`

*   **What it does:**
    1.  **Wakes up One Thread:** Wakes up a *single* arbitrary thread that is currently waiting on this object's monitor. If multiple threads are waiting, there's no guarantee which one will be chosen (it's non-deterministic).
    2.  **Does NOT Release Lock Immediately:** The awakened thread does not immediately execute. It becomes `RUNNABLE` and competes for the lock *after* the thread that called `notify()` releases the lock (i.e., exits its `synchronized` block).
    3.  **No Effect if No Threads Waiting:** If no threads are waiting on this object, `notify()` does nothing.

*   **Key Points:**
    *   **`IllegalMonitorStateException`:** Thrown if the current thread does not own the object's monitor.
    *   Use when only one thread needs to be woken up, or when any one of the waiting threads can proceed.

### `notifyAll()`

*   **Signature:**
    *   `public final void notifyAll()`

*   **What it does:**
    1.  **Wakes up All Threads:** Wakes up *all* threads that are currently waiting on this object's monitor.
    2.  **Does NOT Release Lock Immediately:** Similar to `notify()`, the awakened threads become `RUNNABLE` and compete for the lock *after* the thread that called `notifyAll()` releases the lock.
    3.  **No Effect if No Threads Waiting:** If no threads are waiting on this object, `notifyAll()` does nothing.

*   **Key Points:**
    *   **`IllegalMonitorStateException`:** Thrown if the current thread does not own the object's monitor.
    *   Generally safer and often preferred over `notify()` in complex scenarios (like producer-consumer with multiple producers and consumers), as it avoids potential deadlocks by ensuring all relevant threads get a chance to re-evaluate their conditions.
    *   Can lead to "thundering herd" problem where many threads wake up, but only one can proceed, causing overhead.

## 4. Key Rules and Best Practices

1.  **Always `synchronized`:** `wait()`, `notify()`, `notifyAll()` must be called from within a `synchronized` block/method, and on the *same object* that the thread is synchronized on.
2.  **`while` loop for `wait()`:** Always call `wait()` inside a `while` loop to guard against spurious wakeups and ensure the condition is *actually* met before proceeding.
3.  **Release Lock:** `wait()` releases the object's monitor; `notify()`/`notifyAll()` do *not* release the monitor immediately. The notifying thread must exit its `synchronized` block for the waiting threads to acquire the lock.
4.  **Atomicity:** The `wait()` method is atomic regarding its entry into the waiting set and the release of the lock.
5.  **`notifyAll()` vs `notify()`:** In general, `notifyAll()` is safer as it wakes up all relevant threads, ensuring none are missed. `notify()` is more performant if you're certain only one specific type of thread needs to be awakened. For producer-consumer, `notifyAll()` is often recommended to cover both producers (waiting for space) and consumers (waiting for items).

---

## 5. Example: Producer-Consumer Problem

This is a classic concurrency problem that perfectly demonstrates the use of `wait()`, `notify()`, and `notifyAll()`.

### Problem Description

We have:
*   A **Shared Buffer**: A fixed-size storage area.
*   A **Producer Thread**: Adds items to the buffer. If the buffer is full, it waits.
*   A **Consumer Thread**: Removes items from the buffer. If the buffer is empty, it waits.

The producer needs to notify the consumer when it adds an item, and the consumer needs to notify the producer when it removes an item.

### Code Structure

1.  **`SharedBuffer` Class:** Manages the `List` (buffer), `put()` (producer), and `get()` (consumer) operations, using `wait()` and `notifyAll()`.
2.  **`Producer` Class:** Implements `Runnable`, uses the `SharedBuffer` to `put()` items.
3.  **`Consumer` Class:** Implements `Runnable`, uses the `SharedBuffer` to `get()` items.
4.  **`WaitNotifyDemo` Class:** Contains the `main` method to set up and start the producer and consumer threads.

### Full Code

```java
// SharedBuffer.java
import java.util.ArrayList;
import java.util.List;

/**
 * Represents a shared buffer between producer and consumer threads.
 * Uses wait() and notifyAll() for thread coordination.
 */
class SharedBuffer {
    private List<Integer> buffer = new ArrayList<>();
    private final int capacity;

    public SharedBuffer(int capacity) {
        this.capacity = capacity;
    }

    /**
     * Puts an item into the buffer. If the buffer is full, the producer
     * thread will wait until space becomes available.
     * @param item The item to put into the buffer.
     * @throws InterruptedException if the thread is interrupted while waiting.
     */
    public void put(int item) throws InterruptedException {
        // Synchronize on 'this' (the SharedBuffer object) to acquire its intrinsic lock.
        synchronized (this) {
            // Use a while loop to guard against spurious wakeups and re-check condition
            while (buffer.size() == capacity) {
                System.out.println("Buffer is FULL. Producer [" + Thread.currentThread().getName() + "] waiting...");
                // Releases the lock on 'this' and waits.
                this.wait();
            }

            buffer.add(item);
            System.out.println("Producer [" + Thread.currentThread().getName() + "] Produced: " + item + ", Buffer size: " + buffer.size());
            
            // Notifies ALL waiting threads (could be consumers or other producers)
            // that the buffer state has changed (it now has an item).
            this.notifyAll(); 
            Thread.sleep(50); // Simulate some work
        }
    }

    /**
     * Gets an item from the buffer. If the buffer is empty, the consumer
     * thread will wait until an item becomes available.
     * @return The item retrieved from the buffer.
     * @throws InterruptedException if the thread is interrupted while waiting.
     */
    public int get() throws InterruptedException {
        int item;
        // Synchronize on 'this' (the SharedBuffer object) to acquire its intrinsic lock.
        synchronized (this) {
            // Use a while loop to guard against spurious wakeups and re-check condition
            while (buffer.isEmpty()) {
                System.out.println("Buffer is EMPTY. Consumer [" + Thread.currentThread().getName() + "] waiting...");
                // Releases the lock on 'this' and waits.
                this.wait();
            }

            item = buffer.remove(0); // Remove from the beginning
            System.out.println("Consumer [" + Thread.currentThread().getName() + "] Consumed: " + item + ", Buffer size: " + buffer.size());

            // Notifies ALL waiting threads (could be producers or other consumers)
            // that the buffer state has changed (it now has space).
            this.notifyAll();
            Thread.sleep(50); // Simulate some work
        }
        return item;
    }
}

// Producer.java
class Producer implements Runnable {
    private SharedBuffer buffer;
    private int itemsToProduce;

    public Producer(SharedBuffer buffer, int itemsToProduce) {
        this.buffer = buffer;
        this.itemsToProduce = itemsToProduce;
    }

    @Override
    public void run() {
        for (int i = 0; i < itemsToProduce; i++) {
            try {
                buffer.put(i);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                System.out.println("Producer interrupted.");
                return;
            }
        }
        System.out.println("Producer [" + Thread.currentThread().getName() + "] finished producing.");
    }
}

// Consumer.java
class Consumer implements Runnable {
    private SharedBuffer buffer;
    private int itemsToConsume;

    public Consumer(SharedBuffer buffer, int itemsToConsume) {
        this.buffer = buffer;
        this.itemsToConsume = itemsToConsume;
    }

    @Override
    public void run() {
        for (int i = 0; i < itemsToConsume; i++) {
            try {
                buffer.get();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                System.out.println("Consumer interrupted.");
                return;
            }
        }
        System.out.println("Consumer [" + Thread.currentThread().getName() + "] finished consuming.");
    }
}

// WaitNotifyDemo.java (Main class)
public class WaitNotifyDemo {
    public static void main(String[] args) {
        // Create a shared buffer with capacity 5
        SharedBuffer buffer = new SharedBuffer(5);

        // Create a producer thread
        Producer producer = new Producer(buffer, 15); // Produce 15 items
        Thread producerThread = new Thread(producer, "Producer-1");

        // Create a consumer thread
        Consumer consumer = new Consumer(buffer, 15); // Consume 15 items
        Thread consumerThread = new Thread(consumer, "Consumer-1");

        // Start both threads
        System.out.println("Starting Producer and Consumer threads...");
        producerThread.start();
        consumerThread.start();

        // Wait for both threads to finish
        try {
            producerThread.join();
            consumerThread.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.out.println("Main thread interrupted.");
        }

        System.out.println("All production and consumption complete.");
    }
}
```

### How to Compile and Run (Input)

1.  **Save:** Save the code above into three separate files: `SharedBuffer.java`, `Producer.java`, `Consumer.java`, and `WaitNotifyDemo.java`. Make sure they are in the same directory.
2.  **Compile:** Open a terminal or command prompt, navigate to the directory where you saved the files, and compile them:
    ```bash
    javac SharedBuffer.java Producer.java Consumer.java WaitNotifyDemo.java
    ```
    (Or simply `javac *.java` if you prefer)
3.  **Run:** Execute the main class:
    ```bash
    java WaitNotifyDemo
    ```

### Expected Output

The exact order of "Produced" and "Consumed" messages might vary due to thread scheduling, but the core logic of waiting and notifying will be evident. You will see messages like:

```
Starting Producer and Consumer threads...
Producer [Producer-1] Produced: 0, Buffer size: 1
Producer [Producer-1] Produced: 1, Buffer size: 2
Consumer [Consumer-1] Consumed: 0, Buffer size: 1
Producer [Producer-1] Produced: 2, Buffer size: 2
Consumer [Consumer-1] Consumed: 1, Buffer size: 1
Producer [Producer-1] Produced: 3, Buffer size: 2
Producer [Producer-1] Produced: 4, Buffer size: 3
Producer [Producer-1] Produced: 5, Buffer size: 4
Producer [Producer-1] Produced: 6, Buffer size: 5
Buffer is FULL. Producer [Producer-1] waiting...
Consumer [Consumer-1] Consumed: 2, Buffer size: 4
Producer [Producer-1] Produced: 7, Buffer size: 5
Buffer is FULL. Producer [Producer-1] waiting...
Consumer [Consumer-1] Consumed: 3, Buffer size: 4
Producer [Producer-1] Produced: 8, Buffer size: 5
Buffer is FULL. Producer [Producer-1] waiting...
Consumer [Consumer-1] Consumed: 4, Buffer size: 4
Producer [Producer-1] Produced: 9, Buffer size: 5
Buffer is FULL. Producer [Producer-1] waiting...
Consumer [Consumer-1] Consumed: 5, Buffer size: 4
Producer [Producer-1] Produced: 10, Buffer size: 5
Buffer is FULL. Producer [Producer-1] waiting...
Consumer [Consumer-1] Consumed: 6, Buffer size: 4
Producer [Producer-1] Produced: 11, Buffer size: 5
Buffer is FULL. Producer [Producer-1] waiting...
Consumer [Consumer-1] Consumed: 7, Buffer size: 4
Producer [Producer-1] Produced: 12, Buffer size: 5
Buffer is FULL. Producer [Producer-1] waiting...
Consumer [Consumer-1] Consumed: 8, Buffer size: 4
Producer [Producer-1] Produced: 13, Buffer size: 5
Buffer is FULL. Producer [Producer-1] waiting...
Consumer [Consumer-1] Consumed: 9, Buffer size: 4
Producer [Producer-1] Produced: 14, Buffer size: 5
Producer [Producer-1] finished producing.
Consumer [Consumer-1] Consumed: 10, Buffer size: 4
Consumer [Consumer-1] Consumed: 11, Buffer size: 3
Consumer [Consumer-1] Consumed: 12, Buffer size: 2
Consumer [Consumer-1] Consumed: 13, Buffer size: 1
Consumer [Consumer-1] Consumed: 14, Buffer size: 0
Consumer [Consumer-1] finished consuming.
All production and consumption complete.
```

In the output, observe:
*   When the buffer reaches its `capacity` (5), the `Producer` thread prints "Buffer is FULL... waiting..." and pauses.
*   When the `Consumer` thread consumes an item and the buffer is no longer full, the `notifyAll()` from the consumer wakes up the producer.
*   Similarly, if the buffer becomes `EMPTY`, the `Consumer` thread prints "Buffer is EMPTY... waiting..." and pauses.
*   When the `Producer` adds an item, the `notifyAll()` from the producer wakes up the consumer.

This continuous cycle of waiting and notifying demonstrates effective thread coordination.

---

## 6. Summary

`wait()`, `notify()`, and `notifyAll()` are the bedrock for implementing synchronized inter-thread communication in Java. They provide a mechanism for threads to conditionally pause their execution and be resumed by other threads when specific conditions are met, all while ensuring proper lock management through the `synchronized` keyword.

*   `wait()`: Relinquishes the lock, puts the thread to sleep, and waits for notification (or timeout).
*   `notify()`: Wakes up one arbitrary thread waiting on the object's lock.
*   `notifyAll()`: Wakes up all threads waiting on the object's lock.

All three must be called from within a `synchronized` block/method, on the object whose lock is held.

## 7. Further Considerations

*   **`wait()` vs `Thread.sleep()`:**
    *   `wait()` releases the object's monitor; `Thread.sleep()` does not.
    *   `wait()` is for inter-thread communication; `Thread.sleep()` is for pausing execution for a duration.
    *   `wait()` must be in a `synchronized` block; `Thread.sleep()` can be called anywhere.
*   **`java.util.concurrent.locks.Condition`:** For more complex and flexible thread coordination scenarios, Java's `java.util.concurrent.locks.Condition` interface (obtained from a `Lock` object) offers a more powerful and explicit way to achieve similar results, often preferred in modern Java concurrency programming over `wait()/notify()` due to better readability, separate waiting sets, and no requirement for `synchronized` blocks (as the `Lock` itself provides mutual exclusion). However, the underlying principles are the same.