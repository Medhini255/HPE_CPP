# After Downloading VictoriaMetrics

---

## Step 1: Begin PostgreSQL Exporter on Port 9188

Run these commands **in the same order**:

```bash
export DATA_SOURCE_NAME="postgresql://prometheus:bmsce@localhost:5432/mydb?sslmode=disable"
postgres_exporter --web.listen-address=":9188" --web.telemetry-path="/metrics"
```

---

## Step 2: Configure `prometheus.yml`

Add the following at the end of your `prometheus.yml` file (make sure indentation is correct):

```yaml
remote_write:
  - url: "http://localhost:8428/api/v1/write"
```

---

## Step 3: Start VictoriaMetrics

Use the following command to start VictoriaMetrics:

```bash
./victoria-metrics-prod -retentionPeriod=1 -storageDataPath=./vm-data
```

---

## Step 4: Start Prometheus

Use the following command to start Prometheus:

```bash
./prometheus
```
```
