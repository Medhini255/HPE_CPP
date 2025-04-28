#  Steps to Configure Grafana with InfluxDB for OVS Metrics

---

###  **Open Grafana in your Browser**

```text
http://localhost:3000
```

###  **Default Login**
- **Username:** `admin`
- **Password:** `admin` (You'll be asked to change it after first login)

---

###  **Add InfluxDB as a Data Source**

- Go to **Configuration > Data Sources**
- Add **InfluxDB**
- **URL:** `http://localhost:8086`
- **Database:** `ovs_metrics`
- Save & Test the connection

---

###  **Create a Dashboard and Panel**

- Go to **Dashboard > New Dashboard**
- Click **Add a new panel**
- Use the following query:

```sql
SELECT * FROM "ovs_stats"
```

- Visualize bridges, ports, interfaces
- Set **Visualization Type:** `Graph` or `Table`
- Save the panel and dashboard

---

#  Grafana Configuration for Flows

###  **Steps to Visualize Flow Counts**

- Open **Grafana Dashboard**
- Create a **New Panel**
- Query:

```sql
SELECT * FROM "ovs_stats"
```

- Add **flows** field to visualize **flow count**
- Set Visualization Type as **Graph** or **Table**
- Save and apply changes

---


