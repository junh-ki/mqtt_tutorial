# This tutorial is done with python version 3.6.8 on Windows 10
# On Command Prompt, install the mqtt client first with (pip install paho-mqtt)

import paho.mqtt.client as mqtt
# broker_address = "iot.eclipse.org" # doesn't work at the moment somehow
import time

####################################################################
def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic =", message.topic)
    print("message qos =", message.qos)
    print("message retain flag =", message.retain)
####################################################################

broker_address = "test.mosquitto.org"

print("# 1. Creating new instance.")
client = mqtt.Client("P1")

print("# 2. Attaching function to callback")
client.on_message = on_message # without parentheses

print("# 3. Connecting to broker")
client.connect(broker_address)

print("# 4. Starting the loop")
client.loop_start()

print("# 5. Subscribe to topic", "house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")

print("# 6. Publish message to topic", "house/bulbs/bulb1")
client.publish("house/bulbs/bulb1", "OFF")

print("# 7. Wait & Stop the loop")
time.sleep(4)
client.loop_stop()
