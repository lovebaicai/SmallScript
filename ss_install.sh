#!/bin/bash

yum install -y epel-release
yum install -y vim git wget zsh telnet docker docker-compose 
systemctl enable docker
systemctl start docker

docker run -d --restart=always -e PASSWORD=qf!!@6I9ZeEuyOgC -p8388:8388 -p8388:8388/udp -d shadowsocks/shadowsocks-libev
