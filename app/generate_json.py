import json
import time
import random
import os

# Define the file path
DATA_FILE = "data/data.json"

# Ensure the data directory exists
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

# List of unique node IDs (you can add more nodes here)
uc3_node_idS = ["uc3-node-01", "uc3-node-02", "uc3-node-03"]

def generate_random_data():
    """Generate random test sensor data for multiple nodes and save it as JSON."""
    nodes_data = []
    
    for uc3_node_id in uc3_node_idS:
        node_data = {
            "uc3_node_id": uc3_node_id,
            "uc3_temperature": round(random.uniform(20, 30), 2),  # °C
            "uc3_humidity": round(random.uniform(40, 70), 2),  # %
            "uc3_pressure": round(random.uniform(990, 1030), 2),  # hPa
            "uc3_cpu_usage": round(random.uniform(10, 90), 2),  # %
            "uc3_memory_usage": round(random.uniform(30, 90), 2),  # %
            "uc3_disk_usage": round(random.uniform(40, 95), 2),  # %
            "uc3_network_latency": round(random.uniform(5, 50), 2),  # ms
            "uc3_battery_level": random.randint(0, 100),  # %
            "uc3_sensor1_reading": round(random.uniform(5, 20), 2),
            "uc3_sensor2_reading": round(random.uniform(1, 10), 2)
        }
        nodes_data.append(node_data)

    # Save data to JSON file
    with open(DATA_FILE, "w") as file:
        json.dump(nodes_data, file, indent=4)

    print(f"Generated Data: {nodes_data}")

if __name__ == "__main__":
    while True:
        generate_random_data()
        time.sleep(10)  # Wait 10 seconds before generating new data
