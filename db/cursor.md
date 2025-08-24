In Oracle SQL (specifically PL/SQL), a **cursor** is a pointer or a control structure that enables traversal over the records in a database. It's essentially a temporary work area created in system memory (SGA for shared SQL area, PGA for private SQL area) when an SQL statement is executed.

When you execute an SQL statement in Oracle, the database system creates a work area known as a **private SQL area** for processing that statement. A cursor is a name or a handle to this private SQL area.

**Why use Cursors?**

SQL statements like `SELECT` often return multiple rows. While a simple `SELECT` statement can be executed directly in SQL*Plus or SQL Developer to display results, within a PL/SQL block, you often need to process these rows one by one. This is where cursors become essential. They allow PL/SQL programs to:

1.  **Process multiple rows returned by a query.**
2.  **Navigate through the result set row by row.**
3.  **Perform operations (e.g., update, delete, other computations) on individual rows.**

---

## Types of Cursors

Oracle provides two types of cursors:

1.  **Implicit Cursors:** Automatically created and managed by Oracle for all SQL statements (DML operations like `INSERT`, `UPDATE`, `DELETE`, and `SELECT INTO` statements that return at most one row). You don't declare them explicitly.
2.  **Explicit Cursors:** Declared and managed by the programmer for `SELECT` statements that are expected to return multiple rows.

---

### 1. Implicit Cursors

Oracle implicitly opens a cursor every time you execute an SQL statement that is not a `SELECT` query returning multiple rows. This includes:

*   `INSERT` statements
*   `UPDATE` statements
*   `DELETE` statements
*   `SELECT INTO` statements (which must return exactly one row)

You don't need to declare, open, or close implicit cursors. Oracle handles all these operations automatically. However, you can use **cursor attributes** to monitor the outcome of implicit SQL operations.

**Implicit Cursor Attributes (SQL% Attributes):**

*   `SQL%ROWCOUNT`: Returns the number of rows affected by the DML statement.
*   `SQL%FOUND`: Returns `TRUE` if at least one row was affected (or found by `SELECT INTO`), `FALSE` otherwise.
*   `SQL%NOTFOUND`: Returns `TRUE` if no row was affected (or found by `SELECT INTO`), `FALSE` otherwise.
*   `SQL%ISOPEN`: Always returns `FALSE` for implicit cursors because Oracle automatically closes them immediately after execution.

**Example 1: Implicit Cursor with `UPDATE`**

Let's assume we have an `employees` table:

```sql
-- Setup: Create a sample table and insert data
CREATE TABLE employees (
    employee_id   NUMBER PRIMARY KEY,
    first_name    VARCHAR2(50),
    last_name     VARCHAR2(50),
    email         VARCHAR2(100) UNIQUE,
    phone_number  VARCHAR2(20),
    hire_date     DATE,
    job_id        VARCHAR2(20),
    salary        NUMBER(8, 2),
    commission_pct NUMBER(2, 2),
    manager_id    NUMBER,
    department_id NUMBER
);

INSERT INTO employees VALUES (100, 'Steven', 'King', 'SKING', '515.123.4567', SYSDATE, 'AD_PRES', 24000, NULL, NULL, 90);
INSERT INTO employees VALUES (101, 'Neena', 'Kochhar', 'NKOCHHAR', '515.123.4568', SYSDATE, 'AD_VP', 17000, NULL, 100, 90);
INSERT INTO employees VALUES (102, 'Lex', 'De Haan', 'LDEHAAN', '515.123.4569', SYSDATE, 'AD_VP', 17000, NULL, 100, 90);
INSERT INTO employees VALUES (103, 'Alexander', 'Hunold', 'AHUNOLD', '590.423.4567', SYSDATE, 'IT_PROG', 9000, NULL, 102, 60);
INSERT INTO employees VALUES (104, 'Bruce', 'Ernst', 'BERNST', '590.423.4568', SYSDATE, 'IT_PROG', 6000, NULL, 103, 60);
INSERT INTO employees VALUES (105, 'Diana', 'Lorentz', 'DLORENTZ', '590.423.4569', SYSDATE, 'IT_PROG', 4200, NULL, 103, 60);
COMMIT;
```

**Input (PL/SQL Block):**

