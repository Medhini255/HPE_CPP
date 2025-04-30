# OVSDB Monitoring Setup Log

---

## 1. Install InfluxDB

### a) Add InfluxDB Repository

```bash
wget -qO- https://repos.influxdata.com/influxdb.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/influxdb.gpg
echo "deb https://repos.influxdata.com/ubuntu focal stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update
```
### b) Install and Start InfluxDB
```bash
sudo apt install influxdb
sudo systemctl start influxdb
sudo systemctl enable influxdb
```
## 2. Create Monitoring Database
```bash
influx
```
```sql
> CREATE DATABASE ovsdb_monitoring;
> SHOW DATABASES;
```
## 3. Install Telegraf
```bash
sudo apt install telegraf
sudo systemctl enable telegraf
sudo systemctl start telegraf
```
## 4. Configure Telegraf to Scrape OVSDB Exporter
### Edit Telegraf configuration:
```bash
sudo nano /etc/telegraf/telegraf.conf
```
### Add the following configuration:
```toml

[[inputs.prometheus]]
  urls            = ["http://localhost:5000/metrics"]
  metric_version  = 2
  name_override   = "ovsdb_exporter"

[[outputs.influxdb]]
  urls     = ["http://127.0.0.1:8086"]
  database = "ovsdb_monitoring"
  username = "admin"
  password = "newStrongPassword"
```
## 5. Error: HTTPS vs HTTP Mismatch
Resolution: Changed urls to use http://localhost:5000/metrics.

## 6. Verify Metrics in InfluxDB
```bash

influx
```
```sql
> USE ovsdb_monitoring;
> SHOW MEASUREMENTS;
> SHOW FIELD KEYS FROM "ovsdb_exporter";
```
## 7. Grafana Setup & Authentication
### If Grafana admin password is forgotten:
``` bash

sudo grafana-cli admin reset-admin-password NewPass123
sudo systemctl restart grafana-server
```
## 8. Dashboard Recommendations
### Panel: Total OVS Ports
```sql
SELECT last("ovs_dp_br_if_total") FROM "ovsdb_exporter"
```
Panel: RX/TX Rate

```sql
SELECT non_negative_derivative(mean("ovs_interface_rx_bytes"),1s) AS RX_Bps,
       non_negative_derivative(mean("ovs_interface_tx_bytes"),1s) AS TX_Bps
FROM "ovsdb_exporter" 
WHERE $timeFilter 
GROUP BY time($__interval)
```
