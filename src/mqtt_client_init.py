"""
This module offers the means to initialize the flags of your mqtt client.
From (http://www.steves-internet-guide.com/client-objects-python-mqtt/)
"""
import paho.mqtt.client as mqtt

class MQTTClient(mqtt.Client):
   """
   MQTT client sub-class with a constructor initializing flags
   """
   def __init__(self,cname,**kwargs):
        """
        """
        super(MQTTClient, self).__init__(cname,**kwargs)
        self.last_pub_time=time.time()
        self.topic_ack=[]
        self.run_flag=True
        self.subscribe_flag=False
        self.bad_connection_flag=False
        self.connected_flag=True
        self.disconnect_flag=False
        self.disconnect_time=0.0
        self.pub_msg_count=0
        self.devices=[]

def Initialise_clients(cname):
    """
    callback assignments & flags setting
    """
    client= mqtt.Client(cname,False)    #don't use clean session
    if mqttclient_log:                  #enable mqqt client logging
        client.on_log=on_log
    client.on_connect= on_connect       #attach function to callback
    client.on_message=on_message        #attach function to callback
    client.on_subscribe=on_subscribe
    #flags set
    client.topic_ack=[]
    client.run_flag=False
    client.running_loop=False
    client.subscribe_flag=False
    client.bad_connection_flag=False
    client.connected_flag=False
    client.disconnect_flag=False
    return client
