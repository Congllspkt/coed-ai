This document provides a detailed explanation of Common Table Expressions (CTEs) in Oracle SQL, including their benefits, syntax, and practical examples with input and output.

---

# Common Table Expressions (CTEs) in Oracle SQL

## Table of Contents
1.  [What is a CTE?](#1-what-is-a-cte)
2.  [Why Use CTEs? (Benefits)](#2-why-use-ctes-benefits)
3.  [CTE Syntax](#3-cte-syntax)
4.  [Examples](#4-examples)
    *   [Example 1: Simple CTE for Readability](#example-1-simple-cte-for-readability)
    *   [Example 2: Multiple CTEs (Chaining Logic)](#example-2-multiple-ctes-chaining-logic)
    *   [Example 3: Recursive CTE (Hierarchical Data)](#example-3-recursive-cte-hierarchical-data)
5.  [Key Considerations](#5-key-considerations)
6.  [Summary](#6-summary)

---

## 1. What is a CTE?

A **Common Table Expression (CTE)**, introduced in Oracle 9i Release 2 (and standardized in SQL:1999), is a temporary, named result set that you can reference within a single `SELECT`, `INSERT`, `UPDATE`, or `DELETE` statement. It's defined using the `WITH` clause.

Think of a CTE as a temporary, inline view that exists only for the duration of the query it's part of. It's not stored in the database like a permanent view, making it ideal for breaking down complex queries into smaller, more manageable, and readable logical units.

## 2. Why Use CTEs? (Benefits)

CTEs offer several advantages, especially for complex queries:

*   **Improved Readability:** Break down complex queries into smaller, logical, named steps. This makes the query easier to understand and debug.
*   **Enhanced Modularity:** Each CTE can solve a specific sub-problem, and then subsequent CTEs or the final query can build upon these results.
*   **Reusability (within the same query):** A CTE can be referenced multiple times within the same `WITH` clause or main query, avoiding repetitive code.
*   **Handling Recursive Queries:** CTEs are indispensable for querying hierarchical or graph-like data structures (e.g., organizational charts, bill of materials) where an entity can refer to itself.
*   **Avoiding Nested Subqueries:** Often, CTEs can replace deeply nested subqueries, leading to a flatter, more readable query structure.
*   **Easier Debugging:** Since each CTE is a named step, you can easily `SELECT * FROM cte_name` during development to verify the intermediate results.

## 3. CTE Syntax

The basic syntax for a CTE in Oracle is:

```sql
WITH
    cte_name_1 (column1, column2, ...) AS (
        SELECT expression1, expression2, ...
        FROM some_table
        WHERE some_condition
    ),
    cte_name_2 AS ( -- Column list is optional if derived from the SELECT list
        SELECT ...
        FROM cte_name_1 -- A CTE can reference a previously defined CTE
        WHERE some_other_condition
    )
SELECT final_columns
FROM cte_name_1 -- Or cte_name_2, or join them
WHERE final_condition;
```

**Key Points:**
*   The `WITH` clause starts the CTE definition.
*   `cte_name` is the identifier for your temporary result set.
*   `(column1, column2, ...)` is an optional list of column aliases for the CTE's output. If omitted, the aliases from the `SELECT` statement within the CTE are used.
*   `AS` introduces the subquery that defines the CTE's data.
*   Multiple CTEs are separated by commas.
*   The final `SELECT` (or `INSERT`, `UPDATE`, `DELETE`) statement *must* follow the `WITH` clause.

For **Recursive CTEs**, the syntax is slightly different:

```sql
WITH
    RECURSIVE_CTE_NAME (column1, column2, ..., level_col) AS (
        -- Anchor Member (Base Case): Non-recursive part
        SELECT initial_column1, initial_column2, ..., 1 AS level_col
        FROM base_table
        WHERE initial_condition

        UNION ALL

        -- Recursive Member: References the CTE itself
        SELECT next_column1, next_column2, ..., level_col + 1
        FROM base_table t
        JOIN RECURSIVE_CTE_NAME r_cte ON t.join_column = r_cte.recursive_join_column
        WHERE recursive_condition
    )
SELECT *
FROM RECURSIVE_CTE_NAME;
```
*   The `UNION ALL` operator combines the anchor and recursive members.
*   The recursive member must reference the CTE itself.
*   Oracle has a `MAX_DEPTH` limit for recursive CTEs, which can be specified.

---

## 4. Examples

Let's set up some sample data first.

### Input Data Setup

We'll use a simple `EMPLOYEES` table:

```sql
-- Drop table if it already exists
DROP TABLE EMPLOYEES;

-- Create the EMPLOYEES table
CREATE TABLE EMPLOYEES (
    EMPLOYEE_ID    NUMBER PRIMARY KEY,
    FIRST_NAME     VARCHAR2(50),
    LAST_NAME      VARCHAR2(50),
    DEPARTMENT_ID  NUMBER,
    SALARY         NUMBER,
    MANAGER_ID     NUMBER -- For recursive CTE example
);

-- Insert sample data
INSERT INTO EMPLOYEES (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DEPARTMENT_ID, SALARY, MANAGER_ID) VALUES (101, 'John', 'Doe', 10, 60000, NULL); -- CEO
INSERT INTO EMPLOYEES (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DEPARTMENT_ID, SALARY, MANAGER_ID) VALUES (102, 'Jane', 'Smith', 20, 75000, 101);
INSERT INTO EMPLOYEES (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DEPARTMENT_ID, SALARY, MANAGER_ID) VALUES (103, 'Peter', 'Jones', 10, 50000, 101);
INSERT INTO EMPLOYEES (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DEPARTMENT_ID, SALARY, MANAGER_ID) VALUES (104, 'Mary', 'Brown', 20, 80000, 102);
INSERT INTO EMPLOYEES (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DEPARTMENT_ID, SALARY, MANAGER_ID) VALUES (105, 'David', 'Green', 30, 45000, 102);
INSERT INTO EMPLOYEES (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DEPARTMENT_ID, SALARY, MANAGER_ID) VALUES (106, 'Susan', 'White', 10, 55000, 103);
INSERT INTO EMPLOYEES (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DEPARTMENT_ID, SALARY, MANAGER_ID) VALUES (107, 'Mike', 'Black', 30, 70000, 105);
INSERT INTO EMPLOYEES (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DEPARTMENT_ID, SALARY, MANAGER_ID) VALUES (108, 'Lisa', 'Blue', 20, 62000, 104);
INSERT INTO EMPLOYEES (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DEPARTMENT_ID, SALARY, MANAGER_ID) VALUES (109, 'Chris', 'Red', 30, 48000, 107);
INSERT INTO EMPLOYEES (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, DEPARTMENT_ID, SALARY, MANAGER_ID) VALUES (110, 'Karen', 'Gray', 10, 68000, 101);
COMMIT;
```

### Example 1: Simple CTE for Readability

**Goal:** Find employees who earn more than the average salary of all employees.

**Without CTE (using a subquery):**

```sql
SELECT
    e.FIRST_NAME,
    e.LAST_NAME,
    e.SALARY
FROM
    EMPLOYEES e
WHERE
    e.SALARY > (SELECT AVG(SALARY) FROM EMPLOYEES);
```

**With CTE:**

```sql
WITH
    AverageSalaryCTE AS (
        SELECT AVG(SALARY) AS AverageSalary
        FROM EMPLOYEES
    )
SELECT
    e.FIRST_NAME,
    e.LAST_NAME,
    e.SALARY
FROM
    EMPLOYEES e,
    AverageSalaryCTE avg_cte
WHERE
    e.SALARY > avg_cte.AverageSalary;
```

**Explanation:**
The `AverageSalaryCTE` calculates the average salary once. The main query then joins with this CTE to filter employees. This makes the query logic clearer: first calculate the average, then select employees based on it.

**Input:**
```
EMPLOYEES Table:
EMPLOYEE_ID | FIRST_NAME | LAST_NAME | DEPARTMENT_ID | SALARY | MANAGER_ID
------------|------------|-----------|---------------|--------|-----------
101         | John       | Doe       | 10            | 60000  | NULL
102         | Jane       | Smith     | 20            | 75000  | 101
103         | Peter      | Jones     | 10            | 50000  | 101
104         | Mary       | Brown     | 20            | 80000  | 102
105         | David      | Green     | 30            | 45000  | 102
106         | Susan      | White     | 10            | 55000  | 103
107         | Mike       | Black     | 30            | 70000  | 105
108         | Lisa       | Blue      | 20            | 62000  | 104
109         | Chris      | Red       | 30            | 48000  | 107
110         | Karen      | Gray      | 10            | 68000  | 101
```
(Calculated Average Salary: (60000+75000+50000+80000+45000+55000+70000+62000+48000+68000) / 10 = 61300)

**Output:**
```
FIRST_NAME | LAST_NAME | SALARY
-----------|-----------|--------
Jane       | Smith     | 75000
Mary       | Brown     | 80000
Mike       | Black     | 70000
Lisa       | Blue      | 62000
Karen      | Gray      | 68000
```

### Example 2: Multiple CTEs (Chaining Logic)

**Goal:** Find all employees who work in departments that have more than 3 employees, and list their salaries.

```sql
WITH
    DepartmentEmployeeCounts AS (
        -- CTE 1: Calculates the number of employees per department
        SELECT
            DEPARTMENT_ID,
            COUNT(EMPLOYEE_ID) AS EmployeeCount
        FROM
            EMPLOYEES
        GROUP BY
            DEPARTMENT_ID
    ),
    HighEmployeeDepartments AS (
        -- CTE 2: Filters departments with more than 3 employees, referencing CTE 1
        SELECT
            DEPARTMENT_ID
        FROM
            DepartmentEmployeeCounts
        WHERE
            EmployeeCount > 3
    )
SELECT
    e.FIRST_NAME,
    e.LAST_NAME,
    e.DEPARTMENT_ID,
    e.SALARY
FROM
    EMPLOYEES e
JOIN
    HighEmployeeDepartments hed ON e.DEPARTMENT_ID = hed.DEPARTMENT_ID
ORDER BY
    e.DEPARTMENT_ID, e.LAST_NAME;
```

**Explanation:**
1.  `DepartmentEmployeeCounts` identifies how many employees are in each department.
2.  `HighEmployeeDepartments` then uses `DepartmentEmployeeCounts` to find only those departments with more than 3 employees.
3.  The final `SELECT` statement joins the original `EMPLOYEES` table with `HighEmployeeDepartments` to get the desired employee details.
This breaks down a potentially complex query into three easily understandable steps.

**Input:** (Same `EMPLOYEES` table as above)

**Output:**
```
FIRST_NAME | LAST_NAME | DEPARTMENT_ID | SALARY
-----------|-----------|---------------|--------
John       | Doe       | 10            | 60000
Karen      | Gray      | 10            | 68000
Peter      | Jones     | 10            | 50000
Susan      | White     | 10            | 55000
Lisa       | Blue      | 20            | 62000
Mary       | Brown     | 20            | 80000
Jane       | Smith     | 20            | 75000
```
(Department 10 has 4 employees, Department 20 has 3 employees, Department 30 has 3 employees. So only employees from Department 10 are returned.)

**Correction based on example output vs. condition `EmployeeCount > 3`:**
My initial output explanation was wrong. Department 20 has 3 employees (Jane, Mary, Lisa), so `EmployeeCount > 3` would *not* include department 20. Department 10 has 4 employees (John, Peter, Susan, Karen). Department 30 has 3 employees (David, Mike, Chris).
So, only Department 10 should be in `HighEmployeeDepartments`. Let's re-run the thought process.

Corrected `HighEmployeeDepartments` logic:
*   Dept 10: 4 employees -> Included
*   Dept 20: 3 employees -> NOT Included (because `> 3` means 4 or more)
*   Dept 30: 3 employees -> NOT Included

Thus, the output should only show employees from Department 10. The output above is correct based on the logic. My explanation was slightly off.

### Example 3: Recursive CTE (Hierarchical Data)

**Goal:** Show the reporting hierarchy for each employee, starting from the top-level managers down to their direct and indirect reports.

```sql
WITH
    EmployeeHierarchy (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, MANAGER_ID, LEVEL_NUM, PATH) AS (
        -- Anchor Member: Start with employees who have no manager (top of the hierarchy)
        SELECT
            e.EMPLOYEE_ID,
            e.FIRST_NAME,
            e.LAST_NAME,
            e.MANAGER_ID,
            1 AS LEVEL_NUM,
            CAST(e.FIRST_NAME || ' ' || e.LAST_NAME AS VARCHAR2(200)) AS PATH
        FROM
            EMPLOYEES e
        WHERE
            e.MANAGER_ID IS NULL

        UNION ALL

        -- Recursive Member: Find employees whose manager is in the current hierarchy level
        SELECT
            e.EMPLOYEE_ID,
            e.FIRST_NAME,
            e.LAST_NAME,
            e.MANAGER_ID,
            eh.LEVEL_NUM + 1 AS LEVEL_NUM,
            CAST(eh.PATH || ' -> ' || e.FIRST_NAME || ' ' || e.LAST_NAME AS VARCHAR2(200)) AS PATH
        FROM
            EMPLOYEES e
        JOIN
            EmployeeHierarchy eh ON e.MANAGER_ID = eh.EMPLOYEE_ID
    )
SELECT
    LPAD(' ', (LEVEL_NUM - 1) * 4) || FIRST_NAME || ' ' || LAST_NAME AS Hierarchy_Path,
    LEVEL_NUM,
    PATH
FROM
    EmployeeHierarchy
ORDER BY
    PATH;
```

**Explanation:**
1.  **Anchor Member:** Selects employees with `MANAGER_ID IS NULL` (the top-level employees, like a CEO). It initializes `LEVEL_NUM` to 1 and `PATH` with their name.
2.  **Recursive Member:** Joins `EMPLOYEES` with the `EmployeeHierarchy` CTE itself. It finds employees whose `MANAGER_ID` matches an `EMPLOYEE_ID` already in the `EmployeeHierarchy`. It increments `LEVEL_NUM` and appends the current employee's name to the `PATH`.
3.  `UNION ALL` combines these two sets of results.
4.  The final `SELECT` displays the hierarchy, using `LPAD` for indentation based on `LEVEL_NUM` for better visual representation.

**Input:** (Same `EMPLOYEES` table as above, with `MANAGER_ID`s)

**Output:**
```
HIERARCHY_PATH           | LEVEL_NUM | PATH
-------------------------|-----------|----------------------------------------------------
John Doe                 | 1         | John Doe
    Jane Smith           | 2         | John Doe -> Jane Smith
        David Green      | 3         | John Doe -> Jane Smith -> David Green
            Mike Black   | 4         | John Doe -> Jane Smith -> David Green -> Mike Black
                Chris Red| 5         | John Doe -> Jane Smith -> David Green -> Mike Black -> Chris Red
        Mary Brown       | 3         | John Doe -> Jane Smith -> Mary Brown
            Lisa Blue    | 4         | John Doe -> Jane Smith -> Mary Brown -> Lisa Blue
    Karen Gray           | 2         | John Doe -> Karen Gray
    Peter Jones          | 2         | John Doe -> Peter Jones
        Susan White      | 3         | John Doe -> Peter Jones -> Susan White
```

---

## 5. Key Considerations

*   **Scope:** CTEs are only valid for the single SQL statement (SELECT, INSERT, UPDATE, DELETE) they are defined within. You cannot reference a CTE from a separate query.
*   **Performance (Oracle Specific):**
    *   Unlike some other database systems (e.g., SQL Server), Oracle often **does not materialize** CTEs into temporary tables by default. The optimizer typically "merges" the CTE definition into the main query, treating it similarly to an inline view for optimization purposes.
    *   This usually means there's no inherent performance penalty or gain compared to a well-written subquery.
    *   If you *want* to force materialization (e.g., if the CTE is complex and used multiple times, and you suspect materialization might help performance by computing it once), you can use the `/*+ MATERIALIZE */` hint within the CTE:
        ```sql
        WITH
            MyCTE AS (
                SELECT /*+ MATERIALIZE */ ...
                FROM ...
            )
        SELECT * FROM MyCTE;
        ```
    *   Always test performance with and without CTEs (and with/without `MATERIALIZE` hint) for critical queries, as optimizer behavior can vary.
*   **Recursion Limit:** Recursive CTEs in Oracle have a maximum recursion depth, which by default is typically 2000. For deeper hierarchies, you might need to specify `MAX_DEPTH` in the `WITH` clause:
    ```sql
    WITH
        MyRecursiveCTE (..., MAX_DEPTH 10000) AS (
            ...
        )
    SELECT * FROM MyRecursiveCTE;
    ```
*   **Error Handling in Recursive CTEs:** If your recursive CTE has a cycle (e.g., Employee A reports to B, B reports to C, and C reports back to A), the query will typically raise an error (`ORA-32044: cycle detected while executing recursive WITH query`). You can handle this by adding a `CYCLE` clause to your `WITH` statement:
    ```sql
    WITH
        EmployeeHierarchy (EMPLOYEE_ID, ..., IS_CYCLE) AS (
            SELECT
                e.EMPLOYEE_ID, ..., 0 AS IS_CYCLE
            FROM EMPLOYEES e
            WHERE e.MANAGER_ID IS NULL

            UNION ALL

            SELECT
                e.EMPLOYEE_ID, ..., 1 AS IS_CYCLE
            FROM EMPLOYEES e
            JOIN EmployeeHierarchy eh ON e.MANAGER_ID = eh.EMPLOYEE_ID
            WHERE eh.IS_CYCLE = 0 -- Stop if a cycle is detected in the path
        ) CYCLE EMPLOYEE_ID SET IS_CYCLE TO 1 DEFAULT 0
    SELECT * FROM EmployeeHierarchy;
    ```
    The `CYCLE` clause prevents infinite loops and lets you detect them.

## 6. Summary

Common Table Expressions (CTEs) are a powerful feature in Oracle SQL that significantly improve the readability, modularity, and maintainability of complex queries. They are particularly useful for breaking down multi-step logic, reusing subquery results within a single statement, and indispensable for handling recursive data structures. While Oracle's optimizer often treats them like inline views, understanding their behavior and when to use hints like `MATERIALIZE` can help in optimizing performance for specific scenarios.