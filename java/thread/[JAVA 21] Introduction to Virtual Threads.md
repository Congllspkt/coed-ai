This document provides a detailed introduction to Virtual Threads in Java 21, including their purpose, how they differ from traditional threads, and practical examples.

---

# Introduction to Virtual Threads in Java 21

## Table of Contents
1.  Introduction
2.  The Problem: Scalability with Traditional Threads
3.  Virtual Threads vs. Platform Threads
    *   Platform Threads
    *   Virtual Threads
    *   Key Differences Summarized
4.  How Virtual Threads Work (Under the Hood)
5.  Benefits of Virtual Threads
6.  Creating Virtual Threads
    *   `Thread.ofVirtual()`
    *   `Executors.newVirtualThreadPerTaskExecutor()`
7.  Examples
    *   Example 1: Basic Virtual Thread Creation
    *   Example 2: Scalability Test (Platform vs. Virtual)
    *   Example 3: Handling Blocking Operations
8.  When to Use Virtual Threads
9.  When NOT to Use Virtual Threads (Considerations)
10. Tooling and Debugging
11. Conclusion

---

## 1. Introduction

Java 21, building upon earlier preview features from Java 19 and 20, officially introduced **Virtual Threads** as a key component of **Project Loom**. Virtual Threads are lightweight, user-mode threads designed to dramatically improve the scalability of server applications, especially those that are I/O-bound.

The core idea is to allow developers to continue using the simple, familiar "thread-per-request" style of programming without the performance and resource overhead associated with traditional operating system (OS) threads.

## 2. The Problem: Scalability with Traditional Threads

Historically, Java's `java.lang.Thread` objects were direct wrappers around OS kernel threads. This "one-to-one" mapping presented several challenges for highly concurrent applications:

*   **Resource Consumption:** Each OS thread requires a significant amount of memory for its stack (typically 1MB-2MB), plus kernel resources. Creating tens of thousands of such threads quickly exhausts memory and system limits.
*   **Context Switching Overhead:** The OS kernel manages context switching between threads. When many threads are active, the overhead of saving and restoring CPU state becomes substantial.
*   **Blocking Operations:** When a traditional thread performs a blocking I/O operation (e.g., waiting for a database query, reading from a network socket), it blocks the underlying OS thread. This OS thread cannot be used for any other task until the I/O operation completes, leading to underutilization of CPU resources.

To mitigate these issues, developers often resorted to complex asynchronous programming models (like `CompletableFuture`, reactive programming frameworks such as Reactor or RxJava) to achieve high concurrency. While powerful, these models increase code complexity and reduce readability.

## 3. Virtual Threads vs. Platform Threads

To understand Virtual Threads, it's crucial to differentiate them from the threads we've been using so far, now officially called **Platform Threads**.

### Platform Threads

*   **Mapping:** Directly map to OS kernel threads (one-to-one).
*   **Memory Footprint:** Heavyweight, requiring a large, fixed-size stack (typically 1-2 MB).
*   **Management:** Managed by the OS kernel (scheduling, context switching).
*   **Quantity:** Limited in number (thousands, not tens of thousands) due to resource constraints.
*   **Blocking:** When a platform thread blocks (e.g., on I/O), its associated OS thread is also blocked and cannot perform other work.
*   **Purpose:** Suitable for CPU-bound tasks where the number of threads is typically close to the number of CPU cores.

### Virtual Threads

*   **Mapping:** Many-to-one mapping to a small pool of platform threads, called **carrier threads**.
*   **Memory Footprint:** Extremely lightweight, with a small, dynamically growing stack.
*   **Management:** Managed by the JVM (scheduling, context switching). Not directly exposed to the OS.
*   **Quantity:** Virtually unlimited (millions are feasible) due to minimal overhead.
*   **Blocking:** When a virtual thread blocks (e.g., on I/O), the JVM "unmounts" it from its carrier thread. The carrier thread is then free to "mount" and run another virtual thread. When the I/O operation completes, the virtual thread is "re-mounted" onto an available carrier thread.
*   **Purpose:** Ideal for I/O-bound tasks where many concurrent operations spend most of their time waiting for external resources.

### Key Differences Summarized

