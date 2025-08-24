In Oracle SQL, an **index** is a schema object that can speed up the retrieval of rows by using a pointer. It's essentially a sorted list of values from the indexed column(s) with corresponding physical locations (ROWIDs) of the rows in the table. Think of it like the index in a book: instead of reading the entire book to find a topic, you look it up in the index, which tells you exactly where to go.

---

# Oracle SQL - Indexes

## Table of Contents
1.  [What is an Index?](#1-what-is-an-index)
2.  [Why Use Indexes?](#2-why-use-indexes)
3.  [When to Use/Not Use Indexes?](#3-when-to-usenot-use-indexes)
4.  [Types of Indexes](#4-types-of-indexes)
    *   [B-Tree Index (Default)](#b-tree-index-default)
    *   [Unique Index](#unique-index)
    *   [Composite/Concatenated Index](#compositeconcatenated-index)
    *   [Function-Based Index (FBI)](#function-based-index-fbi)
    *   [Bitmap Index (Briefly)](#bitmap-index-briefly)
5.  [Basic Syntax: Creating and Managing Indexes](#5-basic-syntax-creating-and-managing-indexes)
6.  [Examples with Input and Output](#6-examples-with-input-and-output)
    *   [Example 1: Basic B-Tree Index](#example-1-basic-b-tree-index)
    *   [Example 2: Unique Index](#example-2-unique-index)
    *   [Example 3: Composite Index](#example-3-composite-index)
    *   [Example 4: Function-Based Index](#example-4-function-based-index)
    *   [Example 5: Dropping an Index](#example-5-dropping-an-index)
    *   [Example 6: Rebuilding an Index](#example-6-rebuilding-an-index)
    *   [Example 7: Viewing Index Information](#example-7-viewing-index-information)
    *   [Example 8: Monitoring Index Usage](#example-8-monitoring-index-usage)
7.  [Best Practices and Considerations](#7-best-practices-and-considerations)
8.  [Conclusion](#8-conclusion)

---

## 1. What is an Index?

An index in Oracle is a database structure associated with a table (or cluster) that helps in locating data rows quickly. It stores a sorted copy of the indexed column(s) along with pointers (ROWIDs) to the actual table rows. When a query needs to retrieve data from an indexed column, Oracle can go directly to the index, find the relevant entries, and then use the ROWIDs to jump straight to the data rows, bypassing a full table scan.

## 2. Why Use Indexes?

The primary purpose of indexes is to **improve the performance of data retrieval (SELECT statements)**. Without indexes, Oracle might have to scan every row in a table to find the data that matches your query criteria, which can be very slow for large tables.

## 3. When to Use/Not Use Indexes?

**Use Indexes When:**
*   **Large Tables:** Tables with many rows where a significant portion of the data won't be retrieved by most queries.
*   **Frequent Queries:** Columns often used in `WHERE` clauses, `JOIN` conditions, `ORDER BY` clauses, or `GROUP BY` clauses.
*   **High Cardinality:** Columns with a large number of distinct values (e.g., `employee_id`, `email_address`).
*   **Unique Constraints:** `PRIMARY KEY` and `UNIQUE` constraints automatically create unique indexes in Oracle.

**Do Not Use Indexes When:**
*   **Small Tables:** For small tables, a full table scan is often faster than using an index, as the overhead of accessing the index can outweigh the benefit.
*   **Frequent DML Operations:** Tables with very frequent `INSERT`, `UPDATE`, or `DELETE` operations. Each DML operation on the table also requires updating the index, which adds overhead and can slow down these operations.
*   **Low Cardinality:** Columns with few distinct values (e.g., `gender`, `status` if there are only a few possible values). In such cases, an index might not significantly reduce the number of block reads.
*   **Columns Not Used in Queries:** Indexing columns that are rarely (or never) used in `WHERE`, `JOIN`, `ORDER BY`, or `GROUP BY` clauses is a waste of resources.

## 4. Types of Indexes

Oracle supports various types of indexes, each optimized for different scenarios.

### B-Tree Index (Default)
This is the most common and default index type. It's suitable for high-cardinality data (many distinct values) and supports efficient retrieval for equality searches and range searches (e.g., `>`, `<`, `BETWEEN`).

### Unique Index
A unique index ensures that all values in the indexed column(s) are unique. Oracle automatically creates a unique index when you define a `PRIMARY KEY` or `UNIQUE` constraint on a table. You can also explicitly create them.

### Composite/Concatenated Index
An index on multiple columns (up to 32 columns). The order of columns in a composite index is crucial, as it dictates how the index can be used by the optimizer. It's most effective when queries include the leading column(s) of the index.

### Function-Based Index (FBI)
An index created on the result of a function or expression involving one or more columns. This is useful when you frequently query using a function on a column (e.g., `UPPER(last_name)`, `TRUNC(hire_date)`).

### Bitmap Index (Briefly)
Suitable for low-cardinality columns (few distinct values) and often used in data warehousing environments. They are highly efficient for complex queries with multiple conditions on low-cardinality columns, but they can suffer from concurrency issues during DML operations in OLTP systems.

---

## 5. Basic Syntax: Creating and Managing Indexes

*   **`CREATE [UNIQUE] INDEX index_name ON table_name (column1 [ASC|DESC], column2 [ASC|DESC], ...);`**
    *   `UNIQUE`: Optional, ensures unique values.
    *   `index_name`: A meaningful name for your index.
    *   `table_name`: The table the index is built on.
    *   `column1, column2, ...`: The column(s) to be indexed. `ASC` (ascending, default) or `DESC` (descending) specifies the sort order.

*   **`ALTER INDEX index_name REBUILD [ONLINE];`**
    *   Used to reorganize an existing index, which can improve performance, reclaim space, or change storage parameters. `ONLINE` allows DML operations on the table while the index is being rebuilt.

*   **`DROP INDEX index_name;`**
    *   Deletes an index.

---

## 6. Examples with Input and Output

Let's set up a sample `employees` table for our examples:

**Input (SQL to create table and insert data):**
```sql
-- Drop table if it exists to ensure a clean start
DROP TABLE employees PURGE;

CREATE TABLE employees (
    employee_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50),
    last_name VARCHAR2(50),
    email VARCHAR2(100) UNIQUE,
    phone_number VARCHAR2(20),
    hire_date DATE,
    job_id VARCHAR2(10),
    salary NUMBER(10, 2),
    department_id NUMBER
);

INSERT INTO employees VALUES (100, 'Steven', 'King', 'steven.king@example.com', '515.123.4567', DATE '2003-06-17', 'AD_PRES', 24000, 90);
INSERT INTO employees VALUES (101, 'Neena', 'Kochhar', 'neena.kochhar@example.com', '515.123.4568', DATE '2005-09-21', 'AD_VP', 17000, 90);
INSERT INTO employees VALUES (102, 'Lex', 'De Haan', 'lex.dehaan@example.com', '515.123.4569', DATE '2001-01-13', 'AD_VP', 17000, 90);
INSERT INTO employees VALUES (103, 'Alexander', 'Hunold', 'alexander.hunold@example.com', '590.423.4567', DATE '2006-01-03', 'IT_PROG', 9000, 60);
INSERT INTO employees VALUES (104, 'Bruce', 'Ernst', 'bruce.ernst@example.com', '590.423.4568', DATE '2007-05-21', 'IT_PROG', 6000, 60);
INSERT INTO employees VALUES (105, 'Diana', 'Lorentz', 'diana.lorentz@example.com', '590.423.5567', DATE '2007-02-07', 'IT_PROG', 4200, 60);
INSERT INTO employees VALUES (106, 'Nancy', 'Greenberg', 'nancy.greenberg@example.com', '515.124.4569', DATE '2002-08-17', 'FI_MGR', 12000, 100);
INSERT INTO employees VALUES (107, 'Daniel', 'Faviet', 'daniel.faviet@example.com', '515.124.4169', DATE '2002-08-16', 'FI_ACCOUNT', 9000, 100);
INSERT INTO employees VALUES (108, 'John', 'Chen', 'john.chen@example.com', '515.124.4269', DATE '2005-09-28', 'FI_ACCOUNT', 8200, 100);
INSERT INTO employees VALUES (109, 'Ismael', 'Sciarra', 'ismael.sciarra@example.com', '515.124.4369', DATE '2005-09-30', 'FI_ACCOUNT', 7700, 100);
INSERT INTO employees VALUES (110, 'Jose Manuel', 'Urman', 'jose.urman@example.com', '515.124.4469', DATE '2006-03-07', 'FI_ACCOUNT', 7800, 100);
INSERT INTO employees VALUES (111, 'Luis', 'Popp', 'luis.popp@example.com', '515.124.4567', DATE '2007-12-07', 'FI_ACCOUNT', 6900, 100);
COMMIT;
```

**Output:**
```
Table EMPLOYEES dropped.
Table EMPLOYEES created.
12 rows inserted.
Commit complete.
```
*(Note: The `PRIMARY KEY` and `UNIQUE` constraints already create indexes `SYS_C00...` behind the scenes.)*

---

### Example 1: Basic B-Tree Index

Creating an index on `last_name` because it's often used in `WHERE` clauses for searching.

**Input (SQL):**
```sql
CREATE INDEX emp_lname_idx ON employees (last_name);
```

**Output:**
```
Index EMP_LNAME_IDX created.
```

**Explanation & Usage (Conceptual):**
Now, if you run a query like `SELECT * FROM employees WHERE last_name = 'King';`, Oracle's optimizer can use `emp_lname_idx` to quickly locate the rows without scanning the entire table.

To *see* if an index is used, you can use `EXPLAIN PLAN`:

**Input (SQL to explain plan):**
```sql
EXPLAIN PLAN FOR SELECT * FROM employees WHERE last_name = 'King';
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

**Output (Example - Actual output might vary slightly depending on Oracle version and environment):**
```
Plan hash value: 2197116743

------------------------------------------------------------------------------------------
| Id  | Operation                   | Name            | Rows  | Bytes | Cost (%CPU)| Time     |
------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT            |                 |     1 |   149 |     1   (0)| 00:00:01 |
|   1 |  TABLE ACCESS BY INDEX ROWID| EMPLOYEES       |     1 |   149 |     1   (0)| 00:00:01 |
|*  2 |   INDEX RANGE SCAN          | EMP_LNAME_IDX   |     1 |       |     1   (0)| 00:00:01 |
------------------------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------
   2 - access("LAST_NAME"='King')
```
**Interpretation:** `INDEX RANGE SCAN` on `EMP_LNAME_IDX` shows that the index was used to find the `last_name = 'King'` efficiently, and then `TABLE ACCESS BY INDEX ROWID` retrieves the full row data using the pointers from the index.

---

### Example 2: Unique Index

Creating a unique index on `phone_number` to ensure no two employees have the same phone number.

**Input (SQL):**
```sql
CREATE UNIQUE INDEX emp_phone_uk ON employees (phone_number);
```

**Output:**
```
Index EMP_PHONE_UK created.
```

**Demonstrating Uniqueness Enforcement:**

**Input (SQL - Attempt to insert a duplicate phone number):**
```sql
INSERT INTO employees VALUES (112, 'Peter', 'Pan', 'peter.pan@example.com', '515.123.4567', DATE '2023-01-01', 'SA_REP', 8000, 80);
```

**Output:**
```
SQL Error: ORA-00001: unique constraint (YOUR_SCHEMA_NAME.EMP_PHONE_UK) violated
```
**Explanation:** Oracle prevents the insertion because `515.123.4567` already exists for `employee_id` 100.

---

### Example 3: Composite Index

Creating an index on `department_id` and `job_id` because these are often combined in queries.

**Input (SQL):**
```sql
CREATE INDEX emp_dept_job_idx ON employees (department_id, job_id);
```

**Output:**
```
Index EMP_DEPT_JOB_IDX created.
```

**Explanation & Usage (Conceptual):**
This index would be effective for queries like:
*   `SELECT * FROM employees WHERE department_id = 90 AND job_id = 'AD_VP';` (uses both columns)
*   `SELECT * FROM employees WHERE department_id = 60;` (uses the leading column `department_id`)

It would *not* be efficient for:
*   `SELECT * FROM employees WHERE job_id = 'IT_PROG';` (cannot use the index efficiently because `job_id` is not the leading column)

**Input (SQL to explain plan for effective use):**
```sql
EXPLAIN PLAN FOR SELECT * FROM employees WHERE department_id = 90 AND job_id = 'AD_VP';
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

**Output (Example):**
```
Plan hash value: 2197116743

------------------------------------------------------------------------------------------
| Id  | Operation                   | Name            | Rows  | Bytes | Cost (%CPU)| Time     |
------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT            |                 |     2 |   298 |     1   (0)| 00:00:01 |
|   1 |  TABLE ACCESS BY INDEX ROWID| EMPLOYEES       |     2 |   298 |     1   (0)| 00:00:01 |
|*  2 |   INDEX RANGE SCAN          | EMP_DEPT_JOB_IDX|     2 |       |     1   (0)| 00:00:01 |
------------------------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------
   2 - access("DEPARTMENT_ID"=90 AND "JOB_ID"='AD_VP')
```
**Interpretation:** `INDEX RANGE SCAN` on `EMP_DEPT_JOB_IDX` confirms the index was used for both conditions.

---

### Example 4: Function-Based Index

Creating an index on the uppercase version of `first_name` to optimize case-insensitive searches.

**Input (SQL):**
```sql
CREATE INDEX emp_upper_fname_idx ON employees (UPPER(first_name));
```

**Output:**
```
Index EMP_UPPER_FNAME_IDX created.
```

**Explanation & Usage (Conceptual):**
This index is useful when your queries look like:
`SELECT * FROM employees WHERE UPPER(first_name) = 'STEVEN';`

**Input (SQL to explain plan for FBI usage):**
```sql
EXPLAIN PLAN FOR SELECT * FROM employees WHERE UPPER(first_name) = 'STEVEN';
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

**Output (Example):**
```
Plan hash value: 2197116743

------------------------------------------------------------------------------------------
| Id  | Operation                   | Name                | Rows  | Bytes | Cost (%CPU)| Time     |
------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT            |                     |     1 |   149 |     1   (0)| 00:00:01 |
|   1 |  TABLE ACCESS BY INDEX ROWID| EMPLOYEES           |     1 |   149 |     1   (0)| 00:00:01 |
|*  2 |   INDEX RANGE SCAN          | EMP_UPPER_FNAME_IDX |     1 |       |     1   (0)| 00:00:01 |
------------------------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------
   2 - access(UPPER("FIRST_NAME")='STEVEN')
```
**Interpretation:** The `INDEX RANGE SCAN` on `EMP_UPPER_FNAME_IDX` shows the function-based index was used.

---

### Example 5: Dropping an Index

Removing the `emp_lname_idx` index.

**Input (SQL):**
```sql
DROP INDEX emp_lname_idx;
```

**Output:**
```
Index EMP_LNAME_IDX dropped.
```

**Explanation:** You would drop an index if it's no longer needed, if it's causing more overhead than benefit, or as a preliminary step before rebuilding it with different parameters.

---

### Example 6: Rebuilding an Index

Rebuilding `emp_dept_job_idx` to defragment it and potentially improve performance/reclaim space.

**Input (SQL):**
```sql
ALTER INDEX emp_dept_job_idx REBUILD;
```

**Output:**
```
Index EMP_DEPT_JOB_IDX altered.
```
**Explanation:** Over time, indexes can become fragmented, or their storage parameters might need adjustment. Rebuilding recreates the index, potentially making it more efficient. You can add `ONLINE` to allow DML operations on the table during the rebuild.

---

### Example 7: Viewing Index Information

Querying Oracle's data dictionary views to see information about indexes.

**Input (SQL - List all user-created indexes on the `employees` table):**
```sql
SELECT
    index_name,
    index_type,
    table_name,
    uniqueness
FROM
    user_indexes
WHERE
    table_name = 'EMPLOYEES';
```

**Output (Example - actual names like `SYS_C00...` are system-generated for constraints):**
```
INDEX_NAME            INDEX_TYPE UNIQUENESS TABLE_NAME
--------------------- ---------- ---------- ----------
SYS_C007421           NORMAL     UNIQUE     EMPLOYEES
SYS_C007422           NORMAL     UNIQUE     EMPLOYEES
EMP_PHONE_UK          NORMAL     UNIQUE     EMPLOYEES
EMP_DEPT_JOB_IDX      NORMAL     NONUNIQUE  EMPLOYEES
EMP_UPPER_FNAME_IDX   FUNCTION-B NONUNIQUE  EMPLOYEES
```
**Explanation:** This shows the type and uniqueness of each index. `SYS_C00...` indexes are created automatically for the `PRIMARY KEY` and `UNIQUE` constraints we defined. `FUNCTION-BASED` confirms our FBI.

**Input (SQL - List columns for indexes on `employees` table):**
```sql
SELECT
    index_name,
    column_position,
    column_name
FROM
    user_ind_columns
WHERE
    table_name = 'EMPLOYEES'
ORDER BY
    index_name, column_position;
```

**Output (Example):**
```
INDEX_NAME            COLUMN_POSITION COLUMN_NAME
--------------------- --------------- --------------------
EMP_DEPT_JOB_IDX                    1 DEPARTMENT_ID
EMP_DEPT_JOB_IDX                    2 JOB_ID
EMP_PHONE_UK                        1 PHONE_NUMBER
EMP_UPPER_FNAME_IDX                 1 SYS_NC00003$
SYS_C007421                         1 EMPLOYEE_ID
SYS_C007422                         1 EMAIL
```
**Explanation:** This shows which columns are part of each index, and their order in composite indexes. `SYS_NC00003$` is an internal name for the expression `UPPER(first_name)` in the function-based index.

---

### Example 8: Monitoring Index Usage

Oracle allows you to monitor index usage to identify indexes that are rarely or never used, which might be candidates for dropping.

**Input (SQL - Start monitoring `emp_dept_job_idx`):**
```sql
ALTER INDEX emp_dept_job_idx MONITORING USAGE;
```

**Output:**
```
Index EMP_DEPT_JOB_IDX altered.
```

**Explanation:** Now, Oracle will track whether this index is used by queries.

*(Perform some queries that might use the index, e.g., `SELECT * FROM employees WHERE department_id = 90 AND job_id = 'AD_VP';`)*

**Input (SQL - Check usage):**
```sql
SELECT index_name, table_name, monitoring, used FROM V$OBJECT_USAGE WHERE index_name = 'EMP_DEPT_JOB_IDX';
```

**Output (Example - after running a query that uses it):**
```
INDEX_NAME          TABLE_NAME MONITORING USED
------------------- ---------- ---------- ----
EMP_DEPT_JOB_IDX    EMPLOYEES  YES        YES
```
**Explanation:** `USED = YES` indicates the index has been used since monitoring began. If it remains `NO` for a long period, it might be an unused index.

**Input (SQL - Stop monitoring):**
```sql
ALTER INDEX emp_dept_job_idx NOMONITORING USAGE;
```

**Output:**
```
Index EMP_DEPT_JOB_IDX altered.
```

---

## 7. Best Practices and Considerations

*   **Don't Over-Index:** Too many indexes can slow down DML operations and consume excessive storage.
*   **Analyze Your Queries:** Index the columns that are most frequently used in `WHERE`, `JOIN`, `ORDER BY`, and `GROUP BY` clauses.
*   **Consider Cardinality:** Index high-cardinality columns (many distinct values) for better selectivity.
*   **Composite Index Order:** For composite indexes, place the most selective or frequently used column first.
*   **Use `EXPLAIN PLAN`:** Always use `EXPLAIN PLAN` to understand how your queries are executed and whether indexes are being used effectively.
*   **Monitor Index Usage:** Regularly check `V$OBJECT_USAGE` to identify and drop unused indexes.
*   **Rebuild When Necessary:** Rebuild indexes if they become fragmented or if there are significant changes to the underlying data that could benefit from a fresh structure.
*   **Invisible Indexes (Oracle 11g+):** You can make an index invisible to the optimizer, allowing you to test the impact of dropping it without actually deleting it. `ALTER INDEX index_name INVISIBLE;`

## 8. Conclusion

Indexes are powerful tools in Oracle SQL for optimizing query performance. By understanding their types, how to create and manage them, and when to apply them, you can significantly improve the responsiveness of your applications. However, it's crucial to use them judiciously, as improper indexing can lead to performance degradation rather than improvement. Always test and monitor the impact of your indexes.