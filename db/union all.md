The `UNION ALL` operator in Oracle SQL (and standard SQL) is used to combine the result sets of two or more `SELECT` statements into a single result set. The key characteristic of `UNION ALL` is that it **includes all rows** from each `SELECT` statement, even if they are duplicates.

---

## UNION ALL Operator in Oracle SQL

### 1. Introduction

The `UNION ALL` operator combines the results of multiple `SELECT` queries into a single result set. It stacks the results of the second (and subsequent) query beneath the results of the first query.

The primary use case for `UNION ALL` is when you need to retrieve data from different tables, or different parts of the same table, and present it as one consolidated list, without filtering out duplicate rows.

### 2. Syntax

```sql
SELECT column1, column2, ...
FROM table1
[WHERE conditions]

UNION ALL

SELECT column1, column2, ...
FROM table2
[WHERE conditions]

UNION ALL

SELECT column1, column2, ...
FROM table3
[WHERE conditions]
-- You can add more UNION ALL clauses as needed
[ORDER BY column_name [ASC | DESC], ...];
```

### 3. Key Characteristics and Rules

*   **Combines Vertically:** Results are appended one after another.
*   **Includes Duplicates:** All rows from all `SELECT` statements are returned, even if identical rows exist across the combined result sets. This is the main difference from `UNION` (which removes duplicates).
*   **Number of Columns:** Each `SELECT` statement within the `UNION ALL` must have the **same number of columns**.
*   **Data Types:** The corresponding columns in each `SELECT` statement must have **compatible data types**. Oracle will perform implicit data type conversion if possible (e.g., `NUMBER` to `VARCHAR2`), but it's best practice to ensure they are the same or explicitly convert them.
*   **Column Names:** The column names in the final result set are determined by the column names from the **first `SELECT` statement**. Subsequent `SELECT` statements' column aliases are ignored.
*   **ORDER BY Clause:** If an `ORDER BY` clause is used, it must be placed at the very end of the entire `UNION ALL` statement, and it should reference columns by their position or by the names defined in the first `SELECT` statement.

### 4. Comparison with `UNION`

| Feature              | `UNION ALL`                                  | `UNION`                                            |
| :------------------- | :------------------------------------------- | :------------------------------------------------- |
| **Duplicate Rows**   | **Keeps all duplicate rows.**                | **Removes duplicate rows.**                        |
| **Performance**      | Generally **faster**                         | Generally **slower** (due to the overhead of de-duplication, which involves sorting or hashing). |
| **Use Case**         | When all records are needed, or performance is critical and duplicates are acceptable/non-existent. | When a distinct list of combined records is required. |

### 5. When to Use `UNION ALL`

*   **Consolidating Reports:** Combining sales data from different quarters, regions, or tables into a single report where every transaction is important.
*   **Archived Data:** Querying current data and historical data (e.g., from an archive table) together.
*   **Performance:** When you are certain there are no duplicates, or you explicitly want duplicates, `UNION ALL` is preferred over `UNION` for better performance on large datasets.
*   **Generating Test Data:** Quickly creating a combined dataset for testing purposes.

---

### 6. Examples

Let's illustrate `UNION ALL` with examples, including input (table creation and data insertion) and output.

#### Example 1: Simple Demonstration of Duplicates

This example will highlight the core difference between `UNION ALL` and `UNION` by including a duplicate row.

**Input (SQL for creating and populating temporary data):**

We'll use Oracle's `DUAL` table for simplicity to simulate data without creating actual tables.

```sql
-- No tables needed, using DUAL for direct row generation
-- Conceptual data for the first SELECT:
-- (1, 'Apple')
-- (2, 'Banana')

-- Conceptual data for the second SELECT (includes a duplicate of 'Apple'):
-- (1, 'Apple')
-- (3, 'Cherry')
```

**SQL Query with `UNION ALL`:**

```sql
SELECT 1 AS product_id, 'Apple' AS product_name FROM DUAL
UNION ALL
SELECT 2 AS product_id, 'Banana' AS product_name FROM DUAL
UNION ALL
SELECT 1 AS product_id, 'Apple' AS product_name FROM DUAL -- This is a duplicate row
UNION ALL
SELECT 3 AS product_id, 'Cherry' AS product_name FROM DUAL;
```

**Output of `UNION ALL`:**

| PRODUCT_ID | PRODUCT_NAME |
| :--------- | :----------- |
| 1          | Apple        |
| 2          | Banana       |
| 1          | Apple        |
| 3          | Cherry       |

**Explanation:** Notice that the row `(1, 'Apple')` appears twice in the result because `UNION ALL` includes all rows without filtering duplicates.

---

**SQL Query with `UNION` (for comparison):**

```sql
SELECT 1 AS product_id, 'Apple' AS product_name FROM DUAL
UNION
SELECT 2 AS product_id, 'Banana' AS product_name FROM DUAL
UNION
SELECT 1 AS product_id, 'Apple' AS product_name FROM DUAL
UNION
SELECT 3 AS product_id, 'Cherry' AS product_name FROM DUAL;
```

**Output of `UNION` (for comparison):**

| PRODUCT_ID | PRODUCT_NAME |
| :--------- | :----------- |
| 1          | Apple        |
| 2          | Banana       |
| 3          | Cherry       |

**Explanation:** With `UNION`, the duplicate row `(1, 'Apple')` is removed, resulting in only unique combinations of `product_id` and `product_name`.

---

