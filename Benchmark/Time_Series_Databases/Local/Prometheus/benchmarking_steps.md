# Benchmarking Prometheus Scrape Performance

## Step 1: Define What You Want to Benchmark in Prometheus

To design a useful benchmark, we need to clearly define your goals.

- Scrape performance (e.g., how many metrics Prometheus can scrape per second)
- Query performance (e.g., how fast it responds to queries via `/api/v1/query`)
- Rule evaluation speed (e.g., how fast it can run alerting/recording rules)
- Remote write throughput (e.g., Prometheus sending to InfluxDB, VictoriaMetrics, etc.)
- Storage performance (e.g., how it handles high-cardinality data over time)

---

## Step 2: Set Up a Local Prometheus Instance

To measure **scrape performance**, we need a running Prometheus that scrapes from a **synthetic target (exporter)**. For now, just install Prometheus locally:

- Download the latest Prometheus binary from the [official site](https://prometheus.io/download/)
- Extract and run Prometheus using the sample config

```bash
./prometheus --config.file=prometheus.yml
```
---

## Step 3: Set Up a Synthetic Exporter to Simulate High Metric Load

To test scrape performance, we need an exporter that:

Exposes a large number of custom metrics (e.g., 10,000+)

Is scrape-compatible with Prometheus (/metrics endpoint)

Runs locally for easy testing
# Instructions
a. Install Prometheus client library:
```bash
pip install prometheus_client
```
b. Create a Python file (load_exporter.py)
c. Run the exporter script:
```bash
python load_exporter.py
```
You should see output confirming it's running.

d. Verify the exporter:
Visit: http://localhost:8000/metrics

---

## Step 4: Configure Prometheus to Scrape the Exporter
Now we tell Prometheus to scrape metrics from your synthetic exporter at http://localhost:8000/metrics.

# Instructions:
Open the prometheus.yml config file (in your Prometheus folder).

Under the scrape_configs: section, add a new job like this:

```yaml

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'synthetic_exporter'
    static_configs:
      - targets: ['localhost:8000']
```

Save the file and restart Prometheus:

```bash
./prometheus --config.file=prometheus.yml
```
Go to http://localhost:9090/targets and confirm:

You see a job called synthetic_exporter

The target localhost:8000 is in the "UP" state

---

## Step 5: Measure Scrape Performance Using Prometheus Metrics
Now that Prometheus is scraping 10,000+ metrics, we’ll query internal Prometheus metrics to evaluate its scrape performance.

Go to http://localhost:9090 and run the following queries in the Prometheus "Graph" tab:

# Queries to Measure Scrape Load
Scrape duration for your exporter:

```promql

scrape_duration_seconds{job="synthetic_exporter"}
```
Scrape samples ingested per second:

```promql

rate(prometheus_scrape_sample_ingestion_rate[1m])
```
Scrape failures (if any):

```promql

scrape_samples_scraped{job="synthetic_exporter"}
```
---

## Step 6: Stress Test by Increasing Metric Cardinality

We'll modify the exporter to:

a) Add label dimensions to metrics-1000 metrics × 10 unique label combinations = 10,000 time series

b) Simulate many unique series, not just metric names

c) Restart the exporter: python load_exporter.py

d) Wait 30 seconds.

e) Go to http://localhost:9090 and re-run the same queries from Step 5.

---

## Step 7: Observe Performance Trends Over Time
Recording how Prometheus behaves under this load using its own metrics — this will help us understand long-term behavior like:

- CPU/memory bottlenecks

- Increased scrape duration

- Dropped targets

- Ingestion lag

Using built-in Prometheus UI-

# Key Metrics to Query Over Time (on http://localhost:9090/graph):
Scrape duration (check if it’s nearing 15s interval):

```promql

max_over_time(scrape_duration_seconds{job="synthetic_exporter"}[5m])
```
Sample ingestion rate (global):

```promql

rate(prometheus_tsdb_head_samples_appended_total[1m])
```
Total time series count:

```promql

prometheus_tsdb_head_series
```
Scrape errors (should be 0 ideally):

```promql

increase(scrape_samples_scraped{job="synthetic_exporter"}[5m])
```
Target scrape health:

```promql

up{job="synthetic_exporter"}
```

---

## Step 8: Automate Benchmarking and Logging with Python
Python script for-
- Periodically querying Prometheus for performance metrics

- Logging them to the console or a file

- Extending later to visualize or analyze trends

# Step 8A: Install Required Python Library

Command to Install:
```bash
pip install requests
```
# Step 8B: Python Script to Log Prometheus Benchmark Metrics
This script will:

- Send PromQL queries to Prometheus

- Log key performance metrics every 10 seconds
  
Tasks-
i) Save this as prometheus_benchmark_logger.py
ii) Run it:
```bash
    
    python3 prometheus_benchmark_logger.py
```
iii) Watch the output
