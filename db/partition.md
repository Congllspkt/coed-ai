The `PARTITION BY` clause in SQL Oracle (and standard SQL) is a fundamental component of **Analytic Functions** (also known as Window Functions). It allows you to divide the rows of a result set into groups or "partitions" and then apply an analytic function to each partition independently.

The key characteristic of analytic functions with `PARTITION BY` is that they perform calculations across a set of table rows that are related to the current row, without collapsing the rows of the original query result. This is a significant difference from `GROUP BY`, which *does* collapse rows into a single summary row.

---

## SQL Oracle: The `PARTITION BY` Clause (Analytic Functions)

### 1. What is `PARTITION BY`?

In the context of Analytic Functions, `PARTITION BY` defines the "window" or "group" of rows over which the function will operate. Think of it as creating logical sub-groups within your dataset, and then the analytic function is applied to each of these sub-groups independently.

### 2. Why Use `PARTITION BY`?

*   **Row-Level Calculations:** Perform calculations (like ranking, running totals, moving averages, comparisons with previous/next rows) without aggregating and losing individual row details.
*   **Comparison within Groups:** Easily compare a row's value to the average, sum, or another value within its specific group.
*   **Ranking:** Assign ranks to rows within categories (e.g., top salesperson per region, highest-paid employee per department).
*   **Business Intelligence:** Vital for complex reporting, trend analysis, and performance monitoring.

### 3. Syntax

The general syntax for an analytic function using `PARTITION BY` is:

```sql
ANALYTIC_FUNCTION (column_name, ...) OVER (
    PARTITION BY expression1, expression2, ...
    ORDER BY expression3, expression4, ...
    -- Optional: Windowing Clause (ROWS/RANGE)
)
```

**Key Components within `OVER()`:**

*   **`PARTITION BY expression1, expression2, ...`**:
    *   This is the core of dividing your data. Rows with the same values for `expression1`, `expression2`, etc., will belong to the same partition.
    *   The analytic function will then calculate its result for each partition separately.
    *   If `PARTITION BY` is omitted, the entire result set is treated as a single partition.
*   **`ORDER BY expression3, expression4, ...`**:
    *   This specifies the logical order of rows *within each partition*.
    *   It's crucial for functions that depend on order, such as `ROW_NUMBER()`, `RANK()`, `LAG()`, `LEAD()`, and running totals (`SUM()`, `AVG()` with a windowing clause).
*   **`[ROWS | RANGE] windowing_clause` (Optional):**
    *   Defines the subset of rows within the partition to which the analytic function is applied. For example, `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` for a running total, or `ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING` for a moving average.
    *   If omitted, the default window frame depends on the analytic function. For most ranking functions, it's `RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` (or equivalent `ROWS`). For aggregate functions used as analytic functions (like `SUM()`, `AVG()`), if `ORDER BY` is present, the default is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. If `ORDER BY` is absent, the default is `RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.

### 4. Common Analytic Functions Used with `PARTITION BY`

*   **Ranking Functions:** `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE()`
*   **Window Aggregates:** `SUM()`, `AVG()`, `COUNT()`, `MAX()`, `MIN()`
*   **Lag/Lead Functions:** `LAG()`, `LEAD()`
*   **First/Last Value:** `FIRST_VALUE()`, `LAST_VALUE()`
*   **Nth Value:** `NTH_VALUE()`
*   **Cumulative Distribution:** `CUME_DIST()`, `PERCENT_RANK()`

### 5. `PARTITION BY` vs. `GROUP BY` (Crucial Distinction)

| Feature           | `PARTITION BY` (Analytic Functions)                                       | `GROUP BY` (Aggregate Functions)                                    |
| :---------------- | :------------------------------------------------------------------------ | :------------------------------------------------------------------ |
| **Row Output**    | Retains all original rows; adds new calculated columns to each row.       | Collapses rows into a single summary row for each group.            |
| **Purpose**       | Calculate values based on a group of related rows *without* aggregation. | Summarize and aggregate data into fewer rows.                       |
| **Context**       | Part of the `OVER()` clause for analytic functions.                       | A standalone clause that follows `FROM` and `WHERE` clauses.       |
| **Example Use**   | Rank employees within each department, calculate running totals.          | Get total sales per department, count unique products.              |
| **Data Visibility** | Each row can "see" other rows within its partition.                      | Rows within a group are aggregated, individual row details are lost. |

---

### 6. Examples (Oracle SQL)

Let's set up some sample data first.

#### **Sample Data Setup**

