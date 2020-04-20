#!/bin/bash
sudo yum install -y epel-release
sudo yum install -y vim git wget zsh telnet docker docker-compose 
sudo systemctl enable docker
sudo systemctl start docker

sudo docker run -d --restart=always -e PASSWORD=qf!!@6I9ZeEuyOgC -p8388:8388 -p8388:8388/udp -d shadowsocks/shadowsocks-libev
