This document provides a detailed overview of Data Definition Language (DDL) in Oracle SQL, including common commands, their syntax, detailed explanations, and practical examples with input and expected output.

---

# Data Definition Language (DDL) in Oracle SQL

Data Definition Language (DDL) commands are used to define, modify, or delete database structures. They are responsible for the overall structure of the database. When you execute a DDL command, it implicitly commits the current transaction. DDL commands cannot be rolled back.

**Key Characteristics of DDL Commands:**

*   **Auto-Commit:** DDL statements automatically commit any pending transactions.
*   **Non-Rollback:** You cannot use the `ROLLBACK` command to undo DDL operations. Once executed, the structural changes are permanent.
*   **Privileges:** Requires specific system privileges (e.g., `CREATE TABLE`, `ALTER TABLE`, `DROP ANY TABLE`).

---

## 1. CREATE Command

The `CREATE` command is used to build new objects in the database.

### 1.1 CREATE TABLE

Used to create a new table in the database.

*   **Syntax:**

    ```sql
    CREATE TABLE table_name (
        column1_name  data_type [DEFAULT default_value] [column_constraint],
        column2_name  data_type [DEFAULT default_value] [column_constraint],
        ...
        [table_constraint]
    );
    ```

*   **Common Oracle Data Types:**
    *   `VARCHAR2(size)`: Variable-length character string.
    *   `NUMBER(p, s)`: Numeric value (p = precision, s = scale).
    *   `DATE`: Date and time value (century, year, month, day, hour, minute, second).
    *   `TIMESTAMP`: Date and time with fractional seconds.
    *   `CLOB`: Character Large Object (for very large text data).
    *   `BLOB`: Binary Large Object (for binary data like images, videos).
    *   `RAW(size)`: Raw binary data.

*   **Constraints:**
    *   `PRIMARY KEY`: Uniquely identifies each record in a table.
    *   `FOREIGN KEY (column_name) REFERENCES other_table(other_column)`: Ensures referential integrity.
    *   `NOT NULL`: Ensures a column cannot have a `NULL` value.
    *   `UNIQUE`: Ensures all values in a column are different.
    *   `CHECK (condition)`: Ensures all values in a column satisfy a specific condition.
    *   `DEFAULT value`: Specifies a default value for a column when none is provided.

*   **Example: Creating an `Employees` Table**

    ```sql
    -- Input SQL
    CREATE TABLE Departments (
        department_id   NUMBER(4)     PRIMARY KEY,
        department_name VARCHAR2(30)  NOT NULL UNIQUE,
        location        VARCHAR2(20)
    );

    CREATE TABLE Employees (
        employee_id     NUMBER(6)     PRIMARY KEY,
        first_name      VARCHAR2(20)  NOT NULL,
        last_name       VARCHAR2(25)  NOT NULL,
        email           VARCHAR2(100) NOT NULL UNIQUE,
        phone_number    VARCHAR2(20),
        hire_date       DATE          DEFAULT SYSDATE,
        job_id          VARCHAR2(10)  NOT NULL,
        salary          NUMBER(8,2)   CHECK (salary > 0),
        commission_pct  NUMBER(2,2),
        manager_id      NUMBER(6),
        department_id   NUMBER(4),
        CONSTRAINT fk_department
            FOREIGN KEY (department_id)
            REFERENCES Departments(department_id)
    );
    ```

    ```
    -- Output
    Table DEPARTMENTS created.
    Table EMPLOYEES created.
    ```

### 1.2 CREATE INDEX

Used to create an index on a table to speed up data retrieval operations.

*   **Syntax:**

    ```sql
    CREATE [UNIQUE] INDEX index_name
    ON table_name (column1 [, column2, ...]);
    ```

*   **Example: Creating an Index on `Employees` Table**

    ```sql
    -- Input SQL
    CREATE INDEX idx_employees_last_name
    ON Employees (last_name);

    CREATE UNIQUE INDEX uidx_employees_email
    ON Employees (email); -- This is redundant if email is already UNIQUE, but demonstrates syntax.
    ```

    ```
    -- Output
    Index IDX_EMPLOYEES_LAST_NAME created.
    Index UIDX_EMPLOYEES_EMAIL created.
    ```

