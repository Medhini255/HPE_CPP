# Steps to Create a Database and Table in PostgreSQL

---

## Step 1: Open PostgreSQL Shell

Run the following command:

```bash
sudo -u postgres psql
```

---

## Step 2: Create a New Database

Create a database by running:

```sql
CREATE DATABASE my_database;
```
>  Replace `my_database` with your desired database name.

---

## Step 3: Verify Database Creation

List all databases to check if your database was created:

```sql
\l
```

---

## Step 4: Switch to the Newly Created Database

Connect to your database:

```sql
\c my_database
```
> Replace `my_database` with the name of your database if different.

---

## Step 5: Create a Table

Create a sample table inside your database:

```sql
CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    metric_name TEXT NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
>  You can modify the table schema according to your needs.

---

## Step 6: Insert a Sample Record

Insert a sample value into the table:

```sql
INSERT INTO metrics (metric_name, value) VALUES ('cpu_usage', 75.5);
```

---

## Step 7: Done!
