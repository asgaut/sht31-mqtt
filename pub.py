import paho.mqtt.client as paho
import time
import json
import sht31
import argparse

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT server, flags: "+str(flags)+" result code "+str(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected with rtn code {0}".format(rc))

def on_publish(client, userdata, mid):
    print("Message id {0} published".format(mid))

parser = argparse.ArgumentParser()
sensor = sht31.Sensor(address = 0x44)

parser.add_argument("-s", "--server", help="MQTT server to connect to", required=True)
parser.add_argument("-p", "--port", type=int, help="Port number to connect to", default=1883)
parser.add_argument("-t", "--topic", help="Topic prefix", default="sht31")
parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
args = parser.parse_args()

topic_prefix = args.topic
print("Topic prefix: " + topic_prefix)

client = paho.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect

if args.verbose:
    client.on_publish = on_publish

client.connect(args.server, args.port)
client.loop_start()

while True:
    (temperature, humidity) = sensor.read_temperature_humidity()
    data = {
        "temperature": temperature,
        "humidity": humidity
    }
    payload = json.dumps(data)
    # general topic
    (rc, mid) = client.publish(topic_prefix + "/json", payload, qos=1)
    # specific topics (recommended by HiveMQ)
    # https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices
    (rc, mid) = client.publish(topic_prefix + "/temperature", temperature, qos=1)
    (rc, mid) = client.publish(topic_prefix + "/humidity", humidity, qos=1)
    time.sleep(60)
