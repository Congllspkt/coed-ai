Creating threads in Java is a fundamental concept for achieving concurrency and parallelism. Java provides two primary ways to create threads:

1.  **Extending the `java.lang.Thread` class.**
2.  **Implementing the `java.lang.Runnable` interface.**

This guide will explain both methods in detail, provide examples with input/output, and discuss best practices.

---

# Creating Threads in Java

## Table of Contents

1.  [Introduction to Threads](#1-introduction-to-threads)
2.  [Method 1: Extending `java.lang.Thread`](#2-method-1-extending-javalangthread)
    *   [Example: MyThread](#example-mythread)
3.  [Method 2: Implementing `java.lang.Runnable`](#3-method-2-implementing-javalangrunnable)
    *   [Example: MyRunnable](#example-myrunnable)
4.  [`start()` vs. `run()`](#4-start-vs-run)
    *   [Example: StartVsRun](#example-startvsrun)
5.  [When to Use Which Method](#5-when-to-use-which-method)
6.  [Common Thread Methods](#6-common-thread-methods)
7.  [Important Considerations](#7-important-considerations)
8.  [Conclusion](#8-conclusion)

---

## 1. Introduction to Threads

In Java, a thread is a lightweight subprocess within a process. It's the smallest unit of processing that can be scheduled by an operating system. Multiple threads can exist within the same process and share its resources (like memory, open files, etc.), but each thread has its own call stack and program counter.

**Why use threads?**
*   **Concurrency:** To perform multiple tasks seemingly simultaneously.
*   **Responsiveness:** To keep a user interface responsive while long-running tasks execute in the background.
*   **Performance:** To utilize multi-core processors by dividing a task into smaller, parallel subtasks.

The Java Virtual Machine (JVM) starts with a primary thread called the `main` thread, which is responsible for executing the `main()` method of your application.

## 2. Method 1: Extending `java.lang.Thread`

The `java.lang.Thread` class itself implements the `Runnable` interface. When you extend `Thread`, your class becomes a thread.

**Steps:**
1.  Create a new class that extends `java.lang.Thread`.
2.  Override the `public void run()` method. This `run()` method contains the code that will be executed by the new thread.
3.  Create an instance of your custom thread class.
4.  Call the `start()` method on your thread instance. This method registers the thread with the thread scheduler and invokes the `run()` method in a new execution thread. **Do not call `run()` directly**, as it will execute the code in the current thread, not a new one.

### Example: MyThread

This example demonstrates a simple thread that counts from 1 to 5, pausing for a short time.

```java
// MyThreadExample.java

// Step 1: Create a class that extends java.lang.Thread
class MyThread extends Thread {

    private String threadName;

    public MyThread(String name) {
        this.threadName = name;
        System.out.println("Creating " + threadName);
    }

    // Step 2: Override the run() method with the thread's logic
    @Override
    public void run() {
        System.out.println("Running " + threadName);
        try {
            for (int i = 1; i <= 5; i++) {
                System.out.println("Thread " + threadName + ": " + i);
                // Pause for a bit
                Thread.sleep(500); // Sleep for 500 milliseconds (0.5 seconds)
            }
        } catch (InterruptedException e) {
            System.out.println("Thread " + threadName + " interrupted.");
        }
        System.out.println("Thread " + threadName + " exiting.");
    }
}

public class MyThreadExample {
    public static void main(String[] args) {
        System.out.println("Main thread started.");

        // Step 3: Create instances of your custom thread class
        MyThread thread1 = new MyThread("Thread-1");
        MyThread thread2 = new MyThread("Thread-2");

        // Step 4: Call the start() method to begin execution in a new thread
        thread1.start();
        thread2.start();

        // Code in the main thread continues to execute concurrently
        try {
            for (int i = 0; i < 3; i++) {
                System.out.println("Main Thread doing its work...");
                Thread.sleep(700);
            }
        } catch (InterruptedException e) {
            System.out.println("Main Thread interrupted.");
        }

        System.out.println("Main thread finished its work.");
        // The main thread will terminate when all non-daemon user threads have finished.
    }
}
```

**To Compile and Run:**

```bash
javac MyThreadExample.java
java MyThreadExample
```

**Example Output:**

*(Note: The exact interleaved order of output may vary each time you run the program due to the nature of thread scheduling.)*

```
Main thread started.
Creating Thread-1
Creating Thread-2
Running Thread-1
Running Thread-2
Thread Thread-1: 1
Thread Thread-2: 1
Main Thread doing its work...
Thread Thread-1: 2
Thread Thread-2: 2
Thread Thread-1: 3
Thread Thread-2: 3
Main Thread doing its work...
Thread Thread-1: 4
Thread Thread-2: 4
Thread Thread-1: 5
Thread Thread-2: 5
Main Thread doing its work...
Thread Thread-1 exiting.
Thread Thread-2 exiting.
Main thread finished its work.
```

**Explanation:**
*   You can see the output from `Main Thread`, `Thread-1`, and `Thread-2` interleave, demonstrating concurrent execution.
*   `Thread.sleep()` pauses the *current* thread for the specified milliseconds, allowing other threads to run.
*   `InterruptedException` is a checked exception thrown by `sleep()` if another thread interrupts the sleeping thread.

## 3. Method 2: Implementing `java.lang.Runnable`

This is generally the **preferred method** for creating threads in Java.

**Why preferred?**
*   **Separation of Concerns:** It separates the task (what needs to be run) from the thread (how it's run). Your class can define the task without necessarily being a thread itself.
*   **Flexibility:** A class implementing `Runnable` can still extend another class. Java does not support multiple inheritance for classes, so if your class already extends another class, you cannot extend `Thread`.
*   **Resource Sharing:** Multiple `Thread` objects can be created using the same `Runnable` instance, allowing them to share common data.
*   **Modern Java:** With `ExecutorService` and `Future` (part of `java.util.concurrent`), `Runnable` (and `Callable`) are the standard interfaces for defining tasks submitted to a thread pool.

**Steps:**
1.  Create a new class that implements the `java.lang.Runnable` interface.
2.  Implement the `public void run()` method. This method contains the code to be executed by the thread.
3.  Create an instance of your `Runnable` implementation.
4.  Create a `java.lang.Thread` object, passing your `Runnable` instance to its constructor.
5.  Call the `start()` method on the `Thread` object.

### Example: MyRunnable

This example shows the same counting logic but implemented using `Runnable`.

```java
// MyRunnableExample.java

// Step 1: Create a class that implements java.lang.Runnable
class MyRunnable implements Runnable {

    private String threadName;

    public MyRunnable(String name) {
        this.threadName = name;
        System.out.println("Creating " + threadName);
    }

    // Step 2: Implement the run() method with the thread's logic
    @Override
    public void run() {
        System.out.println("Running " + threadName);
        try {
            for (int i = 1; i <= 5; i++) {
                System.out.println("Thread " + threadName + ": " + i);
                Thread.sleep(500); // Sleep for 500 milliseconds
            }
        } catch (InterruptedException e) {
            System.out.println("Thread " + threadName + " interrupted.");
        }
        System.out.println("Thread " + threadName + " exiting.");
    }
}

public class MyRunnableExample {
    public static void main(String[] args) {
        System.out.println("Main thread started.");

        // Step 3: Create instances of your Runnable implementation
        MyRunnable runnable1 = new MyRunnable("Runnable-1");
        MyRunnable runnable2 = new MyRunnable("Runnable-2");

        // Step 4: Create Thread objects, passing the Runnable instance
        Thread thread1 = new Thread(runnable1);
        Thread thread2 = new Thread(runnable2);

        // Step 5: Call the start() method on the Thread object
        thread1.start();
        thread2.start();

        // Main thread continues concurrently
        try {
            for (int i = 0; i < 3; i++) {
                System.out.println("Main Thread doing its work...");
                Thread.sleep(700);
            }
        } catch (InterruptedException e) {
            System.out.println("Main Thread interrupted.");
        }

        System.out.println("Main thread finished its work.");
    }
}
```

**To Compile and Run:**

```bash
javac MyRunnableExample.java
java MyRunnableExample
```

**Example Output:**

*(Again, the exact interleaved order will vary.)*

```
Main thread started.
Creating Runnable-1
Creating Runnable-2
Running Runnable-1
Running Runnable-2
Thread Runnable-1: 1
Thread Runnable-2: 1
Main Thread doing its work...
Thread Runnable-1: 2
Thread Runnable-2: 2
Thread Runnable-1: 3
Thread Runnable-2: 3
Main Thread doing its work...
Thread Runnable-1: 4
Thread Runnable-2: 4
Thread Runnable-1: 5
Thread Runnable-2: 5
Main Thread doing its work...
Thread Runnable-1 exiting.
Thread Runnable-2 exiting.
Main thread finished its work.
```

**Explanation:**
The output is very similar to the `Thread` extension example, but the underlying structure emphasizes the separation between the `Runnable` task and the `Thread` execution mechanism.

## 4. `start()` vs. `run()`

This is a very common point of confusion for beginners.

*   **`thread.start()`:** This is the correct way to begin the execution of a new thread. It performs essential setup (like registering the thread with the OS and JVM) and then calls the `run()` method in the newly created thread.
*   **`thread.run()`:** If you call `run()` directly (e.g., `myThreadInstance.run()` or `myRunnableInstance.run()`), the `run()` method will simply execute as a regular method call within the *current thread* (the thread that called it). No new thread is created, and no concurrent execution happens.

### Example: StartVsRun

```java
// StartVsRunExample.java

class Task implements Runnable {
    private String name;

    public Task(String name) {
        this.name = name;
    }

    @Override
    public void run() {
        System.out.println(Thread.currentThread().getName() + " is executing Task: " + name);
        try {
            Thread.sleep(200);
        } catch (InterruptedException e) {
            System.err.println(name + " was interrupted.");
        }
        System.out.println(Thread.currentThread().getName() + " finished Task: " + name);
    }
}

public class StartVsRunExample {
    public static void main(String[] args) {
        System.out.println("Main Thread ID: " + Thread.currentThread().getId());
        System.out.println("Main Thread Name: " + Thread.currentThread().getName());

        // Scenario 1: Correctly starting a new thread
        System.out.println("\n--- Calling thread.start() ---");
        Task task1 = new Task("Task A (with start())");
        Thread threadA = new Thread(task1, "Worker-A"); // Assign a name to the thread
        threadA.start(); // This creates a new thread for task1

        // Scenario 2: Incorrectly calling run() directly
        System.out.println("\n--- Calling runnable.run() directly ---");
        Task task2 = new Task("Task B (with direct run())");
        // This executes Task B in the main thread, not a new thread.
        // It's just a regular method call.
        task2.run();

        System.out.println("\n--- Calling thread.run() directly ---");
        // This is also possible if your class extends Thread
        class DirectRunThread extends Thread {
            public DirectRunThread(String name) { super(name); }
            @Override public void run() {
                System.out.println(Thread.currentThread().getName() + " is executing DirectRunThread.");
            }
        }
        DirectRunThread directThread = new DirectRunThread("Direct-Run-Thread");
        directThread.run(); // Executes in main thread

        System.out.println("\nMain Thread continues after all calls.");
        try {
            Thread.sleep(500); // Give threadA a chance to finish
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("Main Thread finished.");
    }
}
```

**To Compile and Run:**

```bash
javac StartVsRunExample.java
java StartVsRunExample
```

**Example Output:**

```
Main Thread ID: 1
Main Thread Name: main

--- Calling thread.start() ---
main is executing Task: Task B (with direct run())
main finished Task: Task B (with direct run())

--- Calling runnable.run() directly ---
main is executing DirectRunThread.
main finished DirectRunThread.

--- Calling thread.run() directly ---
Worker-A is executing Task: Task A (with start())

Main Thread continues after all calls.
Worker-A finished Task: Task A (with start())
Main Thread finished.
```

**Explanation:**
*   Notice how "Worker-A" is the thread name for `Task A`, while "main" is the thread name for `Task B` and `DirectRunThread`. This clearly shows that `start()` creates a new thread, but `run()` executed directly does not.
*   The order of "Main Thread continues..." and `Worker-A` output further demonstrates that `Task A` runs concurrently, while `Task B` and `DirectRunThread` complete *before* "Main Thread continues..." is printed.

## 5. When to Use Which Method

*   **Implement `Runnable` (Preferred):**
    *   When your class already extends another class (due to Java's single inheritance).
    *   When you want to separate the "task" (what to do) from the "thread" (how to do it). This promotes better design and reusability.
    *   When you plan to use thread pools (`ExecutorService`), as they work with `Runnable` (and `Callable`) tasks.
    *   When multiple threads need to execute the *same logic* but possibly operate on *different data* or the *same shared data*.

*   **Extend `Thread`:**
    *   For very simple, self-contained threads where the class's sole purpose is to be a thread, and it doesn't need to extend any other class.
    *   Less flexible and generally discouraged for complex applications.

**In modern Java development, the `Runnable` interface combined with `ExecutorService` (from `java.util.concurrent`) is the standard and recommended approach for managing threads, as it provides a robust framework for thread creation, management, and pooling.**

## 6. Common Thread Methods

Besides `start()` and `run()`, here are a few other important `Thread` class methods:

*   `static void sleep(long millis)`: Pauses the currently executing thread for a specified number of milliseconds. Throws `InterruptedException`.
*   `static Thread currentThread()`: Returns a reference to the currently executing thread object.
*   `String getName()`: Returns the name of this thread.
*   `void setName(String name)`: Changes the name of this thread.
*   `long getId()`: Returns the identifier of this thread.
*   `void join()`: Waits for this thread to die. Useful when one thread needs to wait for another to complete its task. (Can throw `InterruptedException`).
*   `void interrupt()`: Interrupts this thread. This sets the thread's interrupted status to true and, if the thread is blocked in an operation like `sleep()`, `wait()`, or `join()`, it throws an `InterruptedException`. It does *not* stop the thread immediately. The thread's `run()` method must check `isInterrupted()` and handle the interruption gracefully.

## 7. Important Considerations

*   **Thread Safety and Synchronization:** When multiple threads access and modify shared data, you can run into concurrency issues like race conditions. Java provides mechanisms like `synchronized` blocks/methods, `volatile` keyword, and classes from `java.util.concurrent.locks` and `java.util.concurrent.atomic` packages to ensure thread safety. This is a crucial topic to study after understanding basic thread creation.
*   **Deadlock, Livelock, Starvation:** These are common problems in concurrent programming that can occur when threads contend for resources.
*   **Thread Pools (`ExecutorService`):** For most real-world applications, directly creating `Thread` objects is less efficient and harder to manage. `ExecutorService` provides a framework to manage a pool of threads, reusing them for multiple tasks, which improves performance and resource utilization.
*   **Exception Handling:** Exceptions thrown in a `run()` method are not caught by the calling thread's `try-catch` block. They are handled by the thread's `UncaughtExceptionHandler` or lead to the thread's termination.

## 8. Conclusion

Understanding how to create and manage threads is fundamental to concurrent programming in Java. While extending `Thread` is straightforward, implementing `Runnable` is generally preferred for its flexibility and better separation of concerns, especially when combined with modern concurrency utilities like `ExecutorService`. Always remember the critical difference between `start()` (creates a new thread) and `run()` (executes in the current thread) to avoid common pitfalls.