```sql
-- Create a table for Employees
CREATE TABLE employees (
    employee_id NUMBER PRIMARY KEY,
    employee_name VARCHAR2(100),
    department VARCHAR2(50),
    salary NUMBER(10, 2),
    hire_date DATE
);

-- Insert sample data
INSERT ALL
    INTO employees (employee_id, employee_name, department, salary, hire_date) VALUES (101, 'Alice', 'HR', 60000, TO_DATE('2020-01-15', 'YYYY-MM-DD'))
    INTO employees (employee_id, employee_name, department, salary, hire_date) VALUES (102, 'Bob', 'HR', 75000, TO_DATE('2019-03-20', 'YYYY-MM-DD'))
    INTO employees (employee_id, employee_name, department, salary, hire_date) VALUES (103, 'Charlie', 'HR', 62000, TO_DATE('2021-08-01', 'YYYY-MM-DD'))
    INTO employees (employee_id, employee_name, department, salary, hire_date) VALUES (201, 'David', 'IT', 80000, TO_DATE('2018-05-10', 'YYYY-MM-DD'))
    INTO employees (employee_id, employee_name, department, salary, hire_date) VALUES (202, 'Eve', 'IT', 95000, TO_DATE('2017-11-22', 'YYYY-MM-DD'))
    INTO employees (employee_id, employee_name, department, salary, hire_date) VALUES (203, 'Frank', 'IT', 80000, TO_DATE('2020-02-28', 'YYYY-MM-DD'))
    INTO employees (employee_id, employee_name, department, salary, hire_date) VALUES (301, 'Grace', 'Sales', 70000, TO_DATE('2019-07-01', 'YYYY-MM-DD'))
    INTO employees (employee_id, employee_name, department, salary, hire_date) VALUES (302, 'Heidi', 'Sales', 90000, TO_DATE('2018-01-01', 'YYYY-MM-DD'))
    INTO employees (employee_id, employee_name, department, salary, hire_date) VALUES (303, 'Ivan', 'Sales', 70000, TO_DATE('2021-04-10', 'YYYY-MM-DD'))
SELECT 1 FROM DUAL;

COMMIT;
```

#### **Input (Employees Table):**

| EMPLOYEE_ID | EMPLOYEE_NAME | DEPARTMENT | SALARY  | HIRE_DATE |
| :---------- | :------------ | :--------- | :------ | :-------- |
| 101         | Alice         | HR         | 60000.00| 15-JAN-20 |
| 102         | Bob           | HR         | 75000.00| 20-MAR-19 |
| 103         | Charlie       | HR         | 62000.00| 01-AUG-21 |
| 201         | David         | IT         | 80000.00| 10-MAY-18 |
| 202         | Eve           | IT         | 95000.00| 22-NOV-17 |
| 203         | Frank         | IT         | 80000.00| 28-FEB-20 |
| 301         | Grace         | Sales      | 70000.00| 01-JUL-19 |
| 302         | Heidi         | Sales      | 90000.00| 01-JAN-18 |
| 303         | Ivan          | Sales      | 70000.00| 10-APR-21 |

---

#### **Example 1: Ranking Employees by Salary within Each Department**

**Problem:** Get the rank of each employee's salary within their respective department, from highest to lowest salary.

**SQL Query:**

```sql
SELECT
    employee_id,
    employee_name,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS salary_rank_in_dept,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_salary_rank_in_dept,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num_in_dept
FROM
    employees
ORDER BY
    department, salary DESC;
```

**Explanation:**
*   `PARTITION BY department`: Divides the employees into separate groups for 'HR', 'IT', and 'Sales'.
*   `ORDER BY salary DESC`: Within each department, salaries are ordered from highest to lowest.
*   `RANK()`: Assigns a rank with gaps for ties (e.g., if two employees tie for 1st, the next rank is 3rd).
*   `DENSE_RANK()`: Assigns a rank without gaps for ties (e.g., if two employees tie for 1st, the next rank is 2nd).
*   `ROW_NUMBER()`: Assigns a unique sequential number within each partition, even for ties.

**Output:**

