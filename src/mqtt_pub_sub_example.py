# This tutorial is done with python version 3.6.8 on Windows 10
# On Command Prompt, install the mqtt client first with (pip install paho-mqtt)

import paho.mqtt.client as mqtt
import time

####################################################################
def on_log(client, userdata, level, buf):
    """
    Troubleshoot function to procee the logging callback.
    It simply prints the log message.
    """
    print("log: ", buf)

def on_connect(client, userdata, flags, rc):
    """
    - From the imported client.py:
    called when the broker responds to our connection request.
    """
    if rc == 0:
        client.connected_flag = True
        print("Connected OK, Returned code =", rc)
        # client.subscrube(topic)
    else:
        print("Bad connection Returned code =", rc)

def on_disconnect(client, userdata, flags, rc=0):
    """
    - From the imported client.py:
    called when the client disconnects from the broker.
    The 'rc' parameter indicates the disconnection state.
    """
    print("DisConnected result code " + str(rc))

def on_message(client, userdata, message):
    """
    Callback function, which basically just prints the received messages
        - From the imported client.py: called when a message has been received 
        on a topic that the client subscribes to. The message variable is a
        MQTTMessage that describes all of the message parameters.
    """
    print("\t- message received =", str(message.payload.decode("utf-8")))
    print("\t- message topic =", message.topic)
    print("\t- message qos =", message.qos)
    print("\t- message retain flag =", message.retain)
####################################################################


# Choose one of the followings to set the broker address
mosquitto = "test.mosquitto.org"
hivemq = "broker.hivemq.com"
eclipse = "iot.eclipse.org" # doesn't work at the moment somehow

broker_address = mosquitto

print("# 1. Creating new instance.")
client = mqtt.Client("P1")
client.connected_flag = False

print("# 2. Attaching a message function & a toubleshoot function to callback")
# Bind all call back functions
client.on_connect = on_connect # Without parentheses
client.on_disconnect = on_disconnect # Without parentheses
client.on_message = on_message # Without parentheses
#client.on_log = on_log # without parentheses

print("# 3. Connecting to broker")
client.connect(broker_address) # This triggers the on_connect callback

print("# 4. Starting the loop")
client.loop_start()

print("# 5. Subscribe to topic", "house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")

print("# 6. Publish message to topic", "house/bulbs/bulb1")
client.publish("house/bulbs/bulb1", "OFF")

print("# 7. Wait & Stop the loop")
while not client.connected_flag:
    time.sleep(1)
client.loop_stop()
client.disconnect()
