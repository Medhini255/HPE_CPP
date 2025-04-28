# OVS Database and Bridge Management

## View Database Schema
```bash
sudo ovsdb-client get-schema
```

## View Databases
```bash
sudo ovsdb-client list-dbs
```

## View Tables
```bash
sudo ovsdb-client list-tables
```

---

## Creating and Managing Bridges

###  Create a Bridge
```bash
sudo ovs-vsctl add-br br-dummy  
sudo ovs-vsctl set bridge br-dummy --fail-mode=secure  # To mimic actual bridge
```

###  Check Created Bridge
```bash
sudo ovs-vsctl show
```
Output Example:
```
e3bc46f5-f241-430a-b391-57f389e1ffba
    Bridge br-dummy
        fail_mode: secure
        Port br-dummy
            Interface br-dummy
                type: internal
    Bridge my-python-bridge
        fail_mode: secure
    ovs_version: "2.17.9"
```

###  Bring Up the Bridge
```bash
sudo ip link set dev br-dummy up
```

---

## Managing Datapaths and Flows

###  Show the Datapath Table Values
```bash
sudo ovs-dpctl show
```
Output Example:
```
system@ovs-system:
  lookups: hit:0 missed:0 lost:0
  flows: 0
  masks: hit:0 total:0 hit/pkt:0.00
  caches:
    masks-cache: size:256
  port 0: ovs-system (internal)
  port 1: br-dummy (internal)
```

###  Allow Traffic to Flow
```bash
ping -I br-dummy 8.8.8.8
```

###  Run the Command Again to See Changes
```bash
sudo ovs-dpctl show
```
Output Example:
```
system@ovs-system:
  lookups: hit:39 missed:3 lost:0
  flows: 2
  masks: hit:44 total:2 hit/pkt:1.05
  cache: hit:26 hit-rate:61.90%
  caches:
    masks-cache: size:256
  port 0: ovs-system (internal)
  port 1: br-dummy (internal)
```

---
