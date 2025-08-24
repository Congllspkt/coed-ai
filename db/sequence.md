Absolutely! Let's dive into Oracle SQL Sequences with detailed explanations and examples, formatted as a markdown file.

---

# Oracle SQL Sequences

## Introduction

An Oracle SQL Sequence is a database object that automatically generates unique sequential numbers. It's commonly used to create primary key values for tables, ensuring that each new record gets a unique identifier without needing manual management or risking concurrency issues. Sequences are independent of any specific table and can be shared by multiple tables or used for various purposes across the database.

## Why Use Sequences?

1.  **Unique Identifiers:** Guarantees that each number generated is unique.
2.  **Concurrency:** Handles concurrent requests for numbers efficiently, preventing race conditions or locking issues that might arise from other methods (like `MAX(id) + 1`).
3.  **Performance:** Oracle generates and caches sequence numbers, making their retrieval very fast.
4.  **Simplicity:** Easy to implement and use in `INSERT` statements.
5.  **Independence:** Not tied to a specific table, allowing for flexible usage.

## 1. Creating a Sequence (`CREATE SEQUENCE`)

The `CREATE SEQUENCE` statement defines a new sequence object and its properties.

### Syntax

```sql
CREATE SEQUENCE sequence_name
[INCREMENT BY n]
[START WITH n]
[MAXVALUE n | NOMAXVALUE]
[MINVALUE n | NOMINVALUE]
[CYCLE | NOCYCLE]
[CACHE n | NOCACHE]
[ORDER | NOORDER];
```

### Parameters Explained

*   **`sequence_name`**: The name of the sequence to be created. This must be unique within your schema.
*   **`INCREMENT BY n`**: Specifies the interval between sequence numbers.
    *   `n` can be a positive or negative integer.
    *   Default is `1`.
    *   Positive `n` for ascending sequences, negative `n` for descending sequences.
*   **`START WITH n`**: Specifies the first sequence number to be generated.
    *   Default is `1`.
*   **`MAXVALUE n`**: The maximum value the sequence can generate.
    *   For ascending sequences, this is the upper limit.
    *   For descending sequences, `MAXVALUE` must be less than `START WITH`.
    *   `NOMAXVALUE` (default) means a maximum value of `10^27` for ascending or `-1` for descending sequences.
*   **`MINVALUE n`**: The minimum value the sequence can generate.
    *   For descending sequences, this is the lower limit.
    *   For ascending sequences, `MINVALUE` must be less than `START WITH`.
    *   `NOMINVALUE` (default) means a minimum value of `1` for ascending or `-10^26` for descending sequences.
*   **`CYCLE` | `NOCYCLE`**:
    *   `CYCLE`: After reaching `MAXVALUE` (for ascending) or `MINVALUE` (for descending), the sequence restarts from `MINVALUE` (for ascending) or `MAXVALUE` (for descending).
    *   `NOCYCLE` (default): The sequence will stop generating numbers after reaching its limit and subsequent calls to `NEXTVAL` will result in an error.
*   **`CACHE n` | `NOCACHE`**:
    *   `CACHE n`: Specifies how many sequence numbers Oracle pre-allocates and keeps in memory for faster access. `n` must be at least 2.
    *   `NOCACHE` (default for older versions, `CACHE 20` for newer versions if not specified): No numbers are pre-allocated.
    *   **Important Note on `CACHE`**: If the database instance crashes or is shut down, any cached but unused sequence numbers are lost, leading to gaps in the sequence. For guaranteed contiguous numbers (though with a performance impact), use `NOCACHE`.
*   **`ORDER` | `NOORDER`**:
    *   `ORDER`: Guarantees that sequence numbers are generated in the order of requests. This is useful in Real Application Clusters (RAC) environments where multiple instances might request numbers concurrently, ensuring chronological order across instances.
    *   `NOORDER` (default): Oracle does not guarantee strict chronological order of sequence numbers being generated if multiple sessions/instances are requesting them at the exact same time. This offers better performance.

### `CREATE SEQUENCE` Examples

#### Example 1: Basic Ascending Sequence

Creates a sequence starting at 1, incrementing by 1, with no upper limit and no caching.

**Input:**

```sql
CREATE SEQUENCE department_id_seq;
```

**Output:**

```
Sequence DEPARTMENT_ID_SEQ created.
```

#### Example 2: Sequence with Specific Start, Increment, and Cache

Creates a sequence for employee IDs, starting at 100, incrementing by 10, with a maximum value of 99999, caching 20 values, and not cycling.

**Input:**

```sql
CREATE SEQUENCE employee_id_seq
    START WITH 100
    INCREMENT BY 10
    MAXVALUE 99999
    NOCYCLE
    CACHE 20;
```

**Output:**

```
Sequence EMPLOYEE_ID_SEQ created.
```

#### Example 3: Descending and Cycling Sequence

Creates a sequence that counts down from 100, decrements by 1, cycles back to 100 after reaching 1.

