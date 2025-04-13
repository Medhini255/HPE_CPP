# OVSDB Setup and Traffic Generation with Exporter

## Step 1: Install Open vSwitch

Install Open vSwitch using the package manager:

```bash
sudo apt update
sudo apt install openvswitch-switch -y
```

Verify that the OVS services are running:

```bash
sudo systemctl status openvswitch-switch
```

Ensure the `ovsdb-server` is active:

```bash
ps aux | grep ovsdb-server
```

---

## Step 2: Clone and Build the OVS Exporter

Install Go if not already installed:

```bash
sudo apt install golang -y
```

Clone the OVS Exporter repository and build the binary:

```bash
git clone https://github.com/greenpau/ovs_exporter.git
cd ovs_exporter
go build -o ovs_exporter ./cmd/ovs_exporter
```

Run the exporter:

```bash
./ovs_exporter --listen 0.0.0.0:9477
```

The metrics will be available at: `http://localhost:9477/metrics`

---

## Step 3: Create OVS Bridge and Internal Port

Create an OVS bridge and an internal port for the server:

```bash
sudo ovs-vsctl add-br br0
sudo ovs-vsctl add-port br0 port1 -- set Interface port1 type=internal
sudo ip link set port1 up
sudo ip addr add 10.10.10.1/24 dev port1
```

---

## Step 4: Install iperf3

Install the traffic generation tool:

```bash
sudo apt install iperf3 -y
```

---

## Step 5: Shell Script to Generate Traffic and Add Ports

Save the following script as `ovs_traffic_gen.sh`:

```bash
#!/bin/bash

BRIDGE="br0"
BASE_IP="10.10.10"
START_INDEX=3
PORT_COUNT=5

# Create server namespace and iperf3 server
sudo ovs-vsctl add-port $BRIDGE port1 -- set Interface port1 type=internal
sudo ip link set port1 up
sudo ip addr add $BASE_IP.1/24 dev port1
sudo ip netns add ns_server
sudo ip link set port1 netns ns_server
sudo ip netns exec ns_server ip link set lo up
sudo ip netns exec ns_server ip link set port1 up
sudo ip netns exec ns_server iperf3 -s -D

# Create client namespaces and start iperf3 clients
for ((i=START_INDEX; i<START_INDEX+PORT_COUNT; i++)); do
  port="port$i"
  ip="$BASE_IP.$i"
  ns="ns_client_$i"

  sudo ovs-vsctl add-port $BRIDGE $port -- set Interface $port type=internal
  sudo ip link set $port up
  sudo ip addr add $ip/24 dev $port

  sudo ip netns add $ns
  sudo ip link set $port netns $ns
  sudo ip netns exec $ns ip link set lo up
  sudo ip netns exec $ns ip link set $port up
  sudo ip netns exec $ns iperf3 -c $BASE_IP.1 -t 10 -i 1 &
done

wait
```

Make the script executable and run it:

```bash
chmod +x ovs_traffic_gen.sh
./ovs_traffic_gen.sh
```

---

## Summary

- Open vSwitch and `ovsdb-server` are used to simulate a virtual network environment.
- The `ovs_exporter` binary collects metrics and exposes them to Prometheus.
- Internal ports are created dynamically and traffic is generated using `iperf3` clients and a server running in network namespaces.

This setup allows monitoring of OVSDB activity through Prometheus and simulates network traffic for observability and testing.

Let me know if you also need the Prometheus configuration or a Grafana dashboard template.
