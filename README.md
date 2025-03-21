# DECICE UC3 Monitoring

This project sets up a monitoring system using ROS2, Prometheus, and Kubernetes. The system includes a ROS2 subscriber that collects sensor data and a Prometheus exporter that exposes the data for monitoring.

## Prerequisites

- Docker
- Kubernetes
- ROS2 Foxy
- Python 3.12

## Building the Docker Image

To build the Docker image, run the following command:

```sh
docker build -t uc3-monitoring .
```

## Running the Docker Container

To run the Docker container, use the following command:

```sh
docker run -p 8001:8001 uc3-monitoring
```

## Deploying to Kubernetes

To deploy the application to a Kubernetes cluster, apply the Kubernetes deployment configuration:

```sh
kubectl apply -f k8s_deployment.yaml
```

## ROS2 Subscriber

The ROS2 subscriber collects sensor data from a specified ROS2 topic and saves it as JSON. The subscriber is implemented in [`app/ros2_subscriber.py`](app/ros2_subscriber.py).

### Running the ROS2 Subscriber

The ROS2 subscriber is managed by Supervisor and runs automatically when the Docker container starts. It subscribes to the `sensor_data` topic and saves the received data to `data/data.json`.

## Prometheus Exporter

The Prometheus exporter reads the JSON data generated by the ROS2 subscriber and exposes it as Prometheus metrics. The exporter is implemented in [`app/prometheus_exporter.py`](app/prometheus_exporter.py).

### Running the Prometheus Exporter

The Prometheus exporter is also managed by Supervisor and runs automatically when the Docker container starts. It exposes the metrics on port 8001.

## Supervisor Configuration

The Supervisor configuration is defined in [`supervisord.conf`](supervisord.conf). It ensures that both the ROS2 subscriber and Prometheus exporter are started and monitored.

## Exposing Metrics

The Prometheus metrics are exposed at `http://localhost:8001/metrics` when running the Docker container locally. In a Kubernetes deployment, the metrics are exposed through an Ingress defined in [`app/k8s_deployment.yaml`](app/k8s_deployment.yaml).

## Building and Pushing Docker Image

To build and push the Docker image to a registry, use the following commands:

```sh
docker build -t your-docker-username/uc3-monitoring .
docker push your-docker-username/uc3-monitoring
```

Replace `your-docker-username` with your actual Docker Hub username.

## License

This project is licensed under the MIT License.
