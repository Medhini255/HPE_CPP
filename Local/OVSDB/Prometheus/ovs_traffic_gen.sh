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
