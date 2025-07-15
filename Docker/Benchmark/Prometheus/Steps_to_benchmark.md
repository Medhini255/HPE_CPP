# Benchmarking Prometheus Remotely using Docker

## Step-by-Step Instructions

### Step 1: Switch to the directory containing benchmark files

```bash
cd path/to/your/benchmark-directory
```
---

### Step 2: Build the Docker Compose setup

Use the appropriate command based on your Docker version:

    For Docker Compose v1.x (standalone):
    
```bash
docker-compose build
```

    For Docker Compose v2.x+ (integrated with Docker CLI):
    
```bash
docker compose build
```
---

### Step 3: Start all containers

    For Docker Compose v1:
    
```bash
docker-compose up
```

    For Docker Compose v2:
    
```bash
docker compose up
```
---

### Step 4: Open a new terminal and switch to the benchmark directory

```bash
cd path/to/your/benchmark-directory
```
---

### Step 5: Run the benchmarking Python script

```bash
python3 benchmark_queries.py
```
---

### Step 6: Open the Prometheus Web UI

Go to:

```
http://localhost:9090/
```
---

### Step 7: Visualize the query graph

Paste the following query into the Prometheus UI query bar:

```sql
max_over_time(scrape_duration_seconds{job="loadgen"}[1m])
```

You should now see graph changes representing scrape duration over time, reflecting your benchmarking activity.