| Feature            | Platform Threads (Traditional)                               | Virtual Threads                                              |
| :----------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Mapping**        | 1:1 to OS kernel threads                                     | M:N (many-to-many) to a small pool of Platform (carrier) threads |
| **Memory**         | High (fixed stack, ~1-2 MB)                                  | Low (dynamic stack, few KBs initially)                       |
| **Management**     | OS kernel                                                    | JVM                                                          |
| **Concurrency**    | Limited (thousands)                                          | Virtually unlimited (millions)                               |
| **Blocking I/O**   | Blocks OS thread                                             | Unmounts from carrier thread, allowing carrier to run another VT |
| **Primary Use Case** | CPU-bound tasks                                              | I/O-bound tasks                                              |
| **Creation**       | `new Thread()` or `Executors.newFixedThreadPool()`           | `Thread.ofVirtual()` or `Executors.newVirtualThreadPerTaskExecutor()` |

## 4. How Virtual Threads Work (Under the Hood)

The magic behind Virtual Threads lies in how the JVM manages them:

1.  **Carrier Threads:** Virtual Threads do not run directly on the OS. Instead, they run *on top of* a small pool of platform threads, which are called **carrier threads**. By default, the JVM uses a `ForkJoinPool` as the scheduler for carrier threads.
2.  **Mounting and Unmounting:**
    *   When a Virtual Thread is ready to run, the JVM "mounts" it onto an available carrier thread.
    *   If the Virtual Thread performs a **blocking I/O operation** (e.g., network call, disk read, `Thread.sleep()`), it doesn't block the carrier thread. Instead, the JVM "unmounts" the Virtual Thread from its carrier. The carrier thread is then immediately free to pick up and run another Virtual Thread.
    *   The state of the unmounted Virtual Thread (its program counter, stack, etc. – known as its **continuation**) is saved in Java heap memory.
    *   Once the blocking I/O operation completes, the Virtual Thread's continuation is reactivated. It then waits in a queue to be "re-mounted" onto an available carrier thread to resume execution.
3.  **Dynamic Stack Expansion:** Unlike platform threads with their fixed, large stacks, Virtual Threads have very small initial stacks. As the execution depth increases, the JVM dynamically expands the stack on the heap. This memory is reclaimed when the stack depth decreases.

This mechanism allows a small number of expensive platform threads to efficiently multiplex an enormous number of lightweight virtual threads, drastically improving throughput for I/O-bound workloads.

## 5. Benefits of Virtual Threads

*   **Massive Scalability:** Handle far more concurrent operations than traditional threads, especially for I/O-bound workloads.
*   **Simplicity:** Retain the familiar, straightforward imperative "thread-per-request" programming style. No need for complex asynchronous callbacks, `CompletableFuture` chains, or reactive frameworks for many use cases.
*   **Resource Efficiency:** Significantly lower memory consumption per thread and less CPU overhead for context switching compared to OS threads.
*   **Improved Throughput:** By not blocking carrier threads during I/O, CPU utilization remains high.
*   **Easier Debugging & Observability:** Tools like `jstack` and debuggers are enhanced to understand and visualize virtual threads, making debugging concurrent applications simpler than with complex async stacks.

## 6. Creating Virtual Threads

Java 21 provides convenient ways to create and manage Virtual Threads:

### Using `Thread.ofVirtual()`

This is the simplest way to create and start a single virtual thread.

```java
Thread virtualThread = Thread.ofVirtual().start(() -> {
    System.out.println("Hello from a Virtual Thread! Thread ID: " + Thread.currentThread().threadId());
    System.out.println("Is Virtual Thread? " + Thread.currentThread().isVirtual());
});

virtualThread.join(); // Wait for the virtual thread to complete
```

You can also use a `Thread.Builder` for more configuration:

```java
Runnable task = () -> {
    System.out.println("Virtual Thread (" + Thread.currentThread().threadId() + ") is running.");
};

Thread.Builder builder = Thread.ofVirtual().name("my-virtual-thread", 0);
Thread vt1 = builder.start(task);
Thread vt2 = builder.start(task); // Creates another virtual thread with name "my-virtual-thread-1"

vt1.join();
vt2.join();
```

### Using `Executors.newVirtualThreadPerTaskExecutor()`

