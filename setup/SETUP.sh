#!/bin/bash

print_color() {
    case $1 in
        red)    echo -e "\e[31m$2\e[0m" ;;
        green)  echo -e "\e[32m$2\e[0m" ;;
        blue)   echo -e "\e[34m$2\e[0m" ;;
        *)      echo "Usage: print_color {red|green|blue} \"your text\"" ;;
    esac
}

print_color blue "update, upgrade"

sudo apt update -y
sudo apt upgrade -y

print_color blue "instalowanie nvim, neofetch, htop"

sudo apt install -y neovim

sudo apt install -y neofetch

sudo apt install -y htop


print_color blue "instalowanie dockera"

curl -sSL https://get.docker.com | sh

print_color blue "Tworzenie kontenera ROSem"

sudo docker build . -t inspekcja:humple-pi5-v1

sudo docker run -it \
    --name=ros2_humble \
    --net=host \
    --privileged \
    -v /dev:/dev \
    inspekcja:humple-pi5-v1 \
    bash

#    -it: Allocates a pseudo-TTY and keeps STDIN open, allowing interaction with the container.
#     --name=ros2_humble: Specifies the name of the container as ros2_humble
#    --net=host: Shares the network namespace with the host, allowing the container to use the host network interface.
#    --privileged: Runs the container in privileged mode, giving it access to all devices on the host.
#    -v /dev:/dev: Mounts the host's /dev directory into the container, giving the container access to all device files on the host.
#    inspekcja:humple-pi5-v1: Specifies the name of the Docker image to use when creating the container.
#    bash: Specifies the command to run inside the container. In this case, it starts a Bash shell.

print_color blue "Remote connection install"

sudo apt install rpi-connect

rpi-connect on

print_color blue "Zalogowanie się do zdalego połączenia - rpi connect"

rpi-connect rpi-connect signin 
