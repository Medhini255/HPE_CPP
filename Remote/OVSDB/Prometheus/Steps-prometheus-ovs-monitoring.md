  # Steps to OVSDB Running on Remote Machine Using Prometheus

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

###  **Machine-B (Prometheus running)**

**Step-1:** Add Machine-A's configuration to Machine-B's `prometheus.yml` file  
```bash
sudo nano /etc/prometheus/prometheus.yml
```

Add this job configuration:
```yaml
- job_name: 'ovs_machine-A'
  static_configs:
    - targets: ['<machine-A-ip>:<exporter-port-no>']
```

**Step-2:** Reload Prometheus configuration  
```bash
sudo systemctl daemon-reload
```

**Step-3:** Start Prometheus  
```bash
sudo systemctl start prometheus
```

**Step-4:** Check for the target's metrics  
```bash
curl http://<machine-A-ip>:<exporter-port-no>/metrics
```

**Step-5:** Run queries on Prometheus UI  

Example Query:  
```text
ovs_dp_br_if_total
```
> (Shows number of interfaces under each bridge.)

---


