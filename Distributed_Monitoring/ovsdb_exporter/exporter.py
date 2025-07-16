from prometheus_client import start_http_server, Gauge
import subprocess
import time

# Define Prometheus metrics
bridge_count_metric = Gauge('ovsdb_bridge_count', 'Number of bridges in OVSDB')
port_count_metric = Gauge('ovsdb_port_count', 'Number of ports in OVSDB')

def get_ovsdb_metrics():
    try:
        # Get number of bridges
        bridges_output = subprocess.check_output(['ovs-vsctl', 'list-br'], text=True)
        bridge_list = bridges_output.strip().split('\n') if bridges_output.strip() else []
        bridge_count = len(bridge_list)
        bridge_count_metric.set(bridge_count)

        # Count ports across all bridges
        total_ports = 0
        for br in bridge_list:
            ports_output = subprocess.check_output(['ovs-vsctl', 'list-ports', br], text=True)
            port_list = ports_output.strip().split('\n') if ports_output.strip() else []
            total_ports += len(port_list)
        
        port_count_metric.set(total_ports)

    except subprocess.CalledProcessError as e:
        print(f"Error while executing ovs-vsctl: {e}")
        bridge_count_metric.set(0)
        port_count_metric.set(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        bridge_count_metric.set(0)
        port_count_metric.set(0)


if __name__ == '__main__':
    # Start Prometheus exporter on port 9101
    start_http_server(9101)
    print("Exporter running on http://localhost:9101/metrics")
    
    while True:
        get_ovsdb_metrics()
        time.sleep(10)
