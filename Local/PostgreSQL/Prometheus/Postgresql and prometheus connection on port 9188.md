# Steps After Downloading Prometheus, PostgreSQL Exporter, and PostgreSQL

---

## Step 1: Start PostgreSQL Exporter on Port 9188

Run the following commands **in the same order**:

```bash
export DATA_SOURCE_NAME="postgresql://prometheus:bmsce@localhost:5432/mydb?sslmode=disable"
postgres_exporter --web.listen-address=":9188" --web.telemetry-path="/metrics"
```

>  Make sure:
> - You replace `bmsce`, `localhost`, `5432`, and `mydb` with your actual PostgreSQL password, host, port, and database name if they are different.

---

## Step 2: Start Prometheus

Start Prometheus by running:

```bash
./prometheus
```

---

## Note:

- The PostgreSQL exporter is being run on **port 9188** instead of the default **9187**.
- **Reason:**  
  Port **9188** already has a PostgreSQL user running.  
  Instead of changing systemd configurations repeatedly, it’s easier and cleaner to run Prometheus-related services on port 9188.

---

 Now Prometheus will start scraping metrics from PostgreSQL Exporter running on port 9188!
