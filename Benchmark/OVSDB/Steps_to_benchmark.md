
# OVSDB Benchmarking Guide

This guide outlines how to run the OVSDB benchmarking script and what outputs it generates.

---

##  Steps to Run

### **Step 1: Start OVSDB Service**

Make sure the OVSDB server is running using the Open vSwitch service:

```bash
sudo systemctl start openvswitch-switch
````

You can verify it's running:

```bash
sudo systemctl status openvswitch-switch
```

---

### **Step 2: Run the Benchmarking Script**

Run the Python benchmarking script with root privileges:

```bash
sudo python3 ovsdb_benchmark.py
```

This will:

* Perform `CREATE`, `READ`, `UPDATE`, and `DELETE` operations
* Record latency, CPU time, and throughput per operation

---

##  Output Files

The script will generate the following files:

###  **Excel-Compatible CSV Files**

* `ovsdb_crud_latency_<timestamp>.csv`: Latency (ms) of each operation
* `ovsdb_summary_<timestamp>.csv`: Summary including average latency, CPU time, and throughput

###  **Graphs (Saved as PNGs)**

* `ovsdb_crud_latency_lineplot.png`: Latency across operation index
* `ovsdb_crud_latency_boxplot.png`: Boxplot of latency per CRUD op
* `ovsdb_avg_latency_line.png`: Average latency per CRUD operation
* `ovsdb_cpu_time.png`: CPU time per operation
* `ovsdb_throughput.png`: Throughput (ops/sec) per operation

---

##  File Locations

All CSV and PNG files will be saved in the current working directory. You can move or archive them as needed for reports or visualization.

---

##  Notes

* The script may require root privileges to access `ovs-vsctl` and `ovsdb-client`.
* Ensure Open vSwitch is installed and `ovsdb-server` is running.
* You can adjust the number of operations by changing `NUM_OPS` in the script.

---
