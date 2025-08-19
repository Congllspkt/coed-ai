A **custom checked exception** in Java is an exception class that you define yourself, and which extends `java.lang.Exception` (or a subclass of `Exception`, but *not* `RuntimeException`). The "checked" part means that the Java compiler *checks* at compile time if a method that throws this exception either handles it with a `try-catch` block or declares it using the `throws` keyword in its method signature.

Custom checked exceptions are essential for signaling **recoverable error conditions** that calling code *should* be aware of and explicitly deal with. They represent specific application-level or business logic errors that are part of your application's expected behavior flow, even if they signify an "error" state.

---

## **1. Why Use Custom Checked Exceptions?**

1.  **Semantic Clarity:** Standard Java exceptions (like `IOException`, `SQLException`) are generic. A custom exception (e.g., `InsufficientFundsException`, `InvalidInputFormatException`) provides domain-specific meaning, making your code easier to understand and maintain.
2.  **Forced Handling:** They enforce a contract between the throwing method and the calling method. The compiler *requires* the caller to either handle the exception or propagate it further, ensuring that critical error conditions are not ignored.
3.  **Encapsulation of Error Details:** You can add specific fields and methods to your custom exception to provide more context about why the error occurred (e.g., `InsufficientFundsException` could carry `requiredAmount` and `availableBalance`).
4.  **Graceful Recovery:** Because they are checked, they guide developers to consider how to recover from or gracefully handle these specific error states.

---

## **2. When to Use Custom Checked Exceptions?**

Use a custom checked exception when:

*   The error represents a **recoverable condition** that the calling code *should* be able to anticipate and react to.
*   The error is a **violation of a business rule** or an application-specific constraint.
*   The calling code needs specific information about the error to decide on a course of action.
*   The problem is outside the direct control of the method (e.g., network issues, invalid user input that violates business logic, database constraints).

**Examples:**
*   `InsufficientFundsException`: When a user tries to withdraw more money than available.
*   `AccountFrozenException`: When an operation is attempted on a locked account.
*   `UserNotFoundException`: When a lookup fails for a specific user ID in an application.
*   `ProductOutOfStockException`: When a user tries to purchase an item not in inventory.

---

## **3. How to Create a Custom Checked Exception**

To create a custom checked exception, you simply define a new class that extends `java.lang.Exception`.

```java
// Basic structure of a custom checked exception
public class MyCustomCheckedException extends Exception {

    // 1. No-argument constructor
    public MyCustomCheckedException() {
        super(); // Call the parent Exception's constructor
    }

    // 2. Constructor with a detail message
    public MyCustomCheckedException(String message) {
        super(message); // Pass the message to the parent Exception
    }

    // 3. Constructor with a cause (another Throwable)
    public MyCustomCheckedException(Throwable cause) {
        super(cause); // Pass the cause to the parent Exception
    }

    // 4. Constructor with a detail message and a cause
    public MyCustomCheckedException(String message, Throwable cause) {
        super(message, cause); // Pass both to the parent Exception
    }

    // Optional: Constructor with suppression and writable stack trace control
    // Used in more advanced scenarios, often not needed for basic custom exceptions.
    public MyCustomCheckedException(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace) {
        super(message, cause, enableSuppression, writableStackTrace);
    }

    // You can add custom fields and methods here to provide more context.
    // private int errorCode;
    // public int getErrorCode() { return errorCode; }
}
```

---

## **4. Detailed Example: Banking Application**

Let's imagine a simple banking application where users can withdraw money. We want to handle specific error conditions:

1.  **Insufficient Funds:** If the withdrawal amount exceeds the available balance.
2.  **Account Frozen:** If the account is marked as frozen.

### **4.1. Step 1: Define Custom Checked Exceptions**

**`InsufficientFundsException.java`**
This exception includes specific data (required amount, available balance) to help the caller understand the exact nature of the problem.

