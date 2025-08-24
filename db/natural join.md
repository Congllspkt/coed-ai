This document provides a detailed explanation of the `NATURAL JOIN` clause in Oracle SQL, including its definition, behavior, advantages, disadvantages, and practical examples with input and output.

---

# Natural Join in Oracle SQL

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [How `NATURAL JOIN` Works](#2-how-natural-join-works)
3.  [Key Characteristics](#3-key-characteristics)
4.  [Syntax](#4-syntax)
5.  [Advantages](#5-advantages)
6.  [Disadvantages and Pitfalls](#6-disadvantages-and-pitfalls)
7.  [Examples](#7-examples)
    *   [Example 1: Basic `NATURAL JOIN` with One Common Column](#example-1-basic-natural-join-with-one-common-column)
    *   [Example 2: `NATURAL JOIN` with Multiple Common Columns](#example-2-natural-join-with-multiple-common-columns)
    *   [Example 3: Pitfall - Unintended Join Due to Accidental Column Name Match](#example-3-pitfall---unintended-join-due-to-accidental-column-name-match)
    *   [Example 4: `NATURAL LEFT JOIN`](#example-4-natural-left-join)
8.  [Comparison with `JOIN ... ON` and `JOIN ... USING`](#8-comparison-with-join--on-and-join--using)
9.  [Conclusion and Best Practices](#9-conclusion-and-best-practices)

---

## 1. Introduction

The `NATURAL JOIN` clause in SQL (and specifically in Oracle SQL) is a type of join that automatically joins two tables based on all columns that have the same name and compatible data types in both tables. It implies an `INNER JOIN` by default unless specified otherwise (e.g., `NATURAL LEFT JOIN`).

The key characteristic is its **implicitness**: you do not explicitly specify the join conditions (`ON` clause) or the common columns (`USING` clause). SQL automatically figures out the join columns based on matching names.

## 2. How `NATURAL JOIN` Works

When you use `NATURAL JOIN` between two tables, Oracle performs the following steps:

1.  **Identifies Common Columns:** It scans both tables to find all columns that share the exact same name.
2.  **Checks Data Types:** For each identified common column, it checks if their data types are compatible for comparison.
3.  **Constructs Implicit `ON` Clause:** It effectively builds an `INNER JOIN` condition using an `AND` operator for all identified common columns. For example, if `TableA` and `TableB` both have columns `COL1` and `COL2`, the `NATURAL JOIN` is equivalent to `TableA INNER JOIN TableB ON TableA.COL1 = TableB.COL1 AND TableA.COL2 = TableB.COL2`.
4.  **Returns Results:** It returns rows where the values in *all* the common columns match in both tables.
5.  **Eliminates Duplicate Common Columns:** In the final result set, the common columns appear only once, unlike an `INNER JOIN ... ON` where they would appear twice unless explicitly aliased or projected.

## 3. Key Characteristics

*   **Automatic Column Detection:** Relies solely on matching column names and data types.
*   **Implicit `INNER JOIN`:** By default, it behaves like an `INNER JOIN`.
*   **Single Appearance of Common Columns:** In the result set, common columns (those used for joining) appear only once, effectively de-duplicating them.
*   **No `ON` or `USING` Clauses:** You cannot combine `NATURAL JOIN` with an `ON` clause or a `USING` clause. Doing so will result in an `ORA-00933: SQL command not properly ended` or similar error.
*   **Supports Outer Joins:** Can be extended to `NATURAL LEFT JOIN`, `NATURAL RIGHT JOIN`, and `NATURAL FULL JOIN`.

## 4. Syntax

The basic syntax for `NATURAL JOIN` is:

```sql
SELECT columns
FROM table1
NATURAL JOIN table2;
```

For outer joins:

```sql
SELECT columns
FROM table1
NATURAL LEFT JOIN table2; -- or NATURAL RIGHT JOIN, NATURAL FULL JOIN
```

You can also chain `NATURAL JOIN`s:

```sql
SELECT columns
FROM table1
NATURAL JOIN table2
NATURAL JOIN table3;
```

## 5. Advantages

*   **Conciseness:** It can be very concise for simple join conditions where column names are perfectly aligned and intended for joining.
*   **Less Typing:** Reduces the amount of SQL code needed compared to explicit `ON` clauses, especially if many columns need to be matched.
*   **Self-Documenting (in Ideal Scenarios):** In a perfectly designed relational schema where shared column names genuinely represent natural join keys, it can be intuitive.

## 6. Disadvantages and Pitfalls

The implicit nature of `NATURAL JOIN` makes it generally **discouraged** in professional SQL development due to several significant disadvantages:

*   **Ambiguity and Lack of Explicitness:** The most significant drawback. The join condition is hidden, making the query harder to understand, maintain, and debug. You can't tell *which* columns are being used for the join without inspecting table schemas.
*   **Unexpected Results (The "Accidental Join"):** If two tables happen to have columns with the same name that are *not* intended to be part of the join condition (e.g., `LAST_UPDATE_DATE`, `DESCRIPTION`, `STATUS`), `NATURAL JOIN` will use them, leading to incorrect or an empty result set. This is a very common and dangerous pitfall.
*   **Schema Evolution Issues:** If a new column is added to both tables and it happens to share the same name (even if semantically unrelated), your `NATURAL JOIN` query will silently change its behavior, potentially breaking logic without any syntax error.
*   **Limited Control:** You have no control over *which* common columns are used for joining. If you only want to join on a subset of common columns, `NATURAL JOIN` is not suitable.
*   **Debugging Difficulty:** When a `NATURAL JOIN` produces unexpected results, it's harder to debug because the join criteria are not explicitly stated in the query.

## 7. Examples

Let's set up some sample tables for our examples.

**Input Setup:**

```sql
-- Drop tables if they exist
DROP TABLE employees PURGE;
DROP TABLE departments PURGE;
DROP TABLE projects PURGE;
DROP TABLE job_history PURGE;

-- Create DEPARTMENTS table
CREATE TABLE departments (
    department_id   NUMBER(4) PRIMARY KEY,
    department_name VARCHAR2(30) NOT NULL,
    location_id     NUMBER(4)
);

-- Insert data into DEPARTMENTS
INSERT INTO departments (department_id, department_name, location_id) VALUES (10, 'Administration', 1700);
INSERT INTO departments (department_id, department_name, location_id) VALUES (20, 'Marketing', 1800);
INSERT INTO departments (department_id, department_name, location_id) VALUES (30, 'Purchasing', 1700);
INSERT INTO departments (department_id, department_name, location_id) VALUES (40, 'Human Resources', 2500);
INSERT INTO departments (department_id, department_name, location_id) VALUES (50, 'Shipping', 1500);
INSERT INTO departments (department_id, department_name, location_id) VALUES (60, 'IT', 1600);
INSERT INTO departments (department_id, department_name, location_id) VALUES (90, 'Executive', 1700);
COMMIT;

-- Create EMPLOYEES table
CREATE TABLE employees (
    employee_id     NUMBER(6) PRIMARY KEY,
    first_name      VARCHAR2(20),
    last_name       VARCHAR2(25) NOT NULL,
    email           VARCHAR2(25) NOT NULL,
    phone_number    VARCHAR2(20),
    hire_date       DATE NOT NULL,
    job_id          VARCHAR2(10) NOT NULL,
    salary          NUMBER(8,2),
    commission_pct  NUMBER(2,2),
    manager_id      NUMBER(6),
    department_id   NUMBER(4), -- Common column with DEPARTMENTS
    last_update_date DATE      -- This will be used for the pitfall example
);

-- Insert data into EMPLOYEES
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (100, 'Steven', 'King', 'SKING', '515.123.4567', DATE '2003-06-17', 'AD_PRES', 24000, NULL, NULL, 90, DATE '2023-01-15');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (101, 'Neena', 'Kochhar', 'NKOCHHAR', '515.123.4568', DATE '2005-09-21', 'AD_VP', 17000, NULL, 100, 90, DATE '2023-02-20');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (102, 'Lex', 'De Haan', 'LDEHAAN', '515.123.4569', DATE '2001-01-13', 'AD_VP', 17000, NULL, 100, 90, DATE '2023-03-01');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (103, 'Alexander', 'Hunold', 'AHUNOLD', '590.423.4567', DATE '2006-01-03', 'IT_PROG', 9000, NULL, 102, 60, DATE '2023-01-25');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (104, 'Bruce', 'Ernst', 'BERNST', '590.423.4568', DATE '2007-05-21', 'IT_PROG', 6000, NULL, 103, 60, DATE '2023-02-10');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (105, 'Diana', 'Lorentz', 'DLORENTZ', '590.423.5567', DATE '2007-02-07', 'IT_PROG', 4200, NULL, 103, 60, DATE '2023-01-05');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (106, 'Valli', 'Pataballa', 'VPATABAL', '590.423.4569', DATE '2006-02-05', 'IT_PROG', 4800, NULL, 103, 60, DATE '2023-03-10');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (107, 'Nancy', 'Greenberg', 'NGREENBE', '515.124.4569', DATE '2002-08-17', 'FI_MGR', 12000, NULL, 101, 10, DATE '2023-01-20');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (108, 'Daniel', 'Faviet', 'DFAVIET', '515.124.4169', DATE '2002-08-16', 'FI_ACCOUNT', 9000, NULL, 107, 10, DATE '2023-02-05');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (109, 'John', 'Chen', 'JCHEN', '515.124.4269', DATE '2005-09-28', 'FI_ACCOUNT', 8200, NULL, 107, 10, DATE '2023-03-15');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (110, 'Ismael', 'Sciarra', 'ISCIARRA', '515.124.4369', DATE '2005-09-30', 'FI_ACCOUNT', 7700, NULL, 107, 10, DATE '2023-01-30');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (111, 'Jose Manuel', 'Urman', 'JURMAN', '515.124.4469', DATE '2006-03-07', 'FI_ACCOUNT', 7800, NULL, 107, 10, DATE '2023-02-25');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (112, 'Luis', 'Popp', 'LPOPP', '515.124.4567', DATE '2007-12-07', 'FI_ACCOUNT', 6900, NULL, 107, 10, DATE '2023-03-05');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (113, 'Laura', 'Bissot', 'LBISSOT', '515.124.5269', DATE '2005-06-21', 'AD_ASST', 3600, NULL, 101, 20, DATE '2023-01-10');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (114, 'Mozhe', 'Maurer', 'MMAURER', '515.124.5369', DATE '2007-06-12', 'AC_MGR', 8000, NULL, 101, 20, DATE '2023-02-01');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (115, 'Karen', 'Partners', 'KPARTNER', '515.124.5469', DATE '2006-01-05', 'AC_MGR', 7000, NULL, 101, 20, DATE '2023-03-08');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (116, 'Alberto', 'Errazuriz', 'AERRAZUR', '515.124.5569', DATE '2005-03-10', 'AC_MGR', 12000, NULL, 101, 20, DATE '2023-01-18');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (117, 'Gerald', 'Cambrault', 'GCAMBRAU', '515.124.6169', DATE '2007-05-15', 'AC_MGR', 11000, NULL, 101, 20, DATE '2023-02-12');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (118, 'Eleni', 'Zlotkey', 'EZLOTKEY', '515.124.6269', DATE '2008-01-29', 'AC_MGR', 10500, NULL, 101, 20, DATE '2023-03-20');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (119, 'Adam', 'Fripp', 'AFRIPP', '650.123.2234', DATE '2005-04-10', 'AC_MGR', 8200, NULL, 101, 20, DATE '2023-01-22');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (120, 'Kelly', 'Chung', 'KCHUNG', '650.123.2235', DATE '2005-06-14', 'AC_MGR', 7700, NULL, 101, 20, DATE '2023-02-08');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (121, 'Jennifer', 'Whalen', 'JWHALEN', '515.123.4444', DATE '2003-09-17', 'AD_ASST', 4400, NULL, 101, 10, DATE '2023-03-25');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (122, 'Pat', 'Fay', 'PFAY', '603.123.6666', DATE '2005-08-17', 'AC_ACCOUNT', 6000, NULL, 115, 20, DATE '2023-01-01');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (123, 'Michael', 'Hartstein', 'MHARTSTE', '515.123.5555', DATE '2004-02-17', 'MK_REP', 13000, NULL, 101, 20, DATE '2023-02-15'); -- Department 20 employees
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (124, 'Shanta', 'Vollman', 'SVOLLMAN', '650.123.3333', DATE '2006-10-10', 'SH_CLERK', 6500, NULL, 120, 50, DATE '2023-03-01');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (125, 'Kevin', 'Mourgos', 'KMOURGOS', '650.123.4444', DATE '2007-11-16', 'SH_CLERK', 5800, NULL, 120, 50, DATE '2023-02-28');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (126, 'Julia', 'Nayer', 'JNAYER', '650.123.5555', DATE '2005-07-02', 'SH_CLERK', 3200, NULL, 120, 50, DATE '2023-03-18');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (127, 'Irene', 'Mikkilineni', 'IMIKKILI', '650.123.6666', DATE '2006-09-28', 'SH_CLERK', 2700, NULL, 120, 50, DATE '2023-01-12');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (128, 'James', 'Landry', 'JLANDRY', '650.123.7777', DATE '2007-01-14', 'SH_CLERK', 2400, NULL, 120, 50, DATE '2023-02-22');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (129, 'Steven', 'Markle', 'SMARKLE', '650.123.8888', DATE '2008-03-08', 'SH_CLERK', 2200, NULL, 120, 50, DATE '2023-03-10');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (130, 'Laura', 'Tien', 'LTIEN', '650.123.9999', DATE '2008-04-18', 'SH_CLERK', 2000, NULL, 120, 50, DATE '2023-01-08');
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (131, 'Joshua', 'Grant', 'JGRANT', '650.123.1111', DATE '2007-07-28', 'SH_CLERK', 2600, NULL, 120, 50, DATE '2023-02-03');

-- Add an employee without a department to show NATURAL LEFT JOIN
INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id, last_update_date)
VALUES (200, 'Unknown', 'Employee', 'UEMPLOYEE', '111.222.3333', DATE '2020-01-01', 'SA_REP', 5000, NULL, NULL, NULL, DATE '2023-04-01');

COMMIT;


-- Create PROJECTS table (for Example 2)
CREATE TABLE projects (
    project_id      NUMBER(6) PRIMARY KEY,
    project_name    VARCHAR2(50) NOT NULL,
    start_date      DATE NOT NULL,
    end_date        DATE,
    department_id   NUMBER(4), -- Common column with DEPARTMENTS
    status          VARCHAR2(20) -- For another common column scenario
);

-- Insert data into PROJECTS
INSERT INTO projects (project_id, project_name, start_date, end_date, department_id, status) VALUES (1, 'ERP Implementation', DATE '2022-01-01', DATE '2023-12-31', 90, 'In Progress');
INSERT INTO projects (project_id, project_name, start_date, end_date, department_id, status) VALUES (2, 'Website Redesign', DATE '2023-03-15', NULL, 20, 'In Progress');
INSERT INTO projects (project_id, project_name, start_date, end_date, department_id, status) VALUES (3, 'HR Portal Dev', DATE '2023-06-01', DATE '2024-06-01', 40, 'Planned');
INSERT INTO projects (project_id, project_name, start_date, end_date, department_id, status) VALUES (4, 'IT Security Audit', DATE '2023-01-10', DATE '2023-04-30', 60, 'Completed');
INSERT INTO projects (project_id, project_name, start_date, end_date, department_id, status) VALUES (5, 'New Product Launch', DATE '2024-01-01', NULL, 20, 'Planned');
INSERT INTO projects (project_id, project_name, start_date, end_date, department_id, status) VALUES (6, 'Cloud Migration', DATE '2023-07-01', NULL, 60, 'In Progress');
COMMIT;

-- Create JOB_HISTORY table (for Example 3 - Pitfall)
CREATE TABLE job_history (
    employee_id     NUMBER(6),
    start_date      DATE,
    end_date        DATE,
    job_id          VARCHAR2(10),
    department_id   NUMBER(4),
    last_update_date DATE     -- This will match EMPLOYEES.LAST_UPDATE_DATE
);

INSERT INTO job_history (employee_id, start_date, end_date, job_id, department_id, last_update_date)
VALUES (101, DATE '1989-09-21', DATE '1993-10-27', 'AC_ACCOUNT', 10, DATE '2023-01-15');
INSERT INTO job_history (employee_id, start_date, end_date, job_id, department_id, last_update_date)
VALUES (101, DATE '1993-10-28', DATE '1998-03-15', 'AC_MGR', 20, DATE '2023-01-15');
INSERT INTO job_history (employee_id, start_date, end_date, job_id, department_id, last_update_date)
VALUES (102, DATE '1993-01-13', DATE '1998-07-24', 'AD_VP', 90, DATE '2023-03-01');
INSERT INTO job_history (employee_id, start_date, end_date, job_id, department_id, last_update_date)
VALUES (103, DATE '1999-01-03', DATE '2006-01-03', 'IT_PROG', 60, DATE '2023-01-25');
INSERT INTO job_history (employee_id, start_date, end_date, job_id, department_id, last_update_date)
VALUES (104, DATE '2000-05-21', DATE '2007-05-21', 'IT_PROG', 60, DATE '2023-02-10');
INSERT INTO job_history (employee_id, start_date, end_date, job_id, department_id, last_update_date)
VALUES (105, DATE '2000-02-07', DATE '2007-02-07', 'IT_PROG', 60, DATE '2023-01-05');
INSERT INTO job_history (employee_id, start_date, end_date, job_id, department_id, last_update_date)
VALUES (106, DATE '2000-02-05', DATE '2006-02-05', 'IT_PROG', 60, DATE '2023-03-10');
COMMIT;
```

---

### Example 1: Basic `NATURAL JOIN` with One Common Column

**Scenario:** Retrieve employee details along with their department names.
**Common Column:** `department_id`

**Query:**

```sql
SELECT
    e.first_name,
    e.last_name,
    d.department_name,
    e.salary
FROM
    employees e
NATURAL JOIN
    departments d
ORDER BY
    e.last_name;
```

**Explanation:**
Oracle automatically detects that both `employees` and `departments` tables have a column named `department_id` with compatible data types. It then performs an `INNER JOIN` on this column. The `department_id` column will appear only once in the result set.

**Output:**

| FIRST_NAME | LAST_NAME   | DEPARTMENT_NAME | SALARY |
| :--------- | :---------- | :-------------- | -----: |
| Laura      | Bissot      | Marketing       |   3600 |
| Gerald     | Cambrault   | Marketing       |  11000 |
| John       | Chen        | Administration  |   8200 |
| Kelly      | Chung       | Marketing       |   7700 |
| Lex        | De Haan     | Executive       |  17000 |
| Alberto    | Errazuriz   | Marketing       |  12000 |
| Bruce      | Ernst       | IT              |   6000 |
| Daniel     | Faviet      | Administration  |   9000 |
| Adam       | Fripp       | Marketing       |   8200 |
| Joshua     | Grant       | Shipping        |   2600 |
| Nancy      | Greenberg   | Administration  |  12000 |
| Michael    | Hartstein   | Marketing       |  13000 |
| Alexander  | Hunold      | IT              |   9000 |
| Steven     | King        | Executive       |  24000 |
| Neena      | Kochhar     | Executive       |  17000 |
| James      | Landry      | Shipping        |   2400 |
| Diana      | Lorentz     | IT              |   4200 |
| Steven     | Markle      | Shipping        |   2200 |
| Mozhe      | Maurer      | Marketing       |   8000 |
| Irene      | Mikkilineni | Shipping        |   2700 |
| Kevin      | Mourgos     | Shipping        |   5800 |
| Julia      | Nayer       | Shipping        |   3200 |
| Valli      | Pataballa   | IT              |   4800 |
| Karen      | Partners    | Marketing       |   7000 |
| Pat        | Fay         | Marketing       |   6000 |
| Luis       | Popp        | Administration  |   6900 |
| Ismael     | Sciarra     | Administration  |   7700 |
| Laura      | Tien        | Shipping        |   2000 |
| Jose Manuel| Urman       | Administration  |   7800 |
| Shanta     | Vollman     | Shipping        |   6500 |
| Jennifer   | Whalen      | Administration  |   4400 |
| Eleni      | Zlotkey     | Marketing       |  10500 |

*(Note: The output columns `department_id` would not be listed twice even if selected as `*`.)*

---

### Example 2: `NATURAL JOIN` with Multiple Common Columns

**Scenario:** Get projects details along with the associated department name.
**Common Columns:** `department_id` (and potentially `status` if it matched).

Let's assume we intend to join `DEPARTMENTS` and `PROJECTS` on `department_id`. If `PROJECTS` also had a `location_id` column, and it matched in `DEPARTMENTS`, `NATURAL JOIN` would use both. For this example, only `department_id` is common.

**Query:**

```sql
SELECT
    p.project_name,
    d.department_name,
    p.status,
    p.start_date
FROM
    projects p
NATURAL JOIN
    departments d
ORDER BY
    p.project_name;
```

**Explanation:**
Oracle finds `department_id` as the only common column between `projects` and `departments`. It performs an `INNER JOIN` on `projects.department_id = departments.department_id`.

**Output:**

| PROJECT_NAME      | DEPARTMENT_NAME | STATUS      | START_DATE |
| :---------------- | :-------------- | :---------- | :--------- |
| Cloud Migration   | IT              | In Progress | 2023-07-01 |
| ERP Implementation| Executive       | In Progress | 2022-01-01 |
| HR Portal Dev     | Human Resources | Planned     | 2023-06-01 |
| IT Security Audit | IT              | Completed   | 2023-01-10 |
| New Product Launch| Marketing       | Planned     | 2024-01-01 |
| Website Redesign  | Marketing       | In Progress | 2023-03-15 |

---

### Example 3: Pitfall - Unintended Join Due to Accidental Column Name Match

**Scenario:** Attempt to join `employees` and `job_history` tables.
**Intended Join:** `employee_id`.
**Accidental Common Column:** `last_update_date` (and `department_id`, `job_id`).

In our setup, `employees` and `job_history` both have `employee_id`, `department_id`, `job_id` and `last_update_date`.
`NATURAL JOIN` will try to match on *all* of them. Since `last_update_date` values in `employees` are typically recent and unique to that table's last modification, while `job_history.last_update_date` might be for the history record itself, matching on `last_update_date` is highly unlikely to produce meaningful results (or any results at all, if dates don't exactly match).

**Query:**

```sql
SELECT
    e.first_name,
    e.last_name,
    jh.start_date AS history_start_date,
    jh.end_date AS history_end_date,
    jh.job_id AS history_job_id,
    e.department_id, -- Common column
    e.last_update_date -- Common column
FROM
    employees e
NATURAL JOIN
    job_history jh
ORDER BY
    e.last_name, jh.start_date;
```

**Explanation:**
Oracle will attempt to join on `employee_id`, `department_id`, `job_id`, *and* `last_update_date`. For a row to appear in the result, *all* these columns must match between `employees` and `job_history`.

Let's look at `employees` employee 101:
`EMPLOYEES`: `employee_id=101`, `department_id=90`, `job_id='AD_VP'`, `last_update_date=DATE '2023-02-20'`

And `job_history` for employee 101:
1. `employee_id=101`, `department_id=10`, `job_id='AC_ACCOUNT'`, `last_update_date=DATE '2023-01-15'`
2. `employee_id=101`, `department_id=20`, `job_id='AC_MGR'`, `last_update_date=DATE '2023-01-15'`

Notice that `department_id`, `job_id`, and `last_update_date` *do not* match between the current `employees` record and *any* of its `job_history` records. This means the `NATURAL JOIN` will produce **no rows** because it requires a match on *all* common columns.

**Output:**

*(No rows selected)*

This demonstrates the severe pitfall: a seemingly logical join (`employees` and `job_history`) yields no results because of an unintended match on `last_update_date` (and potentially `department_id`, `job_id` if an employee changed departments or jobs and that's reflected in `job_history`). If you intended to join only on `employee_id`, this query is disastrously wrong.

---

### Example 4: `NATURAL LEFT JOIN`

**Scenario:** Retrieve all employees and their department names. If an employee does not have an assigned department, still list the employee.
**Common Column:** `department_id`

**Query:**

```sql
SELECT
    e.first_name,
    e.last_name,
    d.department_name
FROM
    employees e
NATURAL LEFT JOIN
    departments d
ORDER BY
    e.last_name;
```

**Explanation:**
This is similar to Example 1, but using `NATURAL LEFT JOIN`. All employees from the `employees` table (the left table) will be included in the result. If an employee's `department_id` does not match any `department_id` in the `departments` table, the department-related columns (`department_name`) will show `NULL`. We included an "Unknown Employee" with `department_id` as `NULL` to demonstrate this.

**Output:**

| FIRST_NAME  | LAST_NAME   | DEPARTMENT_NAME |
| :---------- | :---------- | :-------------- |
| Laura       | Bissot      | Marketing       |
| Gerald      | Cambrault   | Marketing       |
| John        | Chen        | Administration  |
| Kelly       | Chung       | Marketing       |
| Lex         | De Haan     | Executive       |
| Alberto     | Errazuriz   | Marketing       |
| Bruce       | Ernst       | IT              |
| Daniel      | Faviet      | Administration  |
| Adam        | Fripp       | Marketing       |
| Joshua      | Grant       | Shipping        |
| Nancy       | Greenberg   | Administration  |
| Michael     | Hartstein   | Marketing       |
| Alexander   | Hunold      | IT              |
| Steven      | King        | Executive       |
| Neena       | Kochhar     | Executive       |
| James       | Landry      | Shipping        |
| Diana       | Lorentz     | IT              |
| Steven      | Markle      | Shipping        |
| Mozhe       | Maurer      | Marketing       |
| Irene       | Mikkilineni | Shipping        |
| Kevin       | Mourgos     | Shipping        |
| Julia       | Nayer       | Shipping        |
| Valli       | Pataballa   | IT              |
| Karen       | Partners    | Marketing       |
| Pat         | Fay         | Marketing       |
| Luis        | Popp        | Administration  |
| Ismael      | Sciarra     | Administration  |
| Laura       | Tien        | Shipping        |
| Unknown     | Employee    | (null)          |
| Jose Manuel | Urman       | Administration  |
| Shanta      | Vollman     | Shipping        |
| Jennifer    | Whalen      | Administration  |
| Eleni       | Zlotkey     | Marketing       |

---

## 8. Comparison with `JOIN ... ON` and `JOIN ... USING`

For clarity and safety, `NATURAL JOIN` is generally less preferred than `JOIN ... ON` or `JOIN ... USING`.

*   **`JOIN ... ON` (Explicit Join Condition):**
    ```sql
    SELECT e.first_name, e.last_name, d.department_name
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id;
    ```
    *   **Pros:** Most explicit, always clear what columns are used. Full control over conditions (e.g., `AND other_condition`).
    *   **Cons:** Can be verbose if many columns are involved. Common columns appear twice if selected with `*`.
    *   **Recommendation:** **Highly recommended** for most scenarios.

*   **`JOIN ... USING` (Explicit Common Columns):**
    ```sql
    SELECT first_name, last_name, department_name
    FROM employees
    JOIN departments USING (department_id);
    ```
    *   **Pros:** More concise than `ON` when tables share common-named columns *and you intend to join only on those*. Common columns appear only once in the result (like `NATURAL JOIN`).
    *   **Cons:** Still requires column names to match exactly. Cannot include complex join conditions beyond equality on specified columns.
    *   **Recommendation:** A good alternative to `ON` when the join is purely on identically named columns, offering conciseness without the hidden conditions of `NATURAL JOIN`.

## 9. Conclusion and Best Practices

While `NATURAL JOIN` offers brevity, its implicit nature introduces significant risks of unintended behavior, especially in larger databases or schemas that evolve over time.

**Best Practices:**

*   **Avoid `NATURAL JOIN` in most production code.** The potential for incorrect results due to accidental column name matches outweighs the benefit of concise syntax.
*   **Prefer `JOIN ... ON` for clarity.** It explicitly states the join conditions, making the query easier to understand, maintain, and debug.
*   **Consider `JOIN ... USING` as an alternative** if you value conciseness for simple equality joins on identically named columns, as it still explicitly lists the columns being used for the join.
*   If you *must* use `NATURAL JOIN` (e.g., in a perfectly controlled, small development environment where you are certain of column naming conventions), ensure you thoroughly test your queries and understand all common column names between the tables involved.