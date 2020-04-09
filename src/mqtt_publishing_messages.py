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

print("# 1. Creating new instance.")
client = mqtt.Client("P1")
client.connected_flag = False
client.bad_connection_flag = False

print("# 2. Attaching a message function & a toubleshoot function to callback")
# Bind all call back functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_log = on_log

print("# 3. Starting the loop")
# This time, I start looping first before I connect to the broker.
client.loop_start()

print("# 4. Connecting to broker")
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
print("# 5. Publishing to broker")
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
print("# 7. Stop the loop & Disconnect")
print("")
client.loop_stop()
client.disconnect()