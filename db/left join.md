The `LEFT JOIN` (also known as `LEFT OUTER JOIN`) is a fundamental type of join in SQL that returns all rows from the *left* table (the first table mentioned in the `FROM` clause) and the matching rows from the *right* table. If there is no match in the right table, `NULL` values are returned for all columns of the right table for those non-matching rows.

It's particularly useful when you want to see all entries from one table, even if they don't have a corresponding entry in another related table.

---

# LEFT JOIN in SQL (Oracle)

## 1. What is LEFT JOIN?

The `LEFT JOIN` clause returns all records from the left table (Table A), and the matching records from the right table (Table B). If there is no match, the result is `NULL` from the right side.

**Key Characteristics:**
*   **Preserves Left Table:** Every row from the left table will appear in the result set at least once.
*   **Matching Rows:** For rows in the left table that have a match in the right table, all corresponding columns from both tables are returned.
*   **Non-Matching Rows:** For rows in the left table that do *not* have a match in the right table, the columns from the right table will contain `NULL` values.
*   **Equivalence:** `LEFT JOIN` is synonymous with `LEFT OUTER JOIN`. The `OUTER` keyword is optional.

## 2. Syntax

The basic syntax for `LEFT JOIN` is:

```sql
SELECT
    table1.column1,
    table1.column2,
    table2.column1,
    table2.column2
FROM
    table1  -- This is the "left" table
LEFT JOIN
    table2  -- This is the "right" table
ON
    table1.common_column = table2.common_column;
```

**Alternative using `USING` clause (when join columns have the same name):**

```sql
SELECT
    table1.column1,
    table1.column2,
    table2.column1,
    table2.column2
FROM
    table1
LEFT JOIN
    table2
USING (common_column); -- common_column must exist in both tables
```

## 3. Example Setup

Let's create two tables, `Departments` and `Employees`, and populate them with some data. This data will include scenarios to demonstrate `LEFT JOIN` effectively.

**Input Data (DDL & DML):**

```sql
-- Create Departments Table
CREATE TABLE Departments (
    department_id   NUMBER PRIMARY KEY,
    department_name VARCHAR2(100) NOT NULL
);

-- Insert data into Departments
INSERT INTO Departments (department_id, department_name) VALUES (10, 'IT');
INSERT INTO Departments (department_id, department_name) VALUES (20, 'HR');
INSERT INTO Departments (department_id, department_name) VALUES (30, 'Sales');
INSERT INTO Departments (department_id, department_name) VALUES (40, 'Marketing');
INSERT INTO Departments (department_id, department_name) VALUES (50, 'Research'); -- Department with no employees yet

-- Create Employees Table
CREATE TABLE Employees (
    employee_id     NUMBER PRIMARY KEY,
    employee_name   VARCHAR2(100) NOT NULL,
    department_id   NUMBER,
    salary          NUMBER
);

-- Insert data into Employees
INSERT INTO Employees (employee_id, employee_name, department_id, salary) VALUES (101, 'Alice', 10, 60000);
INSERT INTO Employees (employee_id, employee_name, department_id, salary) VALUES (102, 'Bob', 10, 65000);
INSERT INTO Employees (employee_id, employee_name, department_id, salary) VALUES (103, 'Charlie', 20, 70000);
INSERT INTO Employees (employee_id, employee_name, department_id, salary) VALUES (104, 'David', 30, 75000);
INSERT INTO Employees (employee_id, employee_name, department_id, salary) VALUES (105, 'Eve', NULL, 50000); -- Employee with no assigned department
INSERT INTO Employees (employee_id, employee_name, department_id, salary) VALUES (106, 'Frank', 99, 58000); -- Employee with a non-existent department_id
INSERT INTO Employees (employee_id, employee_name, department_id, salary) VALUES (107, 'Grace', 30, 72000);

-- Commit the changes
COMMIT;
```

**Verify Input Data:**

```sql
SELECT * FROM Departments;
```

**Output:**
```
DEPARTMENT_ID | DEPARTMENT_NAME
--------------|-----------------
           10 | IT
           20 | HR
           30 | Sales
           40 | Marketing
           50 | Research
```

```sql
SELECT * FROM Employees;
```

**Output:**
```
EMPLOYEE_ID | EMPLOYEE_NAME | DEPARTMENT_ID | SALARY
------------|---------------|---------------|-------
        101 | Alice         |            10 |  60000
        102 | Bob           |            10 |  65000
        103 | Charlie       |            20 |  70000
        104 | David         |            30 |  75000
        105 | Eve           |          NULL |  50000
        106 | Frank         |            99 |  58000
        107 | Grace         |            30 |  72000
```

---

## 4. Examples of LEFT JOIN

### Example 1: Basic LEFT JOIN

**Scenario:** Retrieve a list of all employees and their corresponding department names. Even if an employee is not assigned to a department, they should still appear in the list.

**SQL Query:**

```sql
SELECT
    e.employee_name,
    e.salary,
    d.department_name
FROM
    Employees e  -- Left table
LEFT JOIN
    Departments d  -- Right table
ON
    e.department_id = d.department_id
ORDER BY
    e.employee_id;
```

**Output:**

```
EMPLOYEE_NAME | SALARY | DEPARTMENT_NAME
--------------|--------|-----------------
Alice         |  60000 | IT
Bob           |  65000 | IT
Charlie       |  70000 | HR
David         |  75000 | Sales
Eve           |  50000 | NULL            -- Employee Eve has NULL department_id
Frank         |  58000 | NULL            -- Employee Frank has department_id 99, which doesn't exist in Departments
Grace         |  72000 | Sales
```

**Explanation:**
*   All 7 rows from the `Employees` table are returned.
*   For employees `Alice`, `Bob`, `Charlie`, `David`, and `Grace`, a matching `department_id` was found in the `Departments` table, so their `department_name` is displayed.
*   For `Eve`, her `department_id` is `NULL`, so there's no match in `Departments`. Consequently, `department_name` is `NULL`.
*   For `Frank`, his `department_id` is `99`, which doesn't exist in `Departments`. Consequently, `department_name` is `NULL`.
*   Notice that 'Research' department (ID 50) does not appear in the output because `Employees` is the left table, and there are no employees associated with 'Research'.

---

### Example 2: Finding Employees Without a Department (using `WHERE` clause with LEFT JOIN)

**Scenario:** Find all employees who are currently not assigned to any existing department. This means their `department_id` is either `NULL` or refers to a `department_id` that doesn't exist in the `Departments` table.

**SQL Query:**

```sql
SELECT
    e.employee_name,
    e.department_id AS employee_dept_id,
    d.department_name
FROM
    Employees e
LEFT JOIN
    Departments d
ON
    e.department_id = d.department_id
WHERE
    d.department_id IS NULL -- Check if there was no match from the right table
ORDER BY
    e.employee_id;
```

**Output:**

```
EMPLOYEE_NAME | EMPLOYEE_DEPT_ID | DEPARTMENT_NAME
--------------|------------------|-----------------
Eve