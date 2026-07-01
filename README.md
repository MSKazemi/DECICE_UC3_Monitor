# DECICE UC3 Monitor — ROS 2 + Prometheus + Kubernetes Edge Telemetry

Monitoring and observability for **Use Case 3 (UC3)** of the EU Horizon Europe
**DECICE** project. DECICE UC3 Monitor collects per-node sensor and system
telemetry, converts it into **Prometheus** metrics, and exposes them for
scraping — packaged as a **Docker** container and deployable to **Kubernetes**.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![ROS 2](https://img.shields.io/badge/ROS%202-Foxy-blueviolet)
![Prometheus](https://img.shields.io/badge/Prometheus-exporter-orange)
![Kubernetes](https://img.shields.io/badge/Kubernetes-ready-326ce5)
![Docker](https://img.shields.io/badge/Docker-container-2496ed)

---

## What is this?

DECICE UC3 Monitor is an open-source monitoring stack that turns edge/IoT node
telemetry into Prometheus metrics for the DECICE Use Case 3 deployment.

- It is for **researchers and engineers** running the DECICE UC3 scenario, and
  anyone who needs a minimal ROS 2 → Prometheus → Kubernetes telemetry bridge.
- It solves the problem of **making edge node sensor and resource-usage data
  observable** in a standard Prometheus/Grafana monitoring pipeline.
- Use it when you need to **collect data from a ROS 2 topic (or a simulated
  source) and expose it as scrapeable `/metrics`** inside a Kubernetes cluster.
- It is different from a general-purpose exporter (e.g. `node_exporter`) because
  it is **purpose-built for the DECICE UC3 node/sensor schema** and bundles a
  ROS 2 subscriber alongside the exporter.
- It is **not** a full observability platform — it does not include Prometheus,
  Grafana, alerting, or long-term storage; it is the **exporter/producer** side
  of that stack.

## Role in DECICE

[DECICE](https://www.decice.eu/) (Device-Edge-Cloud Intelligent Collaboration
framEwork) is an EU Horizon Europe project building an AI-based, open, and
portable framework for scheduling and optimizing workloads across a federated
cloud–edge–HPC continuum. This repository provides the **monitoring/telemetry
component for DECICE Use Case 3**, feeding node- and sensor-level metrics into
the observability layer that DECICE decision-making relies on.

## Architecture

The container runs two long-lived processes, supervised by **Supervisor**:

```
  ROS 2 topic ("sensor_data")                simulated node/sensor data
            │                                          │
            ▼                                          ▼
  app/ros2_subscriber.py                     app/generate_json.py
            │                                          │
            └──────────────► data/data.json ◄──────────┘
                                   │
                                   ▼
                     app/prometheus_exporter.py
                                   │
                                   ▼
                 Prometheus metrics on :8001/metrics
                                   │
                                   ▼
             Kubernetes Service + NGINX Ingress (namespace uc3)
```

- **`app/prometheus_exporter.py`** — reads `data/data.json` and publishes
  Prometheus gauges (labeled per `uc3_node_id`) on port **8001**, refreshing
  every 5 seconds.
- **`app/generate_json.py`** — generates simulated multi-node sensor/system data
  every 10 seconds (useful for testing without a live ROS 2 source).
- **`app/ros2_subscriber.py`** — a ROS 2 (`rclpy`) subscriber for the
  `sensor_data` topic that persists received messages to `data/data.json`.

> Note: the bundled `supervisord.conf` starts `generate_json.py` (simulated
> data) together with the exporter. Swap it for `ros2_subscriber.py` to ingest
> live ROS 2 telemetry.

## Metrics exposed

All gauges are labeled by `uc3_node_id`:

| Metric | Description | Unit |
|---|---|---|
| `uc3_uc3_temperature` | Temperature | °C |
| `uc3_uc3_humidity` | Humidity | % |
| `uc3_uc3_pressure` | Pressure | hPa |
| `uc3_uc3_cpu_usage` | CPU usage | % |
| `uc3_uc3_memory_usage` | Memory usage | % |
| `uc3_uc3_disk_usage` | Disk usage | % |
| `uc3_uc3_network_latency` | Network latency | ms |
| `uc3_uc3_battery_level` | Battery level | % |
| `uc3_uc3_sensor1_reading` | Sensor 1 reading | — |
| `uc3_uc3_sensor2_reading` | Sensor 2 reading | — |
| `uc3_last_seen` | Timestamp of last data update | Unix seconds |

## Prerequisites

- Docker
- Kubernetes (for cluster deployment)
- ROS 2 Foxy (for live ROS 2 ingestion)
- Python 3.12

## Quickstart

### Build the Docker image

```sh
docker build -t uc3-monitoring .
```

### Run the container

```sh
docker run -p 8001:8001 uc3-monitoring
```

Metrics are then available at:

```
http://localhost:8001/metrics
```

Expected output (excerpt):

```
# HELP uc3_uc3_temperature uc3_temperature in Celsius
# TYPE uc3_uc3_temperature gauge
uc3_uc3_temperature{uc3_node_id="uc3-node-01"} 24.71
uc3_uc3_cpu_usage{uc3_node_id="uc3-node-01"} 63.20
uc3_last_seen{uc3_node_id="uc3-node-01"} 1.7...e+09
```

## Deploying to Kubernetes

Apply the bundled manifest (Deployment + Service + NGINX Ingress in the `uc3`
namespace):

```sh
kubectl apply -f app/k8s_deployment.yaml
```

In the cluster, metrics are exposed via the Ingress host
`monitoring.uc3.local` at the `/metrics` path (edit the manifest to match your
image, host, and data volume).

## Build and push the image

```sh
docker build -t your-docker-username/uc3-monitoring .
docker push your-docker-username/uc3-monitoring
```

Replace `your-docker-username` with your registry namespace and update the
`image:` field in `app/k8s_deployment.yaml`.

## Components

- **ROS 2 subscriber** — [`app/ros2_subscriber.py`](app/ros2_subscriber.py):
  subscribes to the `sensor_data` topic and writes messages to
  `data/data.json`.
- **Prometheus exporter** — [`app/prometheus_exporter.py`](app/prometheus_exporter.py):
  reads the JSON and exposes metrics on port 8001.
- **Data generator** — [`app/generate_json.py`](app/generate_json.py):
  produces simulated node/sensor data for testing.
- **Supervisor config** — [`supervisord.conf`](supervisord.conf): starts and
  monitors the data process and the exporter inside the container.
- **Kubernetes manifest** — [`app/k8s_deployment.yaml`](app/k8s_deployment.yaml).

## Use cases

- Exposing DECICE UC3 edge-node telemetry to a Prometheus/Grafana stack.
- Prototyping a ROS 2 → Prometheus → Kubernetes monitoring pipeline.
- Demonstrating cloud–edge observability for the DECICE continuum.

## Limitations / when NOT to use

- Ships only the **exporter/producer** — bring your own Prometheus, Grafana,
  and alerting.
- The default container runs **simulated data**; wire in `ros2_subscriber.py`
  for real ROS 2 telemetry.
- Uses a simple file (`data/data.json`) as the hand-off between producer and
  exporter — not intended for high-frequency or high-cardinality workloads.
- Targets **ROS 2 Foxy**; other distributions may need Dockerfile changes.

## FAQ

**Q: What port are the metrics on?** Port `8001`, at `/metrics`.

**Q: Do I need ROS 2 to try it?** No — the default setup uses the simulated
data generator, so you can run the container and see metrics immediately.

**Q: How are per-node metrics distinguished?** Every gauge carries a
`uc3_node_id` label (e.g. `uc3-node-01`).

**Q: Which ROS 2 topic and message type?** The subscriber listens on
`sensor_data` using `std_msgs/String`; adjust for your own topic and type.

## Acknowledgement — EU funding

DECICE UC3 Monitor is developed in the context of the **DECICE** project
(Device-Edge-Cloud Intelligent Collaboration framEwork), funded by the
**European Union's Horizon Europe** research and innovation programme under
**Grant Agreement No. 101092582**. Project website:
[https://www.decice.eu/](https://www.decice.eu/).

## License

This project is licensed under the MIT License.
