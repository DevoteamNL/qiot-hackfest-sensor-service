#!/bin/bash

podman run -d -p 8888:8888  --privileged --name=air-quality-sensor bentaljaard/air-quality-sensor:aarch64-1.0
cp *.service /etc/systemd/system
systemctl enable air-quality-sensor.service
systemctl start air-quality-sensor
#systemctl status air-quality-sensor