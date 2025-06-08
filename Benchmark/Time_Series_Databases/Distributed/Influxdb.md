

---

##  Steps to Benchmark Influxdb Running on Remote Machine

---

###  **Assumption**

Influxdb is running remotely and accessible via:

```
http://<remote-ip-address>:8086
```

---

###  Step 1: **Create Database benchmark in the remote machine**
```bash
influx
```
```sql
create database benchmark;
exit
```
---

###  Step 2: **Generate Benchmark Data**

Use the `tsbs_generate_data` tool you built earlier:

```bash
./tsbs/bin/tsbs_generate_data --use-case=cpu-only --format=influx --scale=10 --file=your_input_file.json

```

* `--format=influx`: ensures the line protocol matches what influxdb expects.
* `--scale=10`: simulates 10 hosts.

---

###  Step 3: **Load Data into Influxdb**

Now load that data into your running Influxdb instance:

```bash
./tsbs/bin/tsbs_load_influx --file=your_input_file.json --urls=http://<remote-ip-address>:8086 --db-name=benchmark --batch-size=10000 --workers=4
```

* Make sure `influxdb` is running and listening on `<remote-ip-address>:8086`.
* You should see stats like rows/sec and total inserted.

---

###  Step 4: **Verify data in Influxdb**

```bash
influx
```
```sql
USE benchmark;
SHOW MEASUREMENTS;
SELECT * FROM cpu LIMIT 5;
exit
```

---

###  Step 5: **Generate Benchmark Queries**

```bash
./tsbs/bin/tsbs_generate_queries \
  --use-case=cpu-only \
  --scale=10 \
  --queries=100 \
  --query-type=cpu-max-all-1 \
  --format=influx \
  --timestamp-start="2016-01-01T00:00:00Z" \
  --timestamp-end="2016-01-02T00:00:00Z" \
  --file=queries.txt
```

---
###  Step 6: **Run the Benchmark Queries**

```bash
./tsbs/bin/tsbs_run_queries_influx \
  --db-name=benchmark \
  --urls=http://<remote-ip-address>:8086 \
  --file=queries.txt \
  --workers=4
```
---
Repeat the same for 1000,10000 queries.
