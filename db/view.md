This document provides a detailed explanation of SQL Views in Oracle, including their purpose, syntax, various types, and comprehensive examples with input SQL and expected output.

---

# Oracle SQL VIEWS

A **VIEW** in SQL Oracle is a virtual table based on the result-set of an SQL query. A view contains rows and columns, just like a real table. The fields in a view are fields from one or more real tables in the database.

It's important to understand that a view does not store data itself (unlike a regular table or a Materialized View). Instead, it's a stored query that, when referenced, dynamically retrieves its data from the underlying base tables.

## Why Use Views? (Benefits)

Views offer several significant advantages:

1.  **Security:** You can restrict user access to specific rows and/or columns of a table. For example, a user might only need to see employee names and departments, not their salaries or personal contact information.
2.  **Simplicity:** Views can simplify complex queries by pre-joining tables, applying filters, or performing aggregations. Users can then query the view as if it were a simple table.
3.  **Data Abstraction/Independence:** Views can shield users from changes in the underlying table structure. If columns are added, removed, or tables are reorganized, you can often redefine the view without affecting applications that access the data through the view.
4.  **Consistency:** Views ensure that complex calculations or data transformations are applied consistently every time the data is accessed.
5.  **Customization:** Different views can be created for different user groups, presenting the data in a way that is most relevant to their needs.
6.  **Data Aggregation:** Views can pre-calculate sums, averages, counts, etc., making reporting faster and simpler.

## Basic View Syntax

### Creating a View

The fundamental syntax to create a view in Oracle is:

```sql
CREATE [OR REPLACE] [FORCE | NOFORCE] VIEW view_name [(column_name, ...)]
AS
  subquery
  [WITH READ ONLY]
  [WITH CHECK OPTION [CONSTRAINT constraint_name]];
```

*   **`CREATE VIEW`**: The basic command to create a view.
*   **`OR REPLACE`**: If the view already exists, this option drops the existing view and recreates it. This is very useful during development.
*   **`FORCE`**: Creates the view even if the underlying tables do not exist or the `SELECT` statement contains errors. The view will be in an `INVALID` state until the issues are resolved.
*   **`NOFORCE`**: (Default) Creates the view only if the `SELECT` statement is valid and the underlying tables exist.
*   **`view_name`**: The name you give to your view.
*   **`(column_name, ...)`**: An optional list of names for the columns in the view. If omitted, the view columns inherit names from the `SELECT` statement.
*   **`subquery`**: Any valid `SELECT` statement. This is the definition of your view.
*   **`WITH READ ONLY`**: Ensures that no DML operations (INSERT, UPDATE, DELETE) can be performed on the view. It makes the view strictly for querying.
*   **`WITH CHECK OPTION`**: Ensures that any DML operation performed on the view satisfies the view's `WHERE` clause. If a row is inserted or updated via the view, and that operation would cause the row to no longer be part of the view's result set, the operation is rejected.

### Dropping a View

To remove a view from the database:

```sql
DROP VIEW view_name;
```

## Detailed Examples

Let's create some sample tables and data to illustrate the concepts.

### Setup: Sample Tables and Data

```sql
-- Input: Create sample tables
CREATE TABLE employees (
    employee_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50),
    last_name VARCHAR2(50),
    email VARCHAR2(100) UNIQUE,
    phone_number VARCHAR2(20),
    hire_date DATE,
    job_id VARCHAR2(10),
    salary NUMBER(8, 2),
    department_id NUMBER
);

CREATE TABLE departments (
    department_id NUMBER PRIMARY KEY,
    department_name VARCHAR2(100) UNIQUE,
    location VARCHAR2(100)
);

-- Input: Insert data into tables
INSERT INTO departments (department_id, department_name, location) VALUES (10, 'IT', 'New York');
INSERT INTO departments (department_id, department_name, location) VALUES (20, 'HR', 'London');
INSERT INTO departments (department_id, department_name, location) VALUES (30, 'Sales', 'Paris');
INSERT INTO departments (department_id, department_name, location) VALUES (40, 'Finance', 'New York');

INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id) VALUES (101, 'John', 'Doe', 'john.doe@example.com', '555-1234', SYSDATE - 365, 'IT_PROG', 60000, 10);
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id) VALUES (102, 'Jane', 'Smith', 'jane.smith@example.com', '555-5678', SYSDATE - 500, 'HR_REP', 45000, 20);
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id) VALUES (103, 'Peter', 'Jones', 'peter.jones@example.com', '555-9012', SYSDATE - 100, 'SALES_REP', 75000, 30);
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id) VALUES (104, 'Alice', 'Williams', 'alice.w@example.com', '555-3456', SYSDATE - 200, 'IT_PROG', 62000, 10);
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id) VALUES (105, 'Bob', 'Brown', 'bob.b@example.com', '555-7890', SYSDATE - 150, 'FIN_ACC', 58000, 40);
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, department_id) VALUES (106, 'Charlie', 'Davis', 'charlie.d@example.com', '555-1122', SYSDATE - 60, 'SALES_REP', 70000, 30);

COMMIT;
```

