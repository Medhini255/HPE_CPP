# Benchmarking Victoria Metrics Remotely using Docker

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
python3 benchmark_query.py
```
---

### Step 6: Open the Victoria Metrics Web UI 
Go to:

```
http://localhost:8428/ui
```
---

### Step 7: Visualize the query graph

Paste the following query into the Victoria metrics UI query bar:

```sql
benchmark_metric_value
```
---

### Step-8: Adding Dashboard in Grafana
- Go to:

 ```
 http://localhost:3000/
 ```
- Add datasource Prometheus
- Enter URL

  ```
  http://victoria-metrics:8428
  ```
- Build Dashboard
- Put the following metric
  
  ```sql
  benchmark_metric_value
  ```
- Save the dashboard
