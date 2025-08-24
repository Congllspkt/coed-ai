The `UNION` operator in Oracle SQL is used to combine the result sets of two or more `SELECT` statements into a single result set. It automatically removes duplicate rows from the final result.

## UNION Operator in Oracle SQL

### 1. Introduction

The `UNION` operator is a set operator that allows you to stack one result set on top of another. It's fundamental for scenarios where you need to retrieve data from different tables, or different parts of the same table, and present them as a unified list, ensuring that each unique row appears only once.

### 2. Core Concept

When you use `UNION`, Oracle performs the following steps:
1.  Executes the first `SELECT` statement.
2.  Executes the second `SELECT` statement (and any subsequent ones).
3.  Combines all the rows from these individual result sets.
4.  Scans the combined set for identical rows and removes duplicates.
5.  Returns the final, de-duplicated result set.

### 3. Syntax

```sql
SELECT column1, column2, ...
FROM table1
WHERE condition1
UNION
SELECT column1, column2, ...
FROM table2
WHERE condition2
[ORDER BY column_name | column_position [ASC | DESC], ...];
```

**Key Points about Syntax:**

*   The `UNION` keyword separates the `SELECT` statements.
*   The `ORDER BY` clause, if used, must appear at the very end of the entire `UNION` query, not on individual `SELECT` statements. It orders the *final combined result set*.
*   Column names in the output will be determined by the column names (or aliases) from the **first `SELECT` statement**.

### 4. Characteristics and Rules

For `UNION` (and other set operators like `INTERSECT`, `MINUS`, `UNION ALL`) to work correctly, the following rules must be met:

1.  **Number of Columns:** Each `SELECT` statement within the `UNION` query must have the **same number of columns** in its `SELECT` list.
2.  **Data Type Compatibility:** The corresponding columns in each `SELECT` statement must have **compatible data types**. Oracle will attempt implicit conversion if types are similar (e.g., `NUMBER` and `VARCHAR2` containing only numbers, `DATE` and `VARCHAR2` containing date strings). However, it's best practice to ensure the types are identical or explicitly cast them for clarity and to prevent unexpected conversion errors. The data type of the output column is determined by Oracle's data type precedence rules (e.g., if you union a `NUMBER` with a `VARCHAR2`, the output column might become `VARCHAR2`).
3.  **Column Names:** The column names in the final result set are inherited from the **first `SELECT` statement**. You can use column aliases in the first `SELECT` to name your output columns.
4.  **De-duplication:** `UNION` automatically removes all duplicate rows. If you want to keep all rows, including duplicates, use `UNION ALL`.
5.  **Performance:** Because `UNION` performs a de-duplication step, it is generally slower than `UNION ALL`.

### 5. `UNION ALL` (for Comparison)

It's crucial to understand `UNION ALL` alongside `UNION`.

*   **`UNION ALL`** combines the result sets of two or more `SELECT` statements **without removing duplicate rows**.
*   It's typically **faster** than `UNION` because it avoids the overhead of sorting and removing duplicates.
*   Use `UNION ALL` when you are certain there are no duplicates you care about, or when you explicitly want to include all duplicate rows.

**Syntax for `UNION ALL`:**

```sql
SELECT column1, column2, ...
FROM table1
WHERE condition1
UNION ALL
SELECT column1, column2, ...
FROM table2
WHERE condition2
[ORDER BY column_name | column_position [ASC | DESC], ...];
```

### 6. Examples

Let's set up some sample tables and data to illustrate `UNION` and `UNION ALL`.

#### Sample Tables Creation and Data Insertion

```sql
-- Table 1: Employees
CREATE TABLE Employees (
    EmployeeID NUMBER PRIMARY KEY,
    FirstName VARCHAR2(50),
    LastName VARCHAR2(50),
    Department VARCHAR2(50),
    Salary NUMBER(10, 2)
);

INSERT INTO Employees (EmployeeID, FirstName, LastName, Department, Salary) VALUES (1, 'Alice', 'Smith', 'HR', 60000);
INSERT INTO Employees (EmployeeID, FirstName, LastName, Department, Salary) VALUES (2, 'Bob', 'Johnson', 'IT', 75000);
INSERT INTO Employees (EmployeeID, FirstName, LastName, Department, Salary) VALUES (3, 'Charlie', 'Brown', 'IT', 80000);
INSERT INTO Employees (EmployeeID, FirstName, LastName, Department, Salary) VALUES (4, 'David', 'Davis', 'Sales', 70000);
INSERT INTO Employees (EmployeeID, FirstName, LastName, Department, Salary) VALUES (5, 'Eve', 'Smith', 'Marketing', 62000);
INSERT INTO Employees (EmployeeID, FirstName, LastName, Department, Salary) VALUES (6, 'Frank', 'Green', 'HR', 60000); -- Duplicate salary for HR

-- Table 2: Consultants (simulating a different type of personnel)
CREATE TABLE Consultants (
    ConsultantID NUMBER PRIMARY KEY,
    FirstName VARCHAR2(50),
    LastName VARCHAR2(50),
    Project VARCHAR2(50),
    HourlyRate NUMBER(10, 2)
);

INSERT INTO Consultants (ConsultantID, FirstName, LastName, Project, HourlyRate) VALUES (101, 'Grace', 'Hopper', 'ERP Impl', 150);
INSERT INTO Consultants (ConsultantID, FirstName, LastName, Project, HourlyRate) VALUES (102, 'Alice', 'Smith', 'HR Audit', 120); -- Alice Smith is also a consultant
INSERT INTO Consultants (ConsultantID, FirstName, LastName, Project, HourlyRate) VALUES (103, 'Heidi', 'Klum', 'Marketing Strat', 110);
INSERT INTO Consultants (ConsultantID, FirstName, LastName, Project, HourlyRate) VALUES (104, 'Eve', 'Smith', 'Cloud Migrat', 130); -- Eve Smith is also a consultant
```