**Output (for setup):**
```
Table EMPLOYEES created.
Table DEPARTMENTS created.
6 rows inserted into DEPARTMENTS.
6 rows inserted into EMPLOYEES.
Commit complete.
```

---

### Example 1: Simple View for Security and Simplicity

A view that only shows public employee information (no salary, no phone number) and includes the department name.

**Input:**

```sql
-- Create a simple view
CREATE VIEW public_employee_info AS
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    e.email,
    e.hire_date,
    d.department_name
FROM
    employees e
JOIN
    departments d ON e.department_id = d.department_id
WHERE
    e.department_id = 10; -- Only show IT department employees for this view
```

**Output:**

```
View PUBLIC_EMPLOYEE_INFO created.
```

**Input:** Querying the view

```sql
SELECT * FROM public_employee_info;
```

**Output:**

| EMPLOYEE_ID | FIRST_NAME | LAST_NAME | EMAIL                | HIRE_DATE | DEPARTMENT_NAME |
| ----------- | ---------- | --------- | -------------------- | --------- | --------------- |
| 101         | John       | Doe       | john.doe@example.com | 08-MAY-23 | IT              |
| 104         | Alice      | Williams  | alice.w@example.com  | 27-DEC-23 | IT              |

**Input:** Describing the view (to see its structure)

```sql
DESCRIBE public_employee_info;
```

**Output:**

```
Name          Null?    Type
------------- -------- -------------
EMPLOYEE_ID   NOT NULL NUMBER
FIRST_NAME             VARCHAR2(50)
LAST_NAME              VARCHAR2(50)
EMAIL         NOT NULL VARCHAR2(100)
HIRE_DATE              DATE
DEPARTMENT_NAME NOT NULL VARCHAR2(100)
```

---

### Example 2: Complex View with Aggregation (Not Updatable)

A view that shows the total number of employees and average salary per department.

**Input:**

```sql
-- Create a complex view with aggregation
CREATE VIEW department_stats AS
SELECT
    d.department_name,
    COUNT(e.employee_id) AS total_employees,
    TRUNC(AVG(e.salary), 2) AS average_salary
FROM
    departments d
LEFT JOIN -- Use LEFT JOIN to include departments with no employees
    employees e ON d.department_id = e.department_id
GROUP BY
    d.department_name
ORDER BY
    d.department_name;
```

**Output:**

```
View DEPARTMENT_STATS created.
```

**Input:** Querying the view

```sql
SELECT * FROM department_stats;
```

**Output:**

| DEPARTMENT_NAME | TOTAL_EMPLOYEES | AVERAGE_SALARY |
| --------------- | --------------- | -------------- |
| Finance         | 1               | 58000          |
| HR              | 1               | 45000          |
| IT              | 2               | 61000          |
| Sales           | 2               | 72500          |

**Note:** Views created with `GROUP BY`, aggregate functions (`COUNT`, `AVG`, `SUM`, etc.), `DISTINCT`, `UNION`, or involving joins on multiple tables where columns are not key-preserved are generally **not updatable**. You cannot `INSERT`, `UPDATE`, or `DELETE` directly on `department_stats`.

---

### Example 3: Using `CREATE OR REPLACE`

If you need to modify the definition of an existing view, `CREATE OR REPLACE` is the easiest way.

Let's add the `job_id` to our `public_employee_info` view.

**Input:**

```sql
-- Modify an existing view using OR REPLACE
CREATE OR REPLACE VIEW public_employee_info AS
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    e.email,
    e.hire_date,
    e.job_id, -- Added new column
    d.department_name
FROM
    employees e
JOIN
    departments d ON e.department_id = d.department_id
WHERE
    e.department_id = 10;
```

**Output:**

```
View PUBLIC_EMPLOYEE_INFO created.
```

**Input:** Query the modified view

```sql
SELECT * FROM public_employee_info;
```

**Output:**

| EMPLOYEE_ID | FIRST_NAME | LAST_NAME | EMAIL                | HIRE_DATE | JOB_ID    | DEPARTMENT_NAME |
| ----------- | ---------- | --------- | -------------------- | --------- | --------- | --------------- |
| 101         | John       | Doe       | john.doe@example.com | 08-MAY-23 | IT_PROG   | IT              |
| 104         | Alice      | Williams  | alice.w@example.com  | 27-DEC-23 | IT_PROG   | IT              |

