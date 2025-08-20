# Demo of Synchronized Methods and Blocks in Java

## Table of Contents
1.  [Introduction to Synchronization](#1-introduction-to-synchronization)
2.  [Understanding Intrinsic Locks (Monitors)](#2-understanding-intrinsic-locks-monitors)
3.  [Synchronized Methods](#3-synchronized-methods)
    *   [Mechanism](#mechanism)
    *   [Example: Race Condition vs. Synchronized Method](#example-race-condition-vs-synchronized-method)
4.  [Synchronized Blocks](#4-synchronized-blocks)
    *   [Mechanism](#mechanism-1)
    *   [Example: Fine-Grained Synchronization with Synchronized Blocks](#example-fine-grained-synchronization-with-synchronized-blocks)
5.  [Key Differences and Use Cases](#5-key-differences-and-use-cases)
6.  [Important Considerations and Best Practices](#6-important-considerations-and-best-practices)
7.  [Conclusion](#7-conclusion)

---

## 1. Introduction to Synchronization

In multi-threaded programming, multiple threads can access and modify shared resources concurrently. This concurrent access can lead to **data inconsistency** and **race conditions**, where the final outcome depends on the unpredictable timing and interleaving of thread execution.

Java provides the `synchronized` keyword as a fundamental mechanism to achieve **thread safety** and ensure **mutual exclusion**. It allows only one thread at a time to execute a specific block of code or a method on a given object, thereby preventing race conditions and maintaining data integrity.

## 2. Understanding Intrinsic Locks (Monitors)

Every object in Java has an associated **intrinsic lock** (also known as a **monitor lock**). When a thread enters a `synchronized` method or block, it attempts to acquire the intrinsic lock of the object associated with that synchronization.

*   If the lock is available, the thread acquires it, enters the synchronized code, and no other thread can acquire that same lock until the current thread releases it.
*   If the lock is already held by another thread, the attempting thread is blocked (put into a waiting state) until the lock is released.

The lock is automatically released when the thread exits the `synchronized` method or block, either normally (reaching the end of the block/method) or abnormally (throwing an exception).

## 3. Synchronized Methods

When you declare a method as `synchronized`, the entire method becomes a critical section.

### Mechanism

*   **For instance methods (`synchronized void myMethod()`):** The thread acquires the intrinsic lock of the *instance* (`this`) on which the method is called. If `obj1.myMethod()` is called, the lock on `obj1` is acquired.
*   **For static methods (`synchronized static void myStaticMethod()`):** The thread acquires the intrinsic lock of the *Class object* (`ClassName.class`) to which the method belongs. This ensures that only one thread can execute any synchronized static method of that class at any given time.

### Example: Race Condition vs. Synchronized Method

Let's demonstrate a common race condition with a simple counter and then fix it using a synchronized method.

#### Problem: Unsynchronized Counter

Multiple threads trying to increment a shared counter without synchronization will often result in an incorrect final count.

**`UnsafeCounter.java`**

```java
public class UnsafeCounter {
    private int count = 0;

    public void increment() {
        // This operation (read-modify-write) is NOT atomic.
        // Multiple threads can read the same value, increment, and then overwrite each other's updates.
        count++; 
    }

    public int getCount() {
        return count;
    }

    public static void main(String[] args) throws InterruptedException {
        UnsafeCounter counter = new UnsafeCounter();
        int numberOfThreads = 1000;
        Thread[] threads = new Thread[numberOfThreads];

        for (int i = 0; i < numberOfThreads; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    counter.increment();
                }
            });
        }

        long startTime = System.nanoTime();

        for (Thread thread : threads) {
            thread.start();
        }

        for (Thread thread : threads) {
            thread.join(); // Wait for all threads to finish
        }

        long endTime = System.nanoTime();

        System.out.println("Expected count: " + (numberOfThreads * 1000));
        System.out.println("Actual count:   " + counter.getCount());
        System.out.println("Time taken (ns): " + (endTime - startTime));
    }
}
```

**Input (How to run):**
Compile and run `UnsafeCounter.java` from your terminal:
```bash
javac UnsafeCounter.java
java UnsafeCounter
```

**Typical Output (will vary due to race condition):**
```
Expected count: 1000000
Actual count:   998765  # This number will almost certainly be less than 1,000,000
Time taken (ns): 123456789
```
*Explanation*: The `count++` operation involves three steps: read `count`, increment its value, and write the new value back. If two threads read the same `count` value before either writes back, one update will be lost, leading to an incorrect final count.

#### Solution: Synchronized Method

By making the `increment()` method `synchronized`, we ensure that only one thread can execute it at a time.

**`SafeCounterMethod.java`**
```java
public class SafeCounterMethod {
    private int count = 0;

    // The 'synchronized' keyword ensures only one thread can execute this method at a time.
    // It acquires the intrinsic lock of the 'SafeCounterMethod' instance ('this').
    public synchronized void increment() {
        count++; // Now this operation is effectively atomic for concurrent access
    }

    public int getCount() {
        return count;
    }

    public static void main(String[] args) throws InterruptedException {
        SafeCounterMethod counter = new SafeCounterMethod();
        int numberOfThreads = 1000;
        Thread[] threads = new Thread[numberOfThreads];

        for (int i = 0; i < numberOfThreads; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    counter.increment();
                }
            });
        }

        long startTime = System.nanoTime();

        for (Thread thread : threads) {
            thread.start();
        }

        for (Thread thread : threads) {
            thread.join(); // Wait for all threads to finish
        }

        long endTime = System.nanoTime();

        System.out.println("Expected count: " + (numberOfThreads * 1000));
        System.out.println("Actual count:   " + counter.getCount());
        System.out.println("Time taken (ns): " + (endTime - startTime));
    }
}
```

**Input (How to run):**
Compile and run `SafeCounterMethod.java` from your terminal:
```bash
javac SafeCounterMethod.java
java SafeCounterMethod
```

**Typical Output:**
```
Expected count: 1000000
Actual count:   1000000  # Always the correct count
Time taken (ns): 234567890 # Note: Time taken might be higher due to synchronization overhead
```
*Explanation*: Each thread wishing to call `increment()` must first acquire the lock on the `counter` object. If the lock is held, the thread waits. This guarantees that `count++` is performed atomically by one thread at a time, leading to the correct result.

## 4. Synchronized Blocks

Synchronized blocks provide a more fine-grained control over synchronization. Instead of locking the entire method, you can lock only a specific part of the code that needs protection.

### Mechanism

The syntax for a synchronized block is: `synchronized (expression) { // critical section }`

*   **`expression`**: This must evaluate to an object. The thread attempts to acquire the intrinsic lock of *that specific object*.
*   **`synchronized (this)`**: Locks on the current instance of the object. This is semantically equivalent to a synchronized instance method.
*   **`synchronized (ClassName.class)`**: Locks on the `Class` object. This is semantically equivalent to a synchronized static method.
*   **`synchronized (someOtherObject)`**: Locks on an arbitrary object. This is often used for finer-grained control or when you need to protect resources that are not directly tied to the current object instance (e.g., a shared resource managed by multiple objects, or different parts of the same object requiring different locks). It's common practice to create a `private final Object lock = new Object();` for this purpose to prevent accidental external locking.

### Example: Fine-Grained Synchronization with Synchronized Blocks

Consider a `Wallet` where deposits and withdrawals happen. We want to ensure that the balance updates are atomic, but other operations (like printing transaction history) might not need to be synchronized with balance changes, or might need a different lock.

#### Solution: Synchronized Block with a Dedicated Lock Object

We'll use a `private final Object` as a dedicated lock for balance modifications. This allows other methods in `Wallet` to run concurrently if they don't need this specific lock.

**`SafeWalletBlock.java`**
```java
public class SafeWalletBlock {
    private double balance = 0.0;
    // A dedicated private final object for locking to protect the balance.
    // This provides fine-grained control and prevents accidental external locking.
    private final Object balanceLock = new Object();

    public void deposit(double amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("Deposit amount cannot be negative.");
        }
        
        // Only the critical section (balance modification) is synchronized
        synchronized (balanceLock) {
            System.out.println(Thread.currentThread().getName() + " is depositing " + amount);
            balance += amount;
            System.out.println(Thread.currentThread().getName() + " new balance: " + balance);
        }
        // Other non-critical operations can happen outside the synchronized block
        // e.g., logging, UI updates, which can execute concurrently with other threads
    }

    public void withdraw(double amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("Withdrawal amount cannot be negative.");
        }
        
        // Only the critical section (balance modification) is synchronized
        synchronized (balanceLock) {
            if (balance >= amount) {
                System.out.println(Thread.currentThread().getName() + " is withdrawing " + amount);
                balance -= amount;
                System.out.println(Thread.currentThread().getName() + " new balance: " + balance);
            } else {
                System.out.println(Thread.currentThread().getName() + " tried to withdraw " + amount + " but insufficient balance: " + balance);
            }
        }
    }

    public double getBalance() {
        // While reading balance, it's generally good practice to synchronize
        // to ensure visibility (happens-before relationship).
        // For simple primitives, `volatile` could also be considered, but `synchronized`
        // provides both mutual exclusion and memory visibility.
        synchronized (balanceLock) {
            return balance;
        }
    }

    public void printStatement() {
        // This operation does not modify balance, so it doesn't need to be synchronized
        // on balanceLock, allowing it to run concurrently with deposit/withdraw operations.
        // If it needed to read a consistent balance, it would need to acquire balanceLock.
        System.out.println(Thread.currentThread().getName() + " is printing statement. Current balance: " + getBalance());
    }

    public static void main(String[] args) throws InterruptedException {
        SafeWalletBlock wallet = new SafeWalletBlock();

        Runnable depositTask = () -> {
            for (int i = 0; i < 50; i++) {
                wallet.deposit(10.0);
                try { Thread.sleep(1); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            }
        };

        Runnable withdrawTask = () -> {
            for (int i = 0; i < 50; i++) {
                wallet.withdraw(5.0);
                try { Thread.sleep(1); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            }
        };

        Thread t1 = new Thread(depositTask, "Depositor-1");
        Thread t2 = new Thread(depositTask, "Depositor-2");
        Thread t3 = new Thread(withdrawTask, "Withdrawer-1");
        Thread t4 = new Thread(withdrawTask, "Withdrawer-2");

        t1.start();
        t2.start();
        t3.start();
        t4.start();

        t1.join();
        t2.join();
        t3.join();
        t4.join();

        System.out.println("\nFinal Balance: " + wallet.getBalance());
        // Expected Final Balance Calculation:
        // (50 deposits/thread * 2 deposit threads * 10 units/deposit) 
        // - (50 withdrawals/thread * 2 withdraw threads * 5 units/withdrawal)
        // = (100 * 10) - (100 * 5)
        // = 1000 - 500 = 500
    }
}
```

**Input (How to run):**
Compile and run `SafeWalletBlock.java` from your terminal:
```bash
javac SafeWalletBlock.java
java SafeWalletBlock
```

**Typical Output (exact interleaving may vary, but balance updates are atomic):**
```
Depositor-1 is depositing 10.0
Depositor-1 new balance: 10.0
Depositor-2 is depositing 10.0
Depositor-2 new balance: 20.0
Withdrawer-1 is withdrawing 5.0
Withdrawer-1 new balance: 15.0
... (many more lines showing interleaved deposits and withdrawals) ...
Withdrawer-2 is withdrawing 5.0
Withdrawer-2 new balance: 495.0
Depositor-1 is depositing 10.0
Depositor-1 new balance: 505.0

Final Balance: 500.0
```
*Explanation*: Despite multiple threads performing deposits and withdrawals concurrently, the final balance is consistently correct because the critical sections (`balance += amount` and `balance -= amount`) are protected by the `balanceLock`. Only one thread can acquire `balanceLock` and modify the balance at any given time, preventing race conditions. Other operations not involving the `balanceLock` (like `printStatement` if it didn't call `getBalance` which uses the lock) can proceed in parallel, demonstrating fine-grained control.

## 5. Key Differences and Use Cases

| Feature           | Synchronized Method (`public synchronized void myMethod()`)                               | Synchronized Block (`synchronized (object) { ... }`)                                            |
| :---------------- | :---------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------ |
| **Granularity**   | Locks the entire method.                                                                  | Locks only a specific part of the code.                                                         |
| **Lock Object**   | Implicitly locks on `this` (for instance methods) or `ClassName.class` (for static methods). | Explicitly locks on the object provided in the parentheses (`this`, `ClassName.class`, or any other object). |
| **Flexibility**   | Less flexible. All code in the method becomes a critical section.                         | More flexible. Allows finer-grained control, protecting only the necessary code.                |
| **Performance**   | May lead to more contention and reduced concurrency if the method contains non-critical code. | Can improve concurrency by allowing non-critical code to run in parallel.                       |
| **Best Use Case** | When the entire method needs to be atomic and protected. Simpler syntax.                  | When only a small portion of a method needs synchronization, or when different parts of an object need different locks. |
| **Memory Visibility** | Ensures memory visibility for all variables accessed within the method.                   | Ensures memory visibility for all variables accessed within the block.                          |

## 6. Important Considerations and Best Practices

*   **Deadlock Potential**: If threads try to acquire multiple locks in different orders, they can get stuck in a deadlock. For example, Thread A acquires Lock X then tries to acquire Lock Y, while Thread B acquires Lock Y then tries to acquire Lock X. Careful design of lock acquisition order can mitigate this.
*   **Reentrancy**: Java's intrinsic locks are reentrant. This means if a thread already holds a lock on an object, it can re-enter any other synchronized method or block that requires the same lock without blocking itself. For example, a synchronized method can call another synchronized method on the same object.
*   **Performance Overhead**: Synchronization introduces overhead (acquiring and releasing locks). Use it judiciously, only when necessary for thread safety. Overuse can lead to reduced performance due to contention and context switching.
*   **Lock Scope**:
    *   **Synchronize on `private final Object` for internal state**: As shown in `SafeWalletBlock`, using a dedicated `private final Object` as a lock object is a common and good practice. It prevents external code from acquiring your lock and causing unexpected blocking, and it makes the intent clear.
    *   **Avoid Synchronizing on `String` literals or `Integer` objects**: These are often interned or cached by the JVM, meaning multiple seemingly distinct objects might actually be the *same* object in memory. Synchronizing on them can lead to unintended global locks that affect unrelated parts of your application.
    *   **Avoid Synchronizing on `this` if it's exposed externally**: If your object (`this`) is passed to other objects, they might inadvertently acquire your object's lock, leading to unexpected contention or deadlocks. A dedicated private lock object avoids this.
*   **Memory Visibility**: Besides mutual exclusion, `synchronized` also guarantees memory visibility. When a thread exits a synchronized block, it automatically writes out all changes it has made to main memory (a "release" operation). When a thread enters a synchronized block, it automatically reads all variables from main memory (an "acquire" operation). This creates a "happens-before" relationship, ensuring that changes made by one thread are visible to subsequent threads entering the same synchronized block.

## 7. Conclusion

The `synchronized` keyword is a cornerstone of concurrent programming in Java, providing robust mechanisms for ensuring thread safety through mutual exclusion and memory visibility. Whether you choose to synchronize entire methods or specific blocks of code depends on the granularity of control required. Understanding intrinsic locks, reentrancy, and best practices helps in writing efficient, correct, and robust multi-threaded applications. While `synchronized` is powerful, modern Java also offers more advanced concurrency utilities in the `java.util.concurrent` package (like `ReentrantLock`, `ReadWriteLock`, `Semaphore`, `CountDownLatch`, etc.) for more complex synchronization scenarios. However, `synchronized` remains fundamental and widely used for many common concurrent programming tasks due to its simplicity and direct language support.