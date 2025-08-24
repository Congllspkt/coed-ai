A **function** in Oracle SQL (PL/SQL) is a named PL/SQL block that performs a specific task and **must return a single value**. Functions are primarily used for computations, data transformations, and returning a result based on input parameters.

Unlike procedures, functions can be called directly within SQL statements (e.g., `SELECT`, `WHERE`, `HAVING` clauses), making them very powerful for extending SQL's capabilities.

---

## Table of Contents
1.  [Key Characteristics](#1-key-characteristics)
2.  [Syntax](#2-syntax)
3.  [Detailed Explanation of Components](#3-detailed-explanation-of-components)
4.  [Examples](#4-examples)
    *   [Setup: Sample Table](#setup-sample-table)
    *   [Example 1: Simple Function (No Parameters)](#example-1-simple-function-no-parameters)
    *   [Example 2: Function with `IN` Parameters](#example-2-function-with-in-parameters)
    *   [Example 3: Function Returning a Calculated Value from a Table](#example-3-function-returning-a-calculated-value-from-a-table)
    *   [Example 4: Function with Error Handling](#example-4-function-with-error-handling)
    *   [Example 5: Calling a Function from a PL/SQL Block](#example-5-calling-a-function-from-a-plsql-block)
    *   [Dropping a Function](#dropping-a-function)
5.  [Functions vs. Procedures](#5-functions-vs-procedures)
6.  [Best Practices](#6-best-practices)
7.  [Conclusion](#7-conclusion)
8.  [Cleanup](#cleanup)

---

## 1. Key Characteristics

*   **Returns a Value:** This is the most crucial distinction. A function *must* have a `RETURN` clause specifying the data type of the value it will return, and it *must* execute a `RETURN` statement at some point.
*   **Parameters:** Can accept zero or more input parameters (always `IN` type if called from SQL).
*   **SQL Integration:** Can be called from SQL expressions (e.g., `SELECT` list, `WHERE` clause, `ORDER BY` clause, `HAVING` clause).
*   **Reusability:** Encapsulates business logic, promoting code reuse.
*   **Purity (Recommendation):** For functions called from SQL, it's a strong best practice that they should not perform DML (Data Manipulation Language - `INSERT`, `UPDATE`, `DELETE`) or DDL (Data Definition Language - `CREATE`, `ALTER`, `DROP`) operations. If they do, they are considered "impure" and might lead to unexpected behavior, especially in complex SQL statements or parallel execution. Oracle strictly enforces this for some contexts (e.g., functions called in a `WHERE` clause cannot modify tables).

## 2. Syntax

```sql
CREATE [OR REPLACE] FUNCTION function_name
    [(parameter1 [IN] datatype1,
      parameter2 [IN] datatype2,
      ...)]
    RETURN return_datatype
    [AUTHID {CURRENT_USER | DEFINER}] -- Optional: determines privilege checking
    [DETERMINISTIC]                   -- Optional: for caching and performance
    [PARALLEL_ENABLE]                 -- Optional: for parallel execution
    [RESULT_CACHE]                    -- Optional: for caching function results
    [PRAGMA AUTONOMOUS_TRANSACTION]   -- Optional: for independent transactions
IS | AS
    -- Declaration Section (Optional)
    -- Declare local variables, cursors, etc.
BEGIN
    -- Executable Section (Mandatory)
    -- SQL statements, PL/SQL logic
    -- MUST contain a RETURN statement
    RETURN expression;
EXCEPTION
    -- Exception Handling Section (Optional)
    -- Handle errors gracefully
    WHEN exception_name THEN
        -- Error handling logic
        RETURN alternative_expression; -- Still must return a value
END [function_name];
/
```

## 3. Detailed Explanation of Components

*   **`CREATE [OR REPLACE] FUNCTION function_name`**:
    *   `CREATE`: Creates a new function.
    *   `OR REPLACE`: If a function with `function_name` already exists, it will be dropped and recreated without errors. This is very common for development.
    *   `function_name`: A unique identifier for the function within its schema. Follows Oracle object naming conventions.

*   **`[(parameter1 [IN] datatype1, ...)]`**:
    *   Optional list of input parameters.
    *   `parameterN`: The name of the parameter.
    *   `[IN]`: Specifies the parameter mode. For functions, `IN` is the default and only mode allowed when the function is called from SQL. `OUT` or `IN OUT` parameters are not permitted for functions called directly within SQL queries.
    *   `datatypeN`: The data type of the parameter (e.g., `NUMBER`, `VARCHAR2`, `DATE`).

*   **`RETURN return_datatype`**:
    *   **Mandatory** clause that specifies the data type of the value the function will return. This can be any valid Oracle scalar or composite data type (e.g., `NUMBER`, `VARCHAR2`, `DATE`, `BOOLEAN`, a user-defined type, or a PL/SQL collection type).

*   **`AUTHID {CURRENT_USER | DEFINER}`**:
    *   **`DEFINER` (default):** The function executes with the privileges of the user who *defined* (created) it.
    *   **`CURRENT_USER`:** The function executes with the privileges of the user who *invokes* it. This is useful for building secure applications.

*   **`DETERMINISTIC`**:
    *   Tells Oracle that for a given set of input parameters, the function will *always* return the same result. This allows Oracle to cache function results, which can significantly improve performance when the function is called repeatedly with the same arguments. **Important:** Do not use this if the function's output depends on external factors (like `SYSDATE`, package variables, or table data that might change).

*   **`PARALLEL_ENABLE`**:
    *   Indicates that the function can be executed in parallel for parallelized queries. This is an advanced optimization.

*   **`RESULT_CACHE`**:
    *   Instructs Oracle to cache the results of the function in the shared global area (SGA). If the function is called again with the same parameters and the underlying data it depends on hasn't changed, the cached result is returned, bypassing re-execution of the function body.

*   **`PRAGMA AUTONOMOUS_TRANSACTION`**:
    *   Allows the function to execute its DML operations in an independent transaction that can be committed or rolled back separately from the main transaction that invoked the function. Use with caution.

*   **`IS | AS`**:
    *   Synonyms, simply mark the beginning of the PL/SQL block's declaration section.

*   **Declaration Section (Optional)**:
    *   Where you declare local variables, constants, cursors, nested procedures, or functions that are used only within this function.

*   **Executable Section (Mandatory)**:
    *   Contains the actual PL/SQL logic, SQL statements, and control structures (loops, `IF` statements) that implement the function's task.
    *   **Must contain at least one `RETURN expression;` statement.**

*   **`RETURN expression;`**:
    *   Exits the function and passes `expression` (which must be compatible with `return_datatype`) back to the caller. Every possible execution path within the function must lead to a `RETURN` statement.

*   **Exception Handling Section (Optional)**:
    *   Uses `WHEN` clauses to define actions for specific errors (exceptions). This ensures the function handles unexpected situations gracefully and can return a meaningful error code or default value.
    *   Even in the exception handler, you must return a value of the specified `return_datatype`.

## 4. Examples

Let's illustrate with some examples.

### Setup: Sample Table

First, let's create a sample `employees` table and insert some data to work with:

```sql
-- Drop table if it exists to ensure a clean start
DROP TABLE employees PURGE;

CREATE TABLE employees (
    employee_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50),
    last_name VARCHAR2(50),
    email VARCHAR2(100),
    phone_number VARCHAR2(20),
    hire_date DATE,
    job_id VARCHAR2(10),
    salary NUMBER(10, 2),
    commission_pct NUMBER(2, 2),
    manager_id NUMBER,
    department_id NUMBER
);

INSERT INTO employees VALUES (100, 'Steven', 'King', 'SKING', '515.123.4567', SYSDATE - 1000, 'AD_PRES', 24000, NULL, NULL, 90);
INSERT INTO employees VALUES (101, 'Neena', 'Kochhar', 'NKOCHHAR', '515.123.4568', SYSDATE - 800, 'AD_VP', 17000, NULL, 100, 90);
INSERT INTO employees VALUES (102, 'Lex', 'De Haan', 'LDEHAAN', '515.123.4569', SYSDATE - 600, 'AD_VP', 17000, NULL, 100, 90);
INSERT INTO employees VALUES (103, 'Alexander', 'Hunold', 'AHUNOLD', '590.423.4567', SYSDATE - 500, 'IT_PROG', 9000, NULL, 102, 60);
INSERT INTO employees VALUES (104, 'Bruce', 'Ernst', 'BERNST', '590.423.4568', SYSDATE - 400, 'IT_PROG', 6000, NULL, 103, 60);
INSERT INTO employees VALUES (105, 'David', 'Austin', 'DAUSTIN', '590.423.4569', SYSDATE - 300, 'IT_PROG', 4800, NULL, 103, 60);
INSERT INTO employees VALUES (106, 'Valli', 'Pataballa', 'VPATABAL', '590.423.4560', SYSDATE - 200, 'IT_PROG', 4800, NULL, 103, 60);
INSERT INTO employees VALUES (107, 'Diana', 'Lorentz', 'DLORENTZ', '590.423.5567', SYSDATE - 100, 'IT_PROG', 4200, NULL, 103, 60);
INSERT INTO employees VALUES (108, 'Nancy', 'Greenberg', 'NGREENBE', '515.124.4569', SYSDATE - 150, 'FI_MGR', 12000, NULL, 101, 100);

COMMIT;
```

### Example 1: Simple Function (No Parameters)

This function returns the total number of employees in the `employees` table.

```sql
CREATE OR REPLACE FUNCTION get_total_employees
RETURN NUMBER
IS
    v_total_employees NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_total_employees
    FROM employees;

    RETURN v_total_employees;
END;
/
```

**Input / Output:**

*   **Input:** (No explicit parameters, uses table data)
*   **Call from SQL:**
    ```sql
    SELECT get_total_employees FROM DUAL;
    ```
*   **Output:**
    ```
    GET_TOTAL_EMPLOYEES
    -------------------
                      9
    ```

*   **Call from PL/SQL:**
    ```sql
    SET SERVEROUTPUT ON;
    DECLARE
        employee_count NUMBER;
    BEGIN
        employee_count := get_total_employees;
        DBMS_OUTPUT.PUT_LINE('Total employees: ' || employee_count);
    END;
    /
    ```
*   **Output:**
    ```
    Total employees: 9
    ```

---

### Example 2: Function with `IN` Parameters

This function calculates an employee's annual bonus based on their salary and a given bonus percentage.

```sql
CREATE OR REPLACE FUNCTION calculate_annual_bonus (
    p_salary            IN NUMBER,
    p_bonus_percentage  IN NUMBER
)
RETURN NUMBER
IS
    v_bonus_amount NUMBER;
BEGIN
    IF p_salary IS NULL OR p_bonus_percentage IS NULL THEN
        RETURN 0; -- Or raise an error, depending on business rules
    END IF;

    v_bonus_amount := p_salary * (p_bonus_percentage / 100);
    RETURN v_bonus_amount;
END;
/
```

**Input / Output:**

*   **Input:** `p_salary` (e.g., 60000), `p_bonus_percentage` (e.g., 10)
*   **Call from SQL (with literal values):**
    ```sql
    SELECT calculate_annual_bonus(60000, 10) AS bonus_for_60k_10pct FROM DUAL;
    ```
*   **Output:**
    ```
    BONUS_FOR_60K_10PCT
    -------------------
                   6000
    ```

*   **Call from SQL (using table columns):**
    ```sql
    SELECT
        employee_id,
        first_name,
        salary,
        calculate_annual_bonus(salary, 12) AS annual_bonus_12pct,
        calculate_annual_bonus(salary, 15) AS annual_bonus_15pct
    FROM
        employees
    WHERE
        salary > 10000;
    ```
*   **Output:**
    ```
    EMPLOYEE_ID FIRST_NAME               SALARY ANNUAL_BONUS_12PCT ANNUAL_BONUS_15PCT
    ----------- -------------------- ---------- ------------------ ------------------
            100 Steven                    24000             2880.0             3600.0
            101 Neena                     17000             2040.0             2550.0
            102 Lex                       17000             2040.0             2550.0
            108 Nancy                     12000             1440.0             1800.0
    ```

---

### Example 3: Function Returning a Calculated Value from a Table

This function calculates an employee's age in years based on their `hire_date`.

```sql
CREATE OR REPLACE FUNCTION get_employee_years_of_service (
    p_employee_id IN NUMBER
)
RETURN NUMBER
IS
    v_hire_date DATE;
    v_years_of_service NUMBER;
BEGIN
    SELECT hire_date
    INTO v_hire_date
    FROM employees
    WHERE employee_id = p_employee_id;

    -- Calculate years of service (approximation)
    v_years_of_service := TRUNC(MONTHS_BETWEEN(SYSDATE, v_hire_date) / 12);

    RETURN v_years_of_service;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        -- Handle case where employee_id does not exist
        RETURN NULL; -- Or -1, or raise a custom exception
    WHEN OTHERS THEN
        -- Handle any other unexpected errors
        RETURN NULL;
END;
/
```

**Input / Output:**

*   **Input:** `p_employee_id` (e.g., 100)
*   **Call from SQL:**
    ```sql
    SELECT
        employee_id,
        first_name || ' ' || last_name AS full_name,
        hire_date,
        get_employee_years_of_service(employee_id) AS years_of_service
    FROM
        employees
    WHERE
        employee_id IN (100, 103, 107, 999); -- 999 to test NO_DATA_FOUND
    ```
*   **Output:** (Note: Years of service will vary based on `SYSDATE` when you run it)
    ```
    EMPLOYEE_ID FULL_NAME            HIRE_DATE YEARS_OF_SERVICE
    ----------- -------------------- --------- ----------------
            100 Steven King          16-JAN-24                2
            103 Alexander Hunold     16-APR-24                1
            107 Diana Lorentz        25-JUL-24                0
            999                      (null)             (null)
    ```

---

### Example 4: Function with Error Handling

This function converts a temperature from Celsius to Fahrenheit, including robust error handling for invalid input.

```sql
CREATE OR REPLACE FUNCTION celsius_to_fahrenheit (
    p_celsius_temp IN NUMBER
)
RETURN NUMBER
IS
    v_fahrenheit_temp NUMBER;
BEGIN
    IF p_celsius_temp IS NULL THEN
        -- Optionally, treat NULL as an error or return NULL
        RAISE_APPLICATION_ERROR(-20001, 'Input Celsius temperature cannot be NULL.');
    END IF;

    v_fahrenheit_temp := (p_celsius_temp * 9/5) + 32;
    RETURN v_fahrenheit_temp;

EXCEPTION
    WHEN OTHERS THEN
        -- Log the error and return a specific indicator or re-raise
        DBMS_OUTPUT.PUT_LINE('Error converting Celsius to Fahrenheit: ' || SQLERRM);
        -- For a function, we must still return a value compatible with the RETURN type.
        -- Returning NULL or a specific error code like -9999 is common.
        RETURN NULL;
END;
/
```

**Input / Output:**

*   **Input 1:** `p_celsius_temp` = 25
*   **Call from SQL:**
    ```sql
    SELECT celsius_to_fahrenheit(25) AS temp_fahrenheit FROM DUAL;
    ```
*   **Output 1:**
    ```
    TEMP_FAHRENHEIT
    ---------------
                 77
    ```

*   **Input 2:** `p_celsius_temp` = NULL (to trigger custom error)
*   **Call from SQL:**
    ```sql
    SELECT celsius_to_fahrenheit(NULL) AS temp_fahrenheit FROM DUAL;
    ```
*   **Output 2:** (Depending on your SQL client, you might see the error directly, or a NULL if the exception handler catches it gracefully and returns NULL)
    ```
    Error starting at line : 1 in command -
    SELECT celsius_to_fahrenheit(NULL) AS temp_fahrenheit FROM DUAL
    Error report -
    ORA-20001: Input Celsius temperature cannot be NULL.
    ORA-06512: at "YOUR_SCHEMA.CELSIUS_TO_FAHRENHEIT", line 8
    ORA-06512: at line 1
    ```
    *Note: If you modify the exception to handle the `RAISE_APPLICATION_ERROR` directly and return `NULL`, the SQL output would just show `NULL`.*

---

### Example 5: Calling a Function from a PL/SQL Block

You can easily call functions from within other PL/SQL blocks, procedures, or even other functions.

```sql
SET SERVEROUTPUT ON;

DECLARE
    v_employee_id NUMBER := 101;
    v_salary      NUMBER;
    v_bonus       NUMBER;
    v_years       NUMBER;
BEGIN
    -- Get salary from employee table
    SELECT salary
    INTO v_salary
    FROM employees
    WHERE employee_id = v_employee_id;

    -- Call calculate_annual_bonus function
    v_bonus := calculate_annual_bonus(v_salary, 10); -- 10% bonus
    DBMS_OUTPUT.PUT_LINE('Employee ' || v_employee_id || ' annual bonus: ' || v_bonus);

    -- Call get_employee_years_of_service function
    v_years := get_employee_years_of_service(v_employee_id);
    DBMS_OUTPUT.PUT_LINE('Employee ' || v_employee_id || ' years of service: ' || v_years);

END;
/
```

**Input / Output:**

*   **Input:** `v_employee_id` = 101 (hardcoded in the block)
*   **Output:** (Years of service will vary based on `SYSDATE`)
    ```
    Employee 101 annual bonus: 1700
    Employee 101 years of service: 2
    ```

---

### Dropping a Function

To remove a function from the database:

```sql
DROP FUNCTION get_total_employees;
DROP FUNCTION calculate_annual_bonus;
DROP FUNCTION get_employee_years_of_service;
DROP FUNCTION celsius_to_fahrenheit;
```

---

## 5. Functions vs. Procedures

While both are named PL/SQL blocks, their primary purpose and usage differ:

| Feature           | Function                                    | Procedure                                          |
| :---------------- | :------------------------------------------ | :------------------------------------------------- |
| **Return Value**  | **MUST** return a single value.             | **Does not** return a value, or can return multiple values via `OUT` parameters. |
| **SQL Usage**     | Can be called in SQL expressions (`SELECT`, `WHERE`, `HAVING`). | **Cannot** be called directly in SQL expressions. Can be called from PL/SQL blocks using `EXECUTE` or `CALL`. |
| **Parameters**    | Primarily `IN` parameters (only `IN` if called from SQL). | Can have `IN`, `OUT`, and `IN OUT` parameters.    |
| **DML/DDL**       | Best practice: Avoid DML/DDL if called from SQL (`PURE` functions). Some contexts strictly enforce this. | Often used to perform DML/DDL operations (e.g., inserting data, updating records). |
| **Primary Use**   | Calculations, data transformations, returning a derived value. | Performing actions, managing transactions, executing a series of DML operations. |
| **Mandatory Keywords** | `RETURN return_datatype` in header, `RETURN expression;` in body. | None for return value. |

---

## 6. Best Practices

*   **Purity:** If a function is meant to be used in SQL queries, it should ideally be "pure" – meaning it doesn't modify database state (no DML/DDL), and its result depends only on its input parameters and existing database data (which isn't modified by the function itself). Use `DETERMINISTIC` if truly pure and performance benefits are desired.
*   **Error Handling:** Always include an `EXCEPTION` section to handle potential errors gracefully. This prevents the calling application from crashing and allows for returning a meaningful default, NULL, or error message.
*   **Naming Conventions:** Use meaningful names that describe the function's purpose (e.g., `GET_TOTAL_SALARY`, `CALCULATE_DISCOUNT`).
*   **Simplicity:** Keep functions focused on a single, well-defined task. Complex logic can be broken down into smaller, more manageable functions or procedures.
*   **Packages:** For related functions, consider organizing them into PL/SQL packages. Packages offer better organization, encapsulation, and can improve performance due to single compilation.
*   **Return NULL vs. Raise Error:** Decide whether to return `NULL` (for "no result" or "invalid input") or `RAISE_APPLICATION_ERROR` (for unrecoverable errors) based on your application's error handling strategy.

---

## 7. Conclusion

Functions in Oracle SQL are powerful tools for encapsulating business logic, performing computations, and extending the capabilities of SQL statements. By understanding their characteristics, syntax, and best practices, you can write efficient, maintainable, and robust PL/SQL code. The key takeaway is that a function *always* returns a single value, which makes it suitable for integration directly into SQL queries as expressions.

---

## Cleanup

To remove the table used in the examples:

```sql
DROP TABLE employees PURGE;
```