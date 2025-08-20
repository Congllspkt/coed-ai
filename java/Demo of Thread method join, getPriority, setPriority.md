This document provides a detailed explanation and practical examples of the `join()`, `getPriority()`, and `setPriority()` methods of the `java.lang.Thread` class.

---

# Java Thread Methods: `join()`, `getPriority()`, `setPriority()`

In Java, threads are fundamental for achieving concurrency, allowing multiple parts of your program to execute independently. The `java.lang.Thread` class provides several methods to manage and interact with threads. This guide focuses on three key methods: `join()`, `getPriority()`, and `setPriority()`.

## 1. `thread.join()` Method

### Purpose
The `join()` method is used to ensure that a thread completes its execution before another thread (typically the calling thread) begins or continues its execution. When `thread.join()` is called, the calling thread (the one that invoked `join()`) will pause its execution until `thread` (the thread on which `join()` was called) dies (finishes its `run()` method) or until the specified timeout occurs.

### Syntax
There are three overloaded versions of the `join()` method:

1.  `public final void join() throws InterruptedException`: Waits indefinitely for the thread to die.
2.  `public final synchronized void join(long millis) throws InterruptedException`: Waits at most `millis` milliseconds for the thread to die. A timeout of `0` means to wait indefinitely.
3.  `public final synchronized void join(long millis, int nanos) throws InterruptedException`: Waits at most `millis` milliseconds plus `nanos` nanoseconds for the thread to die.

### How it Works
When `join()` is called on a `Thread` object, the current thread (the one executing the `join()` call) enters a waiting state. It will only resume execution when:
*   The target thread (the one `join()` was called upon) finishes its `run()` method and terminates.
*   The specified timeout (if any) expires.
*   The current thread (the one waiting) is interrupted. In this case, an `InterruptedException` is thrown.

**Analogy:** Imagine you're waiting for a friend to finish their work before you can go out. Calling `friend.join()` means you'll stand by and wait until they're done.

### Common Use Cases
*   **Dependency Management:** When one thread's work depends on the completion of another thread. For instance, a main thread might start several worker threads, and then need to `join()` them all to collect results before processing them further.
*   **Ordered Execution:** To enforce a specific order of execution for concurrent tasks (though `join()` implies a blocking dependency, which might not always be the most efficient for pure ordering).

### Important Notes
*   **`InterruptedException`**: Since `join()` blocks the calling thread, it can be interrupted while waiting. You **must** handle `InterruptedException` by either catching it or declaring it in the method signature.
*   **Blocks Caller**: Be aware that `join()` will block the thread that calls it. This can lead to performance issues if used indiscriminately or if the joined thread takes a very long time.

### Example: `join()`

This example demonstrates how `join()` ensures the "Main Thread" waits for the "Worker Thread" to finish its task.

```java
// WorkerThread.java
class WorkerThread extends Thread {
    private String name;

    public WorkerThread(String name) {
        this.name = name;
    }

    @Override
    public void run() {
        System.out.println(name + " started.");
        try {
            // Simulate doing some work
            for (int i = 1; i <= 3; i++) {
                System.out.println(name + " is working... Step " + i);
                Thread.sleep(500); // Sleep for 0.5 seconds
            }
        } catch (InterruptedException e) {
            System.out.println(name + " was interrupted while working.");
            Thread.currentThread().interrupt(); // Restore the interrupted status
        }
        System.out.println(name + " finished.");
    }
}

// JoinDemo.java
public class JoinDemo {
    public static void main(String[] args) {
        System.out.println("Main Thread started.");

        WorkerThread thread1 = new WorkerThread("Worker-1");
        WorkerThread thread2 = new WorkerThread("Worker-2");

        // Start the threads
        thread1.start();
        thread2.start();

        try {
            System.out.println("Main Thread is waiting for Worker-1 to finish...");
            thread1.join(); // Main thread waits for thread1 to complete

            System.out.println("Main Thread is waiting for Worker-2 to finish...");
            thread2.join(2000); // Main thread waits for thread2, with a 2-second timeout

            System.out.println("All worker threads have finished (or timed out).");

        } catch (InterruptedException e) {
            System.out.println("Main Thread was interrupted while waiting.");
            Thread.currentThread().interrupt();
        }

        System.out.println("Main Thread finished its execution.");
    }
}
```

