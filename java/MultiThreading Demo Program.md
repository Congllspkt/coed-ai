Multi-threading in Java allows you to execute multiple parts of your program concurrently, leading to better utilization of CPU resources, improved responsiveness for user interfaces, and more efficient handling of I/O operations.

This markdown file will cover:
1.  **What is Multi-threading?**
2.  **Why use Multi-threading?**
3.  **Core Concepts**
    *   `Thread` class
    *   `Runnable` interface
    *   `start()` vs `run()`
4.  **Creating Threads (Examples)**
    *   Extending the `Thread` class
    *   Implementing the `Runnable` interface (Recommended)
5.  **Thread Synchronization (Handling Race Conditions)**
    *   The Problem
    *   The Solution (`synchronized` keyword)
6.  **Advanced Thread Management: `ExecutorService`**
7.  **Important Thread Methods (`sleep()`, `join()`)**

---

# Multi-threading Demo Program in Java

## 1. What is Multi-threading?

Multi-threading is a concept where a single program can have multiple independent paths of execution (threads) running simultaneously. Each thread has its own call stack but shares the same memory space (heap) with other threads of the same process.

## 2. Why use Multi-threading?

*   **Responsiveness:** Keeps the application responsive to user input while performing long-running tasks in the background (e.g., downloading a file, processing data).
*   **Performance:** Can significantly improve performance by utilizing multiple CPU cores, especially for compute-intensive tasks that can be broken down into smaller, independent sub-tasks.
*   **Resource Utilization:** Efficiently uses system resources by allowing I/O operations (which are slow) to run in parallel with CPU-bound computations.
*   **Simplicity (for specific tasks):** Some problems are naturally parallel and can be more simply designed using multiple threads.

## 3. Core Concepts

### `Thread` Class
The `java.lang.Thread` class is the fundamental class for thread creation and manipulation in Java. It provides constructors and methods for creating and operating on threads.

### `Runnable` Interface
The `java.lang.Runnable` interface is a functional interface that represents a task that can be executed by a thread. It has a single method: `public void run()`.

### `start()` vs `run()`
*   **`start()`:** This method is used to begin the execution of a thread. It registers the thread with the JVM and calls the `run()` method in a *new* thread of execution. You call `start()` only once.
*   **`run()`:** This method contains the code that will be executed by the new thread. If you call `run()` directly, it will execute the code in the *current* thread, just like any other method call, and no new thread will be created.

## 4. Creating Threads (Examples)

There are two primary ways to create threads in Java:

### Method 1: Extending the `Thread` Class

In this approach, you create a class that extends `java.lang.Thread` and overrides its `run()` method.

**`MyThread.java`**
```java
// MyThread.java
class MyThread extends Thread {
    private String threadName;
    private int iterations;

    // Constructor to give the thread a name and define iterations
    public MyThread(String name, int iterations) {
        this.threadName = name;
        this.iterations = iterations;
        System.out.println("Creating " +  threadName );
    }

    // The code that will be executed by the new thread
    @Override
    public void run() {
        System.out.println("Running " +  threadName );
        try {
            for(int i = 1; i <= iterations; i++) {
                System.out.println("Thread: " + threadName + ", Count: " + i);
                // Pause for a bit to simulate work
                Thread.sleep(50);
            }
        } catch (InterruptedException e) {
            System.out.println("Thread " +  threadName + " interrupted.");
        }
        System.out.println("Thread " +  threadName + " exiting.");
    }
}

// ThreadDemo1.java
public class ThreadDemo1 {
    public static void main(String args[]) {
        System.out.println("Main thread started.");

        // Create instances of MyThread
        MyThread thread1 = new MyThread("Thread-1", 5);
        MyThread thread2 = new MyThread("Thread-2", 5);

        // Start the threads. This calls the run() method in a new thread.
        thread1.start();
        thread2.start();

        System.out.println("Main thread finished starting other threads.");
        // The main thread might finish before thread1 and thread2,
        // as they run concurrently.
    }
}
```

**How to compile and run:**
```bash
javac MyThread.java ThreadDemo1.java
java ThreadDemo1
```

