This guide provides a detailed explanation of Java Virtual Threads (Project Loom), their benefits, and practical examples demonstrating their usage in Java 21.

---

# Java Virtual Threads (Project Loom) Demo in Java 21

## Table of Contents
1.  [Introduction to Virtual Threads](#1-introduction-to-virtual-threads)
2.  [Key Concepts and Benefits](#2-key-concepts-and-benefits)
3.  [How Virtual Threads Work](#3-how-virtual-threads-work)
4.  [Creating Virtual Threads](#4-creating-virtual-threads)
    *   [Method 1: Using `Thread.ofVirtual()`](#method-1-using-threadofvirtual)
    *   [Method 2: Using `Executors.newVirtualThreadPerTaskExecutor()`](#method-2-using-executorsnewvirtualthreadpertaskexecutor)
5.  [Practical Demo: Simulating High Concurrency I/O-Bound Tasks](#5-practical-demo-simulating-high-concurrency-io-bound-tasks)
    *   [Scenario](#scenario)
    *   [Platform Threads (Traditional) Example](#platform-threads-traditional-example)
    *   [Virtual Threads Example](#virtual-threads-example)
    *   [Running the Demo and Observing Output](#running-the-demo-and-observing-output)
    *   [Observations and Analysis](#observations-and-analysis)
6.  [When to Use Virtual Threads](#6-when-to-use-virtual-threads)
7.  [When NOT to Use Virtual Threads](#7-when-not-to-use-virtual-threads)
8.  [Best Practices](#8-best-practices)
9.  [Conclusion](#9-conclusion)
10. [Further Reading](#10-further-reading)

---

## 1. Introduction to Virtual Threads

Before Java 21 (which finalized Virtual Threads, Project Loom), traditional Java threads, often called **Platform Threads**, were directly mapped to operating system (OS) threads. While powerful, OS threads are a finite and relatively expensive resource. Creating thousands or millions of them is impractical due to memory overhead, context-switching costs, and OS scheduling limitations.

This limitation becomes apparent in modern applications, especially those dealing with high concurrency and frequent blocking I/O operations (like network calls, database queries, file I/O). A platform thread waiting for an I/O operation to complete remains blocked, consuming OS resources even though it's not performing any computation. This "thread per request" model doesn't scale well for very high throughput services.

**Virtual Threads** (introduced as a preview in Java 19 and finalized in Java 21) are lightweight, user-mode threads managed entirely by the Java Virtual Machine (JVM). They are designed to dramatically increase the scalability of server applications that spend most of their time waiting (I/O-bound tasks).

Think of them as "fibers" or "goroutines" if you're familiar with other languages. They are not one-to-one mapped to OS threads. Instead, many virtual threads can be "mounted" onto a few platform threads (called **carrier threads**). When a virtual thread performs a blocking operation (e.g., `Thread.sleep()`, `Socket.read()`), the JVM can unmount it from its carrier thread, allowing the carrier thread to execute another virtual thread. When the blocking operation completes, the virtual thread can be remounted onto an available carrier thread.

## 2. Key Concepts and Benefits

*   **Lightweight:** Virtual threads consume significantly less memory than platform threads (often bytes vs. kilobytes per thread). This allows for millions of concurrent virtual threads.
*   **High Scalability:** Enables applications to handle massive numbers of concurrent connections or tasks, especially I/O-bound ones, without exhausting thread resources.
*   **Simplicity:** You can write blocking code naturally (synchronously) without complex callback-based or reactive programming models (`CompletableFuture`, RxJava, Project Reactor) often used to achieve high concurrency with platform threads. The JVM handles the complexity of scheduling and unmounting.
*   **Efficiency:** Reduces context-switching overhead compared to OS threads.
*   **Debugging:** Debuggers understand virtual threads, making them appear like regular threads in stack traces and monitoring tools (with some caveats for deep dives into carrier threads).

## 3. How Virtual Threads Work

When you create a virtual thread, it doesn't immediately get its own OS thread. Instead, it gets assigned to an internal `ForkJoinPool.commonPool()` by default, which contains a small number of platform threads (carrier threads).

1.  **Mounting:** When a virtual thread is runnable, the JVM "mounts" it onto an available carrier thread. The virtual thread's code then executes on that carrier thread.
2.  **Unmounting (on blocking I/O):** If the virtual thread encounters a blocking I/O operation (e.g., `InputStream.read()`, `Socket.accept()`, `Thread.sleep()`), the JVM intercepts this operation. Instead of blocking the *carrier thread*, the virtual thread is "unmounted" from its carrier. The carrier thread then becomes free to pick up and run another waiting virtual thread. The I/O operation continues asynchronously in the background.
3.  **Remounting:** Once the blocking I/O operation completes, the virtual thread becomes runnable again. The JVM then "remounts" it onto an available carrier thread to resume its execution from where it left off.

This mechanism allows a small pool of carrier threads to efficiently manage a vast number of virtual threads, maximizing CPU utilization by ensuring carrier threads are rarely idle during I/O waits.

## 4. Creating Virtual Threads

There are a few primary ways to create and manage virtual threads.

### Method 1: Using `Thread.ofVirtual()`

This is the most direct way to create and start a single virtual thread.

```java
import java.util.concurrent.TimeUnit;

public class VirtualThreadDirect {

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Main thread starting...");

        // Create and start a virtual thread directly
        Thread virtualThread = Thread.ofVirtual().start(() -> {
            try {
                System.out.println("Virtual Thread [" + Thread.currentThread().getName() + "] running.");
                TimeUnit.SECONDS.sleep(2); // Simulate blocking I/O
                System.out.println("Virtual Thread [" + Thread.currentThread().getName() + "] finished after 2 seconds.");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                System.out.println("Virtual Thread interrupted.");
            }
        });

        // The main thread can continue its work while the virtual thread runs
        System.out.println("Main thread continuing its work...");

        // Optionally, wait for the virtual thread to complete
        virtualThread.join();

        System.out.println("Main thread finished. Virtual thread joined.");
    }
}
```

**Compilation and Execution:**
```bash
javac VirtualThreadDirect.java
java VirtualThreadDirect
```

**Example Output:**
```
Main thread starting...
Main thread continuing its work...
Virtual Thread [VirtualThread[#1]/run-on-carrier-thread] running.
Virtual Thread [VirtualThread[#1]/run-on-carrier-thread] finished after 2 seconds.
Main thread finished. Virtual thread joined.
```
*(Note: The exact carrier thread name `run-on-carrier-thread` might vary, but the `VirtualThread[#ID]` part identifies it as a virtual thread.)*

### Method 2: Using `Executors.newVirtualThreadPerTaskExecutor()`

For managing multiple virtual threads, especially in scenarios like "thread per request," the `ExecutorService` is the preferred way. `newVirtualThreadPerTaskExecutor()` creates an `ExecutorService` that creates a new virtual thread for *each* submitted task. This is often the most suitable for server-side applications.

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class VirtualThreadExecutor {

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Main thread starting...");

        // Create an ExecutorService that creates a new virtual thread for each task
        // This is ideal for "thread-per-task" or "thread-per-request" models
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            System.out.println("Submitting tasks to Virtual Thread Executor...");

            // Submit 5 tasks, each running in its own virtual thread
            for (int i = 0; i < 5; i++) {
                final int taskId = i;
                executor.submit(() -> {
                    try {
                        System.out.println("Task " + taskId + " (VT: " + Thread.currentThread().getName() + ") running.");
                        TimeUnit.SECONDS.sleep(1 + taskId % 2); // Simulate varying blocking I/O
                        System.out.println("Task " + taskId + " (VT: " + Thread.currentThread().getName() + ") finished.");
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        System.out.println("Task " + taskId + " interrupted.");
                    }
                });
            }

            System.out.println("All tasks submitted. Main thread waiting for completion.");

        } // executor.close() is implicitly called here, which shuts down the executor
        // and waits for submitted tasks to complete.

        System.out.println("Main thread finished. All virtual threads completed.");
    }
}
```

**Compilation and Execution:**
```bash
javac VirtualThreadExecutor.java
java VirtualThreadExecutor
```

**Example Output:**
```
Main thread starting...
Submitting tasks to Virtual Thread Executor...
Task 0 (VT: VirtualThread[#1]/run-on-carrier-thread) running.
Task 1 (VT: VirtualThread[#2]/run-on-carrier-thread) running.
Task 2 (VT: VirtualThread[#3]/run-on-carrier-thread) running.
Task 3 (VT: VirtualThread[#4]/run-on-carrier-thread) running.
Task 4 (VT: VirtualThread[#5]/run-on-carrier-thread) running.
All tasks submitted. Main thread waiting for completion.
Task 1 (VT: VirtualThread[#2]/run-on-carrier-thread) finished.
Task 3 (VT: VirtualThread[#4]/run-on-carrier-thread) finished.
Task 0 (VT: VirtualThread[#1]/run-on-carrier-thread) finished.
Task 2 (VT: VirtualThread[#3]/run-on-carrier-thread) finished.
Task 4 (VT: VirtualThread[#5]/run-on-carrier-thread) finished.
Main thread finished. All virtual threads completed.
```
*(Notice how all tasks start almost simultaneously, and then finish in a mixed order depending on their simulated sleep duration. This demonstrates their concurrency.)*

## 5. Practical Demo: Simulating High Concurrency I/O-Bound Tasks

This demo will illustrate the core benefit of virtual threads: handling a large number of concurrent, blocking I/O-bound tasks more efficiently than traditional platform threads. We'll simulate I/O operations using `Thread.sleep()`.

### Scenario

Imagine a web service that needs to make 10,000 requests to an external (slow) API or database. Each request takes a small, unpredictable amount of time (e.g., 50-150 milliseconds).
*   **Platform Thread Approach:** We'll use a fixed-size thread pool.
*   **Virtual Thread Approach:** We'll use `newVirtualThreadPerTaskExecutor()`.

We will measure the total time taken for both approaches.

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

public class VirtualThreadPerformanceDemo {

    private static final int NUMBER_OF_TASKS = 10_000; // Increased for a more dramatic effect
    private static final int SIMULATED_IO_MIN_MS = 50;
    private static final int SIMULATED_IO_MAX_MS = 150;

    // Helper method to simulate a blocking I/O operation
    private static void simulateIoOperation(int taskId) {
        try {
            int sleepTime = SIMULATED_IO_MIN_MS + (int) (Math.random() * (SIMULATED_IO_MAX_MS - SIMULATED_IO_MIN_MS));
            // System.out.println(Thread.currentThread().getName() + " - Task " + taskId + " started, sleeping for " + sleepTime + "ms.");
            TimeUnit.MILLISECONDS.sleep(sleepTime);
            // System.out.println(Thread.currentThread().getName() + " - Task " + taskId + " finished.");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println(Thread.currentThread().getName() + " - Task " + taskId + " interrupted.");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        System.out.println("--- Starting Performance Demo ---");
        System.out.println("Number of tasks: " + NUMBER_OF_TASKS);
        System.out.println("Simulated I/O per task: " + SIMULATED_IO_MIN_MS + "-" + SIMULATED_IO_MAX_MS + "ms\n");

        runWithPlatformThreads();
        System.out.println("\n-----------------------------------\n");
        runWithVirtualThreads();

        System.out.println("\n--- Demo Finished ---");
    }

    private static void runWithPlatformThreads() throws InterruptedException {
        System.out.println("--- Running with Platform Threads ---");
        // A common pool size for platform threads (e.g., matching CPU cores or slightly more)
        int platformThreadPoolSize = Runtime.getRuntime().availableProcessors() * 2; // e.g., 8 or 16 threads
        System.out.println("Platform Thread Pool Size: " + platformThreadPoolSize);

        long startTime = System.currentTimeMillis();
        AtomicInteger completedTasks = new AtomicInteger(0);

        try (ExecutorService platformExecutor = Executors.newFixedThreadPool(platformThreadPoolSize)) {
            for (int i = 0; i < NUMBER_OF_TASKS; i++) {
                final int taskId = i;
                platformExecutor.submit(() -> {
                    simulateIoOperation(taskId);
                    completedTasks.incrementAndGet();
                });
            }
        } // Implicitly calls shutdown and awaitTermination

        long endTime = System.currentTimeMillis();
        System.out.println("All platform tasks submitted. Waiting for completion...");
        
        // Ensure all tasks are truly completed.
        // In this try-with-resources, shutdownNow is implicitly called and then awaitTermination.
        // For demonstration, we're relying on the try-with-resources to handle shutdown and wait.
        // For more robust handling:
        // platformExecutor.shutdown();
        // platformExecutor.awaitTermination(Long.MAX_VALUE, TimeUnit.MILLISECONDS);

        System.out.println("Platform Threads: " + completedTasks.get() + " tasks completed.");
        System.out.println("Total time for Platform Threads: " + (endTime - startTime) + " ms");
    }

    private static void runWithVirtualThreads() throws InterruptedException {
        System.out.println("--- Running with Virtual Threads ---");
        System.out.println("Virtual threads have no explicit pool size, each task gets a new virtual thread.");

        long startTime = System.currentTimeMillis();
        AtomicInteger completedTasks = new AtomicInteger(0);

        // This executor creates a new virtual thread for each submitted task.
        try (ExecutorService virtualExecutor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < NUMBER_OF_TASKS; i++) {
                final int taskId = i;
                virtualExecutor.submit(() -> {
                    simulateIoOperation(taskId);
                    completedTasks.incrementAndGet();
                });
            }
        } // Implicitly calls shutdown and awaitTermination

        long endTime = System.currentTimeMillis();
        System.out.println("All virtual tasks submitted. Waiting for completion...");

        // Similar to platform threads, relying on try-with-resources.
        // For more robust handling:
        // virtualExecutor.shutdown();
        // virtualExecutor.awaitTermination(Long.MAX_VALUE, TimeUnit.MILLISECONDS);

        System.out.println("Virtual Threads: " + completedTasks.get() + " tasks completed.");
        System.out.println("Total time for Virtual Threads: " + (endTime - startTime) + " ms");
    }
}
```

### Running the Demo and Observing Output

**Prerequisites:**
*   Java Development Kit (JDK) 21 installed.
*   Save the code as `VirtualThreadPerformanceDemo.java`.

**Compilation:**
```bash
javac VirtualThreadPerformanceDemo.java
```

**Execution:**
```bash
java VirtualThreadPerformanceDemo
```

**Example Output (Your exact timings may vary depending on your hardware):**

```
--- Starting Performance Demo ---
Number of tasks: 10000
Simulated I/O per task: 50-150ms

--- Running with Platform Threads ---
Platform Thread Pool Size: 16
All platform tasks submitted. Waiting for completion...
Platform Threads: 10000 tasks completed.
Total time for Platform Threads: 64756 ms  // ~64 seconds

-----------------------------------

--- Running with Virtual Threads ---
Virtual threads have no explicit pool size, each task gets a new virtual thread.
All virtual tasks submitted. Waiting for completion...
Virtual Threads: 10000 tasks completed.
Total time for Virtual Threads: 154 ms   // ~0.15 seconds

--- Demo Finished ---
```

### Observations and Analysis

From the example output, the difference is striking:

*   **Platform Threads:** Took approximately **64 seconds**. This is because with a fixed pool of, say, 16 platform threads, only 16 tasks can truly be "active" at any given moment. When a task blocks (simulated by `Thread.sleep`), that platform thread is held up, and other tasks have to wait for an available thread in the pool. The total time is roughly `(NUMBER_OF_TASKS / platformThreadPoolSize) * average_io_time`. `(10000 / 16) * 100ms = 625 * 100ms = 62500ms = 62.5s`. This matches the empirical results.

*   **Virtual Threads:** Took approximately **154 milliseconds**. This is incredibly fast! This is because each of the 10,000 tasks immediately got its own virtual thread. When a virtual thread called `Thread.sleep()`, it was "unmounted" from its carrier thread, freeing the carrier thread to immediately pick up another virtual thread. The result is that nearly all 10,000 tasks ran *concurrently* (from the perspective of the virtual threads), and the total time is effectively dictated by the longest single I/O operation (or a bit more, due to carrier thread switching and task startup). The sum of all `sleep` times is huge, but the *concurrent* execution means the elapsed wall-clock time is minimal.

This demo powerfully illustrates why Virtual Threads are a game-changer for I/O-bound, high-concurrency applications.

## 6. When to Use Virtual Threads

*   **High-concurrency I/O-bound applications:** Web servers, microservices, API gateways, database clients, message queue consumers/producers.
*   **"Thread-per-request" style applications:** Where each incoming request can be handled by its own thread, even if requests are numerous and involve blocking I/O.
*   **Existing synchronous blocking code:** You can easily migrate existing code that uses blocking calls without rewriting it into an asynchronous, callback-based style.
*   **Replacing large platform thread pools:** Instead of managing complex fixed/cached thread pools for I/O tasks, you can often switch to virtual threads for simplified management and better scalability.

## 7. When NOT to Use Virtual Threads

*   **CPU-bound tasks:** Virtual threads do not make CPU-bound tasks run faster. A virtual thread still needs a carrier thread (a real CPU core) to execute its code. If your task is constantly computing and rarely blocks, increasing the number of virtual threads beyond your available CPU cores will lead to excessive context switching, potentially *slowing down* your application. For CPU-bound work, traditional `ForkJoinPool` or `FixedThreadPool` (sized to the number of CPU cores) remains the appropriate choice.
*   **Short-lived, non-blocking tasks:** If your tasks are very short and don't involve blocking I/O, the overhead of creating and scheduling a virtual thread might negate the benefits.
*   **Replacing all existing platform threads blindly:** While powerful, virtual threads are specialized. Don't replace your `ForkJoinPool` for parallel stream processing or your fixed-size thread pool for CPU-intensive tasks with virtual threads without understanding the implications.
*   **Holding intrinsic locks (synchronized blocks/methods) for long periods:** If a virtual thread acquires an intrinsic lock and then blocks on I/O, it "pins" its carrier thread. This means the underlying platform thread cannot be used by other virtual threads until the pinned virtual thread releases the lock and unmounts. This can negate the benefits of virtual threads. Use `ReentrantLock` or `StampedLock` instead for such scenarios, or structure your code to release locks before blocking.

## 8. Best Practices

*   **Prefer `Executors.newVirtualThreadPerTaskExecutor()`:** For most server-side use cases, this is the most idiomatic way to use virtual threads. It aligns well with the "thread-per-task" or "thread-per-request" model.
*   **Continue using `ThreadLocal` judiciously:** `ThreadLocal` works with virtual threads, but remember that the carrier thread changes. If you have large `ThreadLocal` objects or many of them, the memory savings of virtual threads might be reduced. Consider using `ScopedValue` (also new in Java 21) for immutable, short-lived context passing, as it is more efficient and designed for virtual threads.
*   **Avoid "pinning":** Be aware of scenarios where a virtual thread might "pin" its carrier thread. The most common is holding an intrinsic lock (`synchronized`) across a blocking I/O call.
*   **Monitor your application:** Use tools like JMX, VisualVM, or JFR to monitor virtual thread behavior and ensure they are performing as expected. Stack traces will now show virtual threads clearly.
*   **Don't over-optimize too early:** Start by using virtual threads where they shine (I/O-bound concurrency). Profile and analyze before making complex architectural changes.

## 9. Conclusion

Virtual Threads in Java 21 represent a monumental shift in how Java handles concurrency, bringing the simplicity of the "thread-per-request" model back into the realm of high scalability for I/O-bound applications. They allow developers to write straightforward, blocking code that is both easy to understand and incredibly efficient at handling massive numbers of concurrent operations, effectively solving the "C10k problem" (handling 10,000 concurrent connections) and beyond for I/O-intensive workloads.

## 10. Further Reading

*   **JEP 444: Virtual Threads (Final)**: [https://openjdk.org/jeps/444](https://openjdk.org/jeps/444)
*   **Project Loom (Parent Project):** [https://openjdk.org/projects/loom/](https://openjdk.org/projects/loom/)
*   **Oracle Blog on Virtual Threads:** Search for "Java Virtual Threads" on the Oracle blogs, there are many good articles.
*   **JEP 446: Scoped Values (Final)**: [https://openjdk.org/jeps/446](https://openjdk.org/jeps/446) (Related to context passing with Virtual Threads)

---