from prometheus_client import start_http_server, Gauge
import json
import time
import os

# Path to JSON data
DATA_FILE = "data/data.json"

# Define Prometheus metrics with labels for node identification
uc3_temperature_metric = Gauge("uc3_uc3_temperature", "uc3_temperature in Celsius", ["uc3_node_id"])
uc3_humidity_metric = Gauge("uc3_uc3_humidity", "uc3_humidity percentage", ["uc3_node_id"])
uc3_pressure_metric = Gauge("uc3_uc3_pressure", "uc3_pressure in hPa", ["uc3_node_id"])
uc3_cpu_usage_metric = Gauge("uc3_uc3_cpu_usage", "CPU usage percentage", ["uc3_node_id"])
uc3_memory_usage_metric = Gauge("uc3_uc3_memory_usage", "Memory usage percentage", ["uc3_node_id"])
uc3_disk_usage_metric = Gauge("uc3_uc3_disk_usage", "Disk usage percentage", ["uc3_node_id"])
uc3_network_latency_metric = Gauge("uc3_uc3_network_latency", "Network latency in ms", ["uc3_node_id"])
uc3_battery_level_metric = Gauge("uc3_uc3_battery_level", "Battery level percentage", ["uc3_node_id"])
sensor1_metric = Gauge("uc3_uc3_sensor1_reading", "Sensor 1 reading", ["uc3_node_id"])
sensor2_metric = Gauge("uc3_uc3_sensor2_reading", "Sensor 2 reading", ["uc3_node_id"])
last_seen_metric = Gauge("uc3_last_seen", "Timestamp of last data update", ["uc3_node_id"])

def update_metrics():
    """Reads JSON data and updates Prometheus metrics for multiple nodes."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                content = file.read().strip()

                # Check if file is empty
                if not content:
                    print("Warning: data.json is empty.")
                    return
                
                # Try parsing the JSON data correctly
                try:
                    data_list = json.loads(content)  # Convert string to JSON
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    return
                
                # Ensure data_list is actually a list
                if not isinstance(data_list, list):
                    print("Error: JSON data should be a list of dictionaries.")
                    return

                # Process each node's data
                for node_data in data_list:
                    if not isinstance(node_data, dict):
                        print(f"Skipping invalid entry: {node_data}")
                        continue

                    uc3_node_id = node_data.get("uc3_node_id", "unknown")  # Unique node identifier

                    # Update Prometheus metrics for this node
                    uc3_temperature_metric.labels(uc3_node_id=uc3_node_id).set(node_data.get("uc3_temperature", float('nan')))
                    uc3_humidity_metric.labels(uc3_node_id=uc3_node_id).set(node_data.get("uc3_humidity", float('nan')))
                    uc3_pressure_metric.labels(uc3_node_id=uc3_node_id).set(node_data.get("uc3_pressure", float('nan')))
                    uc3_cpu_usage_metric.labels(uc3_node_id=uc3_node_id).set(node_data.get("uc3_cpu_usage", float('nan')))
                    uc3_memory_usage_metric.labels(uc3_node_id=uc3_node_id).set(node_data.get("uc3_memory_usage", float('nan')))
                    uc3_disk_usage_metric.labels(uc3_node_id=uc3_node_id).set(node_data.get("uc3_disk_usage", float('nan')))
                    uc3_network_latency_metric.labels(uc3_node_id=uc3_node_id).set(node_data.get("uc3_network_latency", float('nan')))
                    uc3_battery_level_metric.labels(uc3_node_id=uc3_node_id).set(node_data.get("uc3_battery_level", float('nan')))
                    sensor1_metric.labels(uc3_node_id=uc3_node_id).set(node_data.get("uc3_sensor1_reading", float('nan')))
                    sensor2_metric.labels(uc3_node_id=uc3_node_id).set(node_data.get("uc3_sensor2_reading", float('nan')))
                    
                    # Set the last seen timestamp for this node
                    last_seen_metric.labels(uc3_node_id=uc3_node_id).set(time.time())

        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Start the Prometheus HTTP server on port 8001
    start_http_server(8001)
    print("Prometheus exporter running on http://localhost:8001/metrics")

    # Periodically update metrics
    while True:
        update_metrics()
        time.sleep(5)  # Update every 5 seconds
