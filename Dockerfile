# Raspberry Pi SHT31 sensor data MQTT publisher

# Base is official slim python image https://hub.docker.com/_/python/
FROM python:3-slim
MAINTAINER Asgaut Eng <asgaut@gmail.com>

RUN pip3 install smbus2 paho-mqtt
COPY sht31.py pub.py /

ENTRYPOINT ["python3", "/pub.py"]