| EMPLOYEE_ID | EMPLOYEE_NAME | DEPARTMENT | SALARY  | SALARY_RANK_IN_DEPT | DENSE_SALARY_RANK_IN_DEPT | ROW_NUM_IN_DEPT |
| :---------- | :------------ | :--------- | :------ | :------------------ | :------------------------ | :-------------- |
| 102         | Bob           | HR         | 75000.00| 1                   | 1                         | 1               |
| 103         | Charlie       | HR         | 62000.00| 2                   | 2                         | 2               |
| 101         | Alice         | HR         | 60000.00| 3                   | 3                         | 3               |
| 202         | Eve           | IT         | 95000.00| 1                   | 1                         | 1               |
| 201         | David         | IT         | 80000.00| 2                   | 2                         | 2               |
| 203         | Frank         | IT         | 80000.00| 2                   | 2                         | 3               |
| 302         | Heidi         | Sales      | 90000.00| 1                   | 1                         | 1               |
| 301         | Grace         | Sales      | 70000.00| 2                   | 2                         | 2               |
| 303         | Ivan          | Sales      | 70000.00| 2                   | 2                         | 3               |

---

#### **Example 2: Department Total Salary and Average Salary (Windowed Aggregation)**

**Problem:** For each employee, show their salary along with the total salary and average salary for their department.

**SQL Query:**

```sql
SELECT
    employee_id,
    employee_name,
    department,
    salary,
    SUM(salary) OVER (PARTITION BY department) AS department_total_salary,
    AVG(salary) OVER (PARTITION BY department) AS department_avg_salary
FROM
    employees
ORDER BY
    department, employee_id;
```

**Explanation:**
*   `PARTITION BY department`: Calculates the `SUM()` and `AVG()` of salaries for all employees *within each department*.
*   Since there's no `ORDER BY` clause within the `OVER()` for these aggregate functions, the sum and average are computed over the *entire* partition (i.e., all rows in that department).
*   Each original row is returned, with the department's total and average salary appended.

**Output:**

| EMPLOYEE_ID | EMPLOYEE_NAME | DEPARTMENT | SALARY  | DEPARTMENT_TOTAL_SALARY | DEPARTMENT_AVG_SALARY |
| :---------- | :------------ | :--------- | :------ | :---------------------- | :-------------------- |
| 101         | Alice         | HR         | 60000.00| 197000.00               | 65666.67              |
| 102         | Bob           | HR         | 75000.00| 197000.00               | 65666.67              |
| 103         | Charlie       | HR         | 62000.00| 197000.00               | 65666.67              |
| 201         | David         | IT         | 80000.00| 255000.00               | 85000.00              |
| 202         | Eve           | IT         | 95000.00| 255000.00               | 85000.00              |
| 203         | Frank         | IT         | 80000.00| 255000.00               | 85000.00              |
| 301         | Grace         | Sales      | 70000.00| 230000.00               | 76666.67              |
| 302         | Heidi         | Sales      | 90000.00| 230000.00               | 76666.67              |
| 303         | Ivan          | Sales      | 70000.00| 230000.00               | 76666.67              |

---

#### **Example 3: Running Total Salary per Department by Hire Date**

**Problem:** Calculate a running total of salaries within each department, ordered by hire date.

**SQL Query:**

```sql
SELECT
    employee_id,
    employee_name,
    department,
    salary,
    hire_date,
    SUM(salary) OVER (PARTITION BY department ORDER BY hire_date ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_dept_salary
FROM
    employees
ORDER BY
    department, hire_date;
```

**Explanation:**
*   `PARTITION BY department`: Ensures the running total is calculated independently for each department.
*   `ORDER BY hire_date ASC`: Defines the order in which salaries are accumulated within each department.
*   `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`: This is the *windowing clause*. It tells `SUM()` to include all rows from the beginning of the partition (`UNBOUNDED PRECEDING`) up to and including the `CURRENT ROW` in its calculation. This is what makes it a "running total."

**Output:**

| EMPLOYEE_ID | EMPLOYEE_NAME | DEPARTMENT | SALARY  | HIRE_DATE | RUNNING_DEPT_SALARY |
| :---------- | :------------ | :--------- | :------ | :-------- | :------------------ |
| 101         | Alice         | HR         | 60000.00| 15-JAN-20 | 60000.00            |
| 102         | Bob           | HR         | 75000.00| 20-MAR-19 | 135000.00           |
| 103         | Charlie       | HR         | 62000.00| 01-AUG-21 | 197000.00           |
| 202         | Eve           | IT         | 95000.00| 22-NOV-17 | 95000.00            |
| 201         | David         | IT         | 80000.00| 10-MAY-18 | 175000.00           |
| 203         | Frank         | IT         | 80000.00| 28-FEB-20 | 255000.00           |
| 302         | Heidi         | Sales      | 90000.00| 01-JAN-18 | 90000.00            |
| 301         | Grace         | Sales      | 70000.00| 01-JUL-19 | 160000.00           |
| 303         | Ivan          | Sales      | 70000.00| 10-APR-21 | 230000.00           |