### 1.3 CREATE VIEW

Used to create a virtual table based on the result-set of a SQL query.

*   **Syntax:**

    ```sql
    CREATE [OR REPLACE] VIEW view_name AS
    SELECT column1, column2, ...
    FROM table_name
    WHERE condition;
    ```

*   **Example: Creating a View for `Active_Employees`**

    ```sql
    -- Input SQL
    CREATE OR REPLACE VIEW Active_Employees_V AS
    SELECT
        e.employee_id,
        e.first_name || ' ' || e.last_name AS full_name,
        e.email,
        e.phone_number,
        e.hire_date,
        e.salary,
        d.department_name
    FROM
        Employees e
    JOIN
        Departments d ON e.department_id = d.department_id
    WHERE
        e.salary > 5000;
    ```

    ```
    -- Output
    View ACTIVE_EMPLOYEES_V created.
    ```

### 1.4 CREATE SEQUENCE

Used to create a sequence, which is a database object that automatically generates unique numbers. Often used for primary key generation.

*   **Syntax:**

    ```sql
    CREATE SEQUENCE sequence_name
        [START WITH initial_value]
        [INCREMENT BY increment_value]
        [MAXVALUE max_value | NOMAXVALUE]
        [MINVALUE min_value | NOMINVALUE]
        [CYCLE | NOCYCLE]
        [CACHE cache_size | NOCACHE]
        [ORDER | NOORDER];
    ```

*   **Example: Creating an `Employee_ID_Seq` Sequence**

    ```sql
    -- Input SQL
    CREATE SEQUENCE employee_id_seq
        START WITH 1000
        INCREMENT BY 1
        MAXVALUE 999999
        NOCYCLE
        CACHE 20;
    ```

    ```
    -- Output
    Sequence EMPLOYEE_ID_SEQ created.
    ```

*   **Using a Sequence:**
    *   `sequence_name.NEXTVAL`: Returns the next available number from the sequence.
    *   `sequence_name.CURRVAL`: Returns the current value of the sequence (only after `NEXTVAL` has been called in the current session).

    ```sql
    -- Input SQL (to show usage)
    SELECT employee_id_seq.NEXTVAL FROM DUAL;
    SELECT employee_id_seq.CURRVAL FROM DUAL;
    ```

    ```
    -- Output (example, numbers will vary)
    1000
    1000
    ```

### 1.5 CREATE USER

Used to create a new database user.

*   **Syntax:**

    ```sql
    CREATE USER username IDENTIFIED BY password
    [DEFAULT TABLESPACE tablespace_name]
    [TEMPORARY TABLESPACE temp_tablespace_name]
    [QUOTA {size_in_k | UNLIMITED} ON tablespace_name]
    [ACCOUNT {LOCK | UNLOCK}]
    [PASSWORD EXPIRE];
    ```

*   **Example: Creating a New User `dev_user`**

    ```sql
    -- Input SQL
    CREATE USER dev_user IDENTIFIED BY DevPass123
    DEFAULT TABLESPACE USERS
    TEMPORARY TABLESPACE TEMP
    QUOTA UNLIMITED ON USERS;
    ```

    ```
    -- Output
    User DEV_USER created.
    ```

### 1.6 CREATE ROLE

Used to create a role, which is a named set of privileges. Roles simplify privilege management.

*   **Syntax:**

    ```sql
    CREATE ROLE role_name [IDENTIFIED BY password | IDENTIFIED EXTERNALLY | IDENTIFIED GLOBALLY];
    ```

*   **Example: Creating a `Developer` Role**

    ```sql
    -- Input SQL
    CREATE ROLE developer;
    ```

    ```
    -- Output
    Role DEVELOPER created.
    ```

### 1.7 CREATE TABLESPACE

Used to create a logical storage unit within the database.

