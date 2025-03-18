import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # Change this to match your topic type
import json
import os

DATA_FILE = "data/data.json"

class ROS2Subscriber(Node):
    def __init__(self):
        super().__init__("ros2_json_collector")
        self.subscription = self.create_subscription(
            String,  # Change to the correct message type
            "sensor_data",  # Change to your ROS2 topic name
            self.listener_callback,
            10
        )
        self.subscription  # Prevent unused variable warning

    def listener_callback(self, msg):
        """Callback function that saves received ROS2 message as JSON."""
        data = {"sensor_data": msg.data}
        with open(DATA_FILE, "w") as file:
            json.dump(data, file)
        self.get_logger().info(f"Saved data: {data}")

def main(args=None):
    rclpy.init(args=args)
    node = ROS2Subscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
