# Full Stack Monitoring Setup Guide

## 1. Install PostgreSQL

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### Start and Enable PostgreSQL
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

---

## 2. Install InfluxDB

### Add InfluxDB Repository
```bash
wget -qO- https://repos.influxdata.com/influxdb.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/influxdb.gpg
echo "deb https://repos.influxdata.com/ubuntu focal stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update
```

### Install and Start InfluxDB
```bash
sudo apt install influxdb
sudo systemctl start influxdb
sudo systemctl enable influxdb
```

---

## 3. Install Telegraf

```bash
sudo apt install telegraf
```

### Edit the Telegraf Configuration
```bash
sudo nano /etc/telegraf/telegraf.conf
```

---

## 4. Install Grafana

```bash
sudo apt install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo apt update
sudo apt install grafana
```

### Start and Enable Grafana Server
```bash
sudo systemctl start grafana-server
sudo systemctl enable grafana-server.service
```

---

## Grafana Login Information

- **Access Grafana at:** [http://localhost:3000](http://localhost:3000)
- **Default Credentials:**
  - Username: `admin`
  - Password: `admin`
```
