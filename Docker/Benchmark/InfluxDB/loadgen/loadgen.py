import requests
import time
import random

INFLUXDB_WRITE_URL = "http://influxdb:8086/write?db=benchmark"
INFLUXDB_QUERY_URL = "http://influxdb:8086/query"

def create_database():
    try:
        resp = requests.post(INFLUXDB_QUERY_URL, params={"q": "CREATE DATABASE benchmark"})
        if resp.status_code == 200:
            print("Database 'benchmark' created or already exists.")
        else:
            print("Failed to create database:", resp.status_code, resp.text)
    except Exception as e:
        print("Error creating DB:", e)

def push_metrics():
    while True:
        lines = []
        timestamp = int(time.time() * 1e9)  # nanoseconds
        for i in range(1000):
            region = f"region_{random.randint(0, 1)}"
            instance = f"inst_{random.randint(0, 4)}"
            job = f"job_0"
            metric_id = f"id_{i}"
            value = random.random()
            line = f'custom_metric,region={region},instance={instance},job={job},metric_id={metric_id} value={value} {timestamp}'
            lines.append(line)

        try:
            resp = requests.post(INFLUXDB_WRITE_URL, data="\n".join(lines))
            if resp.status_code == 204:
                print(f" Wrote 1000 metrics at {time.strftime('%H:%M:%S')}")
            else:
                print(f"Failed to write metrics: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"Exception while pushing metrics: {e}")

        time.sleep(2)

if __name__ == "__main__":
    print("Starting load generator for InfluxDB...")
    create_database()
    time.sleep(2)
    push_metrics() 

    
# import subprocess
# import re
# import time
# import requests

# INFLUXDB_URL = "http://influxdb:8086/write?db=benchmark"
# INFLUXDB_QUERY_URL = "http://influxdb:8086/query"

# def create_database():
#     try:
#         resp = requests.post(INFLUXDB_QUERY_URL, params={"q": "CREATE DATABASE benchmark"})
#         if resp.status_code == 200:
#             print("Database 'benchmark' created or already exists.")
#         else:
#             print("Failed to create database:", resp.status_code, resp.text)
#     except Exception as e:
#         print("Error creating DB:", e)

# def parse_ovs_interfaces():
#     result = subprocess.run(["ovs-vsctl", "list", "interface"], capture_output=True, text=True)
#     lines = result.stdout.strip().split("\n")

#     metrics = []
#     current = {}
#     for line in lines:
#         line = line.strip()
#         if not line:
#             continue
#         if line.startswith("_uuid"):
#             if current:
#                 metrics.append(current)
#             current = {}
#         elif ':' in line:
#             key, value = line.split(":", 1)
#             current[key.strip()] = value.strip()
#     if current:
#         metrics.append(current)
#     return metrics

# def extract_stat_fields(stat_string):
#     stats = {}
#     stat_string = stat_string.strip("{}")
#     for pair in stat_string.split(","):
#         if "=" in pair:
#             k, v = pair.split("=")
#             stats[k.strip()] = int(v.strip())
#     return stats

# def push_to_influx(metrics):
#     timestamp = int(time.time() * 1e9)
#     lines = []

#     for m in metrics:
#         name = m.get("name", "unknown").strip('"')
#         stats_str = m.get("statistics", "{}")
#         stats = extract_stat_fields(stats_str)

#         for stat_key, stat_val in stats.items():
#             line = f"ovsdb_stats,interface={name},stat={stat_key} value={stat_val} {timestamp}"
#             lines.append(line)

#     try:
#         resp = requests.post(INFLUXDB_URL, data="\n".join(lines))
#         if resp.status_code == 204:
#             print(f"Wrote {len(lines)} metrics at {time.strftime('%H:%M:%S')}")
#         else:
#             print(f"Failed to write metrics: {resp.status_code}, {resp.text}")
#     except Exception as e:
#         print(f"Error sending to InfluxDB: {e}")

# if __name__ == "__main__":
#     create_database()
#     while True:
#         try:
#             ovs_metrics = parse_ovs_interfaces()
#             push_to_influx(ovs_metrics)
#         except Exception as e:
#             print(f"Loop error: {e}")
#         time.sleep(5)


