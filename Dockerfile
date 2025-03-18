# Use the official ROS 2 Foxy Desktop base image
FROM osrf/ros:foxy-desktop

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt update && apt install -y \
    python3-colcon-common-extensions \
    python3-pip \
    python3-venv \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /app/venv

# Activate the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip, setuptools, and install required Python dependencies
RUN pip install --upgrade pip setuptools wheel colcon-common-extensions prometheus_client

# Setup ROS2 workspace
RUN mkdir -p /app/ros2_ws/src && cd /app/ros2_ws && \
    git clone -b foxy https://github.com/ros2/rclpy.git src/rclpy && \
    bash -c "source /opt/ros/foxy/setup.bash && colcon build --symlink-install --packages-select rclpy" && \
    echo "source /app/ros2_ws/install/setup.bash" >> /app/venv/bin/activate

# Copy application files
COPY . /app/

# Copy Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Ensure correct permissions for Python scripts
RUN chmod +x /app/app/generate_json.py /app/app/prometheus_exporter.py

# Expose necessary port for Prometheus metrics
EXPOSE 8001

# Start Supervisor to run both ROS 2-based data generator & Prometheus Exporter
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