*   **Syntax:**

    ```sql
    CREATE TABLESPACE tablespace_name
    DATAFILE 'path/to/datafile.dbf' SIZE 100M
    [AUTOEXTEND ON NEXT 10M MAXSIZE UNLIMITED]
    [LOGGING | NOLOGGING]
    [EXTENT MANAGEMENT LOCAL | DICTIONARY]
    [SEGMENT SPACE MANAGEMENT AUTO | MANUAL];
    ```

*   **Example: Creating a `Dev_Data` Tablespace**

    ```sql
    -- Input SQL (path needs to be valid on your system)
    CREATE TABLESPACE dev_data
    DATAFILE 'C:\app\oracle\oradata\ORCL\dev_data01.dbf' SIZE 100M
    AUTOEXTEND ON NEXT 10M MAXSIZE UNLIMITED
    LOGGING
    EXTENT MANAGEMENT LOCAL
    SEGMENT SPACE MANAGEMENT AUTO;
    ```

    ```
    -- Output
    Tablespace DEV_DATA created.
    ```

### 1.8 CREATE SYNONYM

Used to create an alias for a database object (like a table, view, or sequence).

*   **Syntax:**

    ```sql
    CREATE [PUBLIC] SYNONYM synonym_name FOR object_name;
    ```

*   **Example: Creating a Synonym for the `Employees` Table**

    ```sql
    -- Input SQL
    CREATE SYNONYM emp FOR Employees;
    ```

    ```
    -- Output
    Synonym EMP created.
    ```

---

## 2. ALTER Command

The `ALTER` command is used to modify the structure of an existing database object.

### 2.1 ALTER TABLE

Used to modify the structure of an existing table.

*   **Adding a Column:**

    ```sql
    -- Input SQL
    ALTER TABLE Employees
    ADD (job_title VARCHAR2(30) DEFAULT 'Software Engineer');
    ```

    ```
    -- Output
    Table EMPLOYEES altered.
    ```

*   **Modifying a Column:** (Be careful with data loss or type incompatibility)

    ```sql
    -- Input SQL
    ALTER TABLE Employees
    MODIFY (phone_number VARCHAR2(30) NULL); -- Change size and allow NULLs
    ```

    ```
    -- Output
    Table EMPLOYEES altered.
    ```

*   **Dropping a Column:**

    ```sql
    -- Input SQL
    ALTER TABLE Employees
    DROP COLUMN job_title;
    ```

    ```
    -- Output
    Table EMPLOYEES altered.
    ```

*   **Adding a Constraint:**

    ```sql
    -- Input SQL
    ALTER TABLE Employees
    ADD CONSTRAINT uk_employee_phone UNIQUE (phone_number);
    ```

    ```
    -- Output
    Table EMPLOYEES altered.
    ```

*   **Dropping a Constraint:**

    ```sql
    -- Input SQL
    ALTER TABLE Employees
    DROP CONSTRAINT uk_employee_phone;
    ```

    ```
    -- Output
    Table EMPLOYEES altered.
    ```