#### Example 2: Combining Sales Data from Different Quarters

Imagine you have separate tables for sales data for different quarters to manage data size, and you want to see all sales for the first half of the year.

**Input (SQL for creating tables and inserting data):**

```sql
-- Drop tables if they exist from previous runs
DROP TABLE sales_q1 CASCADE CONSTRAINTS;
DROP TABLE sales_q2 CASCADE CONSTRAINTS;

-- Create SALES_Q1 table
CREATE TABLE sales_q1 (
    sale_id      NUMBER PRIMARY KEY,
    product_id   NUMBER,
    sale_date    DATE,
    amount       NUMBER(10, 2)
);

-- Insert data into SALES_Q1
INSERT INTO sales_q1 (sale_id, product_id, sale_date, amount) VALUES (1, 101, DATE '2023-01-15', 150.00);
INSERT INTO sales_q1 (sale_id, product_id, sale_date, amount) VALUES (2, 102, DATE '2023-02-20', 200.50);
INSERT INTO sales_q1 (sale_id, product_id, sale_date, amount) VALUES (3, 101, DATE '2023-03-10', 150.00);
INSERT INTO sales_q1 (sale_id, product_id, sale_date, amount) VALUES (4, 103, DATE '2023-03-25', 75.25);
COMMIT;

-- Create SALES_Q2 table
CREATE TABLE sales_q2 (
    sale_id      NUMBER PRIMARY KEY,
    product_id   NUMBER,
    sale_date    DATE,
    amount       NUMBER(10, 2)
);

-- Insert data into SALES_Q2
INSERT INTO sales_q2 (sale_id, product_id, sale_date, amount) VALUES (5, 101, DATE '2023-04-05', 150.00);
INSERT INTO sales_q2 (sale_id, product_id, sale_date, amount) VALUES (6, 104, DATE '2023-05-12', 300.75);
INSERT INTO sales_q2 (sale_id, product_id, sale_date, amount) VALUES (7, 102, DATE '2023-06-01', 200.50);
INSERT INTO sales_q2 (sale_id, product_id, sale_date, amount) VALUES (8, 105, DATE '2023-06-18', 99.99);
COMMIT;
```

**SQL Query with `UNION ALL`:**

```sql
SELECT product_id, sale_date, amount
FROM sales_q1
WHERE sale_date BETWEEN DATE '2023-01-01' AND DATE '2023-03-31' -- Filter for Q1
UNION ALL
SELECT product_id, sale_date, amount
FROM sales_q2
WHERE sale_date BETWEEN DATE '2023-04-01' AND DATE '2023-06-30' -- Filter for Q2
ORDER BY sale_date; -- Order the entire combined result set
```

**Output of `UNION ALL`:**

| PRODUCT_ID | SALE_DATE           | AMOUNT  |
| :--------- | :------------------ | :------ |
| 101        | 2023-01-15 00:00:00 | 150.00  |
| 102        | 2023-02-20 00:00:00 | 200.50  |
| 101        | 2023-03-10 00:00:00 | 150.00  |
| 103        | 2023-03-25 00:00:00 | 75.25   |
| 101        | 2023-04-05 00:00:00 | 150.00  |
| 104        | 2023-05-12 00:00:00 | 300.75  |
| 102        | 2023-06-01 00:00:00 | 200.50  |
| 105        | 2023-06-18 00:00:00 | 99.99   |

**Explanation:**
The query successfully combines all sales records from `sales_q1` and `sales_q2` that fall within their respective quarters. Even though `product_id` 101 and 102 appear in both tables, the individual `sale_id` and `sale_date` make these distinct transactions, so `UNION ALL` correctly lists them all. The `ORDER BY` clause ensures the final combined result is sorted by sale date.

---

#### Example 3: Combining Data with Different Column Aliases

This example demonstrates how `UNION ALL` handles column aliases.

**Input:** (Using `DUAL` again for direct values)

```sql
-- Conceptual data for the first SELECT:
-- (10, 'Red')
-- (20, 'Blue')

-- Conceptual data for the second SELECT:
-- (30, 'Green')
-- (10, 'Red')
```

**SQL Query:**

```sql
SELECT 10 AS id_value, 'Red' AS color_name FROM DUAL
UNION ALL
SELECT 20 AS id_value, 'Blue' AS color_name FROM DUAL
UNION ALL
SELECT 30 AS item_id, 'Green' AS item_color FROM DUAL -- Different aliases in second SELECT
UNION ALL
SELECT 10 AS item_id, 'Red' AS item_color FROM DUAL;   -- Different aliases, and a duplicate
```

**Output:**

| ID_VALUE | COLOR_NAME |
| :------- | :--------- |
| 10       | Red        |
| 20       | Blue       |
| 30       | Green      |
| 10       | Red        |

**Explanation:**
Even though the second and third `SELECT` statements use `item_id` and `item_color` as aliases, the final output columns are named `ID_VALUE` and `COLOR_NAME`, which are taken from the *first* `SELECT` statement. The duplicate row `(10, 'Red')` is also preserved.

---

### 7. Performance Considerations

`UNION ALL` is generally more performant than `UNION` because it avoids the overhead of sorting and de-duplicating rows. When working with very large datasets, this performance difference can be significant. If you are certain that your individual `SELECT` queries will not produce duplicate rows that you would want to remove, or if you explicitly want to keep all rows (including logical duplicates from different sources), always prefer `UNION ALL`.

---