---

#### Example 1: Basic `UNION` - Combining and De-duplicating Names

Let's get a unique list of all first names of people in both `Employees` and `Consultants`.

**Input (Data in Tables):**

`Employees`:
| EMPLOYEEID | FIRSTNAME | LASTNAME | DEPARTMENT | SALARY |
| ---------- | --------- | -------- | ---------- | ------ |
| 1          | Alice     | Smith    | HR         | 60000  |
| 2          | Bob       | Johnson  | IT         | 75000  |
| 3          | Charlie   | Brown    | IT         | 80000  |
| 4          | David     | Davis    | Sales      | 70000  |
| 5          | Eve       | Smith    | Marketing  | 62000  |
| 6          | Frank     | Green    | HR         | 60000  |

`Consultants`:
| CONSULTANTID | FIRSTNAME | LASTNAME | PROJECT       | HOURLYRATE |
| ------------ | --------- | -------- | ------------- | ---------- |
| 101          | Grace     | Hopper   | ERP Impl      | 150        |
| 102          | Alice     | Smith    | HR Audit      | 120        |
| 103          | Heidi     | Klum     | Marketing Strat | 110        |
| 104          | Eve       | Smith    | Cloud Migrat  | 130        |

**Query:**

```sql
SELECT FirstName FROM Employees
UNION
SELECT FirstName FROM Consultants;
```

**Output (Oracle SQL Developer/SQL*Plus):**

```
FIRSTNAME
---------
Alice
Bob
Charlie
David
Eve
Frank
Grace
Heidi

8 rows selected.
```
**Explanation:** Notice that `Alice` and `Eve` appear only once, even though they are present in both tables. `UNION` automatically de-duplicated them.

---

#### Example 2: `UNION ALL` - Combining without De-duplication

Let's get all first names, including duplicates.

**Input:** (Same as Example 1)

**Query:**

```sql
SELECT FirstName FROM Employees
UNION ALL
SELECT FirstName FROM Consultants;
```

**Output:**

```
FIRSTNAME
---------
Alice
Bob
Charlie
David
Eve
Frank
Grace
Alice
Heidi
Eve

10 rows selected.
```
**Explanation:** `Alice` and `Eve` now appear twice because `UNION ALL` includes all rows from both result sets without checking for duplicates.

---

#### Example 3: `UNION` with Compatible Columns and Aliases

Let's combine a list of all personnel (employees and consultants), showing their full name, their primary role/department/project, and their "type" (Employee/Consultant). We'll also demonstrate column aliases and type compatibility.

**Input:** (Same as Example 1)

**Query:**

```sql
SELECT
    FirstName || ' ' || LastName AS FullName,
    Department AS RoleContext,
    'Employee' AS PersonnelType,
    Salary AS CompensationValue -- Renaming Salary to a generic term
FROM Employees
UNION
SELECT
    FirstName || ' ' || LastName AS FullName,
    Project AS RoleContext,
    'Consultant' AS PersonnelType,
    HourlyRate * 160 AS CompensationValue -- Assuming 160 hours/month for rough comparison
FROM Consultants
ORDER BY FullName; -- ORDER BY applies to the final result
```

**Output:**

