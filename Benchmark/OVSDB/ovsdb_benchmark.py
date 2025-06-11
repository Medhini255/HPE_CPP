import subprocess
import time
import csv
import json
import psutil
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime

SOCKET = "unix:/var/run/openvswitch/db.sock"
TABLE = "Bridge"
NUM_OPS = 100
results = []
summary_stats = []

def get_ovsdb_pid():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'ovsdb-server' in proc.info['name'] or \
           any('ovsdb-server' in part for part in (proc.info['cmdline'] or [])):
            return proc.info['pid']
    return None

def run_ovsdb_command(json_cmd):
    cmd = ["ovsdb-client", "transact", SOCKET, json_cmd]
    start = time.time()
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.time()
    return round((end - start) * 1000, 3)  # in ms

def get_first_uuid():
    cmd = ["ovs-vsctl", "--format=json", "list", TABLE]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(result.stdout)
        return data["data"][0][0]
    except Exception:
        return None

def benchmark_op(operation, build_cmd_fn):
    print(f"â–¶ {operation} benchmark...")
    latencies = []
    start_batch = time.time()
    pid = get_ovsdb_pid()
    ovs_proc = psutil.Process(pid)

    ovs_proc.cpu_percent(interval=1.0)  # Warm-up

    for i in range(NUM_OPS):
        json_cmd = build_cmd_fn(i)
        latency = run_ovsdb_command(json_cmd)
        latencies.append(latency)
        results.append([operation, latency])

    cpu_times = ovs_proc.cpu_times()
    cpu_user_time = cpu_times.user
    cpu_system_time = cpu_times.system
    cpu_total_time = cpu_user_time + cpu_system_time
    cpu_after = round(cpu_total_time, 3)

    print(f"ðŸ§  CPU time used: {cpu_after:.3f}s (User: {cpu_user_time:.3f}s, System: {cpu_system_time:.3f}s)")

    end_batch = time.time()
    total_time = end_batch - start_batch
    throughput = round(NUM_OPS / total_time, 2)
    avg_latency = round(sum(latencies) / NUM_OPS, 3)

    print(f"âœ… {operation}: Avg Latency = {avg_latency} ms | Throughput = {throughput} ops/sec | CPU Time = {cpu_after}s")
    summary_stats.append({
        "operation": operation,
        "avg_latency": avg_latency,
        "throughput": throughput,
        "cpu_time": cpu_after
    })

def build_create_cmd(i):
    row = '{"name": "br-bench-%d"}' % i
    return f'["Open_vSwitch", {{"op": "insert", "table": "{TABLE}", "row": {row}}}]'

def build_read_cmd(i):
    return f'["Open_vSwitch", {{"op": "select", "table": "{TABLE}", "where": []}}]'

def build_update_cmd(i):
    uuid = get_first_uuid()
    if not uuid:
        return None
    return f'''["Open_vSwitch", {{
        "op": "update",
        "table": "{TABLE}",
        "where": [["_uuid", "==", ["uuid", "{uuid}"]]],
        "row": {{"external_ids": ["map", [["k{i}", "v{i}"]]]}}
    }}]'''

def build_delete_cmd(i):
    uuid = get_first_uuid()
    if not uuid:
        return None
    return f'''["Open_vSwitch", {{
        "op": "delete",
        "table": "{TABLE}",
        "where": [["_uuid", "==", ["uuid", "{uuid}"]]]
    }}]'''

def run_all():
    benchmark_op("CREATE", build_create_cmd)
    benchmark_op("READ", build_read_cmd)
    benchmark_op("UPDATE", build_update_cmd)
    benchmark_op("DELETE", build_delete_cmd)
    print("SUMMARY DEBUG:", summary_stats)

def save_latency_csv():
    filename = f"ovsdb_crud_latency_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Operation", "Latency_ms"])
        writer.writerows(results)
    print(f"ðŸ“ Latency log saved to {filename}")

def save_summary_csv():
    filename = f"ovsdb_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["operation", "avg_latency", "throughput", "cpu_time"])
        writer.writeheader()
        writer.writerows(summary_stats)
    print(f"ðŸ“ Summary saved to {filename}")

# def plot_latency():
#     df = pd.DataFrame(results, columns=["Operation", "Latency_ms"])
#     plt.figure(figsize=(10, 6))
#     for op in df["Operation"].unique():
#         df_op = df[df["Operation"] == op]
#         plt.hist(df_op["Latency_ms"], bins=20, alpha=0.6, label=op)
#     plt.title("OVSDB CRUD Operation Latency")
#     plt.xlabel("Latency (ms)")
#     plt.ylabel("Frequency")
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()
#     plt.savefig("ovsdb_crud_latency_histogram.png")
#     plt.show()

#     plt.figure(figsize=(8, 6))
#     df.boxplot(column="Latency_ms", by="Operation", grid=True)
#     plt.title("Latency Distribution per Operation")
#     plt.suptitle("")
#     plt.ylabel("Latency (ms)")
#     plt.savefig("ovsdb_crud_latency_boxplot.png")
#     plt.show()
def plot_latency():
    df = pd.DataFrame(results, columns=["Operation", "Latency_ms"])
    plt.figure(figsize=(10, 6))

    for op in df["Operation"].unique():
        df_op = df[df["Operation"] == op].reset_index(drop=True)
        plt.plot(df_op.index, df_op["Latency_ms"], label=op)

    plt.title("OVSDB Latency over Operations")
    plt.xlabel("Operation Index")
    plt.ylabel("Latency (ms)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("ovsdb_crud_latency_lineplot.png")
    plt.show()

    # Optional: keep boxplot too if you want both
    plt.figure(figsize=(8, 6))
    df.boxplot(column="Latency_ms", by="Operation", grid=True)
    plt.title("Latency Distribution per Operation")
    plt.suptitle("")
    plt.ylabel("Latency (ms)")
    plt.savefig("ovsdb_crud_latency_boxplot.png")
    plt.show()


def plot_summary_graphs():
    df = pd.DataFrame(summary_stats)

    plt.figure(figsize=(8, 5))
    plt.bar(df["operation"], df["throughput"], color="skyblue")
    plt.title("OVSDB Throughput per Operation")
    plt.ylabel("Throughput (ops/sec)")
    plt.xlabel("Operation")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig("ovsdb_throughput.png")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.bar(df["operation"], df["cpu_time"], color="lightcoral")
    plt.title("OVSDB CPU Time per Operation")
    plt.ylabel("CPU Time (seconds)")
    plt.xlabel("Operation")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig("ovsdb_cpu_time.png")
    plt.show()

def main():
    run_all()
    save_latency_csv()
    save_summary_csv()
    plot_latency()
    plot_summary_graphs()

if __name__ == "__main__":
    main()
