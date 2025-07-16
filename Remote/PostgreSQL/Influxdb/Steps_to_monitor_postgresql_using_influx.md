# Steps to PostgreSQL Running on Remote Machine Using Influxdb

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

###  **Machine-B (Influxdb running)**

**Step-1:** Install and Start InfluxDB
```bash
sudo apt install influxdb
sudo systemctl start influxdb
sudo systemctl enable influxdb
```
**Step-2:** Create Monitoring Database
```bash
influx
```
```sql
> CREATE DATABASE post_remote;
> SHOW DATABASES;
```
**Step-3:** Install Telegraf
```bash
sudo apt install telegraf
sudo systemctl enable telegraf
sudo systemctl start telegraf
```
**Step-4:** Configure Telegraf to Scrape Postgres Exporter
#### Edit Telegraf configuration:
```bash
sudo nano /etc/telegraf/telegraf.conf
```
#### Add the following configuration:
```toml

[[inputs.postgresql]]
  urls            = ["http://<machine-A-ip>:<machine-A-port_no>/metrics"]
  metric_version  = 2
  name_override   = "postgres_exporter"

[[outputs.influxdb]]
  urls     = ["http://127.0.0.1:8086"]
  database = "post_remote"
  username = "admin"
  password = "newStrongPassword"
```

**Step-5:** Verify Metrics in InfluxDB
```bash

influx
```
```sql
> USE post_remote;
> SHOW MEASUREMENTS;
> SHOW FIELD KEYS "post_remote" FROM "postgres_exporter";
```
**Step-6:** Grafana Setup & Authentication
#### If Grafana admin password is forgotten:
``` bash

sudo grafana-cli admin reset-admin-password NewPass123
sudo systemctl restart grafana-server
```
**Step-7:** Dashboard Recommendations
```sql

```
