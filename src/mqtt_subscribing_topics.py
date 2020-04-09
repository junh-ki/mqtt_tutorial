import paho.mqtt.client as mqtt
import time
import logging
import sys
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
    logging.info("in on subscribe callback result " + str(mid))
    for topic in topic_ack:
        if topic[1] == mid:
            # mid value here is compared with the ret[1] that is also mid. 
            # see the subscribe > try > if part
            topic[2] = 1 #set acknowledged flag
            logging.info("subscription acknowledged  " + topic[0])
            client.suback_flag = True
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

def check_subs():
    #returns flase if have an unacknowledged subsription
    for topic in topic_ack:
        if topic[2] == 0:
            logging.info("subscription to "+ topic[0] + " not acknowledged")
            return(False)
    return True 

mqtt.Client.connected_flag=False#create flag in class

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

################################################################################
print("# 3. Prepare a list of topic tuples - ")
topics = [("house/lights/bulb1", 0), ("house/lights/bulb2", 1)]
# The second argument for each tuple represents QoS (should be either 0, 1 or 2. 
# Otherwise, you will get an invalid QoS level error.)
topic_ack = []

print("# 4. Connect to broker - ", broker_address)
try:
    client.connect(broker_address, port)    #establish connection
except:
    print("Connection Failed.")
    sys.exit(1) # It should quit or raise flag to quit or retry.
client.loop_start()
while not client.connected_flag: # wait in loop
    print("In Wait Loop")
    time.sleep(1)

print("# 5. Subscribe " + str(topics))
# try:
#     ret = client.subscribe(topics)
#     if ret[0] == 0:
#         logging.info("subscribed to topic " + str(topics) 
#             + ", return code " + str(ret)) 
#         # return code (0-success, 1 2... - packet_id)
#         topic_ack.append([topics, ret[1], 0]) #keep track of subscription
#         # the ret[1] value here is compared with the mid value 
#         # in the on_subscribe method
#     else:
#         logging.info("error on subscribing " + str(ret))
#         client.loop_stop()
#         sys.exit(1)
# except Exception as e:
#     logging.info("error on subscribe" + str(e))
#     client.loop_stop()
#     sys.exit(1)

for topic in topics:
    try:
        ret = client.subscribe(topic) # topic = a tuple ("topic", QoS)
        # The subscribe function returns a tuple to indicate success, 
        # and also a message id(mid) which is used as a tracking code.
        # (success_code, mid-packet_id) success_code: 0 success/ else failure
        if ret[0] == 0:
            logging.info("subscribed to topic " + str(topic[0]) 
                + ", return code " + str(ret)) 
            # return code (0-success, 1 2... - packet_id)
            topic_ack.append([topic[0], ret[1], 0]) #keep track of subscription
            # the ret[1] value here is compared with the mid value 
            # in the on_subscribe method
        else:
            logging.info("error on subscribing " + str(ret))
            client.loop_stop()
            sys.exit(1)
    except Exception as e:
        logging.info("error on subscribe" + str(e))
        client.loop_stop()
        sys.exit(1)

print("6. Waiting for all subs")
while not check_subs():
    time.sleep(1)
################################################################################
time.sleep(3)
msg = "off"
print("Publishing topic = ", topics[0][0], ", message = ", msg)
client.publish(topics[0][0], msg)
time.sleep(4)
client.loop_stop()
client.disconnect()
