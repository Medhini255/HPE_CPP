# Benchmarking Influxdb Remotely using Docker

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

### Step 6: Check if Influxdb is running

Go to:

```
http://localhost:8086/metrics
```
---

### Step 7: Checking the database creation and data inserted

```bash
docker exec -it <influxdb-container-name> influx
```

```sql
show databases;
use benchmark;
show measurements;
select * from custom_metric;
```

---

### Step 8: Visualize in grafana

Save the data source as influx with the following url-

```
http://<influx-container-name>:8086
```
Create dashboard with the following metric to see the graph

```
custom_metric
```
