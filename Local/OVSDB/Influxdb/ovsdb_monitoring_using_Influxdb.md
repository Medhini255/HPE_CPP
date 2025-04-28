# OVS + InfluxDB + Grafana Monitoring Setup

## Goal
Monitor Open vSwitch (OVS) stats and visualize them in Grafana using InfluxDB as the time-series database.

---

## 1. Installation Steps

### Update & Upgrade System
```bash
sudo apt update  
sudo apt upgrade
```

### Install Open vSwitch
```bash
sudo apt install openvswitch-switch
```

### Install InfluxDB (v1.x)
```bash
sudo apt install influxdb influxdb-client
```

### Start and Enable InfluxDB
```bash
sudo systemctl start influxdb  
sudo systemctl enable influxdb
```

### Verify InfluxDB is Running
```bash
curl -G http://localhost:8086/query --data-urlencode "q=SHOW DATABASES"
```

### Install Grafana
```bash
sudo apt install -y apt-transport-https software-properties-common wget  
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -  
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list  
sudo apt update  
sudo apt install grafana  
sudo systemctl start grafana-server  
sudo systemctl enable grafana-server
```

---

## 2. Python Script Setup

### Install Requests Module
```bash
pip install requests
```

### Create `monitor_ovs.py` Script
Add your Python script (example content should be filled here).

### Run the Script
```bash
sudo python3 monitor_ovs.py
```

---

## 3. Configure OVS Bridges & Ports

### View Existing Setup
```bash
sudo ovs-vsctl show
```

### Add Bridges and Ports
```bash
sudo ovs-vsctl add-br br0  
sudo ovs-vsctl add-port br0 dummy0 -- set Interface dummy0 type=internal

sudo ovs-vsctl add-br br1  
sudo ovs-vsctl add-port br1 dummy1 -- set Interface dummy1 type=internal  
sudo ovs-vsctl add-port br1 dummy2 -- set Interface dummy2 type=internal
```

### Recheck Updated Config
```bash
sudo ovs-vsctl show
```

---

## 4. Setup Grafana
- Open Grafana in your browser:  
  `http://localhost:3000`
- Default login:  
  Username: `admin`  
  Password: `admin` (you'll be asked to change it)
- Add **InfluxDB** as a Data Source:  
  URL: `http://localhost:8086`  
  Database: `ovs_metrics`
- Create a Dashboard → Add Panel  
- Use the measurement `ovs_stats` and visualize bridges, ports, interfaces.

---

## 5. Cleanup Commands (Optional)
```bash
sudo ovs-vsctl del-br br0  
sudo ovs-vsctl del-br br1
```

---

## 6. Adding Flows Monitoring

###  View Existing Flows
```bash
sudo ovs-ofctl dump-flows br0
```

###  Add Flows
```bash
sudo ovs-ofctl add-flow br0 "priority=10,in_port=1,actions=output:2"  
sudo ovs-ofctl add-flow br0 "priority=10,in_port=2,actions=output:1"
```

###  Verify Flow Table
```bash
sudo ovs-ofctl dump-flows br0
```

###  Modify Python Script for Flows Monitoring

Add this function to monitor flows:
```python
def get_ovs_flows():
    try:
        output = subprocess.check_output(["ovs-ofctl", "dump-flows", "br0"]).decode()
        flow_count = output.count("priority=")
        return flow_count
    except subprocess.CalledProcessError as e:
        print("Error fetching OVS flows:", e)
        return 0
```

Modify the main loop to include flows:
```python
while True:
    b, p, i = get_ovs_stats()
    f = get_ovs_flows()
    print(f"Sending to InfluxDB → Bridges: {b}, Ports: {p}, Interfaces: {i}, Flows: {f}")
    send_to_influx(b, p, i)
    time.sleep(10)
```

---

## 7. Cleanup Commands (Optional)
```bash
sudo ovs-vsctl del-br br0  
sudo ovs-vsctl del-br br1
```

---
