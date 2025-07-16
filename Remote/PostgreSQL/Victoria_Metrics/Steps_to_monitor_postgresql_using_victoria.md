# Steps to PostgreSQL Running on Remote Machine Using Victoria Metrics

---

###  **Machine-A (PostgreSQL running)**

**Step-1:** Allow TCP on the port on which Postgres exporter is running  
```bash
sudo ufw allow <port-no>/tcp
```

**Step-2:** Get Machine A's IP  
```bash
hostname -I
```

**Step-3:** Start PostgreSQL Database  
(Start your PostgreSQL service if not already running.)

**Step-4:** Run the Postgres Exporter  
```bash
export DATA_SOURCE_NAME="postgresql://prometheus:bmsce@localhost:5432/mydb?sslmode=disable"
postgres_exporter --web.listen-address=":9188" --web.telemetry-path="/metrics"
```
> **Default exporter port:** 9187

---

###  **Machine-B (VictoriaMetrics running)**

**Step-1:** Add Machine-A's configuration to Machine-B's `victoriametrics.yml` file  
```bash
sudo nano /etc/victoriametrics/victoriametrics.yml
```

Add this job configuration:
```yaml
- job_name: 'postgresql_machine-A'
  static_configs:
    - targets: ['<machine-A-ip>:<exporter-port-no>']
```

**Step-2:** Reload systemd configuration  
```bash
sudo systemctl daemon-reload
```

**Step-3:** Start VictoriaMetrics  
```bash
sudo victoria-metrics -storageDataPath=/var/lib/victoria-metrics -promscrape.config=/etc/victoriametrics/victoriametrics.yml
```

**Step-4:** Check for the target's metrics  
```bash
curl http://<machine-A-ip>:<exporter-port-no>/metrics
```

**Step-5:** Run queries on VictoriaMetrics UI  

Example Query:  
```text
pg_stat_database_blks_read
```