---

### Example 4: `WITH READ ONLY` Option

This option prevents any DML operations (INSERT, UPDATE, DELETE) on the view, enhancing security.

**Input:**

```sql
-- Create a view with READ ONLY option
CREATE VIEW hr_department_employees_ro AS
SELECT
    employee_id,
    first_name,
    last_name,
    email
FROM
    employees
WHERE
    department_id = 20
WITH READ ONLY;
```

**Output:**

```
View HR_DEPARTMENT_EMPLOYEES_RO created.
```

**Input:** Attempt to insert into the `READ ONLY` view

```sql
INSERT INTO hr_department_employees_ro (employee_id, first_name, last_name, email)
VALUES (107, 'Mike', 'Tyson', 'mike.t@example.com');
```

**Output:**

```
Error starting at line : 1 in command -
INSERT INTO hr_department_employees_ro (employee_id, first_name, last_name, email)
VALUES (107, 'Mike', 'Tyson', 'mike.t@example.com')
Error report -
ORA-42399: cannot perform a DML operation on a read-only view
```

---

### Example 5: `WITH CHECK OPTION`

This option ensures that any rows modified or inserted through the view conform to the `WHERE` clause of the view definition.

**Input:**

```sql
-- Create a view for Sales employees with CHECK OPTION
CREATE VIEW sales_employees_check AS
SELECT
    employee_id,
    first_name,
    last_name,
    department_id
FROM
    employees
WHERE
    department_id = 30
WITH CHECK OPTION CONSTRAINT sales_dept_check;
```

**Output:**

```
View SALES_EMPLOYEES_CHECK created.
```

**Input:** Attempt to insert a new sales employee (valid for the view)

```sql
INSERT INTO sales_employees_check (employee_id, first_name, last_name, department_id)
VALUES (108, 'Sarah', 'Connor', 30);
```

**Output:**

```
1 row inserted.
```

**Input:** Attempt to insert an employee for a different department (invalid for the view)

```sql
INSERT INTO sales_employees_check (employee_id, first_name, last_name, department_id)
VALUES (109, 'Kyle', 'Reese', 10);
```

**Output:**

```
Error starting at line : 1 in command -
INSERT INTO sales_employees_check (employee_id, first_name, last_name, department_id)
VALUES (109, 'Kyle', 'Reese', 10)
Error report -
ORA-01402: view WITH CHECK OPTION where-clause violation
```

The `ORA-01402` error indicates that the `WITH CHECK OPTION` constraint was violated because the new row (`department_id = 10`) would not appear in the `sales_employees_check` view (which is filtered for `department_id = 30`).

---

### Example 6: View Updatability (DML on Simple Views)

For simple views based on a single table and no complex operations, you can perform `INSERT`, `UPDATE`, and `DELETE` operations directly on the view, and these changes are propagated to the underlying base table.

**Input:** Check initial data for an employee in the base table

```sql
SELECT employee_id, first_name, last_name, salary FROM employees WHERE employee_id = 101;
```

**Output:**

| EMPLOYEE_ID | FIRST_NAME | LAST_NAME | SALARY |
| ----------- | ---------- | --------- | ------ |
| 101         | John       | Doe       | 60000  |

**Input:** Create a simple updatable view (e.g., for IT employees, showing only a few columns)

```sql
CREATE VIEW it_employee_salaries AS
SELECT employee_id, first_name, last_name, salary
FROM employees
WHERE department_id = 10;
```

**Output:**

```
View IT_EMPLOYEE_SALARIES created.
```

**Input:** Update an employee's salary through the view

```sql
UPDATE it_employee_salaries
SET salary = 65000
WHERE employee_id = 101;
```

**Output:**

```
1 row updated.
```

**Input:** Check the view again

```sql
SELECT employee_id, first_name, last_name, salary FROM it_employee_salaries WHERE employee_id = 101;
```

**Output:**

| EMPLOYEE_ID | FIRST_NAME | LAST_NAME | SALARY |
| ----------- | ---------- | --------- | ------ |
| 101         | John       | Doe       | 65000  |

**Input:** Check the base table to confirm propagation

```sql
SELECT employee_id, first_name, last_name, salary FROM employees WHERE employee_id = 101;
```

**Output:**

| EMPLOYEE_ID | FIRST_NAME | LAST_NAME | SALARY |
| ----------- | ---------- | --------- | ------ |
| 101         | John       | Doe       | 65000  |

**Note:** The changes made via the view were successfully propagated to the `employees` base table.

---

### Example 7: Using Oracle Data Dictionary Views

Oracle provides data dictionary views to get information about existing views.

**Input:** List all views owned by the current user