```sql
SET SERVEROUTPUT ON;
DECLARE
    v_rows_updated NUMBER;
BEGIN
    UPDATE employees
    SET salary = salary * 1.10
    WHERE department_id = 60;

    v_rows_updated := SQL%ROWCOUNT;

    IF SQL%FOUND THEN
        DBMS_OUTPUT.PUT_LINE(v_rows_updated || ' employees had their salaries updated.');
    ELSE
        DBMS_OUTPUT.PUT_LINE('No employees found in department 60 to update.');
    END IF;

    -- Demonstrating SQL%ISOPEN (always FALSE for implicit cursors)
    IF SQL%ISOPEN THEN
        DBMS_OUTPUT.PUT_LINE('Implicit cursor is open.');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Implicit cursor is closed (as expected).');
    END IF;

    -- Another example: SELECT INTO
    DECLARE
        emp_name VARCHAR2(100);
        emp_sal  NUMBER;
    BEGIN
        SELECT first_name || ' ' || last_name, salary
        INTO emp_name, emp_sal
        FROM employees
        WHERE employee_id = 100;

        DBMS_OUTPUT.PUT_LINE('Employee 100: ' || emp_name || ', Salary: ' || emp_sal);

        -- What if it finds no rows?
        BEGIN
            SELECT first_name
            INTO emp_name
            FROM employees
            WHERE employee_id = 999; -- Non-existent ID
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                DBMS_OUTPUT.PUT_LINE('No employee found with ID 999.');
                DBMS_OUTPUT.PUT_LINE('SQL%FOUND: ' || CASE WHEN SQL%FOUND THEN 'TRUE' ELSE 'FALSE' END);
                DBMS_OUTPUT.PUT_LINE('SQL%NOTFOUND: ' || CASE WHEN SQL%NOTFOUND THEN 'TRUE' ELSE 'FALSE' END);
        END;

    END;

    COMMIT;
END;
/
```

**Output:**

```
3 employees had their salaries updated.
Implicit cursor is closed (as expected).
Employee 100: Steven King, Salary: 26400
No employee found with ID 999.
SQL%FOUND: FALSE
SQL%NOTFOUND: TRUE

PL/SQL procedure successfully completed.
```

---

### 2. Explicit Cursors

You declare an explicit cursor when you anticipate that a `SELECT` statement might return more than one row. These cursors give you programmatic control over the fetching process.

**Steps for using an Explicit Cursor:**

1.  **DECLARE:** Define the cursor by naming it and associating it with a `SELECT` statement.
2.  **OPEN:** Execute the `SELECT` statement and identify the active set (the rows that satisfy the query criteria). The cursor points to the first row.
3.  **FETCH:** Retrieve rows one by one from the active set into PL/SQL variables.
4.  **CLOSE:** Release the resources held by the cursor.

**Explicit Cursor Attributes:**

These attributes are used with the declared cursor name (e.g., `my_cursor%ROWCOUNT`).

*   `%ROWCOUNT`: Returns the number of rows fetched so far by the cursor.
*   `%FOUND`: Returns `TRUE` if the last `FETCH` returned a row, `FALSE` otherwise.
*   `%NOTFOUND`: Returns `TRUE` if the last `FETCH` did not return a row, `FALSE` otherwise. (Often used to exit a loop).
*   `%ISOPEN`: Returns `TRUE` if the cursor is open, `FALSE` if it's closed.

---

#### 2.1. Basic Explicit Cursor (Manual Declare, Open, Fetch, Close)

This demonstrates the fundamental steps.

**Input (PL/SQL Block):**

```sql
SET SERVEROUTPUT ON;
DECLARE
    -- 1. DECLARE the cursor
    CURSOR emp_cursor IS
        SELECT employee_id, first_name, salary
        FROM employees
        WHERE department_id = 90
        ORDER BY salary DESC;

    -- Variables to hold fetched data
    v_emp_id   employees.employee_id%TYPE;
    v_fname    employees.first_name%TYPE;
    v_salary   employees.salary%TYPE;

BEGIN
    DBMS_OUTPUT.PUT_LINE('--- Processing Employees in Department 90 ---');

    -- 2. OPEN the cursor
    OPEN emp_cursor;

    LOOP
        -- 3. FETCH data into variables
        FETCH emp_cursor INTO v_emp_id, v_fname, v_salary;

        -- Check if any row was fetched
        EXIT WHEN emp_cursor%NOTFOUND; -- Exit loop if no more rows

        -- Process the fetched row
        DBMS_OUTPUT.PUT_LINE('ID: ' || v_emp_id || ', Name: ' || v_fname || ', Salary: ' || v_salary);

        -- Demonstrate %ROWCOUNT attribute
        -- DBMS_OUTPUT.PUT_LINE('Rows fetched so far: ' || emp_cursor%ROWCOUNT);

    END LOOP;

    DBMS_OUTPUT.PUT_LINE('Total employees processed: ' || emp_cursor%ROWCOUNT);
    DBMS_OUTPUT.PUT_LINE('Is cursor open after loop? ' || CASE WHEN emp_cursor%ISOPEN THEN 'TRUE' ELSE 'FALSE' END);

    -- 4. CLOSE the cursor
    CLOSE emp_cursor;

    DBMS_OUTPUT.PUT_LINE('Is cursor open after close? ' || CASE WHEN emp_cursor%ISOPEN THEN 'TRUE' ELSE 'FALSE' END);

END;
/
```

