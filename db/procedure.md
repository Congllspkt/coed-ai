This document provides a detailed explanation of `PROCEDURE` in Oracle SQL, including its purpose, syntax, parameter types, and practical examples with input and output.

---

# Oracle SQL Procedures

## Table of Contents
1.  [Introduction to Procedures](#1-introduction-to-procedures)
2.  [Why Use Procedures?](#2-why-use-procedures)
3.  [Basic Syntax](#3-basic-syntax)
4.  [Parameter Modes (IN, OUT, IN OUT)](#4-parameter-modes-in-out-in-out)
    *   [IN Parameter](#in-parameter)
    *   [OUT Parameter](#out-parameter)
    *   [IN-OUT Parameter](#in-out-parameter)
5.  [Setup: Sample Table and Data](#5-setup-sample-table-and-data)
6.  [Examples](#6-examples)
    *   [Example 1: Procedure without Parameters](#example-1-procedure-without-parameters)
    *   [Example 2: Procedure with IN Parameters](#example-2-procedure-with-in-parameters)
    *   [Example 3: Procedure with OUT Parameters](#example-3-procedure-with-out-parameters)
    *   [Example 4: Procedure with IN-OUT Parameters](#example-4-procedure-with-in-out-parameters)
    *   [Example 5: Procedure with Error Handling](#example-5-procedure-with-error-handling)
7.  [Executing Procedures](#7-executing-procedures)
8.  [Dropping Procedures](#8-dropping-procedures)
9.  [Conclusion](#9-conclusion)

---

## 1. Introduction to Procedures

In Oracle SQL (specifically PL/SQL), a **procedure** is a named PL/SQL block that performs one or more actions. Unlike functions, procedures do not necessarily return a value, although they can return multiple values through `OUT` parameters. Procedures are pre-compiled and stored in the database, making them reusable and efficient.

They are an integral part of application development in Oracle, allowing complex business logic to be encapsulated and executed easily.

## 2. Why Use Procedures?

Using procedures offers several significant advantages:

*   **Modularity:** Break down complex tasks into smaller, manageable units, improving code organization and readability.
*   **Reusability:** Once created, a procedure can be called multiple times from different applications or other PL/SQL blocks, reducing code duplication.
*   **Performance:** Procedures are compiled once and stored in the database. Subsequent calls execute the pre-compiled code, leading to faster execution times.
*   **Security:** Users can be granted privileges to execute a procedure without being granted direct access to the underlying tables, enhancing data security.
*   **Data Integrity:** Procedures can enforce complex business rules and data validation logic, ensuring data consistency.
*   **Reduced Network Traffic:** Instead of sending multiple SQL statements over the network, an application can call a single procedure that executes all necessary operations on the server side.

## 3. Basic Syntax

The basic syntax for creating a procedure in Oracle SQL is:

```sql
CREATE [OR REPLACE] PROCEDURE procedure_name
    (parameter1_name [IN | OUT | IN OUT] datatype [DEFAULT default_value],
     parameter2_name [IN | OUT | IN OUT] datatype,
     ...)
[AUTHID DEFINER | CURRENT_USER] -- Optional: Specifies the rights for procedure execution
IS | AS
    -- Declaration section (optional):
    -- Declare local variables, cursors, nested subprograms, etc.
BEGIN
    -- Executable section:
    -- SQL statements and PL/SQL code
    -- Business logic goes here
EXCEPTION
    -- Exception handling section (optional):
    -- Handle errors that might occur during execution
    WHEN exception_name THEN
        -- Handle the specific exception
    WHEN OTHERS THEN
        -- Handle any other unhandled exception
END [procedure_name];
/
```

**Key Components:**

*   `CREATE [OR REPLACE] PROCEDURE procedure_name`:
    *   `CREATE`: Creates a new procedure.
    *   `OR REPLACE`: If a procedure with `procedure_name` already exists, it will be dropped and recreated without an error.
*   `(`...`)`: Defines the parameters the procedure accepts. Each parameter has a name, a mode (`IN`, `OUT`, `IN OUT`), a data type, and optionally a default value.
*   `IS` or `AS`: Separates the procedure header from its body.
*   `DECLARE` section (implicit before `BEGIN`): Used to declare local variables, constants, cursors, and other PL/SQL constructs that are only visible within the procedure.
*   `BEGIN...END;`: Encapsulates the executable part of the procedure, containing SQL statements and PL/SQL code.
*   `EXCEPTION...END;`: An optional section for handling errors gracefully.

## 4. Parameter Modes (IN, OUT, IN OUT)

Parameters allow you to pass values into a procedure and/or receive values back from it. There are three modes for parameters:

### IN Parameter

*   **Purpose:** Used to pass values *into* the procedure. The procedure can read the value but cannot modify it.
*   **Default Mode:** If no mode is specified, `IN` is the default.
*   **Example Usage:** Providing an employee ID to retrieve their details, or an amount to update a balance.

### OUT Parameter

*   **Purpose:** Used to return values *from* the procedure to the calling environment. The procedure can assign a value to an `OUT` parameter, but it cannot read its initial value.
*   **Requirement:** An `OUT` parameter must be a variable in the calling program to store the returned value.
*   **Example Usage:** Returning an employee's name and salary based on their ID, or the status of an operation.

### IN-OUT Parameter

*   **Purpose:** Used to pass an initial value *into* the procedure, which can then be modified *within* the procedure, and the modified value is returned *out* to the calling environment.
*   **Requirement:** An `IN OUT` parameter must be a variable in the calling program.
*   **Example Usage:** Passing an account balance, performing a transaction (e.g., deposit or withdrawal), and returning the new balance.

---

## 5. Setup: Sample Table and Data

Before diving into examples, let's create a simple `employees` table and insert some data that our procedures will interact with.

**Input (SQL):**

```sql
-- Drop table if it exists to ensure a clean start
DROP TABLE employees PURGE;

-- Create the employees table
CREATE TABLE employees (
    employee_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(100),
    salary NUMBER(10, 2),
    department_id NUMBER
);

-- Insert sample data
INSERT INTO employees (employee_id, first_name, salary, department_id) VALUES (101, 'Alice', 60000.00, 10);
INSERT INTO employees (employee_id, first_name, salary, department_id) VALUES (102, 'Bob', 75000.00, 20);
INSERT INTO employees (employee_id, first_name, salary, department_id) VALUES (103, 'Charlie', 50000.00, 10);
INSERT INTO employees (employee_id, first_name, salary, department_id) VALUES (104, 'David', 90000.00, 30);
INSERT INTO employees (employee_id, first_name, salary, department_id) VALUES (105, 'Eve', 65000.00, 20);

COMMIT;

-- Verify data
SELECT * FROM employees;
```

**Output (Example from SQL Developer/SQL*Plus):**

```
Table dropped.
Table created.
1 row inserted.
1 row inserted.
1 row inserted.
1 row inserted.
1 row inserted.
Commit complete.

EMPLOYEE_ID FIRST_NAME     SALARY DEPARTMENT_ID
----------- ---------- ---------- -------------
        101 Alice         60000.00            10
        102 Bob           75000.00            20
        103 Charlie       50000.00            10
        104 David         90000.00            30
        105 Eve           65000.00            20
```

---

## 6. Examples

### Example 1: Procedure without Parameters

This procedure will simply print a message and update the salaries of all employees in a specific department.

**Input (SQL):**

```sql
-- Create the procedure
CREATE OR REPLACE PROCEDURE increase_dept_salary_fixed
IS
BEGIN
    DBMS_OUTPUT.PUT_LINE('Executing increase_dept_salary_fixed procedure...');

    -- Increase salary for employees in department 10 by 1000
    UPDATE employees
    SET salary = salary + 1000
    WHERE department_id = 10;

    DBMS_OUTPUT.PUT_LINE('Salaries for department 10 increased by 1000.');

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END increase_dept_salary_fixed;
/

-- Execute the procedure
SET SERVEROUTPUT ON; -- Enable DBMS_OUTPUT for seeing messages
EXEC increase_dept_salary_fixed;

-- Verify the changes
SELECT * FROM employees WHERE department_id = 10;
```

**Output (Example from SQL Developer/SQL*Plus):**

```
Procedure INCREASE_DEPT_SALARY_FIXED compiled

Executing increase_dept_salary_fixed procedure...
Salaries for department 10 increased by 1000.

PL/SQL procedure successfully completed.

EMPLOYEE_ID FIRST_NAME     SALARY DEPARTMENT_ID
----------- ---------- ---------- -------------
        101 Alice         61000.00            10
        103 Charlie       51000.00            10
```

### Example 2: Procedure with IN Parameters

This procedure will take an employee ID and an amount as `IN` parameters to increase a specific employee's salary.

**Input (SQL):**

```sql
-- Create the procedure
CREATE OR REPLACE PROCEDURE update_employee_salary (
    p_employee_id IN employees.employee_id%TYPE,
    p_salary_increase_amount IN NUMBER
)
IS
    v_rows_updated NUMBER;
BEGIN
    DBMS_OUTPUT.PUT_LINE('Updating salary for employee ID: ' || p_employee_id || ' by ' || p_salary_increase_amount);

    UPDATE employees
    SET salary = salary + p_salary_increase_amount
    WHERE employee_id = p_employee_id;

    v_rows_updated := SQL%ROWCOUNT;

    IF v_rows_updated = 0 THEN
        DBMS_OUTPUT.PUT_LINE('Employee ID ' || p_employee_id || ' not found.');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Salary updated successfully for employee ID: ' || p_employee_id);
    END IF;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Error updating salary: ' || SQLERRM);
END update_employee_salary;
/

-- Execute the procedure (increase salary for Bob (102) by 2500)
SET SERVEROUTPUT ON;
EXEC update_employee_salary(102, 2500);

-- Execute the procedure for a non-existent employee
EXEC update_employee_salary(999, 1000);

-- Verify the changes for Bob
SELECT * FROM employees WHERE employee_id = 102;
```

**Output (Example from SQL Developer/SQL*Plus):**

```
Procedure UPDATE_EMPLOYEE_SALARY compiled

Updating salary for employee ID: 102 by 2500
Salary updated successfully for employee ID: 102

PL/SQL procedure successfully completed.

Updating salary for employee ID: 999 by 1000
Employee ID 999 not found.

PL/SQL procedure successfully completed.

EMPLOYEE_ID FIRST_NAME     SALARY DEPARTMENT_ID
----------- ---------- ---------- -------------
        102 Bob           77500.00            20
```

### Example 3: Procedure with OUT Parameters

This procedure will take an employee ID (`IN`) and return the employee's first name and current salary (`OUT`).

**Input (SQL):**

```sql
-- Create the procedure
CREATE OR REPLACE PROCEDURE get_employee_details (
    p_employee_id IN employees.employee_id%TYPE,
    p_first_name OUT employees.first_name%TYPE,
    p_salary OUT employees.salary%TYPE
)
IS
BEGIN
    SELECT first_name, salary
    INTO p_first_name, p_salary
    FROM employees
    WHERE employee_id = p_employee_id;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        p_first_name := NULL;
        p_salary := NULL;
        DBMS_OUTPUT.PUT_LINE('Employee ID ' || p_employee_id || ' not found.');
    WHEN OTHERS THEN
        p_first_name := NULL;
        p_salary := NULL;
        DBMS_OUTPUT.PUT_LINE('Error retrieving employee details: ' || SQLERRM);
END get_employee_details;
/

-- Execute the procedure
SET SERVEROUTPUT ON;
DECLARE
    v_first_name employees.first_name%TYPE;
    v_salary employees.salary%TYPE;
BEGIN
    -- Get details for Alice (101)
    get_employee_details(101, v_first_name, v_salary);
    IF v_first_name IS NOT NULL THEN
        DBMS_OUTPUT.PUT_LINE('Employee ID 101: Name = ' || v_first_name || ', Salary = ' || v_salary);
    END IF;

    -- Try to get details for a non-existent employee
    get_employee_details(888, v_first_name, v_salary);
    IF v_first_name IS NOT NULL THEN -- This block won't execute for 888
        DBMS_OUTPUT.PUT_LINE('Employee ID 888: Name = ' || v_first_name || ', Salary = ' || v_salary);
    END IF;
END;
/
```

**Output (Example from SQL Developer/SQL*Plus):**

```
Procedure GET_EMPLOYEE_DETAILS compiled

Employee ID 101: Name = Alice, Salary = 61000
Employee ID 888 not found.

PL/SQL procedure successfully completed.
```

### Example 4: Procedure with IN-OUT Parameters

This procedure will take an employee ID (`IN`) and an existing salary value (`IN OUT`). It will calculate a new salary based on a percentage increase and return the new salary via the same `IN OUT` parameter.

**Input (SQL):**

```sql
-- Create the procedure
CREATE OR REPLACE PROCEDURE apply_salary_increase_and_get_new (
    p_employee_id IN employees.employee_id%TYPE,
    p_increase_percent IN NUMBER,
    p_current_salary IN OUT employees.salary%TYPE -- IN OUT parameter
)
IS
    v_new_salary employees.salary%TYPE;
BEGIN
    -- Retrieve current salary if p_current_salary was not passed or for validation
    -- For an IN OUT parameter, p_current_salary *already contains* the value passed in.
    -- We can choose to use the passed value or fetch from the DB.
    -- Let's fetch from DB for robustness and to illustrate.
    SELECT salary
    INTO p_current_salary -- Update the IN OUT parameter with DB value
    FROM employees
    WHERE employee_id = p_employee_id;

    DBMS_OUTPUT.PUT_LINE('Original salary for employee ' || p_employee_id || ': ' || p_current_salary);

    -- Calculate new salary
    v_new_salary := p_current_salary * (1 + p_increase_percent / 100);

    -- Update the employee's salary in the database
    UPDATE employees
    SET salary = v_new_salary
    WHERE employee_id = p_employee_id;

    -- Assign the new salary back to the IN OUT parameter
    p_current_salary := v_new_salary;

    DBMS_OUTPUT.PUT_LINE('New salary for employee ' || p_employee_id || ': ' || p_current_salary);
    COMMIT;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Employee ID ' || p_employee_id || ' not found.');
        p_current_salary := NULL; -- Indicate no valid salary was returned
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Error applying salary increase: ' || SQLERRM);
        p_current_salary := NULL; -- Indicate no valid salary was returned
END apply_salary_increase_and_get_new;
/

-- Execute the procedure
SET SERVEROUTPUT ON;
DECLARE
    v_emp_id NUMBER := 103; -- Charlie
    v_percentage NUMBER := 10; -- 10% increase
    v_salary employees.salary%TYPE;
BEGIN
    -- We don't need to initialize v_salary here if we fetch it inside the procedure.
    -- However, it must be declared as a variable.
    DBMS_OUTPUT.PUT_LINE('--- Before Procedure Call ---');
    SELECT salary INTO v_salary FROM employees WHERE employee_id = v_emp_id;
    DBMS_OUTPUT.PUT_LINE('Charlie''s initial salary from DB: ' || v_salary);

    -- Call the procedure. v_salary will be passed in, modified, and returned.
    apply_salary_increase_and_get_new(v_emp_id, v_percentage, v_salary);

    DBMS_OUTPUT.PUT_LINE('--- After Procedure Call ---');
    DBMS_OUTPUT.PUT_LINE('Charlie''s new salary (returned via IN OUT): ' || v_salary);

    -- Verify the actual change in the database
    SELECT salary INTO v_salary FROM employees WHERE employee_id = v_emp_id;
    DBMS_OUTPUT.PUT_LINE('Charlie''s new salary from DB: ' || v_salary);
END;
/
```

**Output (Example from SQL Developer/SQL*Plus):**

```
Procedure APPLY_SALARY_INCREASE_AND_GET_NEW compiled

--- Before Procedure Call ---
Charlie's initial salary from DB: 51000
Original salary for employee 103: 51000
New salary for employee 103: 56100
--- After Procedure Call ---
Charlie's new salary (returned via IN OUT): 56100
Charlie's new salary from DB: 56100

PL/SQL procedure successfully completed.
```

### Example 5: Procedure with Error Handling

This example demonstrates using an `EXCEPTION` block to handle a common error: `NO_DATA_FOUND` (when a `SELECT INTO` statement returns no rows).

**Input (SQL):**

```sql
-- Create the procedure with error handling
CREATE OR REPLACE PROCEDURE get_employee_email (
    p_employee_id IN employees.employee_id%TYPE,
    p_email OUT VARCHAR2 -- Assuming email column could be added or exists
)
IS
    v_email_local VARCHAR2(100);
BEGIN
    -- This example assumes 'email' column exists, let's update our table temporarily
    -- If you are following exactly, add email column first.
    -- ALTER TABLE employees ADD email VARCHAR2(100);
    -- UPDATE employees SET email = LOWER(first_name) || '@example.com' WHERE employee_id = 101;
    -- UPDATE employees SET email = LOWER(first_name) || '@example.com' WHERE employee_id = 102;
    -- For simplicity, let's stick to first_name and handle NO_DATA_FOUND.

    SELECT first_name -- Use first_name as a placeholder for a column that might not be found
    INTO v_email_local -- Assign to a local variable
    FROM employees
    WHERE employee_id = p_employee_id;

    p_email := v_email_local || '@example.com'; -- Simulate email generation

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Error: Employee ID ' || p_employee_id || ' not found.');
        p_email := NULL; -- Set OUT parameter to NULL to indicate no data
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('An unexpected error occurred: ' || SQLERRM);
        p_email := NULL;
END get_employee_email;
/

-- Execute the procedure with a valid ID
SET SERVEROUTPUT ON;
DECLARE
    v_emp_id NUMBER := 104; -- David
    v_email_address VARCHAR2(100);
BEGIN
    get_employee_email(v_emp_id, v_email_address);
    IF v_email_address IS NOT NULL THEN
        DBMS_OUTPUT.PUT_LINE('Employee ' || v_emp_id || ' email: ' || v_email_address);
    ELSE
        DBMS_OUTPUT.PUT_LINE('Could not retrieve email for employee ' || v_emp_id);
    END IF;

    DBMS_OUTPUT.PUT_LINE('---');

    -- Execute the procedure with an invalid ID
    v_emp_id := 999;
    get_employee_email(v_emp_id, v_email_address);
    IF v_email_address IS NOT NULL THEN
        DBMS_OUTPUT.PUT_LINE('Employee ' || v_emp_id || ' email: ' || v_email_address);
    ELSE
        DBMS_OUTPUT.PUT_LINE('Could not retrieve email for employee ' || v_emp_id);
    END IF;
END;
/
```

**Output (Example from SQL Developer/SQL*Plus):**

```
Procedure GET_EMPLOYEE_EMAIL compiled

Employee 104 email: David@example.com
---
Error: Employee ID 999 not found.
Could not retrieve email for employee 999

PL/SQL procedure successfully completed.
```

## 7. Executing Procedures

There are several ways to execute a procedure:

1.  **Using `EXEC` or `EXECUTE` (SQL*Plus/SQL Developer shorthand):**
    ```sql
    EXEC procedure_name(arg1, arg2, ...);
    -- or
    EXECUTE procedure_name(arg1, arg2, ...);
    ```
    This is a convenient shorthand for anonymous PL/SQL blocks.

2.  **From a PL/SQL Block:**
    ```sql
    BEGIN
        procedure_name(arg1, arg2, ...);
    END;
    /
    ```
    This is the standard way to call a procedure within another PL/SQL program.
    For `OUT` and `IN OUT` parameters, you must declare variables to hold the returned values.

3.  **From other PL/SQL subprograms (functions, other procedures, packages):**
    Simply call the procedure by its name within the code.

## 8. Dropping Procedures

To remove a procedure from the database, use the `DROP PROCEDURE` statement:

**Input (SQL):**

```sql
DROP PROCEDURE update_employee_salary;
```

**Output (Example):**

```
Procedure dropped.
```

## 9. Conclusion

Procedures are a fundamental building block in Oracle PL/SQL for developing robust, efficient, and maintainable database applications. By understanding their syntax, parameter modes, and how to handle errors, you can effectively encapsulate complex business logic and enhance the overall quality of your database solutions.