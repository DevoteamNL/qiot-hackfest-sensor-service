#!/bin/bash

podman run -d -p 8888:8888 --network=qiot --privileged --name=air-quality-sensor bentaljaard/air-quality-sensor:aarch64-latest
cp *.service /etc/systemd/system
systemctl enable air-quality-sensor.service
systemctl start air-quality-sensor
#systemctl status air-quality-sensor
