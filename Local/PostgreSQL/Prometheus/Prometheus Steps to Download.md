# Steps to Install and Set Up Prometheus

---

## Step 1: Update System Packages

```bash
sudo apt update && sudo apt upgrade -y
```

---

## Step 2: Create a Prometheus User

Create a dedicated Prometheus user:

```bash
sudo useradd --no-create-home --shell /bin/false prometheus
```

---

## Step 3: Download Prometheus

Use `wget` to download Prometheus:

```bash
wget https://github.com/prometheus/prometheus/releases/latest/download/prometheus-linux-amd64.tar.gz
```

---

## Step 4: Extract the Downloaded File

Extract the contents:

```bash
tar -xvf prometheus-linux-amd64.tar.gz
```

---

## Step 5: Rename the Directory

Rename for convenience:

```bash
mv prometheus-linux-amd64 prometheus
```

> **Note:** Your step mentioned `.tar.gz` file renaming, but you should rename the extracted **folder**, not the `.tar.gz` file.

---

## Step 6: Set Correct Permissions

Assign ownership to Prometheus user:

```bash
sudo chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus
```

---

## Step 7: Create a Prometheus systemd Service

Create and edit the systemd file:

```bash
sudo nano /etc/systemd/system/prometheus.service
```

Paste the following content:

```ini
[Unit]
Description=Prometheus Monitoring System
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
    --config.file=/etc/prometheus/prometheus.yml \
    --storage.tsdb.path=/var/lib/prometheus \
    --web.listen-address=0.0.0.0:9090 \
    --storage.tsdb.retention.time=15d

[Install]
WantedBy=multi-user.target
```

---

## Step 8: Reload systemd and Start Prometheus

Run the following commands **in order**:

```bash
sudo systemctl daemon-reload
sudo systemctl start prometheus
```

---

## Step 9: Check Prometheus Status

Check if Prometheus is running:

```bash
sudo systemctl status prometheus