*   **Renaming a Table:** (Alternatively, use the `RENAME` command, see section 5)

    ```sql
    -- Input SQL
    ALTER TABLE Employees
    RENAME TO Staff;
    ```

    ```
    -- Output
    Table EMPLOYEES altered.
    ```

    (To continue examples, we'll assume the table is renamed back to `Employees` or adjust accordingly.)
    ```sql
    ALTER TABLE Staff RENAME TO Employees;
    ```

### 2.2 ALTER INDEX

Used to rebuild or modify properties of an index.

*   **Rebuilding an Index:** (Often done to improve performance or reclaim space)

    ```sql
    -- Input SQL
    ALTER INDEX idx_employees_last_name REBUILD;
    ```

    ```
    -- Output
    Index IDX_EMPLOYEES_LAST_NAME altered.
    ```

### 2.3 ALTER SEQUENCE

Used to modify the properties of an existing sequence.

*   **Example: Changing `INCREMENT BY` for `Employee_ID_Seq`**

    ```sql
    -- Input SQL
    ALTER SEQUENCE employee_id_seq
    INCREMENT BY 10
    MAXVALUE 9999999;
    ```

    ```
    -- Output
    Sequence EMPLOYEE_ID_SEQ altered.
    ```

### 2.4 ALTER USER

Used to modify user properties like password, default tablespace, or quota.

*   **Example: Changing user password and quota**

    ```sql
    -- Input SQL
    ALTER USER dev_user IDENTIFIED BY NewDevPass456
    QUOTA 50M ON USERS;
    ```

    ```
    -- Output
    User DEV_USER altered.
    ```

### 2.5 ALTER TABLESPACE

Used to modify tablespace properties, such as adding datafiles or changing autoextend settings.

*   **Example: Adding a datafile to `Dev_Data` Tablespace**

    ```sql
    -- Input SQL (path needs to be valid on your system)
    ALTER TABLESPACE dev_data
    ADD DATAFILE 'C:\app\oracle\oradata\ORCL\dev_data02.dbf' SIZE 50M
    AUTOEXTEND ON NEXT 5M MAXSIZE 500M;
    ```

    ```
    -- Output
    Tablespace DEV_DATA altered.
    ```

---

## 3. DROP Command

The `DROP` command is used to remove an object from the database.

### 3.1 DROP TABLE

Used to delete an existing table from the database.

*   **Syntax:**

    ```sql
    DROP TABLE table_name [CASCADE CONSTRAINTS] [PURGE];
    ```
    *   `CASCADE CONSTRAINTS`: Automatically drops all referential integrity constraints that refer to primary and unique keys in the table being dropped.
    *   `PURGE`: Skips the Recycle Bin and permanently drops the table immediately.

*   **Example: Dropping `Employees` Table**

    ```sql
    -- Input SQL (This will fail if Employees table has data and is referenced by other tables)
    -- DROP TABLE Employees;

    -- To drop both tables cleanly, start with the child table (Employees) or use CASCADE CONSTRAINTS
    DROP TABLE Employees CASCADE CONSTRAINTS;
    DROP TABLE Departments;
    ```

    ```
    -- Output
    Table EMPLOYEES dropped.
    Table DEPARTMENTS dropped.
    ```

### 3.2 DROP INDEX

Used to delete an index from the database.

*   **Example: Dropping `idx_employees_last_name` Index**

    ```sql
    -- Input SQL (Recreate table and index for demonstration if needed)
    -- CREATE TABLE Employees (employee_id NUMBER PRIMARY KEY, last_name VARCHAR2(50));
    -- CREATE INDEX idx_employees_last_name ON Employees (last_name);
    DROP INDEX idx_employees_last_name;
    ```

    ```
    -- Output
    Index IDX_EMPLOYEES_LAST_NAME dropped.
    ```

### 3.3 DROP VIEW

Used to delete a view from the database.

*   **Example: Dropping `Active_Employees_V` View**

    ```sql
    -- Input SQL
    DROP VIEW Active_Employees_V;
    ```

    ```
    -- Output
    View ACTIVE_EMPLOYEES_V dropped.
    ```

### 3.4 DROP SEQUENCE

Used to delete a sequence from the database.

*   **Example: Dropping `Employee_ID_Seq` Sequence**

    ```sql
    -- Input SQL
    DROP SEQUENCE employee_id_seq;
    ```

    ```
    -- Output
    Sequence EMPLOYEE_ID_SEQ dropped.
    ```

### 3.5 DROP USER

Used to delete a database user.

*   **Syntax:**

    ```sql
    DROP USER username [CASCADE];
    ```
    *   `CASCADE`: Drops all schema objects (tables, views, etc.) owned by the user before dropping the user.

*   **Example: Dropping `dev_user`**

    ```sql
    -- Input SQL
    DROP USER dev_user;
    ```

    ```
    -- Output
    User DEV_USER dropped.
    ```

### 3.6 DROP ROLE

Used to delete a role from the database.

*   **Example: Dropping `developer` Role**

    ```sql
    -- Input SQL
    DROP ROLE developer;
    ```

    ```
    -- Output
    Role DEVELOPER dropped.
    ```

### 3.7 DROP TABLESPACE

Used to delete a tablespace.

*   **Syntax:**

    ```sql
    DROP TABLESPACE tablespace_name [INCLUDING CONTENTS [AND DATAFILES] [CASCADE CONSTRAINTS]];
    ```

*   **Example: Dropping `Dev_Data` Tablespace**

    ```sql
    -- Input SQL
    DROP TABLESPACE dev_data INCLUDING CONTENTS AND DATAFILES;
    ```

    ```
    -- Output
    Tablespace DEV_DATA dropped.
    ```

### 3.8 DROP SYNONYM

Used to delete a synonym.

*   **Example: Dropping `emp` Synonym**

    ```sql
    -- Input SQL
    DROP SYNONYM emp;
    ```

    ```
    -- Output
    Synonym EMP dropped.
    ```

---

## 4. TRUNCATE Command

The `TRUNCATE` command is used to remove all rows from a table, but it's classified as DDL because it's fast, non-rollbackable, and deallocates the space used by the table.

*   **Syntax:**

    ```sql
    TRUNCATE TABLE table_name [REUSE STORAGE];
    ```
    *   `REUSE STORAGE`: Retains the storage allocated for the removed rows.

*   **Difference from `DELETE`:**
    *   `TRUNCATE` is much faster for large tables as it deallocates the data pages and logs only the deallocation.
    *   `TRUNCATE` operations cannot be rolled back.
    *   `TRUNCATE` operations do not fire DML triggers.
    *   `TRUNCATE` resets the high-water mark of the table.

*   **Example: Truncating `Departments` Table**

    ```sql
    -- Input SQL (Recreate table and insert some data for demonstration)
    CREATE TABLE Departments (
        department_id   NUMBER(4)     PRIMARY KEY,
        department_name VARCHAR2(30)  NOT NULL UNIQUE,
        location        VARCHAR2(20)
    );
    INSERT INTO Departments VALUES (10, 'IT', 'New York');
    INSERT INTO Departments VALUES (20, 'HR', 'London');
    COMMIT;

    TRUNCATE TABLE Departments;
    ```

    ```
    -- Output
    Table DEPARTMENTS truncated.
    ```

---

## 5. RENAME Command

The `RENAME` command is used to change the name of a table, index, sequence, or view. For columns, `ALTER TABLE ... RENAME COLUMN` is used.

*   **Syntax:**

    ```sql
    RENAME old_object_name TO new_object_name;
    ```

*   **Example: Renaming a Table**

    ```sql
    -- Input SQL (Recreate table for demonstration)
    CREATE TABLE OldTableName (id NUMBER);

    RENAME OldTableName TO NewTableName;
    ```

    ```
    -- Output
    Table OLDTABLENAME renamed.
    ```

*   **Example: Renaming a Column (using `ALTER TABLE`)**

    ```sql
    -- Input SQL
    ALTER TABLE NewTableName
    RENAME COLUMN id TO new_id;
    ```

    ```
    -- Output
    Table NEWTABLENAME altered.
    ```

---

## 6. COMMENT ON Command

The `COMMENT ON` command is used to add comments to tables or columns, which helps in documenting the database schema. These comments are stored in data dictionary views (e.g., `ALL_TAB_COMMENTS`, `ALL_COL_COMMENTS`).

*   **Syntax:**

    ```sql
    COMMENT ON TABLE table_name IS 'Your table comment here';
    COMMENT ON COLUMN table_name.column_name IS 'Your column comment here';
    ```

*   **Example: Adding Comments to `Departments` Table and `department_name` Column**

    ```sql
    -- Input SQL (Recreate table for demonstration)
    CREATE TABLE Departments (
        department_id   NUMBER(4)     PRIMARY KEY,
        department_name VARCHAR2(30)  NOT NULL UNIQUE,
        location        VARCHAR2(20)
    );

    COMMENT ON TABLE Departments IS 'Stores information about company departments.';
    COMMENT ON COLUMN Departments.department_name IS 'The official name of the department.';
    ```

    ```
    -- Output
    Comment created.
    Comment created.
    ```

---

This comprehensive guide covers the most frequently used DDL commands in Oracle SQL, providing the necessary details and examples for understanding and applying them effectively.