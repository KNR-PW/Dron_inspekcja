#!/bin/bash

# Install ROS2 base and development tools
apt install ros-humble-ros-base -y
apt install ros-dev-tools -y

# Configure shell to source ROS2 setup
# Optionally, you could append the ROS2 setup to your bashrc:
# echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
echo 'source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash' >> ~/.bashrc