**Input:**

```sql
CREATE SEQUENCE reverse_id_seq
    START WITH 100
    INCREMENT BY -1
    MINVALUE 1
    MAXVALUE 100
    CYCLE
    NOCACHE;
```

**Output:**

```
Sequence REVERSE_ID_SEQ created.
```

## 2. Using a Sequence

You access sequence values using two pseudo-columns: `NEXTVAL` and `CURRVAL`.

### `NEXTVAL`

*   **`sequence_name.NEXTVAL`**: Retrieves the *next* available number from the sequence.
*   **Important**: The first call to `NEXTVAL` in a session initializes the sequence and returns the `START WITH` value. Subsequent calls return the next number based on `INCREMENT BY`.
*   A call to `NEXTVAL` increments the sequence *regardless* of whether the transaction is committed or rolled back.

### `CURRVAL`

*   **`sequence_name.CURRVAL`**: Retrieves the *current* value of the sequence. This is the last value generated by `NEXTVAL` *in your current session*.
*   **Restriction**: You cannot use `CURRVAL` before you have called `NEXTVAL` at least once in your current session for that specific sequence. Doing so will result in an error (`ORA-08002: sequence_name.CURRVAL is not yet defined in this session`).

### Usage Examples

#### Example 1: Getting the Next Value

**Input:**

```sql
SELECT employee_id_seq.NEXTVAL FROM DUAL;
```

**Output (first call in session):**

```
   NEXTVAL
----------
       100
```

**Input:**

```sql
SELECT employee_id_seq.NEXTVAL FROM DUAL; -- Second call
```

**Output (second call in session, incremented by 10):**

```
   NEXTVAL
----------
       110
```

#### Example 2: Inserting Data with `NEXTVAL`

Let's assume we have an `employees` table:

```sql
CREATE TABLE employees (
    employee_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50),
    last_name VARCHAR2(50),
    hire_date DATE DEFAULT SYSDATE
);
```

**Input:**

```sql
INSERT INTO employees (employee_id, first_name, last_name)
VALUES (employee_id_seq.NEXTVAL, 'Alice', 'Smith');

INSERT INTO employees (employee_id, first_name, last_name)
VALUES (employee_id_seq.NEXTVAL, 'Bob', 'Johnson');

SELECT employee_id, first_name, last_name FROM employees;
```

**Output:**

```
2 rows inserted.
2 rows inserted.

EMPLOYEE_ID FIRST_NAME LAST_NAME
----------- ---------- ---------
        120 Alice      Smith
        130 Bob        Johnson
```
*(Note: `NEXTVAL` was called twice, so 110 and 120 were used by the `DUAL` query earlier. Now it starts from 130 for 'Alice' and 140 for 'Bob').*

#### Example 3: Using `CURRVAL`

To get the employee ID just assigned to Alice for an audit log, you'd use `CURRVAL`.

**Input:**

```sql
-- First, insert a new employee using NEXTVAL
INSERT INTO employees (employee_id, first_name, last_name)
VALUES (employee_id_seq.NEXTVAL, 'Charlie', 'Brown');

-- Now, use CURRVAL to get the ID just generated for Charlie
SELECT employee_id_seq.CURRVAL FROM DUAL;

-- Or use it in another INSERT statement within the same transaction/session
INSERT INTO audit_log (log_id, employee_id, action)
VALUES (audit_log_seq.NEXTVAL, employee_id_seq.CURRVAL, 'Employee hired'); -- Assuming audit_log_seq exists
```

**Output (for `SELECT employee_id_seq.CURRVAL FROM DUAL;`):**

```
   CURRVAL
----------
       150
```

## 3. Altering a Sequence (`ALTER SEQUENCE`)

You can modify most properties of an existing sequence, *except* for its `START WITH` value. To change `START WITH`, you must drop and recreate the sequence.

### Syntax

```sql
ALTER SEQUENCE sequence_name
[INCREMENT BY n]
[MAXVALUE n | NOMAXVALUE]
[MINVALUE n | NOMINVALUE]
[CYCLE | NOCYCLE]
[CACHE n | NOCACHE]
[ORDER | NOORDER];
```

### `ALTER SEQUENCE` Examples

#### Example 1: Change Increment and Maxvalue

**Input:**

```sql
ALTER SEQUENCE employee_id_seq
    INCREMENT BY 5
    MAXVALUE 100000;
```

**Output:**

```
Sequence EMPLOYEE_ID_SEQ altered.
```

Now, subsequent calls to `NEXTVAL` will increment by 5. If `employee_id_seq.NEXTVAL` was last 150, the next call would return 155.

#### Example 2: Change to `NOCACHE`

**Input:**

```sql
ALTER SEQUENCE employee_id_seq NOCACHE;
```

**Output:**

```
Sequence EMPLOYEE_ID_SEQ altered.
```

## 4. Dropping a Sequence (`DROP SEQUENCE`)

