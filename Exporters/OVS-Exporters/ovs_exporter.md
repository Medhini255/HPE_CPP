# Steps to Install OVS Exporter

---

## Step 1: Clone the OVS Exporter Repository

```bash
git clone https://github.com/greenpau/ovs_exporter.git
```

---

## Step 2: Navigate to the Project Directory

```bash
cd ovs_exporter
```

---

## Step 3: Navigate to Source Code Directory

```bash
cd cmd
cd ovs_exporter
```

---

## Step 4: Build the Exporter

```bash
go build
```

---

## Step 5: Move Back to Project Root

```bash
cd ..
cd ..
```

---

## Step 6: Run Make Commands

Build the project:

```bash
make
```

Quick test the build:

```bash
make qtest
```

---

## Default Running Port

- The **OVS Exporter** runs by default on **port 5000**.

---

## Description

- This exporter is mainly used for **monitoring Bridges and Ports** in Open vSwitch.
