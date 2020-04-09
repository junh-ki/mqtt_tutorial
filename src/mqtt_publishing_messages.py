import paho.mqtt.client as mqtt
import time
import logging
# Choose one of the followings to set the broker address
mosquitto = "test.mosquitto.org"
hivemq = "broker.hivemq.com"
eclipse = "iot.eclipse.org" # doesn't work at the moment somehow
broker_address = mosquitto
port = 1883
logging.basicConfig(level = logging.INFO)
#use DEBUG, INFO, WARNING

def on_log(client, userdata, level, buf):
    """
    Troubleshoot function to procee the logging callback.
    It simply prints the log message.
    """
    logging.info(buf)

def on_connect(client, userdata, flags, rc):
    """
    - From the imported client.py:
    called when the broker responds to our connection request.
    """
    if rc == 0:
        client.connected_flag = True
        logging.info("Connected OK")
        # client.subscrube(topic)
    else:
        client.bad_connection_flag = True
        logging.info("Bad Connection, Returned Code = " + str(rc))
        client.loop_stop()

def on_disconnect(client, userdata, rc):
    """
    - From the imported client.py:
    called when the client disconnects from the broker.
    The 'rc' parameter indicates the disconnection state.
    """
    client.connected_flag = False
    logging.info("Client Disconnected OK, Result Code = " + str(rc))
    
def on_publish(client, userdata, mid):
    logging.info("In on_pub callback mid = " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
    logging.info("Subscribed")

def on_message(client, userdata, message):
    """
    Callback function, which basically just prints the received messages
        - From the imported client.py: called when a message has been received 
        on a topic that the client subscribes to. The message variable is a
        MQTTMessage that describes all of the message parameters.
    """
    topic = message.topic   # ??
    msgr = str(message.payload.decode("utf-8"))
    msgr = "Message Received " + msgr
    logging.info(msgr)

def reset():
    ret = client.publish("house/bulb1", "", 0, True)    # publish

print("# 1. Create new instance.")
client = mqtt.Client("P1")
client.connected_flag = False
client.bad_connection_flag = False

print("# 2. Attach callback functions to callbacks")
# Bind all call back functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_log = on_log

print("# 3. Start the loop")
# This time, I start looping first before I connect to the broker.
client.loop_start()

print("# 4. Connect to broker")
try:
    client.connect(broker_address, port)    #establish connection
    while not client.connected_flag: # wait in loop
        print("In Wait Loop")
        time.sleep(1)
except:
    print("Connection Failed.")
    sys.exit(1) # It should quit or raise flag to quit or retry.
time.sleep(3)

print("")
print("# 5. Publish to broker")
print("")
ret = client.publish("house/bulb1", "Test message 0", 0) #publish
print("published return =", ret)
#client.loop()
time.sleep(3)
print("")
ret = client.publish("house/bulb1", "Test message 1", 1) #publish
print("published return =", ret)
#client.loop()
time.sleep(3)
print("")
ret = client.publish("house/bulb1", "Test message 2", 2) #publish
print("published return =", ret)
#client.loop()
time.sleep(3)

print("")
print("# 6. Subscribe to the topic")
client.subscribe("house/bulb1", 2)
time.sleep(10) #delay to catch any messages coming through
#client.loop()
#reset()

print("")
print("# 7. Stop the loop & Disconnect")
print("")
client.loop_stop()
client.disconnect()