**To Compile and Run:**

1.  Save the first code block as `WorkerThread.java`.
2.  Save the second code block as `JoinDemo.java`.
3.  Open a terminal or command prompt in the directory where you saved the files.
4.  Compile: `javac WorkerThread.java JoinDemo.java`
5.  Run: `java JoinDemo`

**Expected Output (Actual output may vary slightly due to thread scheduling, but the `join()` effect will be clear):**

```
Main Thread started.
Worker-1 started.
Worker-2 started.
Worker-1 is working... Step 1
Main Thread is waiting for Worker-1 to finish...
Worker-2 is working... Step 1
Worker-1 is working... Step 2
Worker-2 is working... Step 2
Worker-1 is working... Step 3
Worker-2 is working... Step 3
Worker-1 finished.
Main Thread is waiting for Worker-2 to finish...
Worker-2 finished.
All worker threads have finished (or timed out).
Main Thread finished its execution.
```

**Observation:** Notice that "Main Thread finished its execution." is printed only *after* both "Worker-1 finished." and "Worker-2 finished." messages appear, demonstrating the blocking nature of `join()`. If `thread1.join()` and `thread2.join()` were removed, "Main Thread finished its execution." would likely print immediately after starting the worker threads.

## 2. `thread.getPriority()` Method

### Purpose
The `getPriority()` method returns the priority of a thread. Thread priorities are integer values ranging from `Thread.MIN_PRIORITY` (1) to `Thread.MAX_PRIORITY` (10). The default priority for a new thread is `Thread.NORM_PRIORITY` (5).

### Syntax
`public final int getPriority()`

### How it Works
This method simply returns the integer value representing the thread's current priority setting. It does not affect the thread's execution; it only provides information.

### Use Cases
*   **Debugging/Monitoring:** To inspect the priority settings of threads in your application.
*   **Verification:** To ensure that thread priorities have been set as expected.

### Important Notes
*   **Hint to Scheduler:** Thread priorities are primarily **hints** to the operating system's thread scheduler. They do not guarantee that a higher-priority thread will always execute before a lower-priority one, or that it will get more CPU time. The actual behavior depends on the underlying operating system and JVM implementation.
*   **Platform-Dependent:** How priorities are mapped to native thread priorities can vary significantly between different operating systems.

### Example: `getPriority()`

```java
// PriorityDemo.java
public class PriorityDemo extends Thread {

    public PriorityDemo(String name) {
        super(name);
    }

    @Override
    public void run() {
        System.out.println("Thread '" + Thread.currentThread().getName() + "' is running with priority: " + Thread.currentThread().getPriority());
    }

    public static void main(String[] args) {
        System.out.println("Main thread priority: " + Thread.currentThread().getPriority());

        // Create threads with default priority
        PriorityDemo defaultThread1 = new PriorityDemo("DefaultThread-1");
        PriorityDemo defaultThread2 = new PriorityDemo("DefaultThread-2");

        System.out.println("Before start - DefaultThread-1 priority: " + defaultThread1.getPriority());
        System.out.println("Before start - DefaultThread-2 priority: " + defaultThread2.getPriority());

        defaultThread1.start();
        defaultThread2.start();

        try {
            // Give a little time for default threads to print their info
            Thread.sleep(100); 
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        System.out.println("\nAfter start - DefaultThread-1 priority: " + defaultThread1.getPriority());
        System.out.println("After start - DefaultThread-2 priority: " + defaultThread2.getPriority());

        // Demonstrate setting and then getting priority
        PriorityDemo highPriorityThread = new PriorityDemo("HighPriorityThread");
        highPriorityThread.setPriority(Thread.MAX_PRIORITY); // Set to 10
        System.out.println("\nBefore start - HighPriorityThread priority: " + highPriorityThread.getPriority());
        highPriorityThread.start();

        PriorityDemo lowPriorityThread = new PriorityDemo("LowPriorityThread");
        lowPriorityThread.setPriority(Thread.MIN_PRIORITY); // Set to 1
        System.out.println("Before start - LowPriorityThread priority: " + lowPriorityThread.getPriority());
        lowPriorityThread.start();

        try {
            // Give a little time for new threads to print their info
            Thread.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        System.out.println("\nAfter start - HighPriorityThread priority: " + highPriorityThread.getPriority());
        System.out.println("After start - LowPriorityThread priority: " + lowPriorityThread.getPriority());
    }
}
```