**Output:**

```
--- Processing Employees in Department 90 ---
ID: 100, Name: Steven, Salary: 26400
ID: 101, Name: Neena, Salary: 17000
ID: 102, Name: Lex, Salary: 17000
Total employees processed: 3
Is cursor open after loop? TRUE
Is cursor open after close? FALSE

PL/SQL procedure successfully completed.
```

---

#### 2.2. Explicit Cursor `FOR` Loop (Recommended)

This is the most common and recommended way to use explicit cursors in PL/SQL because it significantly simplifies the code. Oracle automatically handles the `OPEN`, `FETCH`, and `CLOSE` operations for you. It implicitly declares a record variable for each row fetched.

**Input (PL/SQL Block):**

```sql
SET SERVEROUTPUT ON;
DECLARE
    -- Declare the cursor, but no need for explicit variables to hold fetched data
    CURSOR emp_sal_cursor IS
        SELECT first_name, last_name, salary
        FROM employees
        WHERE department_id = 60
        ORDER BY salary ASC;

BEGIN
    DBMS_OUTPUT.PUT_LINE('--- Employees in Department 60 (Cursor FOR Loop) ---');

    -- The FOR loop implicitly declares a record variable (e.g., 'emp_rec')
    FOR emp_rec IN emp_sal_cursor LOOP
        DBMS_OUTPUT.PUT_LINE('Name: ' || emp_rec.first_name || ' ' || emp_rec.last_name || ', Salary: ' || emp_rec.salary);
    END LOOP;

    DBMS_OUTPUT.PUT_LINE('--- Finished processing ---');

    -- You cannot use cursor attributes directly with the loop variable like emp_sal_cursor%ROWCOUNT inside the loop,
    -- as the cursor is managed implicitly.
    -- If you need total row count, you might need to declare an explicit counter or use a different cursor approach.

END;
/
```

**Output:**

```
--- Employees in Department 60 (Cursor FOR Loop) ---
Name: Diana Lorentz, Salary: 4200
Name: Bruce Ernst, Salary: 6000
Name: Alexander Hunold, Salary: 9900
--- Finished processing ---

PL/SQL procedure successfully completed.
```

**Advantages of Cursor `FOR` Loop:**

*   **Simplicity:** Fewer lines of code.
*   **Automatic Management:** Oracle handles `OPEN`, `FETCH` (row by row), `EXIT WHEN %NOTFOUND`, and `CLOSE`.
*   **Performance:** Often optimized by the compiler.
*   **Type Safety:** The loop variable is implicitly declared as a record type, matching the cursor's select list.

---

#### 2.3. Explicit Cursor with Parameters

You can pass parameters to cursors, making them more flexible and reusable.

**Input (PL/SQL Block):**

```sql
SET SERVEROUTPUT ON;
DECLARE
    -- Cursor with a parameter for department_id
    CURSOR dept_emp_cursor (p_dept_id IN NUMBER) IS
        SELECT first_name, last_name, salary
        FROM employees
        WHERE department_id = p_dept_id
        ORDER BY last_name;

BEGIN
    DBMS_OUTPUT.PUT_LINE('--- Employees in Department 90 (using parameter) ---');
    FOR emp_rec IN dept_emp_cursor(90) LOOP -- Pass 90 as parameter
        DBMS_OUTPUT.PUT_LINE('Name: ' || emp_rec.first_name || ' ' || emp_rec.last_name || ', Salary: ' || emp_rec.salary);
    END LOOP;

    DBMS_OUTPUT.PUT_LINE(CHR(10) || '--- Employees in Department 60 (using parameter) ---');
    FOR emp_rec IN dept_emp_cursor(60) LOOP -- Pass 60 as parameter
        DBMS_OUTPUT.PUT_LINE('Name: ' || emp_rec.first_name || ' ' || emp_rec.last_name || ', Salary: ' || emp_rec.salary);
    END LOOP;

    DBMS_OUTPUT.PUT_LINE(CHR(10) || '--- Employees in Department 10 (non-existent) ---');
    FOR emp_rec IN dept_emp_cursor(10) LOOP -- Pass 10 as parameter (no employees)
        DBMS_OUTPUT.PUT_LINE('Name: ' || emp_rec.first_name || ' ' || emp_rec.last_name || ', Salary: ' || emp_rec.salary);
    END LOOP;
    DBMS_OUTPUT.PUT_LINE('No employees found for department 10.');

END;
/
```