```java
// InsufficientFundsException.java
public class InsufficientFundsException extends Exception {

    private double requiredAmount;
    private double availableBalance;

    public InsufficientFundsException(String message, double requiredAmount, double availableBalance) {
        super(message);
        this.requiredAmount = requiredAmount;
        this.availableBalance = availableBalance;
    }

    // Constructor without specific amounts, for general messages
    public InsufficientFundsException(String message) {
        super(message);
    }

    public double getRequiredAmount() {
        return requiredAmount;
    }

    public double getAvailableBalance() {
        return availableBalance;
    }
}
```

**`AccountFrozenException.java`**
A simpler exception, just carrying a message.

```java
// AccountFrozenException.java
public class AccountFrozenException extends Exception {

    public AccountFrozenException(String message) {
        super(message);
    }
}
```

### **4.2. Step 2: Create a Class That Throws the Exceptions**

**`BankAccount.java`**
This class has a `withdraw` method that can throw our custom checked exceptions. Notice the `throws` clause in the method signature.

```java
// BankAccount.java
public class BankAccount {
    private String accountNumber;
    private double balance;
    private boolean isFrozen;

    public BankAccount(String accountNumber, double initialBalance) {
        this(accountNumber, initialBalance, false); // Default not frozen
    }

    public BankAccount(String accountNumber, double initialBalance, boolean isFrozen) {
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
        this.isFrozen = isFrozen;
        System.out.printf("Account %s created with balance %.2f (Frozen: %b)%n", accountNumber, balance, isFrozen);
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    public double getBalance() {
        return balance;
    }

    public boolean isFrozen() {
        return isFrozen;
    }

    /**
     * Attempts to withdraw a specified amount from the account.
     * Throws custom checked exceptions for specific error conditions.
     *
     * @param amount The amount to withdraw.
     * @throws InsufficientFundsException If the balance is less than the withdrawal amount.
     * @throws AccountFrozenException If the account is currently frozen.
     */
    public void withdraw(double amount) throws InsufficientFundsException, AccountFrozenException {
        if (amount <= 0) {
            throw new IllegalArgumentException("Withdrawal amount must be positive.");
        }

        if (isFrozen) {
            throw new AccountFrozenException("Account " + accountNumber + " is currently frozen. Withdrawal denied.");
        }

        if (balance < amount) {
            throw new InsufficientFundsException(
                "Cannot withdraw " + amount + " from account " + accountNumber + ". Insufficient funds.",
                amount,
                balance
            );
        }

        this.balance -= amount;
        System.out.printf("Successfully withdrew %.2f from account %s. New balance: %.2f%n", amount, accountNumber, this.balance);
    }
}
```

### **4.3. Step 3: Create a Main Application to Handle the Exceptions**

**`BankingApp.java`**
This class demonstrates how a caller uses `try-catch` blocks to handle the custom checked exceptions.