**To Compile and Run:**

1.  Save the code block as `PriorityDemo.java`.
2.  Compile: `javac PriorityDemo.java`
3.  Run: `java PriorityDemo`

**Expected Output (Exact order of `Thread is running...` lines may vary, but priority values will be correct):**

```
Main thread priority: 5
Before start - DefaultThread-1 priority: 5
Before start - DefaultThread-2 priority: 5
Thread 'DefaultThread-1' is running with priority: 5
Thread 'DefaultThread-2' is running with priority: 5

After start - DefaultThread-1 priority: 5
After start - DefaultThread-2 priority: 5

Before start - HighPriorityThread priority: 10
Before start - LowPriorityThread priority: 1
Thread 'HighPriorityThread' is running with priority: 10
Thread 'LowPriorityThread' is running with priority: 1

After start - HighPriorityThread priority: 10
After start - LowPriorityThread priority: 1
```

## 3. `thread.setPriority()` Method

### Purpose
The `setPriority()` method allows you to change the priority of a thread. This can influence the operating system's thread scheduler in determining which thread gets CPU time.

### Syntax
`public final void setPriority(int newPriority)`

### Parameters
*   `newPriority`: An integer value representing the desired priority. Must be between `Thread.MIN_PRIORITY` (1) and `Thread.MAX_PRIORITY` (10).

### Throws
*   `IllegalArgumentException`: If `newPriority` is outside the valid range (1-10).

### How it Works
When `setPriority()` is called, the JVM attempts to map the given Java thread priority to an appropriate native thread priority, and then informs the underlying operating system's scheduler about this change. The scheduler *may* use this information to prioritize the thread's access to CPU time.

### Use Cases
*   **Optimizing Performance:** Assigning higher priority to critical, time-sensitive tasks and lower priority to background, non-essential tasks.
*   **Resource Management:** Attempting to ensure that important threads receive more CPU cycles than less important ones.

### Important Notes
*   **No Guarantee:** As mentioned with `getPriority()`, setting a priority is a **hint**, not a command. There is no guarantee that a higher-priority thread will run before a lower-priority one, or get more execution time. Actual behavior is highly dependent on the OS and JVM.
*   **Starvation Risk:** Setting very high priorities for certain threads can potentially lead to "starvation" for lower-priority threads, where the lower-priority threads might never get a chance to run if the higher-priority threads are always runnable.
*   **Avoid Over-reliance:** Do not use thread priorities as a primary mechanism for synchronization or ensuring correctness. For robust thread coordination, use proper synchronization primitives like `synchronized` blocks, `wait()`, `notify()`, `Lock` objects, `Semaphore`, `CountDownLatch`, etc.

### Example: `setPriority()`

This example demonstrates setting different priorities and observes their (non-guaranteed) effect.

