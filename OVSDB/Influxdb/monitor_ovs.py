import subprocess
import time
import requests

INFLUXDB_URL = "http://localhost:8086/write?db=ovs_metrics"

def get_ovs_stats():
    try:
        output = subprocess.check_output(['ovs-vsctl', 'show']).decode()
        bridges = output.count("Bridge")
        ports = output.count("Port")
        interfaces = output.count("Interface")
        return bridges, ports, interfaces
    except Exception as e:
        print("Error fetching OVS stats:", e)
        return 0, 0, 0

while True:
    bridges, ports, interfaces = get_ovs_stats()
    payload = f"ovs_stats bridges={bridges},ports={ports},interfaces={interfaces}"
    try:
        requests.post(INFLUXDB_URL, data=payload)
        print(f"Sending to InfluxDB → Bridges: {bridges}, Ports: {ports}, Interfaces: {interfaces}")
    except Exception as e:
        print("Error sending to InfluxDB:", e)
    time.sleep(5)
