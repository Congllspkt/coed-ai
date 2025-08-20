# Java Thread Methods Demo

This document provides a detailed explanation and examples for key Java `Thread` methods: `getId()`, `threadId()`, `getName()`, `setName()`, `currentThread()`, and `sleep()`.

---

## Table of Contents

1.  [Introduction to Java Threads](#1-introduction-to-java-threads)
2.  [`getId()` Method](#2-getid-method)
3.  [`threadId()` Method (Java 19+)](#3-threadid-method-java-19)
4.  [`getName()` Method](#4-getname-method)
5.  [`setName()` Method](#5-setname-method)
6.  [`currentThread()` Method](#6-currentthread-method)
7.  [`sleep()` Method](#7-sleep-method)
8.  [Consolidated Demo Application](#8-consolidated-demo-application)
9.  [Conclusion](#9-conclusion)

---

## 1. Introduction to Java Threads

In Java, threads are lightweight processes that enable concurrent execution within a single program. They allow a program to perform multiple tasks simultaneously, improving responsiveness and efficiency. The `java.lang.Thread` class is the foundation for thread management in Java.

The methods discussed here are crucial for identifying, naming, controlling, and interacting with threads.

---

## 2. `getId()` Method

*   **Signature:** `public long getId()`
*   **Purpose:** Returns the identifier of this Thread. The thread ID is a positive `long` number generated when this thread was created. The ID is unique within a JVM instance and remains constant for the thread's lifetime, even after it terminates.
*   **Return Type:** `long` (the thread's ID).

### Example: `getId()`

**`GetIdExample.java`**

```java
public class GetIdExample {
    public static void main(String[] args) {
        // Get the ID of the main thread
        Thread mainThread = Thread.currentThread();
        System.out.println("Main Thread ID: " + mainThread.getId());

        // Create and start a new thread
        Thread myThread = new Thread(() -> {
            System.out.println("Custom Thread ID: " + Thread.currentThread().getId());
        });
        myThread.start();
    }
}
```

**How to Compile and Run:**

```bash
javac GetIdExample.java
java GetIdExample
```

**Expected Output (IDs will vary):**

```
Main Thread ID: 1
Custom Thread ID: 13
```

**Explanation:**
The `getId()` method returns a unique numerical identifier for each thread. The `main` thread usually has ID `1`, and subsequent threads created by the JVM or your application will get higher, unique IDs.

---

## 3. `threadId()` Method (Java 19+)

*   **Signature:** `public long threadId()`
*   **Purpose:** Returns the identifier of this Thread. This method is functionally identical to `getId()` but was introduced in Java 19 as the preferred way to get a thread's ID, aligning with newer concurrency features.
*   **Return Type:** `long` (the thread's ID).

### Example: `threadId()`

**`ThreadIdExample.java`**

```java
public class ThreadIdExample {
    public static void main(String[] args) {
        // Get the ID of the main thread using threadId()
        Thread mainThread = Thread.currentThread();
        System.out.println("Main Thread ID (via threadId()): " + mainThread.threadId());

        // Create and start a new thread
        Thread myThread = new Thread(() -> {
            System.out.println("Custom Thread ID (via threadId()): " + Thread.currentThread().threadId());
        });
        myThread.start();
    }
}
```

**How to Compile and Run (requires Java 19 or later):**

```bash
javac ThreadIdExample.java
java ThreadIdExample
```

**Expected Output (IDs will vary, similar to `getId()`):**

```
Main Thread ID (via threadId()): 1
Custom Thread ID (via threadId()): 13
```

**Explanation:**
For practical purposes, `threadId()` behaves just like `getId()`. If you are using Java 19 or later, `threadId()` is the recommended method.

---

## 4. `getName()` Method

*   **Signature:** `public String getName()`
*   **Purpose:** Returns the name of this thread. Thread names are useful for debugging and logging purposes, making it easier to identify which thread is performing a particular task. If a name is not explicitly set, the JVM assigns a default name like "Thread-0", "Thread-1", etc.
*   **Return Type:** `String` (the thread's name).

### Example: `getName()`

**`GetNameExample.java`**

```java
public class GetNameExample {
    public static void main(String[] args) {
        // Get the name of the main thread
        Thread mainThread = Thread.currentThread();
        System.out.println("Main Thread Name: " + mainThread.getName());

        // Create a new thread without setting a custom name
        Thread defaultNamedThread = new Thread(() -> {
            System.out.println("Default Named Thread Name: " + Thread.currentThread().getName());
        });
        defaultNamedThread.start();

        // Create a new thread with a custom name in the constructor
        Thread customNamedThread = new Thread("WorkerThread-A") {
            @Override
            public void run() {
                System.out.println("Custom Named Thread Name: " + Thread.currentThread().getName());
            }
        };
        customNamedThread.start();
    }
}
```

**How to Compile and Run:**

```bash
javac GetNameExample.java
java GetNameExample
```

**Expected Output (order might vary):**

```
Main Thread Name: main
Default Named Thread Name: Thread-0
Custom Named Thread Name: WorkerThread-A
```

**Explanation:**
The `main` thread is always named "main". Threads created without a specific name get a default name like "Thread-0", "Thread-1", etc., while threads initialized with a name parameter will use that custom name.

---

## 5. `setName()` Method

*   **Signature:** `public void setName(String name)`
*   **Purpose:** Changes the name of this thread to the specified `name`. This can be done at any point after the thread is created. Setting meaningful names for your threads greatly aids in debugging and monitoring.
*   **Parameters:** `name` - the new name for the thread.
*   **Return Type:** `void`.

### Example: `setName()`

**`SetNameExample.java`**

```java
public class SetNameExample {
    public static void main(String[] args) {
        Thread workerThread = new Thread(() -> {
            System.out.println("Before setName(), Thread Name: " + Thread.currentThread().getName());
            Thread.currentThread().setName("MyDynamicWorker"); // Set name inside the thread's run method
            System.out.println("After setName(), Thread Name: " + Thread.currentThread().getName());
        });

        System.out.println("Before start(), Initial Name of workerThread object: " + workerThread.getName());
        workerThread.setName("InitialWorker"); // Set name before starting the thread

        System.out.println("After setName('InitialWorker'), Name of workerThread object: " + workerThread.getName());

        workerThread.start();

        // Give worker thread a moment to run and set its name
        try {
            workerThread.join(); // Wait for workerThread to finish
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Main thread interrupted while waiting for workerThread.");
        }
    }
}
```

**How to Compile and Run:**

```bash
javac SetNameExample.java
java SetNameExample
```

**Expected Output:**

```
Before start(), Initial Name of workerThread object: Thread-0
After setName('InitialWorker'), Name of workerThread object: InitialWorker
Before setName(), Thread Name: InitialWorker
After setName(), Thread Name: MyDynamicWorker
```

**Explanation:**
You can set a thread's name even before it starts, and you can also change its name while it's running (though it's generally good practice to set it before `start()` for consistency). The `getName()` method reflects the most recently set name.

---

## 6. `currentThread()` Method

*   **Signature:** `public static Thread currentThread()`
*   **Purpose:** Returns a reference to the currently executing thread object. This is a static method, meaning you call it directly on the `Thread` class (e.g., `Thread.currentThread()`). It's essential when you need to perform operations on the thread that is currently running the code.
*   **Return Type:** `Thread` (the currently executing thread).

### Example: `currentThread()`

**`CurrentThreadExample.java`**

```java
public class CurrentThreadExample {
    public static void main(String[] args) {
        // In the main method, currentThread() refers to the main thread
        System.out.println("In main method, current thread is: " + Thread.currentThread().getName());

        Runnable myTask = () -> {
            // Inside the run method of a new thread, currentThread() refers to that new thread
            System.out.println("In myTask's run method, current thread is: " + Thread.currentThread().getName());
        };

        Thread thread1 = new Thread(myTask, "Worker-1");
        Thread thread2 = new Thread(myTask, "Worker-2");

        thread1.start();
        thread2.start();
    }
}
```

**How to Compile and Run:**

```bash
javac CurrentThreadExample.java
java CurrentThreadExample
```

**Expected Output (order might vary for Worker-1 and Worker-2):**

```
In main method, current thread is: main
In myTask's run method, current thread is: Worker-1
In myTask's run method, current thread is: Worker-2
```

**Explanation:**
`Thread.currentThread()` provides a convenient way to get a reference to the thread that is currently executing the code. This is useful for self-referential operations or for logging purposes to know which thread is performing an action.

---

## 7. `sleep()` Method

*   **Signature:**
    *   `public static void sleep(long millis)`
    *   `public static void sleep(long millis, int nanos)`
*   **Purpose:** Causes the thread that is currently executing to temporarily cease execution for the specified number of milliseconds (and nanoseconds). The thread does not lose ownership of any monitors (locks) it may have. This method is often used to pause a thread, simulate work, or wait for resources to become available.
*   **Parameters:**
    *   `millis`: The length of time to sleep in milliseconds.
    *   `nanos`: `0-999999` additional nanoseconds to sleep.
*   **Throws:** `InterruptedException` if any thread has interrupted the current thread. The `InterruptedException` is a checked exception, so it must be caught or declared to be thrown.
*   **Return Type:** `void`.

### Example: `sleep()`

**`SleepExample.java`**

```java
public class SleepExample {
    public static void main(String[] args) {
        System.out.println(Thread.currentThread().getName() + " starts.");

        try {
            System.out.println(Thread.currentThread().getName() + " is going to sleep for 2 seconds.");
            Thread.sleep(2000); // Sleep for 2000 milliseconds (2 seconds)
            System.out.println(Thread.currentThread().getName() + " woke up after 2 seconds.");

            System.out.println(Thread.currentThread().getName() + " is going to sleep for 1 second and 500 milliseconds.");
            Thread.sleep(1500, 500000); // Sleep for 1.5 seconds and 500,000 nanoseconds
            System.out.println(Thread.currentThread().getName() + " woke up after 1.5 seconds.");

        } catch (InterruptedException e) {
            // Handle the interruption if the thread is woken up prematurely
            System.out.println(Thread.currentThread().getName() + " was interrupted while sleeping.");
            Thread.currentThread().interrupt(); // Re-interrupt the current thread
        }

        System.out.println(Thread.currentThread().getName() + " ends.");
    }
}
```

**How to Compile and Run:**

```bash
javac SleepExample.java
java SleepExample
```

**Expected Output (with delays between lines):**

```
main starts.
main is going to sleep for 2 seconds.
// --- 2-second delay ---
main woke up after 2 seconds.
main is going to sleep for 1 second and 500 milliseconds.
// --- 1.5-second delay ---
main woke up after 1.5 seconds.
main ends.
```

**Explanation:**
`Thread.sleep()` pauses the *currently executing* thread. The `main` thread in this example pauses for the specified durations. The `InterruptedException` must be handled because another thread could potentially call `interrupt()` on this sleeping thread, waking it up prematurely.

---

## 8. Consolidated Demo Application

This application demonstrates most of the methods covered in a single, more practical scenario.

**`ThreadDemoApp.java`**

```java
import java.util.concurrent.TimeUnit; // For cleaner sleep syntax

class MyThread extends Thread {
    private String taskName;
    private long sleepDurationMillis;

    public MyThread(String name, String taskName, long sleepDurationMillis) {
        // Call super constructor to set the thread's name
        super(name);
        this.taskName = taskName;
        this.sleepDurationMillis = sleepDurationMillis;
    }

    @Override
    public void run() {
        // Demonstrating currentThread(), getName(), getId(), threadId()
        Thread current = Thread.currentThread();
        System.out.println(String.format("[%s (ID:%d/tID:%d)] - %s: Starting task...",
                current.getName(), current.getId(), current.threadId(), taskName));

        try {
            // Demonstrating sleep()
            System.out.println(String.format("[%s] - %s: Working for %dms...",
                    current.getName(), taskName, sleepDurationMillis));
            // Using TimeUnit for readability
            TimeUnit.MILLISECONDS.sleep(sleepDurationMillis);
            System.out.println(String.format("[%s] - %s: Task completed.",
                    current.getName(), taskName));

        } catch (InterruptedException e) {
            System.out.println(String.format("[%s] - %s: Was interrupted!", current.getName(), taskName));
            current.interrupt(); // Re-interrupt the thread
        }
    }
}

public class ThreadDemoApp {
    public static void main(String[] args) {
        // --- Demonstrate Main Thread ---
        Thread mainThread = Thread.currentThread();
        System.out.println("--- Main Thread Info ---");
        System.out.println("Main Thread Name: " + mainThread.getName());
        System.out.println("Main Thread ID: " + mainThread.getId());
        // For Java 19+, use threadId(). Otherwise, getId() is sufficient.
        System.out.println("Main Thread threadId(): " + mainThread.threadId());
        System.out.println("------------------------\n");

        // --- Create and Start Custom Threads ---

        // Thread 1: Set name in constructor, demonstrate sleep
        MyThread thread1 = new MyThread("LoggerThread", "Log processing", 1500);
        thread1.start(); // Start the thread

        // Thread 2: Set name using setName() before start, shorter sleep
        MyThread thread2 = new MyThread("Unassigned", "Data fetching", 800);
        System.out.println("Before starting, thread2's object name: " + thread2.getName());
        thread2.setName("FetcherThread"); // Change name before start
        System.out.println("After setName, thread2's object name: " + thread2.getName());
        thread2.start();

        // Thread 3: Demonstrate dynamic name change after start (less common)
        MyThread thread3 = new MyThread("InitialWorker", "Heavy computation", 2500);
        thread3.start();
        System.out.println("Main: Shortly after starting, thread3's object name: " + thread3.getName());

        // Introduce a small delay in main to potentially see thread3's initial name output
        try {
            TimeUnit.MILLISECONDS.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        // We can change thread3's name from main thread while it's running
        thread3.setName("ComputeThread-Renamed");
        System.out.println("Main: After renaming, thread3's object name: " + thread3.getName());


        // Main thread waiting for others to complete (optional, but good for clean exit)
        try {
            thread1.join();
            thread2.join();
            thread3.join();
        } catch (InterruptedException e) {
            System.err.println("Main thread interrupted while waiting for child threads.");
            Thread.currentThread().interrupt();
        }

        System.out.println("\nAll custom threads have finished. Main thread ending.");
    }
}
```

**How to Compile and Run:**

```bash
javac ThreadDemoApp.java
java ThreadDemoApp
```

**Expected Output (Actual order of output from `MyThread` instances may vary due to thread scheduling, but the content will be similar):**

```
--- Main Thread Info ---
Main Thread Name: main
Main Thread ID: 1
Main Thread threadId(): 1
------------------------

Before starting, thread2's object name: Unassigned
After setName, thread2's object name: FetcherThread
[LoggerThread (ID:13/tID:13)] - Log processing: Starting task...
[FetcherThread (ID:14/tID:14)] - Data fetching: Starting task...
[InitialWorker (ID:15/tID:15)] - Heavy computation: Starting task...
[LoggerThread] - Log processing: Working for 1500ms...
[FetcherThread] - Data fetching: Working for 800ms...
Main: Shortly after starting, thread3's object name: InitialWorker
Main: After renaming, thread3's object name: ComputeThread-Renamed
[FetcherThread] - Data fetching: Task completed.
[LoggerThread] - Log processing: Task completed.
[ComputeThread-Renamed] - Heavy computation: Task completed.

All custom threads have finished. Main thread ending.
```

**Explanation:**

1.  **Main Thread Info:** Displays the `main` thread's name, `getId()`, and `threadId()`.
2.  **`MyThread` Class:**
    *   Extends `Thread` for simplicity.
    *   Its `run()` method uses `Thread.currentThread()`, `getName()`, `getId()`, `threadId()` to identify itself.
    *   It uses `TimeUnit.MILLISECONDS.sleep()` to simulate work, demonstrating the `sleep()` method.
3.  **Thread Creation:**
    *   `thread1`: Name set directly in the `MyThread` constructor (which passes it to `Thread`'s constructor).
    *   `thread2`: Name initially "Unassigned" by constructor, then changed using `setName("FetcherThread")` *before* `start()`. The `run()` method then reflects this new name.
    *   `thread3`: Name "InitialWorker" by constructor. After `start()`, the main thread *re-names* it using `thread3.setName("ComputeThread-Renamed")`. You can see this change reflected when `thread3` eventually prints its completion message.
4.  **`join()` Method:** Used in the `main` method to wait for all created threads to complete their execution before the `main` thread itself finishes. This ensures a clean shutdown and that you see all thread output.

---

## 9. Conclusion

The `Thread` methods `getId()`, `threadId()`, `getName()`, `setName()`, `currentThread()`, and `sleep()` are fundamental for managing and debugging concurrent applications in Java.
*   `getId()` and `threadId()` provide unique identifiers.
*   `getName()` and `setName()` help in identifying threads with human-readable labels.
*   `currentThread()` gives access to the thread currently executing the code.
*   `sleep()` allows for controlled pausing of a thread.

Understanding and effectively using these methods is crucial for building robust and performant multi-threaded Java applications.