```
FULLNAME       ROLECONTEXT       PERSONNELTYPE COMPENSATIONVALUE
-------------- ----------------- ------------- -----------------
Alice Smith    HR                Employee      60000
Bob Johnson    IT                Employee      75000
Charlie Brown  IT                Employee      80000
David Davis    Sales             Employee      70000
Eve Smith      Marketing         Employee      62000
Frank Green    HR                Employee      60000
Grace Hopper   ERP Impl          Consultant    24000
Heidi Klum     Marketing Strat   Consultant    17600

8 rows selected.
```
**Explanation:**
*   We use string concatenation (`||`) to create `FullName`.
*   `Department` and `Project` are aliased to `RoleContext` because they represent a similar concept in different tables.
*   A literal string `'Employee'` or `'Consultant'` is selected to create a `PersonnelType` column.
*   `Salary` and `HourlyRate * 160` are both numeric and represent compensation, so they are compatible and aliased to `CompensationValue`.
*   The `ORDER BY FullName` clause sorts the entire combined result.
*   Notice that "Alice Smith" and "Eve Smith" are present in both original tables, but since the `RoleContext` and `PersonnelType` values are different, the *entire row* is not considered a duplicate, so both their Employee and Consultant records appear. If *all* selected columns were identical for both Alice Employee and Alice Consultant, only one would appear.

---

#### Example 4: Mismatched Column Counts (Error Example)

This demonstrates what happens when the number of columns doesn't match.

**Query:**

```sql
SELECT EmployeeID, FirstName FROM Employees
UNION
SELECT ConsultantID, FirstName, LastName FROM Consultants; -- Error: too many columns in second SELECT
```

**Output (Error Message):**

```
Error starting at line : 1 in command -
SELECT EmployeeID, FirstName FROM Employees
UNION
SELECT ConsultantID, FirstName, LastName FROM Consultants
Error at Command Line : 4 Column : 1
Error report -
SQL Error: ORA-01789: query block has incorrect number of result columns
01789. 00000 -  "query block has incorrect number of result columns"
*Cause:    Union, minus or intersect types of queries must have the same number of result columns.
*Action:   Correct the number of result columns.
```
**Explanation:** Oracle explicitly tells you that the number of result columns must be the same.

---

#### Example 5: Data Type Mismatch (Compatibility Example)

Oracle is quite flexible with implicit conversions, but it's important to be aware.

**Query:** (Combining a number and a string, where the string can be converted to a number)

```sql
SELECT EmployeeID, Salary FROM Employees
UNION ALL
SELECT ConsultantID, TO_NUMBER(HourlyRate) FROM Consultants; -- HourlyRate is already NUMBER, this is just for demonstration
```

This would work because `Salary` and `HourlyRate` are both `NUMBER`. If `HourlyRate` was `VARCHAR2` and contained only numbers, Oracle would still likely convert it successfully without `TO_NUMBER` explicitly, but it's good practice to ensure consistency or cast.

**Query:** (Combining a date and a string that cannot be converted to a date)

```sql
-- Let's imagine we have a table with a DATE column and try to union it with a VARCHAR2 column
-- This would be problematic if the VARCHAR2 was not a valid date format.
-- For example:
-- SELECT hire_date FROM Employees
-- UNION ALL
-- SELECT 'NOT A DATE' FROM DUAL; -- This would fail
```

### 7. When to use `UNION` vs. `UNION ALL`

| Feature           | `UNION`                                     | `UNION ALL`                                  |
| :---------------- | :------------------------------------------ | :------------------------------------------- |
| **Duplicate Rows** | Removes duplicate rows                      | Keeps all duplicate rows                     |
| **Performance**   | Slower (due to de-duplication/sorting)     | Faster (no de-duplication overhead)        |
| **Use Case**      | When you need a distinct list of combined data. | When you need all data and duplicates are acceptable or expected. |
| **Examples**      | - Unique list of all product IDs from multiple warehouses. <br> - A consolidated list of all customer email addresses. | - Combining sales transactions from different quarters, where individual transactions can be identical across quarters. <br> - Appending log entries from different servers. |

### 8. Common Pitfalls and Considerations

*   **Column Order:** The order of columns in the `SELECT` list matters for compatibility, not just their names. The first column of the first `SELECT` must be compatible with the first column of the second `SELECT`, and so on.
*   **NULL Values:** `NULL` values are treated like any other value when checking for duplicates. Two rows are considered duplicates if all their non-NULL columns are identical and their NULL columns match positionally.
*   **Performance Tuning:** For very large datasets, `UNION ALL` is often preferred for performance. If de-duplication is critical, consider if there's a more efficient way to achieve it (e.g., using `DISTINCT` on a subquery or a `GROUP BY` clause if only specific columns need to be unique).
*   **`ORDER BY` Placement:** Always remember `ORDER BY` must be at the very end of the entire `UNION` statement.

### 9. Summary

The `UNION` operator is a powerful tool in Oracle SQL for combining result sets from multiple queries. It's essential for creating consolidated views of data across different tables or different logical sections of data. Always consider the impact of duplicate removal and performance when choosing between `UNION` and `UNION ALL`, and ensure your queries adhere to the rules of column count and data type compatibility.

---

#### Cleanup (Optional)

```sql
DROP TABLE Employees;
DROP TABLE Consultants;
```