```java
// BankingApp.java
public class BankingApp {

    public static void main(String[] args) {

        BankAccount account1 = new BankAccount("ACC001", 500.0);
        BankAccount account2 = new BankAccount("ACC002", 1000.0);
        BankAccount account3 = new BankAccount("ACC003", 200.0, true); // This account is frozen

        System.out.println("\n--- Test Case 1: Successful Withdrawal ---");
        try {
            account1.withdraw(150.0); // Should succeed
        } catch (InsufficientFundsException | AccountFrozenException e) {
            // This block should not be reached for a successful withdrawal
            System.err.println("Unexpected error during successful withdrawal: " + e.getMessage());
        } catch (IllegalArgumentException e) {
            System.err.println("Input error: " + e.getMessage());
        }

        System.out.println("\n--- Test Case 2: Withdrawal - Insufficient Funds ---");
        try {
            account2.withdraw(1200.0); // Should throw InsufficientFundsException
        } catch (InsufficientFundsException e) {
            System.err.println("Withdrawal failed due to insufficient funds for " + account2.getAccountNumber() + ":");
            System.err.println("  " + e.getMessage());
            System.err.printf("  Required: %.2f, Available: %.2f%n", e.getRequiredAmount(), e.getAvailableBalance());
            // Here you might log the error, suggest alternative actions, etc.
        } catch (AccountFrozenException e) {
            System.err.println("Withdrawal failed (account frozen): " + e.getMessage());
        } catch (IllegalArgumentException e) {
            System.err.println("Input error: " + e.getMessage());
        }

        System.out.println("\n--- Test Case 3: Withdrawal - Account Frozen ---");
        try {
            account3.withdraw(50.0); // Should throw AccountFrozenException
        } catch (InsufficientFundsException e) {
            System.err.println("Withdrawal failed (insufficient funds): " + e.getMessage());
        } catch (AccountFrozenException e) {
            System.err.println("Withdrawal failed for " + account3.getAccountNumber() + ":");
            System.err.println("  " + e.getMessage());
            // Here you might inform the user to contact support, etc.
        } catch (IllegalArgumentException e) {
            System.err.println("Input error: " + e.getMessage());
        }

        System.out.println("\n--- Test Case 4: Withdrawal - Invalid Amount (Unchecked Exception) ---");
        try {
            account1.withdraw(-10.0); // Should throw IllegalArgumentException (unchecked)
        } catch (InsufficientFundsException | AccountFrozenException e) {
            System.err.println("Withdrawal failed unexpectedly: " + e.getMessage());
        } catch (IllegalArgumentException e) {
            System.err.println("Input validation error: " + e.getMessage());
        }
    }
}
```

---

## **5. Compilation and Execution**

To compile and run this example, save the files as `InsufficientFundsException.java`, `AccountFrozenException.java`, `BankAccount.java`, and `BankingApp.java` in the same directory.

**Compile:**
```bash
javac InsufficientFundsException.java AccountFrozenException.java BankAccount.java BankingApp.java
```

**Run:**
```bash
java BankingApp
```

---

## **6. Input and Output**

**Input:** (Implicit in the `BankingApp.java` code)
The `main` method of `BankingApp` performs several test withdrawals with different scenarios.

**Output:**

```
Account ACC001 created with balance 500.00 (Frozen: false)
Account ACC002 created with balance 1000.00 (Frozen: false)
Account ACC003 created with balance 200.00 (Frozen: true)

--- Test Case 1: Successful Withdrawal ---
Successfully withdrew 150.00 from account ACC001. New balance: 350.00

--- Test Case 2: Withdrawal - Insufficient Funds ---
Withdrawal failed due to insufficient funds for ACC002:
  Cannot withdraw 1200.0 from account ACC002. Insufficient funds.
  Required: 1200.00, Available: 1000.00

--- Test Case 3: Withdrawal - Account Frozen ---
Withdrawal failed for ACC003:
  Account ACC003 is currently frozen. Withdrawal denied.

--- Test Case 4: Withdrawal - Invalid Amount (Unchecked Exception) ---
Input validation error: Withdrawal amount must be positive.
```

---

## **7. Summary and Key Takeaways**

*   **Definition:** Custom checked exceptions extend `java.lang.Exception`.
*   **Purpose:** To signal recoverable, domain-specific error conditions that calling code *must* acknowledge and handle.
*   **Enforcement:** The Java compiler enforces handling (`try-catch`) or declaration (`throws`).
*   **Design:** Give them meaningful names, and include constructors that take a `String message` and/or a `Throwable cause`. Add specific fields to provide more context about the error.
*   **Contrast with Unchecked Exceptions:** If an error is typically unrecoverable and indicates a programming bug (e.g., `NullPointerException`, `IllegalArgumentException`), extending `java.lang.RuntimeException` for a custom **unchecked** exception might be more appropriate. Checked exceptions are for scenarios where the calling code is expected to be able to do something meaningful with the error.