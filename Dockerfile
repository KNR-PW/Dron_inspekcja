FROM ubuntu:jammy 

RUN locale  # check for UTF-8
RUN apt update && apt install locales -y
RUN locale-gen pl_PL pl_PL.UTF-8
RUN update-locale LC_ALL=pl_PL.UTF-8 LANG=pl_PL.UTF-8
RUN export LANG=pl_PL.UTF-8

# Set the timezone
ENV ROS_VERSION=2
ENV ROS_DISTRO=humble
ENV ROS_PYTHON_VERSION=3
ENV TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Add the necessary repository and update the system packages
RUN apt install software-properties-common -y
RUN add-apt-repository universe
RUN apt update && apt install curl -y
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null
RUN apt update && apt upgrade -y

# Set the working directory and copy the scripts
WORKDIR /ros2_project
COPY install_ros2.sh /ros2_project/

# Make the scripts executable and execute them
RUN chmod +x ./*.sh
RUN ./install_ros2.sh
