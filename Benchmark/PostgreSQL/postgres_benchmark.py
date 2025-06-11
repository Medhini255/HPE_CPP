import psycopg2
import time
import csv
import psutil
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime

DB_PARAMS = {
    "dbname": "benchmarkdb",
    "user": "benchmarkuser",
    "password": "benchmarkpass",
    "host": "localhost",
    "port": 5432
}

TABLE = "benchmark_table"
NUM_OPS = 100
results = []
summary_stats = []

def get_postgres_pid():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'postgres' in proc.info['name']:
            return proc.info['pid']
    return None

def run_query(cursor, query, values=None):
    start = time.time()
    cursor.execute(query, values or ())
    end = time.time()
    return round((end - start) * 1000, 3)  # in ms

def benchmark_op(operation, conn, cursor, build_query_fn):
    print(f"â–¶ {operation} benchmark...")
    latencies = []
    start_batch = time.time()
    pid = get_postgres_pid()
    postgres_proc = psutil.Process(pid)

    postgres_proc.cpu_percent(interval=1.0)  # Warm-up

    for i in range(NUM_OPS):
        query, values = build_query_fn(i)
        latency = run_query(cursor, query, values)
        latencies.append(latency)
        results.append([operation, latency])
        conn.commit()

    cpu_times = postgres_proc.cpu_times()
    cpu_user_time = cpu_times.user
    cpu_system_time = cpu_times.system
    cpu_total_time = cpu_user_time + cpu_system_time
    cpu_after = round(cpu_total_time, 3)

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

def build_create_query(i):
    return ("INSERT INTO benchmark_table (name, value) VALUES (%s, %s)", (f"name{i}", f"value{i}"))

def build_read_query(i):
    return ("SELECT * FROM benchmark_table LIMIT 1", None)

def build_update_query(i):
    return ("UPDATE benchmark_table SET value = %s WHERE id = (SELECT id FROM benchmark_table LIMIT 1)", (f"updated{i}",))

def build_delete_query(i):
    return ("DELETE FROM benchmark_table WHERE id = (SELECT id FROM benchmark_table LIMIT 1)", None)

def setup_database():
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            id SERIAL PRIMARY KEY,
            name TEXT,
            value TEXT
        );
    """)
    conn.commit()
    return conn, cursor

def run_all(conn, cursor):
    benchmark_op("CREATE", conn, cursor, build_create_query)
    benchmark_op("READ", conn, cursor, build_read_query)
    benchmark_op("UPDATE", conn, cursor, build_update_query)
    benchmark_op("DELETE", conn, cursor, build_delete_query)
    print("SUMMARY DEBUG:", summary_stats)

def save_latency_csv():
    filename = f"postgres_crud_latency_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Operation", "Latency_ms"])
        writer.writerows(results)
    print(f"ðŸ“ Latency log saved to {filename}")

def save_summary_csv():
    filename = f"postgres_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["operation", "avg_latency", "throughput", "cpu_time"])
        writer.writeheader()
        writer.writerows(summary_stats)
    print(f"ðŸ“ Summary saved to {filename}")

def plot_latency():
    df = pd.DataFrame(results, columns=["Operation", "Latency_ms"])
    plt.figure(figsize=(10, 6))
    for op in df["Operation"].unique():
        df_op = df[df["Operation"] == op].reset_index(drop=True)
        plt.plot(df_op.index, df_op["Latency_ms"], label=op)
    plt.title("PostgreSQL Latency over Operations")
    plt.xlabel("Operation Index")
    plt.ylabel("Latency (ms)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("postgres_latency_lineplot.png")
    plt.show()

    plt.figure(figsize=(8, 6))
    df.boxplot(column="Latency_ms", by="Operation", grid=True)
    plt.title("Latency Distribution per Operation")
    plt.suptitle("")
    plt.ylabel("Latency (ms)")
    plt.savefig("postgres_latency_boxplot.png")
    plt.show()

def plot_summary_graphs():
    df = pd.DataFrame(summary_stats)
    plt.figure(figsize=(8, 5))
    plt.bar(df["operation"], df["throughput"], color="skyblue")
    plt.title("PostgreSQL Throughput per Operation")
    plt.ylabel("Throughput (ops/sec)")
    plt.xlabel("Operation")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig("postgres_throughput.png")
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.bar(df["operation"], df["cpu_time"], color="lightcoral")
    plt.title("PostgreSQL CPU Time per Operation")
    plt.ylabel("CPU Time (seconds)")
    plt.xlabel("Operation")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig("postgres_cpu_time.png")
    plt.show()

def main():
    conn, cursor = setup_database()
    run_all(conn, cursor)
    save_latency_csv()
    save_summary_csv()
    plot_latency()
    plot_summary_graphs()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