**Expected Output (Order may vary due to concurrency):**
```
Main thread started.
Creating Thread-1
Creating Thread-2
Running Thread-1
Running Thread-2
Main thread finished starting other threads.
Thread: Thread-1, Count: 1
Thread: Thread-2, Count: 1
Thread: Thread-1, Count: 2
Thread: Thread-2, Count: 2
Thread: Thread-1, Count: 3
Thread: Thread-2, Count: 3
Thread: Thread-1, Count: 4
Thread: Thread-2, Count: 4
Thread: Thread-1, Count: 5
Thread: Thread-2, Count: 5
Thread Thread-1 exiting.
Thread Thread-2 exiting.
```
*Note: The exact interleaved order of "Thread-1, Count: X" and "Thread-2, Count: Y" will vary each time you run the program, demonstrating concurrency.*

### Method 2: Implementing the `Runnable` Interface (Recommended)

This is the preferred approach for creating threads in Java because:
*   It allows your class to extend another class while still being a thread (Java doesn't support multiple inheritance of classes).
*   It separates the task (what needs to be run) from the thread (how it is run).

**`MyRunnable.java`**
```java
// MyRunnable.java
class MyRunnable implements Runnable {
    private String threadName;
    private int iterations;

    // Constructor to give the thread a name and define iterations
    public MyRunnable(String name, int iterations) {
        this.threadName = name;
        this.iterations = iterations;
        System.out.println("Creating " +  threadName );
    }

    // The code that will be executed by the new thread
    @Override
    public void run() {
        System.out.println("Running " +  threadName );
        try {
            for(int i = 1; i <= iterations; i++) {
                System.out.println("Runnable Thread: " + threadName + ", Count: " + i);
                // Pause for a bit to simulate work
                Thread.sleep(70); // Slightly different sleep to show distinction
            }
        } catch (InterruptedException e) {
            System.out.println("Runnable Thread " +  threadName + " interrupted.");
        }
        System.out.println("Runnable Thread " +  threadName + " exiting.");
    }
}

// ThreadDemo2.java
public class ThreadDemo2 {
    public static void main(String args[]) {
        System.out.println("Main thread started for Runnable demo.");

        // Create instances of MyRunnable
        MyRunnable runnable1 = new MyRunnable("Runnable-1", 5);
        MyRunnable runnable2 = new MyRunnable("Runnable-2", 5);

        // Create Thread objects, passing the Runnable instance to their constructor
        Thread threadA = new Thread(runnable1);
        Thread threadB = new Thread(runnable2);

        // Start the threads. This calls the run() method of the Runnable in a new thread.
        threadA.start();
        threadB.start();

        System.out.println("Main thread finished starting Runnable threads.");
    }
}
```

**How to compile and run:**
```bash
javac MyRunnable.java ThreadDemo2.java
java ThreadDemo2
```

**Expected Output (Order may vary due to concurrency):**
```
Main thread started for Runnable demo.
Creating Runnable-1
Creating Runnable-2
Main thread finished starting Runnable threads.
Running Runnable-1
Running Runnable-2
Runnable Thread: Runnable-1, Count: 1
Runnable Thread: Runnable-2, Count: 1
Runnable Thread: Runnable-1, Count: 2
Runnable Thread: Runnable-2, Count: 2
Runnable Thread: Runnable-1, Count: 3
Runnable Thread: Runnable-2, Count: 3
Runnable Thread: Runnable-1, Count: 4
Runnable Thread: Runnable-2, Count: 4
Runnable Thread: Runnable-1, Count: 5
Runnable Thread: Runnable-2, Count: 5
Runnable Thread Runnable-1 exiting.
Runnable Thread Runnable-2 exiting.
```

## 5. Thread Synchronization (Handling Race Conditions)

When multiple threads try to access and modify the same shared resource concurrently, it can lead to inconsistent or incorrect results. This is known as a **race condition**.

### The Problem: Race Condition (Unsynchronized Access)

Let's say we have a shared `Counter` object that multiple threads try to increment. Without proper synchronization, the final count might be less than expected.

**`SharedCounter.java`**
```java
// SharedCounter.java
class SharedCounter {
    private int count = 0;

    // Unsynchronized method to increment the counter
    public void increment() {
        count++; // This operation is not atomic (read, modify, write)
    }

    public int getCount() {
        return count;
    }
}

// CounterTask.java
class CounterTask implements Runnable {
    private SharedCounter counter;
    private int iterations;

    public CounterTask(SharedCounter counter, int iterations) {
        this.counter = counter;
        this.iterations = iterations;
    }

    @Override
    public void run() {
        for (int i = 0; i < iterations; i++) {
            counter.increment();
        }
    }
}

// RaceConditionDemo.java
public class RaceConditionDemo {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("--- Race Condition Demo (Unsynchronized) ---");

        SharedCounter counter = new SharedCounter();
        int numberOfThreads = 5;
        int incrementsPerThread = 10000; // Each thread increments 10,000 times
        int expectedTotal = numberOfThreads * incrementsPerThread;

        Thread[] threads = new Thread[numberOfThreads];

        for (int i = 0; i < numberOfThreads; i++) {
            threads[i] = new Thread(new CounterTask(counter, incrementsPerThread));
            threads[i].start();
        }

        // Wait for all threads to finish
        for (int i = 0; i < numberOfThreads; i++) {
            threads[i].join(); // main thread waits for each worker thread to complete
        }

        System.out.println("Expected Total: " + expectedTotal);
        System.out.println("Actual Total (Unsynchronized): " + counter.getCount());

        // The actual total will likely be less than the expected total due to race conditions.
    }
}
```

**How to compile and run:**
```bash
javac SharedCounter.java CounterTask.java RaceConditionDemo.java
java RaceConditionDemo
```

**Expected Output (Actual Total will vary, but likely less than expected):**
```
--- Race Condition Demo (Unsynchronized) ---
Expected Total: 50000
Actual Total (Unsynchronized): 47123 // This number will be different each run, and likely less than 50000
```
*Explanation:* The `count++` operation is not atomic. It involves three steps: 1. Read `count`, 2. Increment `count`, 3. Write `count` back. If two threads read the same value of `count` before either writes back, they both perform the increment based on the old value, leading to one update being lost.

### The Solution: `synchronized` Keyword

The `synchronized` keyword in Java is used to achieve thread safety. It can be applied to:
*   **Methods:** When a `synchronized` method is called, the intrinsic lock of the object (for instance methods) or the class (for static methods) is acquired. Only one thread can execute a `synchronized` method on a given object at a time.
*   **Blocks:** You can synchronize a specific block of code on any arbitrary object. This allows for finer-grained control over locking.

Let's fix the `SharedCounter` using `synchronized`.

**`SynchronizedCounter.java`**
```java
// SynchronizedCounter.java
class SynchronizedCounter {
    private int count = 0;

    // Synchronized method to increment the counter
    public synchronized void increment() {
        count++; // Now this operation is atomic with respect to other synchronized calls on this object
    }

    // You can also use a synchronized block, which is more flexible
    public void incrementSynchronizedBlock() {
        // 'this' refers to the current instance of SynchronizedCounter, acting as the lock object
        synchronized (this) {
            count++;
        }
    }

    public int getCount() {
        return count;
    }
}

// SynchronizedCounterTask.java (can reuse CounterTask or create a new one pointing to SynchronizedCounter)
// For simplicity, let's make a new one to point to the synchronized counter's increment method explicitly
class SynchronizedCounterTask implements Runnable {
    private SynchronizedCounter counter;
    private int iterations;

    public SynchronizedCounterTask(SynchronizedCounter counter, int iterations) {
        this.counter = counter;
        this.iterations = iterations;
    }

    @Override
    public void run() {
        for (int i = 0; i < iterations; i++) {
            // Using the synchronized method
            counter.increment();
            // Or using the synchronized block method:
            // counter.incrementSynchronizedBlock();
        }
    }
}

// SynchronizationDemo.java
public class SynchronizationDemo {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("\n--- Synchronization Demo (Synchronized) ---");

        SynchronizedCounter synchronizedCounter = new SynchronizedCounter();
        int numberOfThreads = 5;
        int incrementsPerThread = 10000;
        int expectedTotal = numberOfThreads * incrementsPerThread;

        Thread[] threads = new Thread[numberOfThreads];

        for (int i = 0; i < numberOfThreads; i++) {
            threads[i] = new Thread(new SynchronizedCounterTask(synchronizedCounter, incrementsPerThread));
            threads[i].start();
        }

        // Wait for all threads to finish
        for (int i = 0; i < numberOfThreads; i++) {
            threads[i].join();
        }

        System.out.println("Expected Total: " + expectedTotal);
        System.out.println("Actual Total (Synchronized): " + synchronizedCounter.getCount());

        // The actual total will now be equal to the expected total.
    }
}
```

**How to compile and run:**
```bash
javac SynchronizedCounter.java SynchronizedCounterTask.java SynchronizationDemo.java
java SynchronizationDemo
```

**Expected Output:**
```
--- Synchronization Demo (Synchronized) ---
Expected Total: 50000
Actual Total (Synchronized): 50000
```
*Explanation:* By adding the `synchronized` keyword to the `increment()` method, we ensure that only one thread can execute this method on the `SynchronizedCounter` object at any given time. This prevents the race condition and guarantees the correct final count.

## 6. Advanced Thread Management: `ExecutorService`

Directly creating and managing `Thread` objects (`new Thread().start()`) can become cumbersome for complex applications. `ExecutorService` (part of `java.util.concurrent`) provides a higher-level abstraction for managing threads and executing tasks. It uses thread pools, which are more efficient as they reuse threads rather than creating new ones for each task.

**Benefits of `ExecutorService`:**
*   **Thread Pooling:** Reuses a fixed number of threads, reducing the overhead of thread creation and destruction.
*   **Task Management:** Provides methods for submitting tasks (`Runnable` or `Callable`) and managing their lifecycle.
*   **Graceful Shutdown:** Allows for controlled shutdown of the thread pool.

**`ExecutorServiceDemo.java`**
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

// A simple task to be executed by the ExecutorService
class SimpleTask implements Runnable {
    private String taskName;

    public SimpleTask(String name) {
        this.taskName = name;
    }

    @Override
    public void run() {
        System.out.println("Starting Task: " + taskName + " by Thread: " + Thread.currentThread().getName());
        try {
            Thread.sleep((long)(Math.random() * 1000)); // Simulate work
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt(); // Restore the interrupted status
            System.out.println("Task: " + taskName + " was interrupted.");
        }
        System.out.println("Finished Task: " + taskName + " by Thread: " + Thread.currentThread().getName());
    }
}

public class ExecutorServiceDemo {
    public static void main(String[] args) {
        System.out.println("--- ExecutorService Demo ---");

        // 1. Create an ExecutorService with a fixed thread pool size
        // This will create a pool of 3 threads.
        ExecutorService executor = Executors.newFixedThreadPool(3);

        // 2. Submit tasks to the ExecutorService
        for (int i = 1; i <= 10; i++) {
            executor.submit(new SimpleTask("Task-" + i));
        }

        // 3. Initiate an orderly shutdown.
        // No new tasks will be accepted, but previously submitted tasks will complete.
        executor.shutdown();

        // 4. Wait for all submitted tasks to complete their execution
        try {
            // Await termination for up to 5 seconds
            if (!executor.awaitTermination(5, TimeUnit.SECONDS)) {
                System.err.println("Executor did not terminate in the specified time.");
                // Optionally, force shutdown if tasks are stuck
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            System.err.println("Main thread interrupted while waiting for executor to terminate.");
            executor.shutdownNow(); // Cancel currently executing tasks
        }

        System.out.println("All tasks submitted to ExecutorService have finished or timed out.");
    }
}
```

**How to compile and run:**
```bash
javac SimpleTask.java ExecutorServiceDemo.java
java ExecutorServiceDemo
```

**Expected Output (Order of tasks may vary, but threads will be reused):**
```
--- ExecutorService Demo ---
Starting Task: Task-1 by Thread: pool-1-thread-1
Starting Task: Task-2 by Thread: pool-1-thread-2
Starting Task: Task-3 by Thread: pool-1-thread-3
Finished Task: Task-1 by Thread: pool-1-thread-1
Starting Task: Task-4 by Thread: pool-1-thread-1
Finished Task: Task-2 by Thread: pool-1-thread-2
Starting Task: Task-5 by Thread: pool-1-thread-2
Finished Task: Task-3 by Thread: pool-1-thread-3
Starting Task: Task-6 by Thread: pool-1-thread-3
Finished Task: Task-4 by Thread: pool-1-thread-1
Starting Task: Task-7 by Thread: pool-1-thread-1
Finished Task: Task-5 by Thread: pool-1-thread-2
Starting Task: Task-8 by Thread: pool-1-thread-2
Finished Task: Task-6 by Thread: pool-1-thread-3
Starting Task: Task-9 by Thread: pool-1-thread-3
Finished Task: Task-7 by Thread: pool-1-thread-1
Starting Task: Task-10 by Thread: pool-1-thread-1
Finished Task: Task-8 by Thread: pool-1-thread-2
Finished Task: Task-9 by Thread: pool-1-thread-3
Finished Task: Task-10 by Thread: pool-1-thread-1
All tasks submitted to ExecutorService have finished or timed out.
```
*Notice how the "Thread: pool-1-thread-X" names repeat, indicating that the same few threads are being reused for different tasks.*

## 7. Important Thread Methods (`sleep()`, `join()`)

### `Thread.sleep(long milliseconds)`
This static method causes the currently executing thread to cease execution for a specified period of time. It throws an `InterruptedException` if another thread interrupts the current thread while it is sleeping.

**Example (already seen in previous demos):**
```java
try {
    Thread.sleep(100); // Pauses the current thread for 100 milliseconds
} catch (InterruptedException e) {
    Thread.currentThread().interrupt(); // Good practice to re-interrupt
    System.out.println("Thread was interrupted while sleeping.");
}
```

### `thread.join()`
The `join()` method allows one thread to wait for the completion of another thread. If `threadA.join()` is called from `threadB`, `threadB` will pause its execution until `threadA` finishes.

**`JoinDemo.java`**
```java
// JoinerThread.java
class JoinerThread extends Thread {
    private String threadName;
    private long sleepTime;

    public JoinerThread(String name, long sleepTime) {
        this.threadName = name;
        this.sleepTime = sleepTime;
        System.out.println("Creating " + threadName);
    }

    @Override
    public void run() {
        System.out.println("Running " + threadName);
        try {
            Thread.sleep(sleepTime); // Simulate work
            System.out.println("Finished " + threadName);
        } catch (InterruptedException e) {
            System.out.println("Thread " + threadName + " interrupted.");
        }
    }
}

public class JoinDemo {
    public static void main(String[] args) {
        System.out.println("Main thread started.");

        JoinerThread t1 = new JoinerThread("HeavyWorker", 3000); // Will take 3 seconds
        JoinerThread t2 = new JoinerThread("QuickWorker", 1000); // Will take 1 second

        t1.start(); // Start HeavyWorker
        t2.start(); // Start QuickWorker

        try {
            System.out.println("Main thread waiting for HeavyWorker to finish...");
            t1.join(); // Main thread waits for t1 to complete
            System.out.println("HeavyWorker has finished.");

            System.out.println("Main thread waiting for QuickWorker to finish...");
            t2.join(); // Main thread waits for t2 to complete
            System.out.println("QuickWorker has finished.");

        } catch (InterruptedException e) {
            System.out.println("Main thread interrupted.");
        }

        System.out.println("Main thread has finished all waiting and is now exiting.");
    }
}
```

**How to compile and run:**
```bash
javac JoinerThread.java JoinDemo.java
java JoinDemo
```

**Expected Output:**
```
Main thread started.
Creating HeavyWorker
Creating QuickWorker
Running HeavyWorker
Running QuickWorker
Main thread waiting for HeavyWorker to finish...
Finished QuickWorker
Finished HeavyWorker
HeavyWorker has finished.
Main thread waiting for QuickWorker to finish...
QuickWorker has finished.
Main thread has finished all waiting and is now exiting.
```
*Explanation:* The main thread initiates both `HeavyWorker` and `QuickWorker`. Because `t1.join()` is called first, the main thread will pause and wait for `HeavyWorker` to complete (3 seconds), even though `QuickWorker` (1 second) might have finished earlier. Only after `HeavyWorker` finishes does the main thread proceed to wait for `QuickWorker`. This demonstrates how `join()` enforces a specific order of execution or synchronization points.

---

This comprehensive demo covers the fundamental aspects of multi-threading in Java, from basic thread creation to synchronization and modern thread management with `ExecutorService`, along with practical examples and their expected outputs.