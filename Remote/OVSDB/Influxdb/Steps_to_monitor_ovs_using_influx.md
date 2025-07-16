  # Steps to OVSDB Running on Remote Machine Using Influxdb

---

###  **Machine-A (OVSDB running)**

**Step-1:** Allow TCP on the port on which OVS exporter is running  
```bash
sudo ufw allow <port-no>/tcp
```

**Step-2:** Get Machine A's IP  
```bash
hostname -I
```

**Step-3:** Start Open vSwitch Database  
```bash
sudo systemctl start openvswitch-switch
```

**Step-4:** Run the OVS exporter  
```bash
cd ovs_exporter
make
make qtest
```
> **Default exporter port:** 5000

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
> CREATE DATABASE ovs_remote;
> SHOW DATABASES;
```
**Step-3:** Install Telegraf
```bash
sudo apt install telegraf
sudo systemctl enable telegraf
sudo systemctl start telegraf
```
**Step-4:** Configure Telegraf to Scrape OVSDB Exporter
#### Edit Telegraf configuration:
```bash
sudo nano /etc/telegraf/telegraf.conf
```
#### Add the following configuration:
```toml

[[inputs.prometheus]]
  urls            = ["http://<machine-A-ip>:<machine-A-port_no>/metrics"]
  metric_version  = 2
  name_override   = "ovsdb_exporter"

[[outputs.influxdb]]
  urls     = ["http://127.0.0.1:8086"]
  database = "ovs_remote"
  username = "admin"
  password = "newStrongPassword"
```

**Step-5:** Verify Metrics in InfluxDB
```bash

influx
```
```sql
> USE ovs_remote;
> SHOW MEASUREMENTS;
> SHOW FIELD KEYS "ovs_remote" FROM "ovsdb_exporter";
```
**Step-6:** Grafana Setup & Authentication
#### If Grafana admin password is forgotten:
``` bash

sudo grafana-cli admin reset-admin-password NewPass123
sudo systemctl restart grafana-server
```
**Step-7:** Dashboard Recommendations
#### Panel: Total OVS Ports
```sql
SELECT last("ovs_dp_br_if_total") FROM "ovsdb_exporter"
```