For managing a pool of virtual threads, `ExecutorService` is the preferred way. Java 21 introduces `newVirtualThreadPerTaskExecutor()`, which creates a new virtual thread for *every* submitted task.

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class VirtualThreadExecutorExample {
    public static void main(String[] args) throws InterruptedException {

        System.out.println("Using newVirtualThreadPerTaskExecutor...");

        // Creates an ExecutorService that creates a new virtual thread for each task.
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < 5; i++) {
                final int taskId = i;
                executor.submit(() -> {
                    System.out.println("Task " + taskId + " running in Virtual Thread: " +
                                       Thread.currentThread().threadId() + ", IsVirtual: " +
                                       Thread.currentThread().isVirtual());
                    try {
                        Thread.sleep(100); // Simulate some work
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                });
            }
        } // ExecutorService is automatically shut down here (try-with-resources)

        System.out.println("All tasks submitted. Main thread continuing...");
        // Give some time for virtual threads to finish if not joined explicitly
        TimeUnit.SECONDS.sleep(1);
    }
}
```

## 7. Examples

### Example 1: Basic Virtual Thread Creation

This example demonstrates the simplest way to create and run a Virtual Thread, and checks its properties.

**`VirtualThreadBasic.java`**
```java
import java.util.concurrent.TimeUnit;

public class VirtualThreadBasic {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("Main Thread ID: " + Thread.currentThread().threadId());
        System.out.println("Main Thread Is Virtual: " + Thread.currentThread().isVirtual());

        // Create and start a Virtual Thread
        Thread virtualThread = Thread.ofVirtual().name("MyFirstVirtualThread").start(() -> {
            System.out.println("\nHello from inside the Virtual Thread!");
            System.out.println("Virtual Thread Name: " + Thread.currentThread().getName());
            System.out.println("Virtual Thread ID: " + Thread.currentThread().threadId());
            System.out.println("Is Virtual Thread? " + Thread.currentThread().isVirtual());

            try {
                TimeUnit.SECONDS.sleep(1); // Simulate some work
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            System.out.println("Virtual Thread finished.");
        });

        System.out.println("\nMain thread waiting for the Virtual Thread to complete...");
        virtualThread.join(); // Wait for the virtual thread to finish its execution

        System.out.println("\nMain thread continues after Virtual Thread completion.");
    }
}
```

**Compilation and Execution:**
```bash
javac VirtualThreadBasic.java
java VirtualThreadBasic
```

**Expected Output:**
```
Main Thread ID: 1
Main Thread Is Virtual: false

Main thread waiting for the Virtual Thread to complete...

Hello from inside the Virtual Thread!
Virtual Thread Name: MyFirstVirtualThread
Virtual Thread ID: 21
Is Virtual Thread? true
Virtual Thread finished.

Main thread continues after Virtual Thread completion.
```
*(Note: Thread ID `21` is an example; it will vary.)*

### Example 2: Scalability Test (Platform vs. Virtual)

This example highlights the scalability difference by attempting to create a large number of threads.

**`ThreadScalability.java`**
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.CountDownLatch;
import java.time.Duration;
import java.time.Instant;

public class ThreadScalability {

    private static final int NUMBER_OF_TASKS = 50_000; // Try 10,000 to 100,000

    public static void runTasks(String type, ExecutorService executor) throws InterruptedException {
        System.out.println("\n--- Running " + NUMBER_OF_TASKS + " tasks with " + type + " threads ---");
        Instant start = Instant.now();
        CountDownLatch latch = new CountDownLatch(NUMBER_OF_TASKS);

        for (int i = 0; i < NUMBER_OF_TASKS; i++) {
            final int taskId = i;
            executor.submit(() -> {
                try {
                    // Simulate a blocking I/O operation
                    TimeUnit.MILLISECONDS.sleep(1);
                    if (taskId % 5000 == 0) {
                        // System.out.println(type + " thread task " + taskId + " complete.");
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    latch.countDown();
                }
            });
        }

        latch.await(); // Wait for all tasks to complete
        executor.shutdown();
        if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
            System.err.println("Executor did not terminate in time.");
        }
        Instant end = Instant.now();
        System.out.println(type + " threads: All tasks completed in " + Duration.between(start, end).toMillis() + " ms.");
    }

    public static void main(String[] args) throws InterruptedException {
        // --- Platform Threads ---
        // Using FixedThreadPool (simulates a typical thread pool)
        // With very large NUMBER_OF_TASKS, this might cause OOM or very slow execution
        // For demonstration, keep pool size reasonable, but note its limitations.
        try {
            ExecutorService platformExecutor = Executors.newFixedThreadPool(200); // Max 200 concurrent platform threads
            runTasks("Platform", platformExecutor);
        } catch (OutOfMemoryError e) {
            System.err.println("!!! OutOfMemoryError with Platform Threads !!! " + e.getMessage());
        } catch (Exception e) {
             System.err.println("!!! Error with Platform Threads !!! " + e.getMessage());
        }


        // --- Virtual Threads ---
        // newVirtualThreadPerTaskExecutor creates a new virtual thread for each task.
        // This is the ideal use case for Virtual Threads.
        try (ExecutorService virtualExecutor = Executors.newVirtualThreadPerTaskExecutor()) {
            runTasks("Virtual", virtualExecutor);
        } catch (Exception e) {
            System.err.println("!!! Error with Virtual Threads !!! " + e.getMessage());
        }
    }
}
```

