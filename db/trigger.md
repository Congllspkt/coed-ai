A **trigger** in SQL Oracle is a stored PL/SQL program unit that is automatically executed (fired) in response to certain events on a database table or schema. These events can be:

*   **DML events:** `INSERT`, `UPDATE`, `DELETE` statements on a table.
*   **DDL events:** `CREATE`, `ALTER`, `DROP` statements for schema objects.
*   **Database events:** `LOGON`, `LOGOFF`, `STARTUP`, `SHUTDOWN`, `SERVERERROR`.

Triggers are powerful tools for enforcing business rules, auditing data changes, maintaining complex data integrity, and automating tasks.

---

## Table of Contents

1.  [Introduction](#1-introduction)
2.  [Trigger Syntax](#2-trigger-syntax)
3.  [Key Components Explained](#3-key-components-explained)
4.  [Types of Triggers](#4-types-of-triggers)
5.  [Practical Use Cases](#5-practical-use-cases)
6.  [Examples with Input and Output](#6-examples-with-input-and-output)
    *   [Example 1: Auditing Data Changes](#example-1-auditing-data-changes)
    *   [Example 2: Data Validation](#example-2-data-validation)
    *   [Example 3: Automatic Column Population](#example-3-automatic-column-population)
7.  [Managing Triggers](#7-managing-triggers)
8.  [Best Practices and Considerations](#8-best-practices-and-considerations)
9.  [Conclusion](#9-conclusion)

---

## 1. Introduction

Triggers provide a way to perform an action automatically when a specified event occurs. They are typically used for:

*   **Auditing:** Recording who, when, and what changed in the database.
*   **Data Validation:** Enforcing complex business rules that cannot be handled by simple constraints (e.g., `CHECK`, `NOT NULL`, `FOREIGN KEY`).
*   **Maintaining Data Integrity:** Synchronizing related data in different tables.
*   **Automatic Derivation:** Populating columns with derived values (e.g., `SYSDATE` for `last_modified_date`).
*   **Event Logging:** Recording database activities.

## 2. Trigger Syntax

Here's the general syntax for creating a DML trigger in Oracle SQL:

```sql
CREATE [OR REPLACE] TRIGGER trigger_name
{BEFORE | AFTER | INSTEAD OF}
{INSERT | UPDATE [OF column_name [, column_name...]] | DELETE}
ON table_name
[REFERENCING OLD AS old_alias NEW AS new_alias] -- Optional: custom aliases for :OLD and :NEW
[FOR EACH ROW]
[WHEN (condition)] -- Optional: row-level trigger condition
DECLARE
    -- Variable declarations (optional)
BEGIN
    -- PL/SQL statements
    -- Access :OLD.column_name and :NEW.column_name here for row-level triggers
END;
/
```

## 3. Key Components Explained

*   **`CREATE [OR REPLACE] TRIGGER trigger_name`**:
    *   `CREATE TRIGGER`: Used to create a new trigger.
    *   `OR REPLACE`: Optional clause to re-create the trigger if it already exists, without dropping it first.
    *   `trigger_name`: A unique name for the trigger within the schema.

*   **`{BEFORE | AFTER | INSTEAD OF}`**: Specifies the **timing** of the trigger relative to the DML event.
    *   **`BEFORE`**: The trigger fires *before* the DML statement is executed. Useful for data validation, auditing before changes, or modifying `:NEW` values before they are committed.
    *   **`AFTER`**: The trigger fires *after* the DML statement is executed. Useful for auditing after changes, propagating changes to other tables, or performing actions based on the final state.
    *   **`INSTEAD OF`**: Used on views that are not inherently updatable (e.g., views with `JOIN`s, `GROUP BY`, `DISTINCT`). The trigger executes its PL/SQL code instead of the actual `INSERT`, `UPDATE`, or `DELETE` on the view, allowing the underlying base tables to be modified.

*   **`{INSERT | UPDATE [OF column_name] | DELETE}`**: Specifies the **DML event(s)** that will fire the trigger.
    *   You can combine events using `OR` (e.g., `BEFORE INSERT OR UPDATE OR DELETE`).
    *   `UPDATE OF column_name`: The trigger fires only if specific columns are updated.

*   **`ON table_name`**: Specifies the table on which the trigger is defined.

*   **`[REFERENCING OLD AS old_alias NEW AS new_alias]`**:
    *   Allows you to define custom aliases for the `:OLD` and `:NEW` pseudorecords. By default, they are `:OLD` and `:NEW`.
    *   `:OLD`: Refers to the row's values *before* the DML operation.
    *   `:NEW`: Refers to the row's values *after* the DML operation (or being inserted).
    *   **Important:**
        *   `INSERT` statements: Only `:NEW` values are available.
        *   `UPDATE` statements: Both `:OLD` and `:NEW` values are available.
        *   `DELETE` statements: Only `:OLD` values are available.
        *   You *cannot* change `:OLD` values, but you *can* change `:NEW` values in a `BEFORE` row-level trigger.

*   **`[FOR EACH ROW]`**: Specifies the **trigger level**.
    *   **`FOR EACH ROW` (Row-Level Trigger)**: The trigger fires once for each row affected by the DML statement. This is the most common type for DML triggers. It has access to `:OLD` and `:NEW` values.
    *   **Omitted (Statement-Level Trigger)**: The trigger fires only once per DML statement, regardless of how many rows are affected. It does *not* have access to `:OLD` or `:NEW` values. Useful for actions that need to happen once per statement (e.g., logging that an `UPDATE` occurred, but not details of each row).

*   **`[WHEN (condition)]`**:
    *   An optional `BOOLEAN` condition that must evaluate to `TRUE` for a **row-level** trigger to fire. The condition can refer to `:OLD` and `:NEW` values.
    *   Example: `WHEN (NEW.salary < OLD.salary)`.

*   **`DECLARE ... BEGIN ... END;`**: The PL/SQL block containing the trigger's logic.
    *   `DECLARE`: Optional section for declaring local variables, cursors, etc.
    *   `BEGIN ... END;`: Contains the executable PL/SQL statements.

## 4. Types of Triggers

Based on timing and level, DML triggers are primarily categorized as:

1.  **BEFORE Statement Trigger:** Fires once before the DML statement executes. No `:OLD` or `:NEW`.
2.  **AFTER Statement Trigger:** Fires once after the DML statement executes. No `:OLD` or `:NEW`.
3.  **BEFORE Row Trigger:** Fires for each row *before* the DML operation on that row. Has access to `:OLD` and `:NEW`. Can modify `:NEW` values.
4.  **AFTER Row Trigger:** Fires for each row *after* the DML operation on that row. Has access to `:OLD` and `:NEW`. Cannot modify `:NEW` values.
5.  **INSTEAD OF Trigger:** Used on views, fires instead of the DML operation on the view. Has access to `:OLD` and `:NEW`.
6.  **System Triggers:** DDL or database event triggers (e.g., `ON SCHEMA.CREATE`, `AFTER LOGON ON DATABASE`).

## 5. Practical Use Cases

*   **Auditing:** Track all changes (inserts, updates, deletes) to sensitive data.
*   **Complex Validation:** Enforce business rules that involve multiple columns, complex logic, or data from other tables.
*   **Automatic Value Generation:** Populate columns like `created_by`, `creation_date`, `last_updated_by`, `last_updated_date`.
*   **Referential Integrity Enforcement:** Implement complex referential actions beyond what `FOREIGN KEY` constraints offer (e.g., cascading deletes to related tables in a non-standard way).
*   **Data Derivation:** Automatically calculate and update derived columns based on changes in other columns.
*   **Security:** Implement custom security policies (e.g., preventing updates during certain hours).

## 6. Examples with Input and Output

Let's set up some tables for our examples:

```sql
-- Create EMPLOYEES table
CREATE TABLE employees (
    employee_id    NUMBER PRIMARY KEY,
    first_name     VARCHAR2(50),
    last_name      VARCHAR2(50),
    email          VARCHAR2(100) UNIQUE,
    phone_number   VARCHAR2(20),
    hire_date      DATE,
    job_id         VARCHAR2(10),
    salary         NUMBER(10, 2),
    commission_pct NUMBER(2, 2),
    manager_id     NUMBER,
    department_id  NUMBER,
    last_updated_by VARCHAR2(100),
    last_updated_date DATE
);

-- Create an audit table
CREATE TABLE employee_audit (
    audit_id        NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
    employee_id     NUMBER,
    old_salary      NUMBER(10, 2),
    new_salary      NUMBER(10, 2),
    old_email       VARCHAR2(100),
    new_email       VARCHAR2(100),
    change_type     VARCHAR2(10), -- INSERT, UPDATE, DELETE
    change_date     TIMESTAMP DEFAULT SYSTIMESTAMP,
    changed_by      VARCHAR2(100) DEFAULT USER
);

-- Insert some initial data
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id)
VALUES (100, 'John', 'Doe', 'john.doe@example.com', '515.123.4567', DATE '2000-01-01', 'IT_PROG', 6000, 60);

INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id)
VALUES (101, 'Jane', 'Smith', 'jane.smith@example.com', '515.123.4568', DATE '2001-05-15', 'SA_REP', 8000, 80);

COMMIT;

-- Verify initial data
SELECT employee_id, first_name, last_name, salary, email, last_updated_date FROM employees;
```

**Initial Output (employees table):**

```
EMPLOYEE_ID FIRST_NAME LAST_NAME SALARY EMAIL                 LAST_UPDATED_DATE
----------- ---------- --------- ------ --------------------- -----------------
        100 John       Doe         6000 john.doe@example.com
        101 Jane       Smith       8000 jane.smith@example.com
```

### Example 1: Auditing Data Changes

**Goal:** Automatically log all `INSERT`, `UPDATE`, and `DELETE` operations on the `employees` table into the `employee_audit` table.

**Trigger Code:**

```sql
CREATE OR REPLACE TRIGGER trg_employee_audit
AFTER INSERT OR UPDATE OR DELETE ON employees
FOR EACH ROW
DECLARE
    v_change_type VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_change_type := 'INSERT';
        INSERT INTO employee_audit (employee_id, new_salary, new_email, change_type)
        VALUES (:NEW.employee_id, :NEW.salary, :NEW.email, v_change_type);
    ELSIF UPDATING THEN
        v_change_type := 'UPDATE';
        INSERT INTO employee_audit (employee_id, old_salary, new_salary, old_email, new_email, change_type)
        VALUES (:OLD.employee_id, :OLD.salary, :NEW.salary, :OLD.email, :NEW.email, v_change_type);
    ELSIF DELETING THEN
        v_change_type := 'DELETE';
        INSERT INTO employee_audit (employee_id, old_salary, old_email, change_type)
        VALUES (:OLD.employee_id, :OLD.salary, :OLD.email, v_change_type);
    END IF;
END;
/
```

**Input & Output:**

1.  **Update an employee's salary:**
    ```sql
    UPDATE employees
    SET salary = 6500
    WHERE employee_id = 100;

    COMMIT;

    SELECT employee_id, first_name, salary FROM employees WHERE employee_id = 100;
    SELECT audit_id, employee_id, old_salary, new_salary, change_type, changed_by FROM employee_audit;
    ```
    **Output (employees):**
    ```
    EMPLOYEE_ID FIRST_NAME SALARY
    ----------- ---------- ------
            100 John         6500
    ```
    **Output (employee_audit):**
    ```
    AUDIT_ID EMPLOYEE_ID OLD_SALARY NEW_SALARY CHANGE_TYPE CHANGED_BY
    -------- ----------- ---------- ---------- ----------- ----------
           1         100       6000       6500 UPDATE      YOUR_USERNAME
    ```

2.  **Insert a new employee:**
    ```sql
    INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id)
    VALUES (102, 'Alice', 'Brown', 'alice.brown@example.com', '515.123.4569', DATE '2022-03-01', 'HR_REP', 4500, 90);

    COMMIT;

    SELECT employee_id, first_name, salary FROM employees WHERE employee_id = 102;
    SELECT audit_id, employee_id, old_salary, new_salary, change_type, changed_by FROM employee_audit;
    ```
    **Output (employees):**
    ```
    EMPLOYEE_ID FIRST_NAME SALARY
    ----------- ---------- ------
            102 Alice        4500
    ```
    **Output (employee_audit):**
    ```
    AUDIT_ID EMPLOYEE_ID OLD_SALARY NEW_SALARY CHANGE_TYPE CHANGED_BY
    -------- ----------- ---------- ---------- ----------- ----------
           1         100       6000       6500 UPDATE      YOUR_USERNAME
           2         102                  4500 INSERT      YOUR_USERNAME
    ```

3.  **Delete an employee:**
    ```sql
    DELETE FROM employees WHERE employee_id = 101;

    COMMIT;

    SELECT employee_id, first_name, salary FROM employees WHERE employee_id = 101; -- Should return no rows
    SELECT audit_id, employee_id, old_salary, new_salary, change_type, changed_by FROM employee_audit;
    ```
    **Output (employees):**
    ```
    no rows selected
    ```
    **Output (employee_audit):**
    ```
    AUDIT_ID EMPLOYEE_ID OLD_SALARY NEW_SALARY CHANGE_TYPE CHANGED_BY
    -------- ----------- ---------- ---------- ----------- ----------
           1         100       6000       6500 UPDATE      YOUR_USERNAME
           2         102                  4500 INSERT      YOUR_USERNAME
           3         101       8000            DELETE      YOUR_USERNAME
    ```

### Example 2: Data Validation

**Goal:** Ensure that an employee's salary is always between 3000 and 20000. If an attempt is made to set it outside this range, prevent the operation and raise an error.

**Trigger Code:**

```sql
CREATE OR REPLACE TRIGGER trg_validate_salary
BEFORE INSERT OR UPDATE OF salary ON employees
FOR EACH ROW
BEGIN
    IF :NEW.salary < 3000 OR :NEW.salary > 20000 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Employee salary must be between 3000 and 20000.');
    END IF;
END;
/
```

**Input & Output:**

1.  **Update with a valid salary:**
    ```sql
    UPDATE employees
    SET salary = 7000
    WHERE employee_id = 100;

    COMMIT;

    SELECT employee_id, salary FROM employees WHERE employee_id = 100;
    ```
    **Output:**
    ```
    EMPLOYEE_ID SALARY
    ----------- ------
            100   7000
    ```
    *(The update is successful)*

2.  **Update with an invalid (too low) salary:**
    ```sql
    UPDATE employees
    SET salary = 2500
    WHERE employee_id = 100;
    ```
    **Output:**
    ```
    Error report -
    ORA-20001: Employee salary must be between 3000 and 20000.
    ORA-06512: at "YOUR_USERNAME.TRG_VALIDATE_SALARY", line 4
    ORA-04088: error during execution of trigger 'YOUR_USERNAME.TRG_VALIDATE_SALARY'
    ```
    *(The update is prevented, and the custom error message is displayed)*

3.  **Insert with an invalid (too high) salary:**
    ```sql
    INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id)
    VALUES (103, 'Bob', 'Johnson', 'bob.johnson@example.com', '515.123.4570', DATE '2023-01-01', 'MK_REP', 25000, 30);
    ```
    **Output:**
    ```
    Error report -
    ORA-20001: Employee salary must be between 3000 and 20000.
    ORA-06512: at "YOUR_USERNAME.TRG_VALIDATE_SALARY", line 4
    ORA-04088: error during execution of trigger 'YOUR_USERNAME.TRG_VALIDATE_SALARY'
    ```
    *(The insert is prevented)*

### Example 3: Automatic Column Population

**Goal:** Automatically set the `last_updated_date` and `last_updated_by` columns whenever an `INSERT` or `UPDATE` occurs on the `employees` table.

**Trigger Code:**

```sql
CREATE OR REPLACE TRIGGER trg_employee_timestamp
BEFORE INSERT OR UPDATE ON employees
FOR EACH ROW
BEGIN
    -- Set the last_updated_date to the current system timestamp
    :NEW.last_updated_date := SYSDATE;

    -- Set the last_updated_by to the current user
    :NEW.last_updated_by := USER;
END;
/
```

**Input & Output:**

1.  **Initial check (note `last_updated_date` is NULL):**
    ```sql
    SELECT employee_id, first_name, last_updated_by, last_updated_date FROM employees WHERE employee_id = 100;
    ```
    **Output:**
    ```
    EMPLOYEE_ID FIRST_NAME LAST_UPDATED_BY LAST_UPDATED_DATE
    ----------- ---------- --------------- -----------------
            100 John
    ```

2.  **Update an employee's email:**
    ```sql
    UPDATE employees
    SET email = 'john.doe.new@example.com'
    WHERE employee_id = 100;

    COMMIT;

    SELECT employee_id, first_name, email, last_updated_by, last_updated_date FROM employees WHERE employee_id = 100;
    ```
    **Output:**
    ```
    EMPLOYEE_ID FIRST_NAME EMAIL                    LAST_UPDATED_BY LAST_UPDATED_DATE
    ----------- ---------- ------------------------ --------------- -----------------
            100 John       john.doe.new@example.com YOUR_USERNAME   2023-10-27 10:30:45
    ```
    *(Note: `last_updated_date` will show the current timestamp, and `last_updated_by` will show your username)*

3.  **Insert a new employee:**
    ```sql
    INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id)
    VALUES (104, 'Charlie', 'Davis', 'charlie.davis@example.com', '515.123.4571', DATE '2021-07-01', 'AD_VP', 15000, 90);

    COMMIT;

    SELECT employee_id, first_name, last_updated_by, last_updated_date FROM employees WHERE employee_id = 104;
    ```
    **Output:**
    ```
    EMPLOYEE_ID FIRST_NAME LAST_UPDATED_BY LAST_UPDATED_DATE
    ----------- ---------- --------------- -----------------
            104 Charlie    YOUR_USERNAME   2023-10-27 10:32:10
    ```
    *(The `last_updated_by` and `last_updated_date` columns are automatically populated upon insert as well.)*

---

## 7. Managing Triggers

*   **Disable a Trigger:**
    ```sql
    ALTER TRIGGER trg_employee_audit DISABLE;
    ```

*   **Enable a Trigger:**
    ```sql
    ALTER TRIGGER trg_employee_audit ENABLE;
    ```

*   **Disable all Triggers on a Table:**
    ```sql
    ALTER TABLE employees DISABLE ALL TRIGGERS;
    ```

*   **Enable all Triggers on a Table:**
    ```sql
    ALTER TABLE employees ENABLE ALL TRIGGERS;
    ```

*   **Drop a Trigger:**
    ```sql
    DROP TRIGGER trg_employee_audit;
    ```

*   **View Trigger Information:**
    ```sql
    SELECT trigger_name, trigger_type, triggering_event, table_name, status
    FROM user_triggers
    WHERE table_name = 'EMPLOYEES';

    -- To view the full trigger code:
    SELECT trigger_body FROM user_triggers WHERE trigger_name = 'TRG_EMPLOYEE_AUDIT';
    ```

---

## 8. Best Practices and Considerations

*   **Keep Triggers Simple:** Avoid complex business logic within triggers. If the logic is extensive, consider using stored procedures or functions and calling them from the trigger.
*   **Avoid Chaining Triggers:** A trigger on Table A causes an action on Table B, which in turn fires a trigger on Table B that causes an action on Table C. This can lead to debugging nightmares and performance issues.
*   **Performance Impact:** Triggers add overhead to DML operations. Design them efficiently. Avoid `SELECT` statements in row-level triggers that query the same table the trigger is on (mutating table error).
*   **Error Handling:** Use `RAISE_APPLICATION_ERROR` to provide meaningful error messages for validation failures.
*   **Test Thoroughly:** Test all possible scenarios, including edge cases and errors.
*   **Documentation:** Document the purpose and logic of each trigger.
*   **Alternatives:** Consider if a simple constraint (e.g., `CHECK`, `NOT NULL`, `UNIQUE`, `FOREIGN KEY`) or a stored procedure might be a better solution before resorting to a trigger. For auto-incrementing primary keys, Oracle 12c+ `IDENTITY` columns are generally preferred over `BEFORE INSERT` triggers with sequences.

## 9. Conclusion

Triggers are a powerful feature in Oracle SQL for automating tasks and enforcing complex business rules at the database level. They are event-driven, firing automatically in response to DML, DDL, or database events. By understanding their types, syntax, and best practices, you can effectively leverage triggers to enhance data integrity, audit changes, and streamline database operations.