---

#### **Example 4: Comparing with Previous Employee's Salary in the Same Department**

**Problem:** Find the salary of the employee hired immediately before the current employee within the same department.

**SQL Query:**

```sql
SELECT
    employee_id,
    employee_name,
    department,
    salary,
    hire_date,
    LAG(salary, 1, 0) OVER (PARTITION BY department ORDER BY hire_date ASC) AS previous_employee_salary
FROM
    employees
ORDER BY
    department, hire_date;
```

**Explanation:**
*   `PARTITION BY department`: Looks for the previous employee only within the same department.
*   `ORDER BY hire_date ASC`: Defines the order for determining "previous."
*   `LAG(salary, 1, 0)`:
    *   `salary`: The column whose value we want from the previous row.
    *   `1`: The offset (look 1 row back).
    *   `0`: The default value if there is no previous row (e.g., for the first employee in a department).

**Output:**

| EMPLOYEE_ID | EMPLOYEE_NAME | DEPARTMENT | SALARY  | HIRE_DATE | PREVIOUS_EMPLOYEE_SALARY |
| :---------- | :------------ | :--------- | :------ | :-------- | :----------------------- |
| 101         | Alice         | HR         | 60000.00| 15-JAN-20 | 0.00                     |
| 102         | Bob           | HR         | 75000.00| 20-MAR-19 | 60000.00                 |
| 103         | Charlie       | HR         | 62000.00| 01-AUG-21 | 75000.00                 |
| 202         | Eve           | IT         | 95000.00| 22-NOV-17 | 0.00                     |
| 201         | David         | IT         | 80000.00| 10-MAY-18 | 95000.00                 |
| 203         | Frank         | IT         | 80000.00| 28-FEB-20 | 80000.00                 |
| 302         | Heidi         | Sales      | 90000.00| 01-JAN-18 | 0.00                     |
| 301         | Grace         | Sales      | 70000.00| 01-JUL-19 | 90000.00                 |
| 303         | Ivan          | Sales      | 70000.00| 10-APR-21 | 70000.00                 |

---

#### **Example 5: NTILE - Divide Employees into Quartiles by Salary within Department**

**Problem:** Divide employees in each department into 4 quartiles based on their salary (highest salary in quartile 1).

**SQL Query:**

```sql
SELECT
    employee_id,
    employee_name,
    department,
    salary,
    NTILE(4) OVER (PARTITION BY department ORDER BY salary DESC) AS salary_quartile_in_dept
FROM
    employees
ORDER BY
    department, salary DESC;
```

**Explanation:**
*   `PARTITION BY department`: Ensures the quartiles are determined independently for each department.
*   `ORDER BY salary DESC`: Orders employees by salary from highest to lowest for quartile assignment.
*   `NTILE(4)`: Divides the rows in each partition into 4 approximately equal groups. The highest salaries get into the lower quartile numbers (1 being the highest).

**Output:**

| EMPLOYEE_ID | EMPLOYEE_NAME | DEPARTMENT | SALARY  | SALARY_QUARTILE_IN_DEPT |
| :---------- | :------------ | :--------- | :------ | :---------------------- |
| 102         | Bob           | HR         | 75000.00| 1                       |
| 103         | Charlie       | HR         | 62000.00| 2                       |
| 101         | Alice         | HR         | 60000.00| 3                       |
| 202         | Eve           | IT         | 95000.00| 1                       |
| 201         | David         | IT         | 80000.00| 2                       |
| 203         | Frank         | IT         | 80000.00| 3                       |
| 302         | Heidi         | Sales      | 90000.00| 1                       |
| 301         | Grace         | Sales      | 70000.00| 2                       |
| 303         | Ivan          | Sales      | 70000.00| 3                       |

*(Note: NTILE divides as evenly as possible. With 3 employees in each department and NTILE(4), it assigns 1, 2, 3 to the employees and skips 4, effectively creating 3 groups based on the count.)*

---

### 7. Clean Up (Optional)

```sql
DROP TABLE employees;
```

---

### Conclusion

The `PARTITION BY` clause is an incredibly powerful feature in Oracle SQL for performing complex calculations and data analysis. By understanding how to use it with various analytic functions, you can write more efficient, readable, and powerful queries that solve a wide range of business problems without the need for multiple subqueries or self-joins. It's a cornerstone for anyone doing serious data analysis in SQL.