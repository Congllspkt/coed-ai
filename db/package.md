Oracle PL/SQL Packages are powerful schema objects that logically group related PL/SQL types, items, and subprograms (procedures and functions). They are fundamental for building modular, maintainable, and efficient applications in an Oracle database.

---

# Oracle PL/SQL Package: A Comprehensive Guide

## Table of Contents

1.  [Introduction](#1-introduction)
2.  [Key Concepts](#2-key-concepts)
    *   [Package Specification (Header)](#package-specification-header)
    *   [Package Body (Implementation)](#package-body-implementation)
    *   [Public vs. Private Items](#public-vs-private-items)
3.  [Advantages of Using Packages](#3-advantages-of-using-packages)
4.  [Syntax](#4-syntax)
5.  [Detailed Examples](#5-detailed-examples)
    *   [Example 1: Basic Package with Procedures and Functions](#example-1-basic-package-with-procedures-and-functions)
    *   [Example 2: Package Variables and Constants (Session-Specific)](#example-2-package-variables-and-constants-session-specific)
    *   [Example 3: Package Initialization Block](#example-3-package-initialization-block)
    *   [Example 4: Overloading Procedures/Functions](#example-4-overloading-proceduresfunctions)
    *   [Example 5: Using Cursors and Records in a Package](#example-5-using-cursors-and-records-in-a-package)
6.  [How to Use/Execute Package Components](#6-how-to-useexecute-package-components)
7.  [How to Drop a Package](#7-how-to-drop-a-package)
8.  [Important Considerations and Best Practices](#8-important-considerations-and-best-practices)
9.  [Conclusion](#9-conclusion)

---

## 1. Introduction

An Oracle PL/SQL Package is a schema object that groups related PL/SQL elements like procedures, functions, variables, constants, cursors, and user-defined types. It consists of two separate parts: a **specification** (or header) and a **body** (or implementation).

Packages promote modularity, reusability, and encapsulation, making database application development more organized and efficient.

## 2. Key Concepts

### Package Specification (Header)

The package specification is the public interface to the package. It declares the *public* items that are accessible from outside the package. It tells users what items are available and how to call them, but not how they are implemented.

*   **What it contains:** Declarations of public procedures, functions, variables, constants, cursors, and types.
*   **Purpose:** To define the interface for external applications and other PL/SQL units.

### Package Body (Implementation)

The package body contains the actual implementation (code) for the procedures and functions declared in the specification. It can also declare and define *private* items (procedures, functions, variables, etc.) that are only accessible from within the package body itself.

*   **What it contains:** Definitions of public procedures/functions declared in the spec, and declarations/definitions of private procedures/functions/variables.
*   **Purpose:** To provide the working code for the public interface and any internal helper logic.

### Public vs. Private Items

*   **Public Items:**
    *   Declared in the **package specification**.
    *   Defined (if procedures/functions) in the **package body**.
    *   Accessible from outside the package (e.g., from SQL, other PL/SQL blocks, applications).
    *   Example: A `PROCEDURE` declared in the spec.

*   **Private Items:**
    *   Declared *and* defined only in the **package body**.
    *   Not visible or accessible from outside the package.
    *   Used for internal helper functions, variables, or logic specific to the package's implementation.
    *   Example: A helper `FUNCTION` defined only in the body.

## 3. Advantages of Using Packages

1.  **Modularization:** Break down large applications into logical, manageable units.
2.  **Encapsulation & Data Hiding:** Hide implementation details from users. Users only see the specification, not the internal workings. Private variables and procedures protect internal state and logic.
3.  **Reusability:** Common procedures, functions, and types can be grouped and reused across multiple applications or parts of an application.
4.  **Performance:**
    *   When a package component is called for the first time in a session, the entire package (both spec and body) is loaded into memory.
    *   Subsequent calls to *any* component within the same package in that session are much faster as the code is already in memory.
5.  **Security:** Granting `EXECUTE` privilege on a package allows users to run its public components without needing direct privileges on underlying tables or individual procedures/functions. This simplifies privilege management.
6.  **Maintainability:** Changes to a package body do not invalidate dependent objects, provided the package specification remains unchanged. This reduces recompilation cascades.
7.  **Persistent Session State:** Package variables (global variables within the package) maintain their values for the duration of a user's session, acting like session-specific global variables.
8.  **Overloading:** Allows defining multiple procedures or functions with the same name within the same package, but with different parameter signatures (different number, order, or data types of parameters).

## 4. Syntax

```sql
-- Package Specification
CREATE OR REPLACE PACKAGE package_name AS
  -- Public declarations
  -- (Procedures, Functions, Variables, Constants, Cursors, Types)

  -- Example: Public Procedure
  PROCEDURE my_public_procedure (
    p_param1 IN NUMBER,
    p_param2 OUT VARCHAR2
  );

  -- Example: Public Function
  FUNCTION my_public_function (
    p_input IN DATE
  ) RETURN BOOLEAN;

  -- Example: Public Variable
  g_session_counter NUMBER := 0;

  -- Example: Public Constant
  c_max_retries CONSTANT NUMBER := 3;

  -- Example: Public Cursor
  CURSOR c_employees IS
    SELECT employee_id, first_name, last_name FROM employees;

  -- Example: Public Type
  TYPE t_employee_rec IS RECORD (
    id        employees.employee_id%TYPE,
    full_name VARCHAR2(100)
  );
  TYPE t_employee_list IS TABLE OF t_employee_rec INDEX BY PLS_INTEGER;

END package_name;
/


-- Package Body
CREATE OR REPLACE PACKAGE BODY package_name AS
  -- Private declarations and definitions (optional)
  -- These are only accessible within this package body.

  -- Example: Private Function
  FUNCTION calculate_checksum (p_data IN VARCHAR2) RETURN VARCHAR2 IS
  BEGIN
    -- Some complex calculation
    RETURN 'CHKSUM_' || SUBSTR(p_data, 1, 5);
  END calculate_checksum;

  -- Implementations for public procedures/functions (must match spec)

  PROCEDURE my_public_procedure (
    p_param1 IN NUMBER,
    p_param2 OUT VARCHAR2
  ) AS
  BEGIN
    DBMS_OUTPUT.PUT_LINE('Executing my_public_procedure with input: ' || p_param1);
    p_param2 := 'Output for ' || p_param1 || ' processed by ' || calculate_checksum('data');
    g_session_counter := g_session_counter + 1; -- Update public package variable
  END my_public_procedure;

  FUNCTION my_public_function (
    p_input IN DATE
  ) RETURN BOOLEAN AS
  BEGIN
    DBMS_OUTPUT.PUT_LINE('Executing my_public_function with input date: ' || TO_CHAR(p_input, 'YYYY-MM-DD'));
    RETURN p_input > SYSDATE - 7; -- True if date is within last 7 days
  END my_public_function;

  -- Optional: Package Initialization Block
  -- This block runs once per session when the package is first referenced.
  BEGIN
    DBMS_OUTPUT.PUT_LINE('Package ' || $$PLSQL_UNIT || ' initialized at ' || TO_CHAR(SYSTIMESTAMP, 'HH24:MI:SS'));
    g_session_counter := 0; -- Ensure counter starts at 0 for each session
  END package_name;
/
```

---

## 5. Detailed Examples

Let's use a sample `EMPLOYEES` table for some examples.

```sql
-- Create a sample EMPLOYEES table if it doesn't exist
CREATE TABLE employees (
    employee_id    NUMBER PRIMARY KEY,
    first_name     VARCHAR2(50),
    last_name      VARCHAR2(50),
    email          VARCHAR2(100) UNIQUE,
    phone_number   VARCHAR2(20),
    hire_date      DATE,
    job_id         VARCHAR2(10),
    salary         NUMBER(8, 2),
    department_id  NUMBER
);

-- Insert some sample data
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id) VALUES
(100, 'John', 'Doe', 'john.doe@example.com', '555-1111', TO_DATE('2020-01-15', 'YYYY-MM-DD'), 'IT_PROG', 60000, 10);
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id) VALUES
(101, 'Jane', 'Smith', 'jane.smith@example.com', '555-2222', TO_DATE('2019-03-20', 'YYYY-MM-DD'), 'SA_REP', 75000, 20);
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id) VALUES
(102, 'Peter', 'Jones', 'peter.jones@example.com', '555-3333', TO_DATE('2021-07-01', 'YYYY-MM-DD'), 'HR_REP', 50000, 30);
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id) VALUES
(103, 'Alice', 'Williams', 'alice.williams@example.com', '555-4444', TO_DATE('2018-11-10', 'YYYY-MM-DD'), 'IT_PROG', 80000, 10);
COMMIT;
```

### Example 1: Basic Package with Procedures and Functions

This example demonstrates a simple package for employee management, including adding a new employee and getting an employee's full name.

**Input (Specification):**

```sql
CREATE OR REPLACE PACKAGE employee_pkg AS
  -- Public Procedure to add a new employee
  PROCEDURE add_employee (
    p_employee_id    IN employees.employee_id%TYPE,
    p_first_name     IN employees.first_name%TYPE,
    p_last_name      IN employees.last_name%TYPE,
    p_email          IN employees.email%TYPE,
    p_phone_number   IN employees.phone_number%TYPE,
    p_hire_date      IN employees.hire_date%TYPE,
    p_job_id         IN employees.job_id%TYPE,
    p_salary         IN employees.salary%TYPE,
    p_department_id  IN employees.department_id%TYPE
  );

  -- Public Function to get an employee's full name
  FUNCTION get_full_name (
    p_employee_id IN employees.employee_id%TYPE
  ) RETURN VARCHAR2;

  -- Public Function to check if an employee exists
  FUNCTION employee_exists (
    p_employee_id IN employees.employee_id%TYPE
  ) RETURN BOOLEAN;

END employee_pkg;
/
```

**Input (Body):**

```sql
CREATE OR REPLACE PACKAGE BODY employee_pkg AS

  -- Private function (only callable within this package body)
  FUNCTION is_valid_salary (p_salary IN employees.salary%TYPE) RETURN BOOLEAN AS
  BEGIN
    RETURN p_salary >= 0 AND p_salary <= 200000; -- Example: Salary range check
  END is_valid_salary;

  -- Implementation of add_employee procedure
  PROCEDURE add_employee (
    p_employee_id    IN employees.employee_id%TYPE,
    p_first_name     IN employees.first_name%TYPE,
    p_last_name      IN employees.last_name%TYPE,
    p_email          IN employees.email%TYPE,
    p_phone_number   IN employees.phone_number%TYPE,
    p_hire_date      IN employees.hire_date%TYPE,
    p_job_id         IN employees.job_id%TYPE,
    p_salary         IN employees.salary%TYPE,
    p_department_id  IN employees.department_id%TYPE
  ) AS
  BEGIN
    IF NOT is_valid_salary(p_salary) THEN
      RAISE_APPLICATION_ERROR(-20001, 'Invalid salary provided. Salary must be between 0 and 200000.');
    END IF;

    INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id)
    VALUES (p_employee_id, p_first_name, p_last_name, p_email, p_phone_number, p_hire_date, p_job_id, p_salary, p_department_id);
    DBMS_OUTPUT.PUT_LINE('Employee ' || p_first_name || ' ' || p_last_name || ' added successfully.');
  EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
      RAISE_APPLICATION_ERROR(-20002, 'Employee ID or Email already exists.');
    WHEN OTHERS THEN
      RAISE_APPLICATION_ERROR(-20003, 'Error adding employee: ' || SQLERRM);
  END add_employee;

  -- Implementation of get_full_name function
  FUNCTION get_full_name (
    p_employee_id IN employees.employee_id%TYPE
  ) RETURN VARCHAR2 AS
    v_full_name VARCHAR2(101); -- 50 + 1 + 50
  BEGIN
    SELECT first_name || ' ' || last_name
    INTO v_full_name
    FROM employees
    WHERE employee_id = p_employee_id;

    RETURN v_full_name;
  EXCEPTION
    WHEN NO_DATA_FOUND THEN
      RETURN NULL;
    WHEN OTHERS THEN
      RAISE_APPLICATION_ERROR(-20004, 'Error getting full name: ' || SQLERRM);
  END get_full_name;

  -- Implementation of employee_exists function
  FUNCTION employee_exists (
    p_employee_id IN employees.employee_id%TYPE
  ) RETURN BOOLEAN AS
    v_count NUMBER;
  BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM employees
    WHERE employee_id = p_employee_id;

    RETURN v_count > 0;
  END employee_exists;

END employee_pkg;
/
```

**Input (Usage):**

```sql
SET SERVEROUTPUT ON;

-- Test add_employee procedure
BEGIN
  employee_pkg.add_employee(
    p_employee_id    => 104,
    p_first_name     => 'Robert',
    p_last_name      => 'Brown',
    p_email          => 'robert.brown@example.com',
    p_phone_number   => '555-5555',
    p_hire_date      => SYSDATE,
    p_job_id         => 'IT_PROG',
    p_salary         => 65000,
    p_department_id  => 10
  );
  COMMIT;
END;
/

-- Test get_full_name function
SELECT employee_pkg.get_full_name(100) AS employee_name FROM DUAL;
SELECT employee_pkg.get_full_name(105) AS employee_name FROM DUAL; -- Non-existent ID

-- Test employee_exists function
BEGIN
  IF employee_pkg.employee_exists(101) THEN
    DBMS_OUTPUT.PUT_LINE('Employee 101 exists.');
  ELSE
    DBMS_OUTPUT.PUT_LINE('Employee 101 does not exist.');
  END IF;

  IF employee_pkg.employee_exists(999) THEN
    DBMS_OUTPUT.PUT_LINE('Employee 999 exists.');
  ELSE
    DBMS_OUTPUT.PUT_LINE('Employee 999 does not exist.');
  END IF;
END;
/

-- Test error handling for add_employee (duplicate ID)
BEGIN
  employee_pkg.add_employee(
    p_employee_id    => 104, -- Duplicate ID
    p_first_name     => 'Test',
    p_last_name      => 'User',
    p_email          => 'test.user@example.com',
    p_phone_number   => '555-6666',
    p_hire_date      => SYSDATE,
    p_job_id         => 'SA_REP',
    p_salary         => 50000,
    p_department_id  => 20
  );
  COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE(SQLERRM);
END;
/
```

**Output:**

```
-- Output for `add_employee(104, ...)`:
Employee Robert Brown added successfully.
PL/SQL procedure successfully completed.

-- Output for `SELECT employee_pkg.get_full_name(100) FROM DUAL;`:
EMPLOYEE_NAME
--------------------
John Doe

-- Output for `SELECT employee_pkg.get_full_name(105) FROM DUAL;`:
EMPLOYEE_NAME
--------------------
(null)

-- Output for `employee_exists` block:
Employee 101 exists.
Employee 999 does not exist.
PL/SQL procedure successfully completed.

-- Output for `add_employee` with duplicate ID (error handling):
ORA-20002: Employee ID or Email already exists.
PL/SQL procedure successfully completed.
```

### Example 2: Package Variables and Constants (Session-Specific)

Package variables maintain their values throughout a user's session. They are reinitialized only when the package specification is recompiled or the session ends.

**Input (Specification):**

```sql
CREATE OR REPLACE PACKAGE session_counter_pkg AS
  -- Public package variable to store a session count
  g_call_count NUMBER := 0;

  -- Public constant
  c_max_count CONSTANT NUMBER := 5;

  -- Public procedure to increment the counter
  PROCEDURE increment_counter;

  -- Public function to get the current counter value
  FUNCTION get_counter RETURN NUMBER;

END session_counter_pkg;
/
```

**Input (Body):**

```sql
CREATE OR REPLACE PACKAGE BODY session_counter_pkg AS

  PROCEDURE increment_counter AS
  BEGIN
    g_call_count := g_call_count + 1;
    DBMS_OUTPUT.PUT_LINE('Counter incremented to: ' || g_call_count);
  END increment_counter;

  FUNCTION get_counter RETURN NUMBER AS
  BEGIN
    RETURN g_call_count;
  END get_counter;

  -- Optional: Initialization block for safety, though g_call_count is initialized in spec
  BEGIN
    DBMS_OUTPUT.PUT_LINE('session_counter_pkg initialized for this session.');
  END session_counter_pkg;
/
```

**Input (Usage):**

```sql
SET SERVEROUTPUT ON;

-- First time calling in a session (initialization block runs)
BEGIN
  session_counter_pkg.increment_counter;
END;
/

-- Subsequent calls (counter persists)
BEGIN
  session_counter_pkg.increment_counter;
  session_counter_pkg.increment_counter;
END;
/

-- Check current value
SELECT session_counter_pkg.get_counter FROM DUAL;

-- Access constant
SELECT session_counter_pkg.c_max_count FROM DUAL;
```

**Output:**

```
-- Output for first `increment_counter`:
session_counter_pkg initialized for this session.
Counter incremented to: 1
PL/SQL procedure successfully completed.

-- Output for subsequent increments:
Counter incremented to: 2
Counter incremented to: 3
PL/SQL procedure successfully completed.

-- Output for `SELECT session_counter_pkg.get_counter FROM DUAL;`:
GET_COUNTER
-----------
          3

-- Output for `SELECT session_counter_pkg.c_max_count FROM DUAL;`:
C_MAX_COUNT
-----------
          5
```

### Example 3: Package Initialization Block

The `BEGIN ... END;` block at the end of the package body (before the final `/`) is the package initialization block. It executes only once per session when the package is first referenced.

**Input (Specification):**

```sql
CREATE OR REPLACE PACKAGE app_config_pkg AS
  -- Public variable to store the initialization timestamp
  g_init_timestamp TIMESTAMP WITH TIME ZONE;

  -- Public function to get the initialization timestamp
  FUNCTION get_init_timestamp RETURN TIMESTAMP WITH TIME ZONE;

END app_config_pkg;
/
```

**Input (Body):**

```sql
CREATE OR REPLACE PACKAGE BODY app_config_pkg AS

  FUNCTION get_init_timestamp RETURN TIMESTAMP WITH TIME ZONE AS
  BEGIN
    RETURN g_init_timestamp;
  END get_init_timestamp;

  -- Package Initialization Block
  BEGIN
    -- This code runs ONLY ONCE when the package is first referenced in a session
    g_init_timestamp := SYSTIMESTAMP;
    DBMS_OUTPUT.PUT_LINE('APP_CONFIG_PKG: Initialized at ' || TO_CHAR(g_init_timestamp, 'YYYY-MM-DD HH24:MI:SS.FF TZR'));
  END app_config_pkg;
/
```

**Input (Usage):**

```sql
SET SERVEROUTPUT ON;

-- First reference (triggers initialization)
SELECT app_config_pkg.get_init_timestamp FROM DUAL;

-- Second reference (does NOT re-trigger initialization, uses stored value)
SELECT app_config_pkg.get_init_timestamp FROM DUAL;

-- Open a NEW SESSION and run the above SELECT statements to see re-initialization.
```

**Output (First Session):**

```
-- Output for first SELECT:
APP_CONFIG_PKG: Initialized at 2023-10-27 10:30:05.123456 -04:00 (timestamp will vary)

GET_INIT_TIMESTAMP
---------------------------------------------------------------------------
27-OCT-23 10.30.05.123456000 AM -04:00

-- Output for second SELECT (no "Initialized at" message, same timestamp):

GET_INIT_TIMESTAMP
---------------------------------------------------------------------------
27-OCT-23 10.30.05.123456000 AM -04:00
```

### Example 4: Overloading Procedures/Functions

Overloading allows you to define multiple procedures or functions with the same name within the same package, as long as their parameter lists differ (different number, order, or data types of parameters).

**Input (Specification):**

```sql
CREATE OR REPLACE PACKAGE log_pkg AS
  -- Overloaded procedure to log messages

  PROCEDURE log_message (
    p_message IN VARCHAR2
  );

  PROCEDURE log_message (
    p_message IN VARCHAR2,
    p_log_level IN VARCHAR2 -- e.g., 'INFO', 'WARNING', 'ERROR'
  );

  PROCEDURE log_message (
    p_message IN VARCHAR2,
    p_log_level IN VARCHAR2,
    p_context IN VARCHAR2
  );

END log_pkg;
/
```

**Input (Body):**

```sql
CREATE OR REPLACE PACKAGE BODY log_pkg AS

  -- Helper private procedure for actual logging
  PROCEDURE write_log (
    p_msg_in IN VARCHAR2,
    p_level_in IN VARCHAR2 DEFAULT 'INFO',
    p_context_in IN VARCHAR2 DEFAULT 'GENERAL'
  ) AS
  BEGIN
    -- In a real application, this would write to a log table or file
    DBMS_OUTPUT.PUT_LINE(
      TO_CHAR(SYSTIMESTAMP, 'YYYY-MM-DD HH24:MI:SS') ||
      ' [' || p_level_in || '] ' ||
      '(' || p_context_in || ') ' ||
      p_msg_in
    );
  END write_log;

  -- Implementation for log_message (1 parameter)
  PROCEDURE log_message (
    p_message IN VARCHAR2
  ) AS
  BEGIN
    write_log(p_message, 'INFO', 'DEFAULT');
  END log_message;

  -- Implementation for log_message (2 parameters)
  PROCEDURE log_message (
    p_message IN VARCHAR2,
    p_log_level IN VARCHAR2
  ) AS
  BEGIN
    write_log(p_message, p_log_level, 'DEFAULT');
  END log_message;

  -- Implementation for log_message (3 parameters)
  PROCEDURE log_message (
    p_message IN VARCHAR2,
    p_log_level IN VARCHAR2,
    p_context IN VARCHAR2
  ) AS
  BEGIN
    write_log(p_message, p_log_level, p_context);
  END log_message;

END log_pkg;
/
```

**Input (Usage):**

```sql
SET SERVEROUTPUT ON;

BEGIN
  log_pkg.log_message('This is a simple info message.');
  log_pkg.log_message('Warning: Disk space low!', 'WARNING');
  log_pkg.log_message('Error processing order.', 'ERROR', 'ORDER_PROCESSING');
  log_pkg.log_message('User login successful for user ' || employee_pkg.get_full_name(100), 'SECURITY', 'AUTHENTICATION');
END;
/
```

**Output:**

```
2023-10-27 10:45:01 [INFO] (DEFAULT) This is a simple info message.
2023-10-27 10:45:01 [WARNING] (DEFAULT) Warning: Disk space low!
2023-10-27 10:45:01 [ERROR] (ORDER_PROCESSING) Error processing order.
2023-10-27 10:45:01 [SECURITY] (AUTHENTICATION) User login successful for user John Doe
PL/SQL procedure successfully completed.
```

### Example 5: Using Cursors and Records in a Package

Packages are ideal for defining custom types (records, tables) and cursors that can be reused by multiple subprograms within the package or even exposed publicly.

**Input (Specification):**

```sql
CREATE OR REPLACE PACKAGE emp_data_pkg AS

  -- Public Record Type definition
  TYPE employee_rec_type IS RECORD (
    id         employees.employee_id%TYPE,
    first_name employees.first_name%TYPE,
    last_name  employees.last_name%TYPE,
    salary     employees.salary%TYPE
  );

  -- Public Table Type definition based on the record type
  TYPE employee_tbl_type IS TABLE OF employee_rec_type INDEX BY PLS_INTEGER;

  -- Public Cursor definition
  CURSOR all_employees_cursor IS
    SELECT employee_id, first_name, last_name, salary
    FROM employees
    ORDER BY employee_id;

  -- Public Procedure to fetch employee data into a table type
  PROCEDURE get_all_employees (
    p_employees OUT employee_tbl_type
  );

  -- Public Function to get an employee's salary
  FUNCTION get_employee_salary (
    p_employee_id IN employees.employee_id%TYPE
  ) RETURN employees.salary%TYPE;

END emp_data_pkg;
/
```

**Input (Body):**

```sql
CREATE OR REPLACE PACKAGE BODY emp_data_pkg AS

  -- Implementation for get_all_employees procedure
  PROCEDURE get_all_employees (
    p_employees OUT employee_tbl_type
  ) AS
    v_idx PLS_INTEGER := 0;
  BEGIN
    FOR rec IN all_employees_cursor LOOP -- Using the public cursor
      v_idx := v_idx + 1;
      p_employees(v_idx).id := rec.employee_id;
      p_employees(v_idx).first_name := rec.first_name;
      p_employees(v_idx).last_name := rec.last_name;
      p_employees(v_idx).salary := rec.salary;
    END LOOP;
  END get_all_employees;

  -- Implementation for get_employee_salary function
  FUNCTION get_employee_salary (
    p_employee_id IN employees.employee_id%TYPE
  ) RETURN employees.salary%TYPE AS
    v_salary employees.salary%TYPE;
  BEGIN
    SELECT salary
    INTO v_salary
    FROM employees
    WHERE employee_id = p_employee_id;

    RETURN v_salary;
  EXCEPTION
    WHEN NO_DATA_FOUND THEN
      RETURN NULL; -- Or raise an application error
  END get_employee_salary;

END emp_data_pkg;
/
```

**Input (Usage):**

```sql
SET SERVEROUTPUT ON;

DECLARE
  l_employees emp_data_pkg.employee_tbl_type;
  l_salary    employees.salary%TYPE;
BEGIN
  -- Test get_all_employees procedure
  emp_data_pkg.get_all_employees(l_employees);

  IF l_employees.COUNT > 0 THEN
    DBMS_OUTPUT.PUT_LINE('--- All Employees ---');
    FOR i IN l_employees.FIRST .. l_employees.LAST LOOP
      DBMS_OUTPUT.PUT_LINE(
        'ID: ' || l_employees(i).id ||
        ', Name: ' || l_employees(i).first_name || ' ' || l_employees(i).last_name ||
        ', Salary: ' || l_employees(i).salary
      );
    END LOOP;
  ELSE
    DBMS_OUTPUT.PUT_LINE('No employees found.');
  END IF;

  DBMS_OUTPUT.PUT_LINE(CHR(10) || '--- Individual Salary Lookup ---');
  -- Test get_employee_salary function
  l_salary := emp_data_pkg.get_employee_salary(101);
  IF l_salary IS NOT NULL THEN
    DBMS_OUTPUT.PUT_LINE('Salary for Employee 101: ' || l_salary);
  ELSE
    DBMS_OUTPUT.PUT_LINE('Employee 101 not found or no salary.');
  END IF;

  l_salary := emp_data_pkg.get_employee_salary(999); -- Non-existent
  IF l_salary IS NOT NULL THEN
    DBMS_OUTPUT.PUT_LINE('Salary for Employee 999: ' || l_salary);
  ELSE
    DBMS_OUTPUT.PUT_LINE('Employee 999 not found or no salary.');
  END IF;

END;
/
```

**Output:**

```
--- All Employees ---
ID: 100, Name: John Doe, Salary: 60000
ID: 101, Name: Jane Smith, Salary: 75000
ID: 102, Name: Peter Jones, Salary: 50000
ID: 103, Name: Alice Williams, Salary: 80000
ID: 104, Name: Robert Brown, Salary: 65000

--- Individual Salary Lookup ---
Salary for Employee 101: 75000
Employee 999 not found or no salary.
PL/SQL procedure successfully completed.
```

---

## 6. How to Use/Execute Package Components

Once a package is compiled, its public components can be accessed using the dot notation (`.`) followed by the component name.

*   **Calling a Procedure:**
    ```sql
    BEGIN
      package_name.procedure_name(parameter1, parameter2, ...);
    END;
    /
    ```
    or from SQL:
    ```sql
    EXEC package_name.procedure_name(parameter1, parameter2, ...);
    ```

*   **Calling a Function:**
    ```sql
    DECLARE
      result_var datatype;
    BEGIN
      result_var := package_name.function_name(parameter1, ...);
      -- Use result_var
    END;
    /
    ```
    or from SQL:
    ```sql
    SELECT package_name.function_name(parameter1, ...) FROM DUAL;
    ```
    (Note: Functions called from SQL must not perform DML operations that affect database state like `INSERT`, `UPDATE`, `DELETE` unless they are explicitly declared as `PRAGMA AUTONOMOUS_TRANSACTION` and adhere to certain purity rules.)

*   **Accessing a Public Variable/Constant:**
    ```sql
    DECLARE
      current_count NUMBER;
    BEGIN
      current_count := session_counter_pkg.g_call_count;
      DBMS_OUTPUT.PUT_LINE('Current count: ' || current_count);
      DBMS_OUTPUT.PUT_LINE('Max count: ' || session_counter_pkg.c_max_count);
    END;
    /
    ```

## 7. How to Drop a Package

You can drop the package body, or both the specification and the body.

*   **To drop only the package body (keeping the specification):**
    ```sql
    DROP PACKAGE BODY package_name;
    ```
    This is useful if you want to rewrite the implementation without affecting dependent objects that rely on the specification. The package will remain valid but its procedures/functions will not be executable until a new body is created.

*   **To drop both the package specification and its body:**
    ```sql
    DROP PACKAGE package_name;
    ```
    This will invalidate any objects that reference the package.

## 8. Important Considerations and Best Practices

*   **Keep Specification Lean:** Only declare items in the specification that truly need to be public. Move internal helper procedures, functions, and variables to the package body as private components.
*   **Clear Naming Conventions:** Use consistent naming (e.g., `_pkg` suffix for packages, `g_` for global package variables, `c_` for constants).
*   **Error Handling:** Implement robust error handling (e.g., `EXCEPTION` blocks, `RAISE_APPLICATION_ERROR`) within package procedures and functions.
*   **Comments:** Document your package specification and body clearly, explaining the purpose of each component, its parameters, and any assumptions.
*   **Version Control:** Store your package code in a version control system.
*   **Security:** Grant `EXECUTE` on the package to roles or users, rather than granting individual privileges on tables or specific procedures.
*   **Dependencies:** Be aware of package dependencies. Changing a package specification requires recompilation of all dependent objects. Changing only the body does not.
*   **Avoid Side Effects in Functions:** Functions called from SQL queries should be "pure" (not modify database state or package global variables in a way that affects subsequent calls) to ensure consistent results and avoid ORA-14551 errors.

## 9. Conclusion

Oracle PL/SQL Packages are a cornerstone of efficient and maintainable database development. By understanding their structure, benefits, and best practices, developers can create robust, scalable, and secure applications. They provide a powerful mechanism for modularizing code, managing session state, and improving the overall performance and organization of PL/SQL applications.