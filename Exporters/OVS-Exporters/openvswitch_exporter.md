# Steps to Install OpenVSwitch Exporter

---

## Step 1: Clone the OpenVSwitch Exporter Repository

```bash
git clone https://github.com/digitalocean/openvswitch_exporter.git
```

---

## Step 2: Navigate to the Project Directory

```bash
cd openvswitch_exporter
```

---

## Step 3: Navigate Further into the Source Code

```bash
cd cmd
cd openvswitch_exporter
```

---

## Step 4: Build the Exporter

Use the `go build` command to build the exporter:

```bash
go build
```

---

## Step 5: Run the OpenVSwitch Exporter

Start the exporter:

```bash
./openvswitch_exporter
```

---

## Default Port

- The OpenVSwitch exporter runs by default on **port 9310**.

---

## Description

This exporter exposes various metrics related to the Linux kernel Open vSwitch datapath using the **generic netlink `ovs_datapath` family**.
