

---

##  Steps to Benchmark VictoriaMetrics Running on Remote Machine

---

###  **Assumption**

VictoriaMetrics is running remotely and accessible via:

```
http://<remote-ip-address>:8428
```

---

###  Step 1: **Generate Benchmark Data**

Use the `tsbs_generate_data` tool you built earlier:

```bash
./tsbs/bin/tsbs_generate_data \
  --use-case=cpu-only \
  --format=victoriametrics \
  --scale=10 \
  --timestamp-start="2016-01-01T00:00:00Z" \
  --timestamp-end="2016-01-02T00:00:00Z" \
  --file=vm-data.txt
```

* `--format=victoriametrics`: ensures the line protocol matches what VM expects.
* `--scale=10`: simulates 10 hosts.

---

###  Step 2: **Load Data into VictoriaMetrics**

Now load that data into your running VictoriaMetrics instance:

```bash
./tsbs/bin/tsbs_load_victoriametrics \
  --file=vm-data.txt \
  --urls=http://<remote-ip-address>:8428/write \
  --workers=4
```

* Make sure `victoria-metrics` is running and listening on `<remote-ip-address>:8428`.
* You should see stats like rows/sec and total inserted.

---

###  Step 3: **Generate Benchmark Queries**

```bash
./tsbs/bin/tsbs_generate_queries \
  --use-case=cpu-only \
  --scale=10 \
  --queries=100 \
  --query-type=cpu-max-all-1 \
  --format=victoriametrics \
  --timestamp-start="2016-01-01T00:00:00Z" \
  --timestamp-end="2016-01-02T00:00:00Z" \
  --file=vm-queries.txt
```

This creates 100 queries like:

```promql
max(rate(cpu_usage_user[1m]))
```

---

###  Step 4: **Run the Benchmark Queries**

```bash
./tsbs/bin/tsbs_run_queries_victoriametrics \
  --file=vm-queries.txt \
  --workers=4 \
  --urls=http://<remote-ip-address>:8428
```

You’ll see output like:

```
read 100 queries
Executed 100 queries in 0.153s
Min: 1.5ms, Max: 9.2ms, Mean: 4.3ms
```

---

###  Optional: Monitor VictoriaMetrics Performance

Open:

```
http://localhost:8428/metrics
```

Look for:

* `vm_rows_inserted_total`
* `vm_queries_total`
* `vm_query_duration_seconds`
Repeat the same for 1000,10000 queries.
These help correlate TSBS benchmark results with actual VM behavior.

---