The `DROP SEQUENCE` statement removes a sequence from the database. This action is irreversible.

### Syntax

```sql
DROP SEQUENCE sequence_name;
```

### `DROP SEQUENCE` Example

**Input:**

```sql
DROP SEQUENCE department_id_seq;
```

**Output:**

```
Sequence DEPARTMENT_ID_SEQ dropped.
```

## Important Considerations and Best Practices

1.  **Gaps in Sequences:**
    *   **`CACHE` Option:** If you use `CACHE` and the database instance crashes or is shut down, any unused numbers in the cache are lost, leading to gaps.
    *   **Rollbacks:** `NEXTVAL` generates a number *immediately*. If the transaction that used `NEXTVAL` is rolled back, that sequence number is still consumed and will not be reused, creating a gap.
    *   **Concurrent Sessions:** If multiple sessions are requesting numbers, some numbers might be generated but not inserted (due to rollbacks or application logic), leading to gaps.
    *   **Solution for No Gaps:** If absolutely no gaps are allowed (rarely a true requirement for primary keys), use `NOCACHE`. Be aware this can have a performance impact, especially in high-transaction systems.

2.  **`START WITH` Cannot Be Altered:** To change the starting value of a sequence, you must `DROP` it and then `CREATE` it again with the desired `START WITH` value.

3.  **`CURRVAL` Session Specificity:** Remember that `CURRVAL` returns the last value *generated by `NEXTVAL` in your current session*. It's not a global "current" value across all sessions.

4.  **Security/Privileges:**
    *   To `CREATE` a sequence, you need the `CREATE SEQUENCE` system privilege.
    *   To `ALTER` or `DROP` a sequence, you must own it or have the `ALTER ANY SEQUENCE` or `DROP ANY SEQUENCE` system privilege.
    *   To use `NEXTVAL` or `CURRVAL` on a sequence, you need `SELECT` privilege on that sequence.

5.  **`IDENTITY` Columns (Oracle 12cR1+):**
    For generating primary keys, Oracle 12c introduced `IDENTITY` columns, which are a simpler, SQL standard-compliant way to define auto-incrementing columns, internally using sequences.
    ```sql
    CREATE TABLE products (
        product_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        product_name VARCHAR2(100)
    );

    INSERT INTO products (product_name) VALUES ('Laptop');
    INSERT INTO products (product_name) VALUES ('Mouse');

    SELECT product_id, product_name FROM products;
    ```
    This approach is generally preferred for simple auto-incrementing primary keys as it ties the sequence management directly to the table column definition.

## Complete Example Workflow

Let's create a full scenario from table creation to sequence usage and cleanup.

**Input:**

```sql
-- 1. Create a Table that will use a sequence for its primary key
CREATE TABLE projects (
    project_id NUMBER PRIMARY KEY,
    project_name VARCHAR2(100) NOT NULL,
    start_date DATE DEFAULT SYSDATE
);

-- Output:
-- Table PROJECTS created.

-- 2. Create a Sequence for the project_id
CREATE SEQUENCE project_id_seq
    START WITH 1
    INCREMENT BY 1
    MAXVALUE 999999999
    NOCYCLE
    CACHE 10;

-- Output:
-- Sequence PROJECT_ID_SEQ created.

-- 3. Insert data using NEXTVAL
INSERT INTO projects (project_id, project_name)
VALUES (project_id_seq.NEXTVAL, 'Website Redesign');

INSERT INTO projects (project_id, project_name)
VALUES (project_id_seq.NEXTVAL, 'Mobile App Development');

-- Output:
-- 1 row inserted.
-- 1 row inserted.

-- 4. Verify the inserted data and generated IDs
SELECT project_id, project_name FROM projects;

-- Output:
-- PROJECT_ID PROJECT_NAME
-- ---------- ----------------------
--          1 Website Redesign
--          2 Mobile App Development

-- 5. Get the current sequence value (last generated in this session)
SELECT project_id_seq.CURRVAL FROM DUAL;

-- Output:
--    CURRVAL
-- ----------
--          2

-- 6. Alter the sequence to increment by 5
ALTER SEQUENCE project_id_seq
    INCREMENT BY 5;

-- Output:
-- Sequence PROJECT_ID_SEQ altered.

-- 7. Insert another project to see the new increment
INSERT INTO projects (project_id, project_name)
VALUES (project_id_seq.NEXTVAL, 'Database Migration');

SELECT project_id, project_name FROM projects;

-- Output:
-- 1 row inserted.

-- Output after SELECT:
-- PROJECT_ID PROJECT_NAME
-- ---------- ----------------------
--          1 Website Redesign
--          2 Mobile App Development
--          7 Database Migration (2 + 5 = 7)

-- 8. Clean up: Drop the sequence and the table
DROP SEQUENCE project_id_seq;
DROP TABLE projects;

-- Output:
-- Sequence PROJECT_ID_SEQ dropped.
-- Table PROJECTS dropped.
```

---