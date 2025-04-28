# OVS Monitoring with Victoria Metrics

## Step 1: Setting up the components

### i) Starting Open vSwitch Database
```bash
sudo systemctl start openvswitch-switch
```

### ii) Running the Exporters
1. Navigate to the exporter directory.
2. Run the exporters (`ovs_exporter`, `openvswitch_exporter`):
```bash
cd ovs_exporter
make
make qtest
```
*Default running port for exporters:*
- OVS Exporter: `5000`
- Open vSwitch Exporter: `9310`

### iii) Configuring `victoriametrics.yml`
- Edit the `victoriametrics.yml` configuration file to include your OVS machine:
```bash
sudo nano /etc/victoriametrics/victoriametrics.yml
```
Example configuration:
```yaml
- job_name: 'ovs_machine-A'
  static_configs:
    - targets: ['<machine-A-ip>:<exporter-port-no>']
```

## Step 2: Check whether metrics are being scraped
1. Check if metrics are being scraped from the OVS exporter:
```bash
curl http://localhost:9310/metrics
```
2. Check if metrics are being scraped from the Open vSwitch exporter:
```bash
curl http://localhost:5000/metrics
```

## Step 3: Check the Active Targets on Victoria Metrics
1. Check the status of the active targets in Victoria Metrics:
```bash
curl http://localhost:8428/targets
```

## Step 4: Query the Data Using the VMUI (Victoria Metrics UI)
Use the Victoria Metrics UI to run the following queries:
- **ovs_interface_tx_bytes**: Transferred bytes of data through the interface.
- **ovs_dp_br_if_total**: Total number of bridges.
- **openvswitch_datapath_stats_flows**: Packet flows.
- **openvswitch_datapath_stats_misses**: Missed packets.
- **openvswitch_datapath_stats_hits**: Packet hits.
```
