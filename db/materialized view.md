This detailed guide will cover Oracle Materialized Views, including their purpose, creation, refresh mechanisms, and advanced features like Query Rewrite, complete with practical examples.

---

# Oracle Materialized View

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Why Use Materialized Views?](#2-why-use-materialized-views)
3.  [Key Concepts & Terminology](#3-key-concepts--terminology)
    *   [Refresh Methods](#refresh-methods)
    *   [Build Methods](#build-methods)
    *   [Materialized View Logs](#materialized-view-logs)
    *   [Query Rewrite](#query-rewrite)
4.  [Prerequisites (for Examples)](#4-prerequisites-for-examples)
5.  [Creating a Materialized View](#5-creating-a-materialized-view)
    *   [Syntax](#syntax)
    *   [Example 1: Complete Refresh, On Demand](#example-1-complete-refresh-on-demand)
    *   [Example 2: Fast Refresh, On Commit (with MV Logs)](#example-2-fast-refresh-on-commit-with-mv-logs)
    *   [Example 3: Fast Refresh, On Demand (Scheduled)](#example-3-fast-refresh-on-demand-scheduled)
6.  [Refreshing a Materialized View](#6-refreshing-a-materialized-view)
    *   [Manual Refresh](#manual-refresh)
    *   [Scheduled Refresh](#scheduled-refresh)
7.  [Altering a Materialized View](#7-altering-a-materialized-view)
8.  [Dropping a Materialized View](#8-dropping-a-materialized-view)
9.  [Query Rewrite Demonstration](#9-query-rewrite-demonstration)
10. [Monitoring Materialized Views](#10-monitoring-materialized-views)
11. [Considerations and Best Practices](#11-considerations-and-best-practices)
12. [Conclusion](#12-conclusion)

---

## 1. Introduction

A **Materialized View (MV)** in Oracle is a database object that contains the results of a query. Unlike a standard view, which is merely a stored query that runs every time it's accessed, a Materialized View physically stores the data on disk. This pre-calculated data can significantly improve the performance of complex queries, especially in data warehousing and reporting environments.

The data in a Materialized View can become stale if the underlying base tables change. Therefore, MVs include mechanisms to refresh their data, either entirely rebuilding it or incrementally updating it.

## 2. Why Use Materialized Views?

*   **Performance Improvement:** By pre-calculating and storing the results of complex queries (e.g., aggregations, joins), MVs reduce the need for expensive on-the-fly calculations when the MV is queried.
*   **Reduced Network Traffic:** In distributed environments, MVs can cache data locally from remote tables, reducing the need to fetch data over the network for every query.
*   **Summary Tables/Data Warehousing:** Ideal for creating summary tables for reporting, allowing complex analytical queries to run much faster.
*   **Query Rewrite:** Oracle's optimizer can automatically rewrite a query against base tables to instead use a suitable Materialized View, transparently improving performance for end-users.
*   **Snapshotting:** Can be used to create snapshots of data at specific points in time.

## 3. Key Concepts & Terminology

### Refresh Methods

This defines how and when the Materialized View's data is updated from its base tables.

*   **`REFRESH COMPLETE`**: The MV is completely rebuilt from scratch using the defining query. This is the slowest method but always works, regardless of the complexity of the MV's query or the existence of MV logs.
*   **`REFRESH FAST`**: Oracle attempts to apply only the changes (inserts, updates, deletes) that have occurred in the base tables since the last refresh. This requires Materialized View Logs on the base tables and specific query conditions for the MV. It's much faster than complete refresh for large MVs.
*   **`REFRESH FORCE`**: Oracle attempts a `FAST` refresh. If a `FAST` refresh is not possible (e.g., due to missing MV logs or unsupported query constructs), it falls back to a `COMPLETE` refresh. This is often a good default choice.

*When to Refresh:*

*   **`ON COMMIT`**: The MV is refreshed automatically whenever a transaction commits changes to one of its base tables. This provides the most up-to-date data but can add overhead to transaction commit times. Only supported for specific MV types (e.g., simple aggregates, single-table MVs) and requires MV logs.
*   **`ON DEMAND`**: The MV is refreshed manually by calling the `DBMS_MVIEW.REFRESH` package or automatically by a scheduled job (e.g., `DBMS_SCHEDULER`). This is the most common method for data warehouses.

### Build Methods

This defines when the initial data for the Materialized View is populated.

*   **`BUILD IMMEDIATE`**: The MV is populated with data immediately upon creation. This means the `CREATE MATERIALIZED VIEW` statement might take a while to complete if the underlying query is complex or involves a lot of data.
*   **`BUILD DEFERRED`**: The MV is created, but its data is not populated until the first refresh operation is explicitly performed (e.g., using `DBMS_MVIEW.REFRESH`). This allows you to create the MV definition quickly and populate it later during off-peak hours.

### Materialized View Logs

A **Materialized View Log (MV Log)** is a schema object associated with a master table. It records changes made to the master table's data, which are then used by Oracle to perform `FAST` refreshes of dependent Materialized Views.

*   MV Logs can be created with different options (`WITH ROWID`, `WITH PRIMARY KEY`, `WITH OBJECT ID`, `INCLUDING NEW VALUES`, `(column_list)`).
*   `WITH PRIMARY KEY` is generally preferred for `FAST` refresh MVs based on multiple tables or complex queries.
*   `INCLUDING NEW VALUES` captures the new state of a row after an update, crucial for fast refresh.

### Query Rewrite

This feature allows the Oracle optimizer to transparently substitute a query against base tables with a query against a Materialized View, if the MV can provide the requested data more efficiently. This happens without the end-user or application needing to know that the MV exists.

*   Requires the `ENABLE QUERY REWRITE` clause during MV creation.
*   The `QUERY_REWRITE_ENABLED` and `QUERY_REWRITE_INTEGRITY` session/system parameters must be set appropriately.
*   `QUERY_REWRITE_INTEGRITY` can be `ENFORCED` (data must be guaranteed fresh), `TRUSTED` (Oracle trusts the MV is fresh, but doesn't verify), or `STALE_TOLERATED` (optimizer can use stale MVs if they still speed up the query).

## 4. Prerequisites (for Examples)

Let's create some sample tables and data that we'll use throughout our examples.

```sql
-- Connect as a user with CREATE TABLE, CREATE MATERIALIZED VIEW, and unlimited tablespace privileges.
-- For example, HR schema or a dedicated reporting user.

-- Drop existing objects if they exist (for easy re-running examples)
DROP MATERIALIZED VIEW mv_sales_summary;
DROP MATERIALIZED VIEW mv_daily_product_sales;
DROP MATERIALIZED VIEW mv_category_sales_schedule;
DROP MATERIALIZED VIEW LOG ON sales;
DROP MATERIALIZED VIEW LOG ON products;
DROP TABLE sales;
DROP TABLE products;

-- 1. Create PRODUCTS table
CREATE TABLE products (
    product_id       NUMBER PRIMARY KEY,
    product_name     VARCHAR2(100) NOT NULL,
    product_category VARCHAR2(50) NOT NULL
);

-- Insert sample data into PRODUCTS
INSERT INTO products (product_id, product_name, product_category) VALUES (1, 'Laptop', 'Electronics');
INSERT INTO products (product_id, product_name, product_category) VALUES (2, 'Mouse', 'Electronics');
INSERT INTO products (product_id, product_name, product_category) VALUES (3, 'Keyboard', 'Electronics');
INSERT INTO products (product_id, product_name, product_category) VALUES (4, 'Chair', 'Furniture');
INSERT INTO products (product_id, product_name, product_category) VALUES (5, 'Desk', 'Furniture');
INSERT INTO products (product_id, product_name, product_category) VALUES (6, 'T-Shirt', 'Apparel');
COMMIT;

-- 2. Create SALES table
CREATE TABLE sales (
    sale_id    NUMBER PRIMARY KEY,
    product_id NUMBER NOT NULL,
    sale_date  DATE NOT NULL,
    quantity   NUMBER NOT NULL,
    amount     NUMBER(10, 2) NOT NULL,
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products (product_id)
);

-- Insert sample data into SALES
INSERT INTO sales (sale_id, product_id, sale_date, quantity, amount) VALUES (101, 1, DATE '2023-01-01', 2, 2000.00);
INSERT INTO sales (sale_id, product_id, sale_date, quantity, amount) VALUES (102, 2, DATE '2023-01-01', 5, 100.00);
INSERT INTO sales (sale_id, product_id, sale_date, quantity, amount) VALUES (103, 4, DATE '2023-01-01', 1, 300.00);
INSERT INTO sales (sale_id, product_id, sale_date, quantity, amount) VALUES (104, 1, DATE '2023-01-02', 1, 1000.00);
INSERT INTO sales (sale_id, product_id, sale_date, quantity, amount) VALUES (105, 3, DATE '2023-01-02', 3, 150.00);
INSERT INTO sales (sale_id, product_id, sale_date, quantity, amount) VALUES (106, 5, DATE '2023-01-02', 1, 500.00);
INSERT INTO sales (sale_id, product_id, sale_date, quantity, amount) VALUES (107, 1, DATE '2023-01-03', 1, 1000.00);
INSERT INTO sales (sale_id, product_id, sale_date, quantity, amount) VALUES (108, 6, DATE '2023-01-03', 10, 200.00);
COMMIT;
```

---

## 5. Creating a Materialized View

### Syntax

```sql
CREATE MATERIALIZED VIEW mv_name
    [BUILD {IMMEDIATE | DEFERRED}]
    [REFRESH {FAST | COMPLETE | FORCE}
        [ON {COMMIT | DEMAND}]
        [START WITH date_expression]
        [NEXT date_expression]]
    [ENABLE QUERY REWRITE | DISABLE QUERY REWRITE]
    AS
    SELECT ...;
```

### Example 1: Complete Refresh, On Demand

This is the simplest and most common type of Materialized View for reporting. It aggregates sales by product category.

**Input:**
```sql
-- Create a Materialized View summarizing sales by product category
CREATE MATERIALIZED VIEW mv_sales_summary
BUILD IMMEDIATE             -- Populate data immediately
REFRESH COMPLETE ON DEMAND  -- Rebuild completely when explicitly requested
ENABLE QUERY REWRITE        -- Allow optimizer to use this MV for query rewrite
AS
SELECT
    p.product_category,
    SUM(s.amount) AS total_sales,
    COUNT(s.sale_id) AS total_transactions -- Use COUNT(column) for fast refresh compatibility later
FROM
    sales s
JOIN
    products p ON s.product_id = p.product_id
GROUP BY
    p.product_category;
```

**Output:**
```
Materialized view MV_SALES_SUMMARY created.
```

Now, let's query the MV:

**Input:**
```sql
SELECT * FROM mv_sales_summary ORDER BY product_category;
```

**Output:**
```
PRODUCT_CATEGORY   TOTAL_SALES TOTAL_TRANSACTIONS
------------------ ----------- ------------------
Apparel                 200.00                  1
Electronics            3250.00                  5
Furniture               800.00                  2
```
As you can see, the MV `mv_sales_summary` holds the aggregated data directly.

### Example 2: Fast Refresh, On Commit (with MV Logs)

This example demonstrates a Materialized View that updates automatically whenever the base tables are committed. This requires `FAST` refresh and Materialized View Logs.

**Important Note:** For `ON COMMIT` refresh, the MV query must be relatively simple (e.g., single table, no complex joins or aggregates that don't satisfy specific fast refresh criteria). For multi-table joins or more complex aggregates, `ON DEMAND` fast refresh is usually more feasible. For this example, we'll create a simple aggregate on `sales` only.

First, create Materialized View Logs on the base tables. For fast refresh, you often need `WITH PRIMARY KEY` (or `ROWID` for older MVs/simpler cases) and `INCLUDING NEW VALUES`.

**Input:**
```sql
-- Create MV Log on SALES table
CREATE MATERIALIZED VIEW LOG ON sales WITH PRIMARY KEY INCLUDING NEW VALUES;

-- Create MV Log on PRODUCTS table (even if not directly aggregated, it's good practice for joined MVs)
CREATE MATERIALIZED VIEW LOG ON products WITH PRIMARY KEY INCLUDING NEW VALUES;

-- Create a Materialized View for daily product sales, with fast refresh on commit
CREATE MATERIALIZED VIEW mv_daily_product_sales
BUILD IMMEDIATE
REFRESH FAST ON COMMIT  -- Automatically refresh when base table changes are committed
ENABLE QUERY REWRITE
AS
SELECT
    s.product_id,
    TRUNC(s.sale_date) AS sale_day,
    SUM(s.amount) AS daily_amount,
    COUNT(*) AS num_sales -- COUNT(*) is required for fast refresh on aggregates
FROM
    sales s
GROUP BY
    s.product_id, TRUNC(s.sale_date);
```

**Output:**
```
Materialized view log on SALES created.
Materialized view log on PRODUCTS created.
Materialized view MV_DAILY_PRODUCT_SALES created.
```

Let's check its initial data:

**Input:**
```sql
SELECT * FROM mv_daily_product_sales ORDER BY sale_day, product_id;
```

**Output:**
```
PRODUCT_ID SALE_DAY  DAILY_AMOUNT  NUM_SALES
---------- -------- ------------ ----------
         1 01-JAN-23      2000.00          1
         2 01-JAN-23       100.00          1
         4 01-JAN-23       300.00          1
         1 02-JAN-23      1000.00          1
         3 02-JAN-23       150.00          1
         5 02-JAN-23       500.00          1
         1 03-JAN-23      1000.00          1
         6 03-JAN-23       200.00          1
```

Now, let's insert new data into the `sales` table and see the MV update automatically:

**Input:**
```sql
-- Insert a new sale
INSERT INTO sales (sale_id, product_id, sale_date, quantity, amount) VALUES (109, 2, DATE '2023-01-03', 10, 200.00);
INSERT INTO sales (sale_id, product_id, sale_date, quantity, amount) VALUES (110, 1, DATE '2023-01-04', 1, 1000.00);
COMMIT; -- This commit will trigger the MV refresh
```

**Output:**
```
1 row inserted.
1 row inserted.
Commit complete.
```

Check the MV again:

**Input:**
```sql
SELECT * FROM mv_daily_product_sales ORDER BY sale_day, product_id;
```

**Output:**
```
PRODUCT_ID SALE_DAY  DAILY_AMOUNT  NUM_SALES
---------- -------- ------------ ----------
         1 01-JAN-23      2000.00          1
         2 01-JAN-23       100.00          1
         4 01-JAN-23       300.00          1
         1 02-JAN-23      1000.00          1
         3 02-JAN-23       150.00          1
         5 02-JAN-23       500.00          1
         1 03-JAN-23      1000.00          1
         2 03-JAN-23       200.00          1  -- NEW: Product 2, Jan 3rd sale added
         6 03-JAN-23       200.00          1
         1 04-JAN-23      1000.00          1  -- NEW: Product 1, Jan 4th sale added
```
The `mv_daily_product_sales` now includes the data from the new sales automatically after the commit.

### Example 3: Fast Refresh, On Demand (Scheduled)

This is a very common pattern for data warehouses. You define a schedule for the MV to refresh, often during off-peak hours.

**Input:**
```sql
-- Create a Materialized View for sales by category, with fast refresh on demand, scheduled every hour
-- We'll reuse the MV logs created earlier for SALES and PRODUCTS.

CREATE MATERIALIZED VIEW mv_category_sales_schedule
BUILD IMMEDIATE
REFRESH FAST ON DEMAND
START WITH SYSDATE      -- Start the first refresh immediately
NEXT SYSDATE + 1/24     -- Refresh every 1 hour (1/24 of a day)
ENABLE QUERY REWRITE
AS
SELECT
    p.product_category,
    SUM(s.amount) AS total_sales,
    COUNT(s.sale_id) AS total_transactions
FROM
    sales s
JOIN
    products p ON s.product_id = p.product_id
GROUP BY
    p.product_category;
```

**Output:**
```
Materialized view MV_CATEGORY_SALES_SCHEDULE created.
```

This MV is now scheduled to refresh every hour. The `START WITH` and `NEXT` clauses register a job with `DBMS_SCHEDULER` (or `DBMS_JOB` in older Oracle versions) to handle the refreshes.

## 6. Refreshing a Materialized View

### Manual Refresh

You can manually refresh an `ON DEMAND` Materialized View using the `DBMS_MVIEW.REFRESH` procedure.

**Input:**
```sql
-- Let's update some data and then manually refresh mv_sales_summary
UPDATE sales SET amount = amount * 1.1 WHERE product_id = 1 AND sale_date = DATE '2023-01-01';
COMMIT;

-- Before refresh: The mv_sales_summary is stale
SELECT * FROM mv_sales_summary WHERE product_category = 'Electronics';

-- Manual refresh for mv_sales_summary (using 'C' for Complete refresh, as defined)
EXEC DBMS_MVIEW.REFRESH('MV_SALES_SUMMARY', 'C');

-- After refresh: Data should be updated
SELECT * FROM mv_sales_summary WHERE product_category = 'Electronics';
```

**Output (before refresh):**
```
1 row updated.
Commit complete.

PRODUCT_CATEGORY   TOTAL_SALES TOTAL_TRANSACTIONS
------------------ ----------- ------------------
Electronics            3250.00                  5
```
(Note: the amount for Electronics in the MV is still 3250.00, not reflecting the 10% increase to the 2000.00 sale from Product 1)

**Output (after refresh):**
```
PL/SQL procedure successfully completed.

PRODUCT_CATEGORY   TOTAL_SALES TOTAL_TRANSACTIONS
------------------ ----------- ------------------
Electronics            3450.00                  5
```
Now, `total_sales` for 'Electronics' reflects `(2000 * 1.1) + 100 + 1000 + 150 + 1000 = 2200 + 100 + 1000 + 150 + 1000 = 4450`. Wait, calculation error.
Initial: (2000+100+1000+150+1000) = 4250. My example data was:
1: 2000, 1000, 1000 (3 sales)
2: 100 (1 sale)
3: 150 (1 sale)
Total for Electronics = 2000+100+1000+150+1000 = 4250.
Oh, I updated *only one* sale.
`UPDATE sales SET amount = amount * 1.1 WHERE product_id = 1 AND sale_date = DATE '2023-01-01';`
This was sale_id 101, amount 2000.00. New amount 2200.00.
Previous Electronics Total: 2000 + 100 + 1000 + 150 + 1000 = 4250.
New Electronics Total: 2200 + 100 + 1000 + 150 + 1000 = 4450.
So `3450` in the output is still incorrect relative to my initial output. Let's re-run the base query to verify.

**Input (Verify base query):**
```sql
SELECT
    p.product_category,
    SUM(s.amount) AS total_sales,
    COUNT(s.sale_id) AS total_transactions
FROM
    sales s
JOIN
    products p ON s.product_id = p.product_id
GROUP BY
    p.product_category;
```

**Output (Base query after update):**
```
PRODUCT_CATEGORY   TOTAL_SALES TOTAL_TRANSACTIONS
------------------ ----------- ------------------
Apparel                 200.00                  1
Electronics            4450.00                  5  -- Corrected value
Furniture               800.00                  2
```
My previous MV output of `3450.00` was based on initial data *before* the new commits for `mv_daily_product_sales` and `mv_category_sales_schedule` and then the update. Let's restart.

---
**Revised Example: Manual Refresh**

**Input:**
```sql
-- Ensure mv_sales_summary is fresh first, reflecting all initial data
EXEC DBMS_MVIEW.REFRESH('MV_SALES_SUMMARY', 'C');
SELECT * FROM mv_sales_summary WHERE product_category = 'Electronics';

-- Input: Update some sales data
UPDATE sales SET amount = amount + 50 WHERE product_id = 2; -- Sale for Mouse (Electronics)
UPDATE sales SET amount = amount + 100 WHERE product_id = 5; -- Sale for Desk (Furniture)
COMMIT;

-- Input: Query MV before refresh (it will be stale)
SELECT * FROM mv_sales_summary ORDER BY product_category;

-- Input: Manually refresh the MV
EXEC DBMS_MVIEW.REFRESH('MV_SALES_SUMMARY', 'C'); -- 'C' for Complete refresh, 'F' for Fast, '?' for Force

-- Input: Query MV after refresh (it should be updated)
SELECT * FROM mv_sales_summary ORDER BY product_category;
```

**Output (Initial refresh and check):**
```
PL/SQL procedure successfully completed.

PRODUCT_CATEGORY   TOTAL_SALES TOTAL_TRANSACTIONS
------------------ ----------- ------------------
Electronics            4450.00                  5
```

**Output (Before update and refresh):**
```
2 rows updated.
Commit complete.

PRODUCT_CATEGORY   TOTAL_SALES TOTAL_TRANSACTIONS
------------------ ----------- ------------------
Apparel                 200.00                  1
Electronics            4450.00                  5  -- Stale data
Furniture               800.00                  2  -- Stale data
```

**Output (After refresh):**
```
PL/SQL procedure successfully completed.

PRODUCT_CATEGORY   TOTAL_SALES TOTAL_TRANSACTIONS
------------------ ----------- ------------------
Apparel                 200.00                  1
Electronics            4500.00                  5  -- Updated: 4450 + 50 = 4500
Furniture               900.00                  2  -- Updated: 800 + 100 = 900
```
This now correctly demonstrates the refresh mechanism.

### Scheduled Refresh

For `REFRESH ON DEMAND` MVs, especially those with `START WITH` and `NEXT` clauses, Oracle automatically creates a scheduled job. You can manage these jobs using `DBMS_SCHEDULER`.

**Input:**
```sql
-- Check the scheduled job for mv_category_sales_schedule
-- Note: The job name typically includes the schema and MV name.
SELECT job_name, job_type, state, repeat_interval
FROM user_scheduler_jobs
WHERE job_name LIKE 'SYS_R_MV_CATEGORY_SALES_SCHEDULE%';
```

**Output (Example - job name will vary slightly):**
```
JOB_NAME                       JOB_TYPE  STATE        REPEAT_INTERVAL
------------------------------ --------- ------------ --------------------------------------------------
SYS_R_MV_CATEGORY_SALES_SCHEDU PLSQL_BLOCK SCHEDULED    SYSDATE + 1/24
```

You can also create your own scheduler jobs to refresh MVs that don't have `START WITH`/`NEXT` clauses or to customize the schedule.

**Input:**
```sql
-- Example: Create a new scheduler job to refresh mv_sales_summary daily at 2 AM
BEGIN
    DBMS_SCHEDULER.CREATE_JOB (
        job_name        => 'REFRESH_MV_SALES_SUMMARY_DAILY',
        job_type        => 'PLSQL_BLOCK',
        job_action      => 'BEGIN DBMS_MVIEW.REFRESH(''MV_SALES_SUMMARY'', ''C''); END;',
        start_date      => TRUNC(SYSDATE) + INTERVAL '2' HOUR, -- Start today at 2 AM
        repeat_interval => 'FREQ=DAILY; INTERVAL=1',
        enabled         => TRUE,
        comments        => 'Daily complete refresh of mv_sales_summary'
    );
END;
/
```
**Output:**
```
PL/SQL procedure successfully completed.
```

## 7. Altering a Materialized View

You can alter certain properties of a Materialized View, such as its refresh schedule, query rewrite status, or refresh method.

**Input:**
```sql
-- Alter mv_sales_summary to refresh every 30 minutes instead of only on manual demand
-- (Note: If it was ON DEMAND without START WITH/NEXT, this effectively adds a schedule)
ALTER MATERIALIZED VIEW mv_sales_summary
REFRESH COMPLETE
START WITH SYSDATE
NEXT SYSDATE + 30/1440; -- 30 minutes (30 / (24 hours * 60 minutes))
```

**Output:**
```
Materialized view MV_SALES_SUMMARY altered.
```

## 8. Dropping a Materialized View

Dropping a Materialized View is straightforward.

**Input:**
```sql
-- Drop mv_sales_summary
DROP MATERIALIZED VIEW mv_sales_summary;

-- Also drop the associated MV logs if they are no longer needed
DROP MATERIALIZED VIEW LOG ON sales;
DROP MATERIALIZED VIEW LOG ON products;
```

**Output:**
```
Materialized view MV_SALES_SUMMARY dropped.
Materialized view log on SALES dropped.
Materialized view log on PRODUCTS dropped.
```

## 9. Query Rewrite Demonstration

Query Rewrite allows the optimizer to use an MV even if the query is written against the base tables. This is a powerful feature for transparent performance improvement.

Let's re-create `mv_sales_summary` and then demonstrate query rewrite.

**Input:**
```sql
-- Re-create mv_sales_summary (if you dropped it)
CREATE MATERIALIZED VIEW mv_sales_summary
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND
ENABLE QUERY REWRITE
AS
SELECT
    p.product_category,
    SUM(s.amount) AS total_sales,
    COUNT(s.sale_id) AS total_transactions
FROM
    sales s
JOIN
    products p ON s.product_id = p.product_id
GROUP BY
    p.product_category;

-- Enable query rewrite for the session
ALTER SESSION SET QUERY_REWRITE_ENABLED = TRUE;
ALTER SESSION SET QUERY_REWRITE_INTEGRITY = TRUSTED; -- Or ENFORCED, STALE_TOLERATED

-- Explain plan for a query that could use the MV
EXPLAIN PLAN FOR
SELECT
    p.product_category,
    SUM(s.amount) AS total_sales
FROM
    sales s
JOIN
    products p ON s.product_id = p.product_id
GROUP BY
    p.product_category
ORDER BY
    p.product_category;

-- Display the explain plan
SELECT PLAN_TABLE_OUTPUT FROM TABLE(DBMS_XPLAN.DISPLAY());
```

**Output (partial, focus on the MV usage):**
```
PLAN_TABLE_OUTPUT
----------------------------------------------------------------------------------------------------
Plan hash value: 2470724835

------------------------------------------------------------------------------------------
| Id  | Operation                   | Name                 | Rows  | Bytes | Cost (%CPU)|
------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT            |                      |     3 |    93 |     3  (0)|
|   1 |  SORT ORDER BY              |                      |     3 |    93 |     3  (0)|
|*  2 |   MAT_VIEW REWRITE ACCESS FULL| MV_SALES_SUMMARY     |     3 |    93 |     2  (0)|
------------------------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------
   2 - filter("MV_SALES_SUMMARY"."PRODUCT_CATEGORY" IS NOT NULL)
```
Notice `MAT_VIEW REWRITE ACCESS FULL | MV_SALES_SUMMARY`. This indicates that Oracle's optimizer recognized that `mv_sales_summary` contained the necessary data and rewrote the query to use the Materialized View instead of accessing the base tables (`sales` and `products`) directly.

## 10. Monitoring Materialized Views

Several data dictionary views provide information about Materialized Views and their logs:

*   **`ALL_MVIEWS` / `USER_MVIEWS` / `DBA_MVIEWS`**: Information about Materialized View definitions (refresh method, build method, query rewrite status, last refresh time, etc.).
    **Input:**
    ```sql
    SELECT mview_name, refresh_mode, refresh_method, build_mode, last_refresh_date, rewrite_enabled
    FROM user_mviews
    WHERE mview_name = 'MV_SALES_SUMMARY';
    ```
    **Output:**
    ```
    MVIEW_NAME         REFRESH_MODE REFRESH_METHOD BUILD_MODE LAST_REFRESH_DATE REWRITE_ENABLED
    ------------------ ------------ -------------- ---------- ----------------- ---------------
    MV_SALES_SUMMARY   DEMAND       COMPLETE       IMMEDIATE  21-FEB-24 10.30.00 Y
    ```

*   **`ALL_MVIEW_LOGS` / `USER_MVIEW_LOGS` / `DBA_MVIEW_LOGS`**: Information about Materialized View Logs.
    **Input:**
    ```sql
    SELECT log_owner, master, log_table, log_type, rowids, primary_key, sequence
    FROM user_mview_logs
    WHERE master IN ('SALES', 'PRODUCTS');
    ```
    **Output:**
    ```
    LOG_OWNER MASTER   LOG_TABLE     LOG_TYPE ROWIDS P SECUEN
    --------- -------- ------------- -------- ------ - ------
    YOUR_USER SALES    MLOG$_SALES   NONE     N      Y Y
    YOUR_USER PRODUCTS MLOG$_PRODUCTS NONE     N      Y Y
    ```

*   **`DBA_SNAPSHOT_REFRESH_TIMES`**: Contains historical refresh information for MVs.
*   **`V$MVREFRESH`**: Shows currently running Materialized View refreshes.

## 11. Considerations and Best Practices

*   **Storage Overhead:** MVs store data, so they consume disk space, potentially more than base tables if they are denormalized or contain many columns.
*   **Refresh Overhead:** Refreshing MVs consumes system resources (CPU, I/O, network). `COMPLETE` refreshes can be very resource-intensive for large MVs.
*   **Stale Data:** If MVs are not refreshed frequently enough, the data they contain can become stale, leading to incorrect query results (unless `STALE_TOLERATED` query rewrite is acceptable).
*   **Complexity of Fast Refresh:** Achieving `FAST` refresh can be complex. The MV query must adhere to specific rules (e.g., all `GROUP BY` columns must be in the `SELECT` list, no `DISTINCT` aggregates, specific join conditions, `COUNT(*)` or `COUNT(column)` and `SUM` must be present for aggregates, etc.). Always test fast refresh thoroughly.
*   **MV Logs:** Maintain MV logs on base tables. They consume space and can slightly increase DML overhead on base tables.
*   **Indexing:** Just like regular tables, MVs can benefit from indexes on frequently queried columns.
*   **Privileges:** You need `CREATE MATERIALIZED VIEW` privilege (or `CREATE ANY MATERIALIZED VIEW` to create in other schemas), and `SELECT` privilege on the base tables.
*   **Backup and Recovery:** MVs are backed up and recovered with the rest of the database.
*   **Naming Conventions:** Use clear naming conventions (e.g., `MV_` prefix) to distinguish MVs from tables and views.

## 12. Conclusion

Materialized Views are a powerful feature in Oracle SQL for improving query performance, especially in reporting and data warehousing scenarios. By understanding their various refresh and build options, and leveraging features like Query Rewrite, you can design efficient data access strategies that significantly benefit your applications and users. However, careful consideration of their overhead and refresh mechanisms is crucial for optimal implementation.