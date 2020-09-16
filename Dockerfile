FROM multiarch/debian-debootstrap:arm64-stretch-slim

RUN apt-get clean
RUN apt-get update

RUN apt-get install -y python3-pip libportaudio2 python3-pil python3-setuptools python3-numpy python3-cffi python3-smbus

RUN pip3 install spidev vcgencmd rpi.gpio enviroplus

WORKDIR /usr/src/app
COPY examples/* ./
CMD ["python3", "all-in-one.py"]
