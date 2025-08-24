A `RIGHT JOIN` (also known as `RIGHT OUTER JOIN`) in SQL is used to combine rows from two or more tables based on a related column between them.

**Key Characteristic:**
A `RIGHT JOIN` returns:
1.  **All rows** from the **right table**, regardless of whether they have a match in the left table.
2.  **Matching rows** from the **left table**.
3.  If there is no match for a right table row in the left table, `NULL` values will be returned for all columns from the left table.

---

## `RIGHT JOIN` in SQL (Oracle)

### 1. Basic Definition

The `RIGHT JOIN` clause returns all records from the right table (table B in `A RIGHT JOIN B`) and the matched records from the left table (table A). If there is no match for a row in the right table, the columns from the left table will have `NULL` values.

### 2. Syntax

```sql
SELECT column1, column2, ...
FROM   left_table
RIGHT JOIN right_table
ON     left_table.common_column = right_table.common_column;
```

**Alternatively, you can use `RIGHT OUTER JOIN` which is synonymous:**

```sql
SELECT column1, column2, ...
FROM   left_table
RIGHT OUTER JOIN right_table
ON     left_table.common_column = right_table.common_column;
```

### 3. How it Works

Imagine two tables: `TableA` (left) and `TableB` (right).
When you perform `TableA RIGHT JOIN TableB ON condition`:

1.  The database starts by taking **every single row** from `TableB`.
2.  For each row in `TableB`, it tries to find matching rows in `TableA` based on the `ON` condition.
3.  If a match is found, the columns from the matching `TableA` row and the `TableB` row are combined into a single result row.
4.  If **no match** is found in `TableA` for a particular row in `TableB`, that `TableB` row is still included in the result set. However, all columns that would normally come from `TableA` for that row will have `NULL` values.
5.  Rows in `TableA` that **do not have a match** in `TableB` are **not included** in the result set.

### 4. Visual Representation

```
      +---------------------+      +---------------------+
      |      Left Table     |      |     Right Table     |
      |---------------------|      |---------------------|
      |   (Matching Rows)   |<-----|   (Matching Rows)   |
      |                     |----->|                     |
      +---------------------+      |---------------------|
                                   | (Unmatched Rows)    |
                                   +---------------------+

                  <------------------------------------>
                             Resulting Set
                       (All of Right, Matched Left,
                        NULLs for Unmatched Left)
```

### 5. Example

Let's set up two tables: `Employees` and `Departments`.

**Input Data Setup:**

```sql
-- Create Departments table
CREATE TABLE Departments (
    dept_id NUMBER PRIMARY KEY,
    dept_name VARCHAR2(100)
);

-- Insert data into Departments
INSERT INTO Departments VALUES (10, 'HR');
INSERT INTO Departments VALUES (20, 'Sales');
INSERT INTO Departments VALUES (30, 'IT');
INSERT INTO Departments VALUES (40, 'Finance'); -- This department has no employees
INSERT INTO Departments VALUES (50, 'Marketing'); -- This department also has no employees
COMMIT;

-- Create Employees table
CREATE TABLE Employees (
    emp_id NUMBER PRIMARY KEY,
    emp_name VARCHAR2(100),
    dept_id NUMBER
    -- FOREIGN KEY (dept_id) REFERENCES Departments(dept_id) -- Not strictly needed for the join itself
);

-- Insert data into Employees
INSERT INTO Employees VALUES (101, 'Alice', 10);
INSERT INTO Employees VALUES (102, 'Bob', 20);
INSERT INTO Employees VALUES (103, 'Charlie', 10);
INSERT INTO Employees VALUES (104, 'David', 60); -- Employee in a non-existent department (will not appear in RIGHT JOIN (Emp RIGHT JOIN Dept))
INSERT INTO Employees VALUES (105, 'Eve', 20);
INSERT INTO Employees VALUES (106, 'Frank', NULL); -- Employee with no assigned department
COMMIT;
```

**Input Data (Tables):**

**`Departments` Table:**
```
+---------+-------------+
| DEPT_ID | DEPT_NAME   |
+---------+-------------+
| 10      | HR          |
| 20      | Sales       |
| 30      | IT          |
| 40      | Finance     |
| 50      | Marketing   |
+---------+-------------+
```

