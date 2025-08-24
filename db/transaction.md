SQL transactions are fundamental for maintaining data integrity and consistency in a database. In Oracle, a transaction is a logical unit of work that contains one or more SQL statements executed by a single user or application. These statements are treated as a single, indivisible sequence of operations.

---

# SQL Transactions in Oracle

## Table of Contents
1.  [What is a Transaction?](#1-what-is-a-transaction)
2.  [ACID Properties](#2-acid-properties)
3.  [Key Transaction Commands](#3-key-transaction-commands)
    *   [`COMMIT`](#commit)
    *   [`ROLLBACK`](#rollback)
    *   [`SAVEPOINT`](#savepoint)
    *   [`ROLLBACK TO SAVEPOINT`](#rollback-to-savepoint)
4.  [Oracle-Specific Transaction Behavior](#4-oracle-specific-transaction-behavior)
    *   [Implicit Transaction Start](#implicit-transaction-start)
    *   [Default Isolation Level: `READ COMMITTED`](#default-isolation-level-read-committed)
    *   [`SET TRANSACTION` Statement](#set-transaction-statement)
    *   [DDL Statements and Implicit Commits](#ddl-statements-and-implicit-commits)
5.  [Examples](#5-examples)
    *   [Example 1: Basic COMMIT and ROLLBACK](#example-1-basic-commit-and-rollback)
    *   [Example 2: Using SAVEPOINT](#example-2-using-savepoint)
    *   [Example 3: `SET TRANSACTION READ ONLY`](#example-3-set-transaction-read-only)
    *   [Example 4: `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE` (Concurrency Example)](#example-4-set-transaction-isolation-level-serializable-concurrency-example)
    *   [Example 5: DDL Implicit Commit](#example-5-ddl-implicit-commit)
6.  [Best Practices](#6-best-practices)
7.  [Conclusion](#7-conclusion)

---

## 1. What is a Transaction?

A transaction in a database is a sequence of operations performed as a single logical unit of work. This means that either all operations within the transaction are successfully completed and recorded (committed), or if any part of the transaction fails, all operations are undone (rolled back) to restore the database to its state before the transaction began.

## 2. ACID Properties

Database transactions are characterized by four key properties, often referred to as ACID:

*   **Atomicity:** Guarantees that all operations within a transaction are treated as a single, indivisible unit. Either all of them succeed, or none of them do. There is no partial completion.
*   **Consistency:** Ensures that a transaction brings the database from one valid state to another. It maintains all defined rules, constraints (primary keys, foreign keys, check constraints), and triggers.
*   **Isolation:** Guarantees that the concurrent execution of transactions results in a system state that would be achieved if transactions were executed sequentially. Each transaction operates independently without interference from other concurrent transactions.
*   **Durability:** Ensures that once a transaction has been committed, its changes are permanent and will survive any subsequent system failures (e.g., power outages, crashes).

## 3. Key Transaction Commands

### `COMMIT`

*   **Purpose:** Makes all changes performed by the current transaction permanent in the database.
*   **Effect:**
    *   Ends the current transaction.
    *   All changes made since the last `COMMIT` or `ROLLBACK` are saved.
    *   Releases any locks held by the transaction.
    *   Makes the changes visible to other transactions.
*   **Syntax:**
    ```sql
    COMMIT;
    ```

### `ROLLBACK`

*   **Purpose:** Undoes all changes performed by the current transaction since the last `COMMIT` or `ROLLBACK`.
*   **Effect:**
    *   Ends the current transaction.
    *   All changes made since the last `COMMIT` or `ROLLBACK` are discarded.
    *   Releases any locks held by the transaction.
    *   Restores the database to its state before the transaction began.
*   **Syntax:**
    ```sql
    ROLLBACK;
    ```

### `SAVEPOINT`

*   **Purpose:** Creates a named marker within the current transaction to which you can later roll back.
*   **Effect:**
    *   Does not end the transaction.
    *   Allows partial rollbacks.
*   **Syntax:**
    ```sql
    SAVEPOINT savepoint_name;
    ```
    *`savepoint_name` is a user-defined identifier.*

### `ROLLBACK TO SAVEPOINT`

*   **Purpose:** Undoes all changes made in the current transaction from the point where the `SAVEPOINT` was created, up to the current point.
*   **Effect:**
    *   Does not end the transaction.
    *   Only rolls back changes made *after* the specified `SAVEPOINT`.
    *   The `SAVEPOINT` itself remains valid unless explicitly released or the transaction is committed/rolled back.
*   **Syntax:**
    ```sql
    ROLLBACK TO SAVEPOINT savepoint_name;
    ```

## 4. Oracle-Specific Transaction Behavior

### Implicit Transaction Start

In Oracle, you do not explicitly use a `START TRANSACTION` command. A new transaction implicitly begins with the first DML (Data Manipulation Language) statement (`INSERT`, `UPDATE`, `DELETE`, `MERGE`, `SELECT FOR UPDATE`) or DDL (Data Definition Language) statement (`CREATE`, `ALTER`, `DROP`) executed in a session, if no other transaction is currently active.

### Default Isolation Level: `READ COMMITTED`

Oracle's default transaction isolation level is `READ COMMITTED`. This means:

*   A transaction can only see changes that have been committed by other transactions. It prevents "dirty reads" (reading uncommitted data).
*   However, it's possible for a transaction to see different results for the same query if another transaction commits changes between two executions of that query within the current transaction (i.e., "non-repeatable reads" are possible).
*   For a consistent view, Oracle uses **read consistency** based on SCN (System Change Number). When a query starts, Oracle ensures that all data it returns is consistent to a single point in time (the SCN when the query began), even if other transactions are concurrently modifying that data.

### `SET TRANSACTION` Statement

This statement is used to set properties for the current transaction, such as its isolation level or whether it is read-only.

*   **`SET TRANSACTION READ ONLY;`**:
    *   Establishes a transaction where you can only execute `SELECT` statements.
    *   Provides a consistent view of the database as of the time the transaction started.
    *   No DML operations are allowed. Useful for reporting that requires a stable snapshot.
*   **`SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;`**:
    *   Provides the highest level of isolation.
    *   Ensures that concurrent transactions execute in such a way that the result is the same as if they had executed one after another (serially).
    *   Prevents "dirty reads," "non-repeatable reads," and "phantom reads."
    *   Can lead to `ORA-08177: can't serialize access for this transaction` errors if concurrent transactions try to modify the same data.

### DDL Statements and Implicit Commits

**Crucial Point:** Any DDL statement (`CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME`) automatically performs an implicit `COMMIT` of any pending DML operations. It also implicitly `COMMIT`s itself. This means you cannot roll back a DDL statement.

## 5. Examples

Let's set up a sample table and some initial data for our examples:

```sql
-- Connect to your Oracle database first
-- For example: sqlplus your_user/your_password@your_database

-- Create a sample table
CREATE TABLE employees (
    employee_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50),
    last_name VARCHAR2(50),
    salary NUMBER(10, 2)
);

-- Insert initial data
INSERT INTO employees (employee_id, first_name, last_name, salary) VALUES (101, 'John', 'Doe', 60000.00);
INSERT INTO employees (employee_id, first_name, last_name, salary) VALUES (102, 'Jane', 'Smith', 75000.00);
INSERT INTO employees (employee_id, first_name, last_name, salary) VALUES (103, 'Peter', 'Jones', 50000.00);

-- Commit the initial data so it's permanent
COMMIT;
```

### Example 1: Basic COMMIT and ROLLBACK

This example demonstrates how to make changes permanent or undo them.

```sql
-- Input SQL:

-- Step 1: Check initial data
SELECT employee_id, first_name, salary FROM employees WHERE employee_id IN (101, 102);

-- Step 2: Start a transaction (implicitly, with the first DML)
-- Give John Doe a raise
UPDATE employees
SET salary = 65000.00
WHERE employee_id = 101;

-- Check current state (only visible to this session, not yet committed)
SELECT employee_id, first_name, salary FROM employees WHERE employee_id IN (101, 102);

-- Step 3: Commit the change
COMMIT;

-- Check state after commit (permanent, visible to all)
SELECT employee_id, first_name, salary FROM employees WHERE employee_id IN (101, 102);

-- Step 4: Start another transaction
-- Give Jane Smith a raise
UPDATE employees
SET salary = 80000.00
WHERE employee_id = 102;

-- Check current state (only visible to this session)
SELECT employee_id, first_name, salary FROM employees WHERE employee_id IN (101, 102);

-- Step 5: Rollback the change for Jane Smith
ROLLBACK;

-- Check state after rollback (change for Jane Smith is undone)
SELECT employee_id, first_name, salary FROM employees WHERE employee_id IN (101, 102);
```

**Output:**

```
-- Step 1 Output: Initial Data
EMPLOYEE_ID FIRST_NAME      SALARY
----------- --------------- --------
        101 John            60000.00
        102 Jane            75000.00

-- Step 2 Output: After UPDATE (before commit/rollback, visible only in this session)
EMPLOYEE_ID FIRST_NAME      SALARY
----------- --------------- --------
        101 John            65000.00
        102 Jane            75000.00

-- Step 3 Output: After COMMIT (John's salary is permanently updated)
EMPLOYEE_ID FIRST_NAME      SALARY
----------- --------------- --------
        101 John            65000.00
        102 Jane            75000.00

-- Step 4 Output: After another UPDATE (before commit/rollback, visible only in this session)
EMPLOYEE_ID FIRST_NAME      SALARY
----------- --------------- --------
        101 John            65000.00
        102 Jane            80000.00

-- Step 5 Output: After ROLLBACK (Jane's salary update is undone, back to 75000)
EMPLOYEE_ID FIRST_NAME      SALARY
----------- --------------- --------
        101 John            65000.00
        102 Jane            75000.00
```

**Explanation:**
*   John's salary update was committed, making it a permanent change.
*   Jane's salary update was rolled back, effectively canceling the change and reverting her salary to its previous committed value.

### Example 2: Using SAVEPOINT

This example shows how `SAVEPOINT` allows for partial rollbacks within a transaction.

```sql
-- Input SQL:

-- Step 1: Check initial data
SELECT employee_id, first_name, salary FROM employees WHERE employee_id IN (101, 102, 103);

-- Step 2: Start a transaction (implicitly)
-- Update John Doe's salary
UPDATE employees
SET salary = 67000.00
WHERE employee_id = 101;

-- Set a savepoint
SAVEPOINT after_john_update;

-- Step 3: Update Jane Smith's salary
UPDATE employees
SET salary = 82000.00
WHERE employee_id = 102;

-- Check current state (visible only in this session)
SELECT employee_id, first_name, salary FROM employees WHERE employee_id IN (101, 102, 103);

-- Step 4: Update Peter Jones' salary (Oops, made a mistake here!)
UPDATE employees
SET salary = 5000.00 -- This is clearly a mistake!
WHERE employee_id = 103;

-- Check current state (visible only in this session)
SELECT employee_id, first_name, salary FROM employees WHERE employee_id IN (101, 102, 103);

-- Step 5: Rollback only the changes after 'after_john_update' (i.e., Peter and Jane's updates)
ROLLBACK TO SAVEPOINT after_john_update;

-- Check state after partial rollback (John's update remains, Jane and Peter's are undone)
SELECT employee_id, first_name, salary FROM employees WHERE employee_id IN (101, 102, 103);

-- Step 6: Now commit the remaining changes (John's salary)
COMMIT;

-- Final check after commit
SELECT employee_id, first_name, salary FROM employees WHERE employee_id IN (101, 102, 103);
```

**Output:**

```
-- Step 1 Output: Initial Data
EMPLOYEE_ID FIRST_NAME      SALARY
----------- --------------- --------
        101 John            65000.00
        102 Jane            75000.00
        103 Peter           50000.00

-- Step 3 Output: After John and Jane updates (before rollback)
EMPLOYEE_ID FIRST_NAME      SALARY
----------- --------------- --------
        101 John            67000.00
        102 Jane            82000.00
        103 Peter           50000.00

-- Step 4 Output: After John, Jane, and Peter updates (Peter's is the mistake)
EMPLOYEE_ID FIRST_NAME      SALARY
----------- --------------- --------
        101 John            67000.00
        102 Jane            82000.00
        103 Peter            5000.00

-- Step 5 Output: After ROLLBACK TO SAVEPOINT (Jane and Peter's updates undone)
EMPLOYEE_ID FIRST_NAME      SALARY
----------- --------------- --------
        101 John            67000.00
        102 Jane            75000.00
        103 Peter           50000.00

-- Step 6 Output: Final state after COMMIT (only John's salary is permanently changed)
EMPLOYEE_ID FIRST_NAME      SALARY
----------- --------------- --------
        101 John            67000.00
        102 Jane            75000.00
        103 Peter           50000.00
```

**Explanation:**
*   We updated John's salary and set a `SAVEPOINT`.
*   Then we updated Jane's and Peter's salaries.
*   Realizing Peter's salary was wrong, we used `ROLLBACK TO SAVEPOINT after_john_update`. This undid only Jane's and Peter's updates, leaving John's update intact.
*   Finally, we committed the transaction, making John's salary change permanent.

### Example 3: `SET TRANSACTION READ ONLY`

This transaction type is useful for consistent reporting when you don't want to accidentally modify data.

```sql
-- Input SQL:

-- Step 1: Set the transaction to READ ONLY
SET TRANSACTION READ ONLY;

-- Step 2: Perform a SELECT (allowed)
SELECT COUNT(*) FROM employees;
SELECT * FROM employees WHERE salary > 70000;

-- Step 3: Try to perform an INSERT (will fail)
INSERT INTO employees (employee_id, first_name, last_name, salary) VALUES (104, 'Alice', 'Wonder', 90000.00);

-- Step 4: Commit the read-only transaction (ends it, no changes are saved anyway)
COMMIT;

-- Step 5: Verify no change occurred
SELECT COUNT(*) FROM employees;
```

**Output:**

```
-- Step 1: Transaction set to READ ONLY.
Transaction set.

-- Step 2: SELECT statements execute successfully.
  COUNT(*)
----------
         3

EMPLOYEE_ID FIRST_NAME      LAST_NAME      SALARY
----------- --------------- -------------- --------
        102 Jane            Smith          75000.00

-- Step 3: Attempt to INSERT fails.
Error starting at line : 8 in command -
INSERT INTO employees (employee_id, first_name, last_name, salary) VALUES (104, 'Alice', 'Wonder', 90000.00)
Error report -
ORA-01456: may not perform insert/delete/update operation inside a READ ONLY transaction

-- Step 4: COMMIT ends the READ ONLY transaction.
Commit complete.

-- Step 5: No new employee exists.
  COUNT(*)
----------
         3
```

**Explanation:**
*   Setting the transaction to `READ ONLY` prevents any DML operations.
*   The `INSERT` statement correctly raised an `ORA-01456` error.
*   `COMMIT` or `ROLLBACK` will end a `READ ONLY` transaction, but since no changes are possible, they don't actually "save" or "undo" anything.

### Example 4: `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE` (Concurrency Example)

This demonstrates the stricter isolation and potential for `ORA-08177` errors when multiple serializable transactions try to modify the same data. This requires **two separate database sessions** to illustrate properly.

---

**Pre-requisite:** Open two separate SQL*Plus or SQL Developer/Toad sessions to the same database user.

**Session 1:**

```sql
-- Input SQL (Session 1):

-- Step 1: Set transaction isolation level to SERIALIZABLE
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Step 2: Update an employee's salary
UPDATE employees
SET salary = 70000.00
WHERE employee_id = 101;

-- DO NOT COMMIT YET IN SESSION 1
-- Keep this session open and the transaction active
```

**Session 2:**

```sql
-- Input SQL (Session 2):

-- Step 1: Set transaction isolation level to SERIALIZABLE
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Step 2: Attempt to update the *same* employee's salary
UPDATE employees
SET salary = 72000.00
WHERE employee_id = 101;

-- This UPDATE will wait, and then likely fail with ORA-08177 if Session 1 commits
-- or tries to update the same row after Session 2 tries to update.
-- More typically, if Session 1 performs the UPDATE first, and then Session 2 tries
-- to update the same row while Session 1 is uncommitted, Session 2 will eventually fail.
```

---

**Expected Output (Session 2, after waiting):**

```
Error starting at line : 5 in command -
UPDATE employees
SET salary = 72000.00
WHERE employee_id = 101
Error report -
ORA-08177: can't serialize access for this transaction
```

**Explanation:**
*   Both sessions started `SERIALIZABLE` transactions.
*   Session 1 updated employee 101. This change is not yet committed.
*   When Session 2 tried to update the *same employee* (101), Oracle detected a potential serialization anomaly. Because `SERIALIZABLE` transactions must produce the same result as if they ran one after another, and allowing Session 2 to update the same row that Session 1 has *already modified* (even if uncommitted) would break this guarantee, Oracle raises `ORA-08177`.
*   Session 2's transaction is effectively rolled back due to this error.
*   **Resolution:** Session 1 would either commit its changes (making them visible and allowing a *new* transaction in Session 2 to see them) or roll back. Then Session 2 could retry its operation.

### Example 5: DDL Implicit Commit

This shows how a DDL statement automatically commits any pending DML.

```sql
-- Input SQL:

-- Step 1: Check initial data for John Doe
SELECT employee_id, first_name, salary FROM employees WHERE employee_id = 101;

-- Step 2: Update John Doe's salary (start a transaction implicitly)
UPDATE employees
SET salary = 68000.00
WHERE employee_id = 101;

-- Check current state (visible only in this session, not yet committed)
SELECT employee_id, first_name, salary FROM employees WHERE employee_id = 101;

-- Step 3: Execute a DDL statement (e.g., CREATE TABLE)
CREATE TABLE temp_log (
    log_id NUMBER,
    log_message VARCHAR2(100)
);

-- Step 4: Attempt to ROLLBACK the UPDATE for John Doe (it should fail/do nothing)
ROLLBACK;

-- Step 5: Check John Doe's salary again (it should be 68000.00, meaning the update committed)
SELECT employee_id, first_name, salary FROM employees WHERE employee_id = 101;

-- Clean up the temporary table
DROP TABLE temp_log;
COMMIT; -- Commit the DROP TABLE as DDL also commits implicitly, but good practice to clean up transaction.
```

**Output:**

```
-- Step 1 Output: Initial salary
EMPLOYEE_ID FIRST_NAME      SALARY
----------- --------------- --------
        101 John            67000.00

-- Step 2 Output: After UPDATE (before DDL, visible only in this session)
EMPLOYEE_ID FIRST_NAME      SALARY
----------- --------------- --------
        101 John            68000.00

-- Step 3 Output: DDL statement executed, implicitly committing the UPDATE
Table TEMP_LOG created.

-- Step 4 Output: ROLLBACK attempt
Rollback complete.

-- Step 5 Output: John's salary is still 68000.00, confirming the implicit commit
EMPLOYEE_ID FIRST_NAME      SALARY
----------- --------------- --------
        101 John            68000.00

-- Clean up
Table TEMP_LOG dropped.
Commit complete.
```

**Explanation:**
*   The `UPDATE` statement started a transaction, but it wasn't explicitly committed.
*   Executing the `CREATE TABLE temp_log` statement automatically committed the pending `UPDATE` on the `employees` table.
*   Therefore, the subsequent `ROLLBACK` command had no effect on John's salary, as the change was already made permanent by the `CREATE TABLE` statement's implicit commit.

## 6. Best Practices

*   **Keep Transactions Short:** Long-running transactions hold locks, consume undo/redo space, and can lead to increased contention and rollback segment issues.
*   **Handle Errors with `ROLLBACK`:** In application code, always include error handling that ensures a `ROLLBACK` occurs if any part of the transaction fails.
*   **Use `SAVEPOINT` Judiciously:** Useful for complex operations where you might want to partially undo work without restarting the entire transaction. Don't overuse them, as they consume resources.
*   **Understand Isolation Levels:** Choose the appropriate isolation level for your application. `READ COMMITTED` is generally good for most OLTP (Online Transaction Processing) applications due to its balance of consistency and concurrency. Use `SERIALIZABLE` only when strict consistency across multiple reads/updates is absolutely critical and you can manage the increased potential for serialization errors.
*   **Be Aware of DDL Auto-Commit:** Never mix DDL and DML operations within the same logical transaction unless you explicitly intend for the DML to be committed by the DDL.
*   **Test Concurrency:** Always test your application's transaction logic under concurrent load to ensure it behaves as expected and handles potential deadlocks or serialization failures gracefully.

## 7. Conclusion

Understanding transactions in Oracle SQL is crucial for developing robust and reliable database applications. By correctly utilizing `COMMIT`, `ROLLBACK`, `SAVEPOINT`, and being aware of Oracle's specific transaction behaviors like implicit starts, default isolation, and DDL auto-commits, you can ensure data integrity and manage concurrency effectively.