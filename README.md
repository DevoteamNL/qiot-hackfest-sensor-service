# QIOT Hackfest Air Quality Sensor Service  

![Docker Image CI](https://github.com/DevoteamNL/qiot-hackfest-sensor-service/workflows/Docker%20Image%20CI/badge.svg)

This service interacts with the Enviroplus HAT (with particulate matter sensor) in order to provide air quality information via a REST api.

## Service Implementation

//TODO

## REST API

//TODO

## Building a docker container for deployment on the raspberry PI

The docker files are structured to provide either a build that can be compiled on the Raspberry PI itself, or (using multiarch) compile an aarch64 docker image on any x86_64 linux machine.

### Compiling in the raspberry itself

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
