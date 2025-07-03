import requests
import time
from datetime import datetime

PROMETHEUS_URL = "http://localhost:9090"

# PromQL queries to monitor
QUERIES = {
    "scrape_duration": 'max_over_time(scrape_duration_seconds{job="synthetic_exporter"}[1m])',
    "sample_ingestion_rate": 'rate(prometheus_tsdb_head_samples_appended_total[1m])',
    "total_series": 'prometheus_tsdb_head_series',
    "up_status": 'up{job="synthetic_exporter"}'
}

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

def log_metrics():
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nâ±ï¸  {timestamp} - Benchmark Report")
        for name, promql in QUERIES.items():
            value = query_prometheus(promql)
            if value is not None:
                print(f"{name:25}: {value}")
            else:
                print(f"{name:25}: No data or error")
        time.sleep(10)  # Wait 10 seconds before next query

if __name__ == "__main__":
    print("ðŸ“Š Starting Prometheus benchmark logger...")
    log_metrics()
