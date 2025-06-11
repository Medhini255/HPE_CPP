
# PostgreSQL Benchmarking Guide

This guide explains how to run the PostgreSQL CRUD benchmarking script and describes the output generated.

---

##  Steps to Run

### **Step 1: Ensure PostgreSQL is Running**

Start PostgreSQL service if not already running:

```bash
sudo systemctl start postgresql
````

Verify the status:

```bash
sudo systemctl status postgresql
```

---

### **Step 2: Run the Benchmarking Script**

Execute the Python benchmarking script:

```bash
sudo python3 postgres_benchmark.py
```

This script will:

* Connect to a PostgreSQL database
* Run `CREATE`, `READ`, `UPDATE`, and `DELETE` operations
* Record latency, throughput, and CPU time for each operation

---

##  Database Configuration

Make sure the following database settings match your local setup in the script:

```python
DB_PARAMS = {
    "dbname": "benchmarkdb",
    "user": "benchmarkuser",
    "password": "benchmarkpass",
    "host": "localhost",
    "port": 5432
}
```

Create the user and database if not already present:

```bash
sudo -u postgres psql
CREATE USER benchmarkuser WITH PASSWORD 'benchmarkpass';
CREATE DATABASE benchmarkdb OWNER benchmarkuser;
\q
```

---

##  Output Files

###  CSV Outputs:

* `postgres_crud_latency_<timestamp>.csv`: Latency (in ms) per operation
* `postgres_summary_<timestamp>.csv`: Summary of average latency, throughput, and CPU time

###  Graph Outputs:

* `postgres_latency_lineplot.png`: Line plot showing latency per CRUD operation over time
* `postgres_latency_boxplot.png`: Boxplot comparing latency distributions
* `postgres_throughput.png`: Bar chart showing operations per second
* `postgres_cpu_time.png`: CPU time bar chart for each operation

---

##  Output Location

All results are saved in the current working directory.

---

##  Notes

* `NUM_OPS = 100` can be changed to scale the test.
* Make sure the benchmark table `benchmark_table` exists; the script auto-creates it.
* You can run multiple iterations to compare performance under different loads or schema configurations.

---