**Compilation and Execution:**
```bash
javac ThreadScalability.java
java ThreadScalability
```

**Expected Output (Illustrative - actual times will vary):**

*For `NUMBER_OF_TASKS = 50_000`*

```
--- Running 50000 tasks with Platform threads ---
Platform threads: All tasks completed in 12345 ms.
```
*(You might observe slower times, or if `NUMBER_OF_TASKS` is too high (e.g., 100,000 with `newFixedThreadPool(1000)`), you might get `OutOfMemoryError` or very long execution times, or `RejectedExecutionException` if the queue is bounded.)*

```
--- Running 50000 tasks with Virtual threads ---
Virtual threads: All tasks completed in 2345 ms.
```
*(Notice the significant speedup and successful completion with Virtual Threads. The time taken is primarily governed by the total `sleep` duration and the number of available carrier threads, not the overhead of creating/managing threads themselves.)*

### Example 3: Handling Blocking Operations

This example demonstrates how Virtual Threads handle blocking operations efficiently, allowing a small number of carrier threads to serve many concurrent tasks.

**`VirtualThreadBlocking.java`**
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.CountDownLatch;
import java.time.Duration;
import java.time.Instant;

public class VirtualThreadBlocking {

    private static final int NUM_VIRTUAL_THREADS = 100; // Number of concurrent virtual threads
    private static final int BLOCKING_TIME_MS = 2000; // How long each thread blocks

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Starting application with " + NUM_VIRTUAL_THREADS + " virtual threads.");
        System.out.println("Each thread will simulate blocking for " + BLOCKING_TIME_MS + " ms.");

        Instant start = Instant.now();
        CountDownLatch latch = new CountDownLatch(NUM_VIRTUAL_THREADS);

        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < NUM_VIRTUAL_THREADS; i++) {
                final int taskId = i;
                executor.submit(() -> {
                    String threadName = Thread.currentThread().getName();
                    long threadId = Thread.currentThread().threadId();
                    System.out.println("Task " + taskId + " (VT: " + threadId + ", " + threadName + ") - Starting blocking operation.");
                    try {
                        // Simulate a blocking I/O call (e.g., network request, DB query)
                        TimeUnit.MILLISECONDS.sleep(BLOCKING_TIME_MS);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    System.out.println("Task " + taskId + " (VT: " + threadId + ", " + threadName + ") - Blocking operation finished.");
                    latch.countDown();
                });
            }
        } // ExecutorService is automatically shut down here

        latch.await(); // Wait for all virtual threads to complete
        Instant end = Instant.now();

        long totalDuration = Duration.between(start, end).toMillis();
        System.out.println("\nAll " + NUM_VIRTUAL_THREADS + " tasks completed in " + totalDuration + " ms.");

        // If this were platform threads, it would take NUM_VIRTUAL_THREADS * BLOCKING_TIME_MS
        // With virtual threads, it should be closer to BLOCKING_TIME_MS + a small overhead.
        System.out.println("Expected duration for a single blocking operation: " + BLOCKING_TIME_MS + " ms.");
    }
}
```

**Compilation and Execution:**
```bash
javac VirtualThreadBlocking.java
java VirtualThreadBlocking
```

**Expected Output (Illustrative - order might vary, but key takeaway is total time):**

```
Starting application with 100 virtual threads.
Each thread will simulate blocking for 2000 ms.
Task 0 (VT: 21, VirtualThread-2) - Starting blocking operation.
Task 1 (VT: 22, VirtualThread-3) - Starting blocking operation.
Task 2 (VT: 23, VirtualThread-4) - Starting blocking operation.
... (many "Starting blocking operation" lines will appear almost simultaneously)
Task 99 (VT: 120, VirtualThread-100) - Starting blocking operation.
... (after approx. 2 seconds) ...
Task 0 (VT: 21, VirtualThread-2) - Blocking operation finished.
Task 1 (VT: 22, VirtualThread-3) - Blocking operation finished.
... (many "Blocking operation finished" lines will appear almost simultaneously)
Task 99 (VT: 120, VirtualThread-100) - Blocking operation finished.

