A `FULL JOIN` (also known as `FULL OUTER JOIN`) combines the results of both `LEFT JOIN` and `RIGHT JOIN`. It returns all rows from both the left and right tables, with `NULL` values for columns where there is no match in the other table.

In essence, a `FULL JOIN` ensures that no data is lost from either table when you're trying to combine them based on a common column.

---

## FULL JOIN in SQL Oracle

### 1. Introduction

The `FULL JOIN` clause in SQL is used to combine rows from two or more tables. It returns:
*   All rows from the left table.
*   All rows from the right table.
*   Where the join condition is met, it returns matching rows.
*   Where there is no match, the columns of the non-matching side will contain `NULL` values.

This is particularly useful when you want to see all data from both datasets, highlighting where matches exist and where data is unique to one of the tables.

### 2. Key Characteristics

*   **Combines All Rows:** Includes every row from both the left and right tables.
*   **Matches Where Possible:** For rows that satisfy the join condition, it presents the combined data.
*   **`NULL` for Non-Matches:** If a row from the left table has no match in the right table, the right table's columns will be `NULL`. Conversely, if a row from the right table has no match in the left table, the left table's columns will be `NULL`.
*   **`FULL JOIN` vs `FULL OUTER JOIN`:** These two terms are synonymous in SQL. `OUTER` is optional but often used for clarity.

### 3. Venn Diagram Analogy

Imagine two sets (tables) as circles:

*   **Left Circle:** Represents `TableA`.
*   **Right Circle:** Represents `TableB`.
*   **Overlap:** Represents the rows that match in both `TableA` and `TableB` (like an `INNER JOIN`).

A `FULL JOIN` covers **all areas** of both circles – the unique parts of `TableA`, the unique parts of `TableB`, and their overlapping intersection.

```
       +-----------------+
       |  TableA Only    |
       |                 |
       |  (Left Non-Match)|
       |                 |     +-----------------+
       +-----------------+     |  TableB Only    |
                 \       /     |                 |
                  \     /      | (Right Non-Match)|
                   \   /       |                 |
                    \ /        +-----------------+
                     X
                    / \
                   /   \
                  /     \
                 /       \
       +-----------------+
       |    Matching     |
       |   (Inner Join)  |
       |                 |
       +-----------------+

```
`FULL JOIN` = `TableA Only` + `TableB Only` + `Matching`

### 4. Syntax

```sql
SELECT
    column1,
    column2,
    ...
FROM
    TableA
FULL [OUTER] JOIN
    TableB ON TableA.common_column = TableB.common_column;
```

*   `TableA`: The left table.
*   `TableB`: The right table.
*   `common_column`: The column(s) used to establish the relationship between the two tables.

### 5. Detailed Example (Oracle SQL)

Let's create two simple tables: `products` and `orders`.

**Scenario:**
*   Some products have corresponding orders.
*   Some products exist but have no orders.
*   Some orders exist for products that might not be in our `products` list (e.g., due to data entry error or historical data).

#### Input Data Setup (DDL & DML)

```sql
-- Drop tables if they already exist for a clean run
DROP TABLE orders PURGE;
DROP TABLE products PURGE;

-- Create Products Table
CREATE TABLE products (
    product_id NUMBER PRIMARY KEY,
    product_name VARCHAR2(100)
);

-- Insert data into Products Table
INSERT INTO products (product_id, product_name) VALUES (1, 'Laptop');
INSERT INTO products (product_id, product_name) VALUES (2, 'Mouse');
INSERT INTO products (product_id, product_name) VALUES (3, 'Keyboard');
INSERT INTO products (product_id, product_name) VALUES (5, 'Webcam'); -- Product with no orders yet

-- Create Orders Table
CREATE TABLE orders (
    order_id NUMBER PRIMARY KEY,
    product_id NUMBER, -- This can be NULL or point to a non-existent product
    quantity NUMBER
);

-- Insert data into Orders Table
INSERT INTO orders (order_id, product_id, quantity) VALUES (101, 2, 5);  -- Mouse (Matches products)
INSERT INTO orders (order_id, product_id, quantity) VALUES (102, 3, 2);  -- Keyboard (Matches products)
INSERT INTO orders (order_id, product_id, quantity) VALUES (103, 4, 1);  -- Order for an unknown product (ID 4 not in products)
INSERT INTO orders (order_id, product_id, quantity) VALUES (104, NULL, 10); -- Order with no product ID (conceptually, a custom item or error)
INSERT INTO orders (order_id, product_id, quantity) VALUES (105, 2, 3); -- Another order for Mouse
COMMIT;
```

#### Input (Current Data in Tables)

**`products` Table:**

| PRODUCT_ID | PRODUCT_NAME |
| :--------- | :----------- |
| 1          | Laptop       |
| 2          | Mouse        |
| 3          | Keyboard     |
| 5          | Webcam       |

