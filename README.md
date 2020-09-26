# QIOT Hackfest Air Quality Sensor Service  

![Docker Image CI](https://github.com/DevoteamNL/qiot-hackfest-sensor-service/workflows/Docker%20Image%20CI/badge.svg)

This service interacts with the Enviroplus HAT (with particulate matter sensor) in order to provide air quality information via a REST api. For more details about the Enviroplus, have a look at their getting started tutorial: https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-plus

## Service Implementation

The sensor service is implemented in Python3 using the standard pimoroni libraries. A simple REST api is made available to allow other services to query the gas and pollution information provided by the sensor. The application is packaged as a docker image that is then able to run on the raspberry. Note that this container will run as a privileged container as it needs to connect to the GPIO pins and low-level components in order to retrieve the values from the sensors.


## REST API

The sensor service exposes 2 simple APIs:

| Gas API Endpoint | HTTP Method |
| ---------- | ---------- |
| /gas | GET | 

Example Response:

```JSON 
{
    "instant": "2020-09-23T13:52:05.897899Z",
    "adc": 0.614,
    "nh3": 140178.34394904462,
    "oxidising": 27130.904183535764,
    "reducing": 354666.66666666686
} 
```

| Pollution API Endpoint | HTTP Method |
| ---------- | ---------- |
| /pollution | GET | 

Example Response:

```JSON 
{
    "instant": "2020-09-23T10:47:42.953579Z",
    "pm1_0": 44,
    "pm2_5": 63,
    "pm10": 65,
    "pm1_0_atm": 31,
    "pm2_5_atm": 46,
    "pm10_atm": 56,
    "gt0_3um": 7254,
    "gt0_5um": 2258,
    "gt1_0um": 382,
    "gt2_5um": 16,
    "gt5_0um": 4,
    "gt10um": 0
} 
```



## Building a docker container for deployment on the raspberry PI

The docker files are structured to provide either a build that can be compiled on the Raspberry PI itself, or (using multiarch) compile an aarch64 docker image on any x86_64 linux machine. https://github.com/DevoteamNL/fedora.git

### Compiling on the raspberry itself

Run the following to build the docker image:

```
podman build -t [docker image tag name] -f Dockerfile.fedora .
```


### Cross-compiling on another x86_64 linux host

First enable the host to use binfmt in order to allow architecture emulation using qemu

``` 
# configure binfmt-support on the Docker host (works locally or remotely, i.e: using boot2docker)
docker run --rm --privileged multiarch/qemu-user-static:register --reset
```

Now you can compile aarch64 docker containers

```
docker build -t [docker image tag name] -f Dockerfile.fedora.multiarch .
```
