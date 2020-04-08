# This tutorial is done with python version 3.6.8 on Windows 10
# On Command Prompt, install the mqtt client first with (pip install paho-mqtt)

import paho.mqtt.client as mqtt
import time
import sys

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
        print("Bad Connection, Returned code =", rc)
        client.bad_connection_flag = True

def on_disconnect(client, userdata, flags, rc=0):
    """
    - From the imported client.py:
    called when the client disconnects from the broker.
    The 'rc' parameter indicates the disconnection state.
    """
    print("DisConnected Result code = " + str(rc))
    client.connected_flag = False

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
client.bad_connection_flag = False

print("# 2. Attaching a message function & a toubleshoot function to callback")
# Bind all call back functions
client.on_connect = on_connect # Without parentheses
client.on_disconnect = on_disconnect # Without parentheses
client.on_message = on_message # Without parentheses
#client.on_log = on_log # without parentheses


print("# 3. Starting the loop")
# This time, I start looping first before I connect to the broker.
client.loop_start()

print("# 4. Connecting to broker")
try:
    client.connect(broker_address) # connect to broker
    while not client.connected_flag: # wait in loop
        print("In Wait Loop")
        time.sleep(1)
except:
    print("Connection Failed.")
    sys.exit(1) # It should quit or raise flag to quit or retry.

run_flag = True
count = 1
# To demonstrate if it automatically connects to the broker when the broker is 
# turned off and on again.
while run_flag:
    print("In Main Loop...")
    msg = "test message " + str(count)
    ret = client.publish("house/2", "test message", 0) # topic, payload, QoS
    print("Publish", ret)
    count += 1
    time.sleep(4)

client.loop_stop()
client.disconnect()