**`orders` Table:**

| ORDER_ID | PRODUCT_ID | QUANTITY |
| :------- | :--------- | :------- |
| 101      | 2          | 5        |
| 102      | 3          | 2        |
| 103      | 4          | 1        |
| 104      |            | 10       |
| 105      | 2          | 3        |

#### The FULL JOIN Query

```sql
SELECT
    p.product_id AS product_table_id,
    p.product_name,
    o.order_id,
    o.product_id AS order_table_product_id,
    o.quantity
FROM
    products p
FULL OUTER JOIN
    orders o ON p.product_id = o.product_id
ORDER BY
    NVL(p.product_id, o.product_id); -- Order by either ID for consistent sorting
```

#### Output

| PRODUCT_TABLE_ID | PRODUCT_NAME | ORDER_ID | ORDER_TABLE_PRODUCT_ID | QUANTITY |
| :--------------- | :----------- | :------- | :--------------------- | :------- |
| 1                | Laptop       |          |                        |          |
| 2                | Mouse        | 101      | 2                      | 5        |
| 2                | Mouse        | 105      | 2                      | 3        |
| 3                | Keyboard     | 102      | 3                      | 2        |
|                  |              | 103      | 4                      | 1        |
| 5                | Webcam       |          |                        |          |
|                  |              | 104      |                        | 10       |

#### Explanation of the Output:

1.  **`product_id = 1` (Laptop):** This product exists in `products` but has no matching `product_id` in `orders`.
    *   `p.product_id`, `p.product_name` show the product details.
    *   `o.order_id`, `o.product_id`, `o.quantity` are `NULL`.
    *   **(Left-only match)**

2.  **`product_id = 2` (Mouse):** This product exists in `products` and has two matching orders (`101` and `105`) in `orders`.
    *   Both sides of the join condition are met and values are shown.
    *   **(Inner Join match)**

3.  **`product_id = 3` (Keyboard):** This product exists in `products` and has one matching order (`102`) in `orders`.
    *   Both sides of the join condition are met and values are shown.
    *   **(Inner Join match)**

4.  **`order_id = 103` (Product ID 4):** This order exists in `orders` with `product_id = 4`, but there is no `product_id = 4` in the `products` table.
    *   `p.product_id`, `p.product_name` are `NULL`.
    *   `o.order_id`, `o.product_id`, `o.quantity` show the order details.
    *   **(Right-only match)**

5.  **`product_id = 5` (Webcam):** This product exists in `products` but has no matching `product_id` in `orders`.
    *   `p.product_id`, `p.product_name` show the product details.
    *   `o.order_id`, `o.product_id`, `o.quantity` are `NULL`.
    *   **(Left-only match)**

6.  **`order_id = 104` (NULL Product ID):** This order exists in `orders` with `product_id` being `NULL`. A `NULL` value will never match another `NULL` or any non-`NULL` value in a join condition (unless explicitly handled with `IS NULL` in the `ON` clause, which is unusual for primary key joins).
    *   `p.product_id`, `p.product_name` are `NULL`.
    *   `o.order_id`, `o.product_id`, `o.quantity` show the order details.
    *   **(Right-only match - effectively, as NULL doesn't match)**

### 6. Important Considerations

*   **Performance:** `FULL JOIN` can be resource-intensive, especially with large tables, as it requires processing and combining all rows from both tables.
*   **Finding Unmatched Rows:** A common use case for `FULL JOIN` is to identify rows that *do not* have a match in the other table. You can achieve this by adding a `WHERE` clause:
    ```sql
    SELECT
        p.product_id AS product_table_id,
        p.product_name,
        o.order_id,
        o.product_id AS order_table_product_id,
        o.quantity
    FROM
        products p
    FULL OUTER JOIN
        orders o ON p.product_id = o.product_id
    WHERE
        p.product_id IS NULL OR o.product_id IS NULL; -- Filters to show only non-matching rows
    ```
    This would return the rows for 'Laptop', 'Webcam', and orders '103', '104'.
*   **`NULL` in Join Conditions:** Be careful when joining on columns that might contain `NULL` values. `NULL` does not equal `NULL` in SQL, so `p.product_id = o.product_id` will *not* match rows where both `p.product_id` and `o.product_id` are `NULL`. If you need to match on `NULL`s, you would need to adjust your `ON` clause using `OR` with `IS NULL` conditions, which is generally complex and indicates potential data design issues.

### Conclusion

`FULL JOIN` is a powerful tool for comprehensive data retrieval, allowing you to see the complete picture by combining all records from two tables and identifying both matching and non-matching entries. It's particularly useful for data analysis, reporting, and auditing where a complete view of related datasets is required.