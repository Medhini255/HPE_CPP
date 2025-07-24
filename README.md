# Distributed Monitoring with Prometheus, VictoriaMetrics & InfluxDB

This project sets up a **distributed monitoring system** using **Prometheus**, **VictoriaMetrics**, and **InfluxDB** across multiple systems in the same network.

## Project Goals

- Deploy Prometheus, VictoriaMetrics, and InfluxDB on **System A**
- Send ovsdb and postgresql metrics from **System B**
- Monitor and validate metric flow across the network
- Enable future benchmarking and visualization

---

## Architecture

System A:
├── Prometheus (port 9090)
├── VictoriaMetrics (port 8428)
└── InfluxDB (port 8086)

System B (Remote Node):
└── Pushes metrics / exposes exporters / sends data to TSDBs

---

## Version Details

Prometheus version details-
prometheus, version 2.31.2+ds1 (branch: debian/sid, revision: 2.31.2+ds1-1ubuntu1.22.04.3)
  build user:       team+pkg-go@tracker.debian.org
  build date:       20241115-22:48:14
  go version:       go1.18.1
  platform:         linux/amd64
  
Victoria metrics version details-
victoria-metrics-20240717-185111-tags-v1.102.0-0-g65bb429b81

InfluxDB version details-
2025-04-08T13:19:53.214224Z	info	InfluxDB starting	{"log_id": "0vmOlDVW000", "version": "1.6.7~rc0", "branch": "unknown", "commit": "unknown"}
2025-04-08T13:19:53.214242Z	info	Go runtime	{"log_id": "0vmOlDVW000", "version": "go1.18.1", "maxprocs": 12}

Open_vSwitch version details-
ovs-vsctl (Open vSwitch) 2.17.9
DB Schema 8.3.0

PostgreSQL version details-
PostgreSQL 14.17 (Ubuntu 14.17-0ubuntu0.22.04.1)