**`Employees` Table:**
```
+--------+----------+---------+
| EMP_ID | EMP_NAME | DEPT_ID |
+--------+----------+---------+
| 101    | Alice    | 10      |
| 102    | Bob      | 20      |
| 103    | Charlie  | 10      |
| 104    | David    | 60      |
| 105    | Eve      | 20      |
| 106    | Frank    | NULL    |
+--------+----------+---------+
```

---

### Example 1: Basic `RIGHT JOIN`

Retrieve all departments and any employees associated with them. Departments without employees should still be listed.

**Query:**
```sql
SELECT
    e.emp_name,
    d.dept_name
FROM
    Employees e
RIGHT JOIN
    Departments d ON e.dept_id = d.dept_id;
```

**Explanation:**
The `Departments` table is the **right table**. This query will return every department, and if there's an employee in that department, their name will appear. If a department has no employees, `NULL` will appear for `emp_name`. Notice that `David` (dept_id 60) and `Frank` (dept_id NULL) from the `Employees` table are not included because their `dept_id` does not match any `dept_id` in the `Departments` table, and `Departments` is the right table (dominant).

**Output:**
```
+----------+-------------+
| EMP_NAME | DEPT_NAME   |
+----------+-------------+
| Alice    | HR          |
| Charlie  | HR          |
| Bob      | Sales       |
| Eve      | Sales       |
| NULL     | IT          |
| NULL     | Finance     |
| NULL     | Marketing   |
+----------+-------------+
```
*(Note: The order of rows might vary, but all these rows will be present.)*

---

### Example 2: Identifying Departments with No Employees

Using `RIGHT JOIN` to find departments that currently have no employees.

**Query:**
```sql
SELECT
    d.dept_name
FROM
    Employees e
RIGHT JOIN
    Departments d ON e.dept_id = d.dept_id
WHERE
    e.emp_id IS NULL; -- Filter for rows where the left table (Employees) had no match
```

**Explanation:**
This query performs the same `RIGHT JOIN` as above but then filters the results. By checking `WHERE e.emp_id IS NULL`, we are specifically looking for rows where a department (from the right table) had no matching employee (from the left table), resulting in `NULL` values for all employee columns, including `emp_id`.

**Output:**
```
+-------------+
| DEPT_NAME   |
+-------------+
| IT          |
| Finance     |
| Marketing   |
+-------------+
```

---

### Example 3: `RIGHT JOIN` with an additional condition

Retrieve employees and their departments, but only for departments starting with 'S'.

**Query:**
```sql
SELECT
    e.emp_name,
    d.dept_name
FROM
    Employees e
RIGHT JOIN
    Departments d ON e.dept_id = d.dept_id
WHERE
    d.dept_name LIKE 'S%';
```

**Explanation:**
The `RIGHT JOIN` still produces all departments and their matching employees (or NULLs for unmatched employees). The `WHERE` clause then filters this *entire result set* to only include rows where the `dept_name` from the `Departments` table starts with 'S'.

**Output:**
```
+----------+-------------+
| EMP_NAME | DEPT_NAME   |
+----------+-------------+
| Bob      | Sales       |
| Eve      | Sales       |
+----------+-------------+
```

---

### When to use `RIGHT JOIN`?

*   When you need to retrieve all records from one table (the right one) and only the matching records from another table (the left one).
*   To identify rows in the right table that do not have a corresponding entry in the left table (as shown in Example 2).
*   It's often used when you have a "master" or "lookup" table (which you want all records from) and a "transactional" or "detail" table (where matches are optional).

### `RIGHT JOIN` vs. `LEFT JOIN`

`RIGHT JOIN` and `LEFT JOIN` are symmetrical. Any query written with a `RIGHT JOIN` can be rewritten as a `LEFT JOIN` by simply swapping the order of the tables.

**Example:**
`Employees e RIGHT JOIN Departments d ON e.dept_id = d.dept_id;`
is equivalent to:
`Departments d LEFT JOIN Employees e ON d.dept_id = e.dept_id;`

Both will produce the exact same result set for the selected columns. The choice between `LEFT JOIN` and `RIGHT JOIN` often comes down to readability and which table you naturally consider to be the "primary" or "starting" point for your query. `LEFT JOIN` is generally more common in practice.