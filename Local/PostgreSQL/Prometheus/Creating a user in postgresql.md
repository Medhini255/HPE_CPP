# Steps to Create a User in PostgreSQL

---

## Step 1: Open PostgreSQL Shell

Run the following command to access the PostgreSQL shell as the `postgres` user:

```bash
sudo -u postgres psql
```

---

## Step 2: Create a New User

Inside the PostgreSQL shell, run:

```sql
CREATE USER <userName> WITH PASSWORD '<yourPasswordforUser>';
```

Replace `<userName>` and `<yourPasswordforUser>` with your desired username and password.

---

## Step 3: Grant Connection Privileges

Allow the user to connect to a specific database:

```sql
GRANT CONNECT ON DATABASE <your_db_name> TO <yourUsername>;
```

---

## Step 4: Switch to the Desired Database

Change to the database you created or want to work on:

```sql
\c your_db_name
```

---

## Step 5: Grant Required Permissions

Execute the following commands **in sequence**:

```sql
GRANT USAGE ON SCHEMA public TO <yourUsername>;
GRANT SELECT ON pg_stat_database TO <yourUsername>;
GRANT SELECT ON pg_stat_user_tables TO <yourUsername>;
GRANT SELECT ON pg_stat_activity TO <yourUsername>;
GRANT SELECT ON pg_stat_bgwriter TO <yourUsername>;
```

Replace `<yourUsername>` with the username you created earlier.
