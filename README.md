# Docker image for publishing SHT31 sensor data to MQTT server

## Building

```sh
$ docker build -t sht31pub .
```

## Running

```sh
$ docker run -d --name sht31publisher --restart=unless-stopped --device /dev/i2c-1 sht31pub -s host.example.com -t skycam/sht31
```

This runs pub.py which publishes measurements to host.example.com.
Default port is 1883.
Default topic is "sht31".

## Example published data

```
asgaut@droplet1:~$ mosquitto_sub -h localhost -t "skycam/#" -v
skycam/sht31/json {"temperature": 4.128709849698637, "humidity": 38.106355382619974}
skycam/sht31/temperature 4.128709849698637
skycam/sht31/humidity 38.106355382619974
```