```java
// PriorityWorker.java
class PriorityWorker extends Thread {
    private int loopCount;

    public PriorityWorker(String name, int loopCount) {
        super(name);
        this.loopCount = loopCount;
    }

    @Override
    public void run() {
        System.out.println(getName() + " started with priority: " + getPriority());
        for (int i = 0; i < loopCount; i++) {
            System.out.println(getName() + ": " + i);
            // Thread.yield() is another hint to the scheduler to allow other threads to run
            // It doesn't guarantee a context switch but makes it more likely.
            Thread.yield(); 
        }
        System.out.println(getName() + " finished.");
    }
}

// SetPriorityDemo.java
public class SetPriorityDemo {
    public static void main(String[] args) {
        System.out.println("Main thread priority: " + Thread.currentThread().getPriority());

        // Create a low priority thread
        PriorityWorker lowPriorityThread = new PriorityWorker("LowPriorityWorker", 20);
        lowPriorityThread.setPriority(Thread.MIN_PRIORITY); // Priority 1

        // Create a high priority thread
        PriorityWorker highPriorityThread = new PriorityWorker("HighPriorityWorker", 20);
        highPriorityThread.setPriority(Thread.MAX_PRIORITY); // Priority 10

        System.out.println("\nStarting threads with different priorities...");

        // Start them (order of starting might influence initial scheduling)
        lowPriorityThread.start();
        highPriorityThread.start();

        // Introduce a slight delay for threads to run
        try {
            Thread.sleep(100); 
            // Wait for both threads to finish to see the complete output
            lowPriorityThread.join();
            highPriorityThread.join();
        } catch (InterruptedException e) {
            System.out.println("Main thread interrupted.");
            Thread.currentThread().interrupt();
        }

        System.out.println("\nDemonstration complete.");
        System.out.println("LowPriorityWorker final priority: " + lowPriorityThread.getPriority());
        System.out.println("HighPriorityWorker final priority: " + highPriorityThread.getPriority());

        // Example of setting an invalid priority (will throw IllegalArgumentException)
        try {
            PriorityWorker invalidPriorityThread = new PriorityWorker("InvalidPriorityWorker", 1);
            invalidPriorityThread.setPriority(0); // Invalid priority
            invalidPriorityThread.start();
        } catch (IllegalArgumentException e) {
            System.err.println("\nCaught expected exception: " + e.getMessage());
        }
    }
}
```

**To Compile and Run:**

1.  Save the first code block as `PriorityWorker.java`.
2.  Save the second code block as `SetPriorityDemo.java`.
3.  Open a terminal or command prompt in the directory where you saved the files.
4.  Compile: `javac PriorityWorker.java SetPriorityDemo.java`
5.  Run: `java SetPriorityDemo`

**Expected Output (Note: The exact interleaved order of "LowPriorityWorker" and "HighPriorityWorker" messages *will vary* significantly between runs and systems. The key is that the priorities are set as requested, and the `IllegalArgumentException` is caught.)**

```
Main thread priority: 5

Starting threads with different priorities...
LowPriorityWorker started with priority: 1
HighPriorityWorker started with priority: 10
HighPriorityWorker: 0
HighPriorityWorker: 1
LowPriorityWorker: 0
HighPriorityWorker: 2
LowPriorityWorker: 1
HighPriorityWorker: 3
HighPriorityWorker: 4
LowPriorityWorker: 2
... (many interleaved lines, actual distribution depends on scheduler) ...
HighPriorityWorker: 19
HighPriorityWorker finished.
LowPriorityWorker: 19
LowPriorityWorker finished.

Demonstration complete.
LowPriorityWorker final priority: 1
HighPriorityWorker final priority: 10

Caught expected exception: Priority out of range
```

**Observation:** While the output shows both threads running, on some systems, you might observe the "HighPriorityWorker" printing more messages consecutively before "LowPriorityWorker" gets a turn, especially initially. However, due to the `Thread.yield()` and the non-deterministic nature of thread scheduling, don't expect a perfectly clean "high runs entirely, then low runs entirely" behavior. The `IllegalArgumentException` for an invalid priority is reliably caught.

---

This concludes the detailed demonstration of `join()`, `getPriority()`, and `setPriority()` methods in Java Threads. Remember to use these methods judiciously, especially `setPriority()`, as their effects are not always guaranteed and can lead to complex debugging challenges if misunderstood.