```sql
SELECT view_name, text FROM user_views;
```

**Output (partial, depending on your views):**

| VIEW_NAME                    | TEXT                                                          |
| ---------------------------- | ------------------------------------------------------------- |
| PUBLIC_EMPLOYEE_INFO         | SELECT e.employee_id, e.first_name, ... FROM employees e JOIN departments d ... WHERE e.department_id = 10 |
| DEPARTMENT_STATS             | SELECT d.department_name, COUNT(e.employee_id) ... GROUP BY d.department_name ... |
| HR_DEPARTMENT_EMPLOYEES_RO   | SELECT employee_id, first_name, ... FROM employees WHERE department_id = 20 |
| SALES_EMPLOYEES_CHECK        | SELECT employee_id, first_name, ... FROM employees WHERE department_id = 30 |
| IT_EMPLOYEE_SALARIES         | SELECT employee_id, first_name, ... FROM employees WHERE department_id = 10 |
| ... (other system views) ... | ...                                                           |

**Input:** Check which columns of a view are updatable (very useful!)

```sql
SELECT table_name, column_name, updatable
FROM user_updatable_columns
WHERE table_name = 'IT_EMPLOYEE_SALARIES';
```

**Output:**

| TABLE_NAME           | COLUMN_NAME | UPDATABLE |
| -------------------- | ----------- | --------- |
| IT_EMPLOYEE_SALARIES | EMPLOYEE_ID | YES       |
| IT_EMPLOYEE_SALARIES | FIRST_NAME  | YES       |
| IT_EMPLOYEE_SALARIES | LAST_NAME   | YES       |
| IT_EMPLOYEE_SALARIES | SALARY      | YES       |

---

## View Updatability Rules

A view is inherently updatable if and only if all DML operations (INSERT, UPDATE, DELETE) on the view can be unambiguously translated into corresponding DML operations on the underlying base table(s).

A view is **NOT updatable** if its `SELECT` statement contains any of the following:

*   **Aggregate functions** (`SUM`, `AVG`, `COUNT`, `MAX`, `MIN`, etc.)
*   A **`GROUP BY` clause**.
*   A **`DISTINCT` keyword**.
*   **Set operators** (`UNION`, `UNION ALL`, `INTERSECT`, `MINUS`).
*   **`ROWNUM` pseudo-column** in the `SELECT` list or `WHERE` clause.
*   **`CONNECT BY` clause**.
*   **Subqueries** in the `SELECT` list.
*   **Joins to multiple tables** where the primary key of the "target" table is not included or is not "key-preserved" in the view. A column is key-preserved if it is part of the primary key of the base table, and that primary key is also the primary key of the join result.
*   **Columns derived from expressions** (e.g., `salary * 1.1`, `UPPER(first_name)`). You can't update `UPPER(first_name)` directly.
*   **`WITH READ ONLY`** clause.

For views involving multiple tables (joins), Oracle tries to determine if the DML operation affects only one "key-preserved" table. If the update is restricted to columns from a single key-preserved table, it might be allowed. However, it's generally safer to assume multi-table join views are not updatable unless carefully designed.

## Materialized Views (Brief Distinction)

While regular views are virtual tables, Oracle also offers **Materialized Views**.

*   **Regular View:**
    *   Does **not** store data.
    *   Always reflects current data from base tables.
    *   Query performance depends on underlying query execution.
*   **Materialized View:**
    *   **Does** store data (it's a physical copy).
    *   Can be refreshed periodically (on commit, on demand, or at scheduled intervals) to reflect changes from base tables.
    *   Used for query **performance optimization**, especially for complex queries, data warehousing, and distributed environments.
    *   Trades off data freshness for query speed.

Creating a Materialized View:
```sql
CREATE MATERIALIZED VIEW mv_department_stats
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
AS
SELECT
    d.department_name,
    COUNT(e.employee_id) AS total_employees,
    TRUNC(AVG(e.salary), 2) AS average_salary
FROM
    departments d
LEFT JOIN
    employees e ON d.department_id = e.department_id
GROUP BY
    d.department_name;
```

## Limitations of Views

*   **Performance Overhead:** For complex views, the underlying query is re-executed every time the view is accessed. This can add overhead compared to querying a pre-calculated table. Materialized views address this.
*   **Debugging:** Debugging issues in views can sometimes be more complex, as the error might originate in the underlying base tables or the view's definition.
*   **Schema Changes:** While views offer some abstraction, significant changes to base tables (e.g., renaming columns that the view uses) still require the view to be modified or recreated.

---

This detailed overview and examples should provide a solid understanding of SQL Views in Oracle. Remember to always choose the right type of view (standard vs. materialized) based on your specific requirements for data freshness, performance, and updatability.