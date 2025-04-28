# VictoriaMetrics Installation

## Step 1: Download VictoriaMetrics
```bash
wget https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.102.0/victoria-metrics-linux-amd64-v1.102.0.tar.gz
```

## Step 2: Extract the Downloaded Tar File
```bash
tar -xvzf victoria-metrics-linux-amd64-v1.102.0.tar.gz
```

## Step 3: Move the Binary to /usr/local/bin
```bash
sudo mv victoria-metrics-prod /usr/local/bin/victoria-metrics
```

## Step 4: Give Execute Permission to the Binary
```bash
sudo chmod +x /usr/local/bin/victoria-metrics
```

## Step 5: Create Configuration Directory
```bash
sudo mkdir -p /etc/victoriametrics
```

## Step 6: Configure victoria-metrics.yml
```bash
sudo nano /etc/victoriametrics/victoriametrics.yml
```

## Step 7: Start VictoriaMetrics
```bash
sudo victoria-metrics -storageDataPath=/var/lib/victoria-metrics -promscrape.config=/etc/victoriametrics/victoriametrics.yml
```

## Step 8: Verify Installation
```bash
curl http://localhost:8428