**Output:**

```
--- Employees in Department 90 (using parameter) ---
Name: Lex De Haan, Salary: 17000
Name: Steven King, Salary: 26400
Name: Neena Kochhar, Salary: 17000

--- Employees in Department 60 (using parameter) ---
Name: Bruce Ernst, Salary: 6000
Name: Alexander Hunold, Salary: 9900
Name: Diana Lorentz, Salary: 4200

--- Employees in Department 10 (non-existent) ---
No employees found for department 10.

PL/SQL procedure successfully completed.
```

---

#### 2.4. Explicit Cursor with `FOR UPDATE` (for locking)

The `FOR UPDATE` clause is used to explicitly lock the rows returned by the cursor's `SELECT` statement. This prevents other sessions from updating or deleting these rows until your transaction commits or rolls back. It's often used when you intend to modify the fetched rows later in the same transaction using `WHERE CURRENT OF cursor_name`.

**Input (PL/SQL Block):**

```sql
SET SERVEROUTPUT ON;
DECLARE
    -- Cursor with FOR UPDATE clause
    CURSOR emp_sal_upd_cursor IS
        SELECT employee_id, first_name, salary
        FROM employees
        WHERE department_id = 60
        FOR UPDATE OF salary; -- Locks the rows for update

    -- Record variable to hold fetched data
    emp_rec emp_sal_upd_cursor%ROWTYPE;

BEGIN
    DBMS_OUTPUT.PUT_LINE('--- Updating Salaries for Department 60 with FOR UPDATE ---');

    OPEN emp_sal_upd_cursor;

    LOOP
        FETCH emp_sal_upd_cursor INTO emp_rec;
        EXIT WHEN emp_sal_upd_cursor%NOTFOUND;

        -- Simulate some processing time
        -- DBMS_LOCK.SLEEP(1);

        -- Update the salary for the current row
        UPDATE employees
        SET salary = emp_rec.salary * 1.05 -- Increase by 5%
        WHERE CURRENT OF emp_sal_upd_cursor; -- Update the row currently pointed to by the cursor

        DBMS_OUTPUT.PUT_LINE('Updated ID: ' || emp_rec.employee_id || ', New Salary: ' || (emp_rec.salary * 1.05));
    END LOOP;

    CLOSE emp_sal_upd_cursor;
    COMMIT; -- Release the locks and save changes
    DBMS_OUTPUT.PUT_LINE('--- Update complete and transaction committed ---');

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK; -- Rollback if any error occurs
        DBMS_OUTPUT.PUT_LINE('An error occurred: ' || SQLERRM);
        IF emp_sal_upd_cursor%ISOPEN THEN
            CLOSE emp_sal_upd_cursor;
        END IF;
END;
/
```

**Output:**

```
--- Updating Salaries for Department 60 with FOR UPDATE ---
Updated ID: 103, New Salary: 10395
Updated ID: 104, New Salary: 6300
Updated ID: 105, New Salary: 4410
--- Update complete and transaction committed ---

PL/SQL procedure successfully completed.
```

---

### Best Practices for Cursors

1.  **Use Cursor `FOR` Loops:** Whenever possible, use cursor `FOR` loops for their simplicity, automatic resource management, and robust error handling.
2.  **Explicitly Close Cursors (if not using `FOR` loop):** Always ensure that explicitly opened cursors are closed, even if an exception occurs. Use an `EXCEPTION` block to handle this.
3.  **Avoid Unnecessary Cursors:** For single-row lookups, `SELECT INTO` is more efficient than an explicit cursor. Handle `NO_DATA_FOUND` with `SELECT INTO`.
4.  **Batch Processing:** For very large data sets, consider `BULK COLLECT` and `FORALL` for improved performance by minimizing context switching between SQL and PL/SQL.
5.  **`FOR UPDATE` with `WHERE CURRENT OF`:** Use these together when you need to lock rows and perform row-level updates based on the fetched data.
6.  **Parameterize Cursors:** Use cursor parameters to make your cursors more flexible and reusable.

Understanding cursors is fundamental for writing robust and efficient PL/SQL programs that interact with data in Oracle databases.