All 100 tasks completed in 20XX ms.
Expected duration for a single blocking operation: 2000 ms.
```
**Observation:** Despite `100` threads each "sleeping" for `2000ms`, the total execution time is only slightly more than `2000ms`. This demonstrates that when a virtual thread blocks, its underlying carrier thread is immediately freed to serve another waiting virtual thread. This is the core benefit for I/O-bound applications.

## 8. When to Use Virtual Threads

*   **I/O-Bound Applications:** Web servers, microservices, database clients, network proxies, message consumers (Kafka, RabbitMQ), file processing. If your application spends most of its time waiting for data from external systems, Virtual Threads are ideal.
*   **High Concurrency Requirements:** When you need to handle tens of thousands or millions of concurrent connections/requests.
*   **Simplifying Asynchronous Code:** If you're currently using complex callback hell or reactive streams just to avoid thread limits, Virtual Threads can allow you to revert to simpler, sequential code that blocks without performance penalty.
*   **Legacy Code Modernization:** Easily integrate into existing codebases without a complete architectural rewrite.

## 9. When NOT to Use Virtual Threads (Considerations)

While powerful, Virtual Threads are not a silver bullet:

*   **CPU-Bound Tasks:** For tasks that are primarily compute-intensive and spend most of their time crunching numbers, Virtual Threads offer no performance benefit over platform threads. The number of such tasks that can run concurrently is still limited by the number of CPU cores. Using too many virtual threads for CPU-bound tasks can even introduce slight scheduling overhead without gain.
*   **Synchronized Blocks and Native Methods (JNI):** When a virtual thread enters a `synchronized` block or executes a native method (JNI), the JVM cannot unmount it from its carrier thread. The carrier thread becomes "pinned" for the duration of the synchronized block or native call. If many virtual threads are frequently pinning carrier threads, it can negate some of the scalability benefits.
    *   **Mitigation for `synchronized`:** Consider using `ReentrantLock` or `StampedLock` which allow the JVM to unmount virtual threads while waiting for the lock.
*   **Thread Locals:** While Virtual Threads fully support `ThreadLocal`, `InheritableThreadLocal`, and `ScopedValue` (a new feature), using too many `ThreadLocal` variables with a very large number of virtual threads can lead to increased memory consumption (as each virtual thread would have its own copy).
*   **Unbounded CPU Usage:** If your application *creates* an excessive number of virtual threads that are *all* CPU-bound, it can lead to resource exhaustion. Virtual Threads simplify concurrency, but they don't magically give you more CPU cores.

## 10. Tooling and Debugging

Java's existing tooling has been updated to support Virtual Threads:

*   **`jstack`:** Shows virtual threads, identifying their carrier threads.
*   **Java Flight Recorder (JFR):** Provides events related to virtual thread lifecycle, pinning, and scheduling.
*   **Debuggers:** Integrated development environments (IDEs) like IntelliJ IDEA and Eclipse recognize and allow debugging of virtual threads, stepping through their code just like platform threads.
*   **`Thread.currentThread().isVirtual()`:** Programmatically check if the current thread is a virtual thread.

## 11. Conclusion

Virtual Threads are a transformative feature in Java 21, making highly concurrent and scalable applications significantly easier to write and maintain. By addressing the limitations of traditional threads for I/O-bound workloads, they allow developers to leverage the familiar imperative programming style without sacrificing performance or resource efficiency. For most modern server applications that spend a lot of time waiting for I/O, Virtual Threads are a game-changer, simplifying code, boosting throughput, and unlocking new levels of scalability.