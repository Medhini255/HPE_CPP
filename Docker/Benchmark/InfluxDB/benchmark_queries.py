import requests
import time
from datetime import datetime

INFLUXDB_URL = "http://localhost:8086/query"
DB = "benchmark"
NUM_QUERIES = 100
SLEEP_INTERVAL = 10  # seconds

# Reuse a single HTTP session for better performance
session = requests.Session()

# Sample InfluxQL queries
QUERIES = {
    "latest_point": f"SELECT last(value) FROM custom_metric",
    "avg_over_time": f"SELECT mean(value) FROM custom_metric WHERE time > now() - 1m GROUP BY time(10s)",
    "series_count": f"SHOW SERIES"
}
# Sample InfluxQL queries for OVSDB metrics
"""QUERIES = {
    "latest_point": f"SELECT last(value) FROM ovsdb_stats",
    "avg_over_time": f"SELECT mean(value) FROM ovsdb_stats WHERE time > now() - 1m GROUP BY time(10s)",
    "series_count": f"SHOW SERIES FROM ovsdb_stats"
}"""


def query_influxdb(query):
    try:
        response = session.get(INFLUXDB_URL, params={"db": DB, "q": query})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Query error: {e}")
        return None

def benchmark_latency():
    durations = []
    for _ in range(NUM_QUERIES):
        start = time.perf_counter()
        resp = query_influxdb(QUERIES["avg_over_time"])
        end = time.perf_counter()

        if resp and "results" in resp:
            durations.append(end - start)
        else:
            print("Query returned no result")
    if durations:
        avg_ms = sum(durations) / len(durations)*1000
        return avg_ms
    return None

def log_metrics():
    while True:
        print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Benchmark Report")

        for name, query in QUERIES.items():
            result = query_influxdb(query)
            if result and "results" in result and "series" in result["results"][0]:
                series = result["results"][0]["series"]
                if name == "series_count":
                    total_series = sum(len(s["values"]) for s in series)
                    print(f"{name:20}: {total_series} series")
                else:
                    for s in series:
                        for val in s.get("values", []):
                            print(f"{name:20}: {val}")
                            break  # Print just one value
            else:
                print(f"{name:20}: No data or error")

        avg_latency = benchmark_latency()
        if avg_latency is not None:
            print(f"{'query_latency_avg (ms)':20}: {avg_latency:.2f}")
        else:
            print(f"{'query_latency_avg (ms)':20}: Error or no data")

        time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    print("Starting InfluxDB benchmark logger...")
    log_metrics()

