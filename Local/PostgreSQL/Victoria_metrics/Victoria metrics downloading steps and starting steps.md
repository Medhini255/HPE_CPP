# Steps to Download and Run VictoriaMetrics

---

## Step 1: Download VictoriaMetrics

Use the following command to download the files from GitHub:

```bash
wget https://github.com/VictoriaMetrics/VictoriaMetrics/releases/download/v1.102.0/victoria-metrics-linux-amd64-v1.102.0.tar.gz
```

---

## Step 2: Extract the Downloaded Files

Extract the downloaded `.tar.gz` file:

```bash
tar -xvzf victoria-metrics-linux-amd64-v1.102.0.tar.gz
```

---

## Step 3: Start VictoriaMetrics

Start the VictoriaMetrics service (it will run on port **8428**):

```bash
./victoria-metrics-prod
```

---

## Step 4: Verify VictoriaMetrics is Running

Check if VictoriaMetrics is running correctly:

```bash
curl http://localhost:8428/health
```
- If it returns `"OK"`, the setup is successful!

---
```
