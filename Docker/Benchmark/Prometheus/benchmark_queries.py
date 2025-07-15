import requests
import time
from datetime import datetime

PROMETHEUS_URL = "http://localhost:9090"

# PromQL queries to monitor
QUERIES = {
    "scrape_duration": 'max_over_time(scrape_duration_seconds{job="loadgen"}[1m])',
    "up_status": 'up{job="loadgen"}'
}

# For benchmarking latency
BENCHMARK_QUERY = "rate(simulated_metric[1m])"  
NUM_BENCHMARK_QUERIES = 10 

def query_prometheus(query):
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": query})
        response.raise_for_status()
        data = response.json()["data"]["result"]
        if data:
            return float(data[0]["value"][1])
        else:
            return None
    except Exception as e:
        print(f"Error querying Prometheus: {e}")
        return None

def benchmark_latency():
    durations = []
    for _ in range(NUM_BENCHMARK_QUERIES):
        start = time.perf_counter()
        resp = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": BENCHMARK_QUERY})
        end = time.perf_counter()

        if resp.status_code == 200:
            durations.append(end - start)
        else:
            print(f"Query failed: {resp.text}")
    if durations:
        avg = sum(durations) / len(durations)
        return avg * 1000  # in milliseconds
    else:
        return None

def log_metrics():
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n  {timestamp} - Benchmark Report")
        
        # Log key Prometheus metrics
        for name, promql in QUERIES.items():
            value = query_prometheus(promql)
            if value is not None:
                print(f"{name:25}: {value}")
            else:
                print(f"{name:25}: No data or error")

        # Log average query latency
        avg_latency = benchmark_latency()
        if avg_latency is not None:
            print(f"{'query_latency_avg (ms)':25}: {avg_latency:.2f}")
        else:
            print(f"{'query_latency_avg (ms)':25}: Error or no data")

        time.sleep(10)

if __name__ == "__main__":
    print(" Starting Prometheus benchmark logger with latency measurement...")
    log_metrics()
