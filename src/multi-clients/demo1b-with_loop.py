#! c:\python34\python3
#!/usr/bin/env python
##demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
##Free to use for any purpose
##If you like and use this code you can
##buy me a drink here https://www.paypal.me/StepenCope
"""
Creates multiple Connections to a broker 
and sends and receives messages. Support SSL and Normal connections
uses the loop_start and stop functions just like a single client
Shows number of thread used
"""
import paho.mqtt.client as mqtt
import time
import json
import threading
import logging

#Note haven't included keys,client_id,client andcname as they are added later in the script
clients=[
{"broker":"test.mosquitto.org","port":1883,"name":"blank","sub_topic":"test1","pub_topic":"test1"},
{"broker":"broker.hivemq.com","port":1883,"name":"blank","sub_topic":"test2","pub_topic":"test2"}
]
nclients=len(clients)
message="test message"

out_queue=[] #use simple array to get printed messages in some form of order
##########
def multi_loop(nclients,flag=True):
   while flag:
      for i in range(nclients):
         client=clients[i]["client"]
         client.loop(0.01)

#########

def on_log(client, userdata, level, buf):
   print(buf)
def on_message(client, userdata, message):
   time.sleep(1)
   msg="message received",str(message.payload.decode("utf-8"))
   #print(msg)
   out_queue.append(msg)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        for i in range(nclients):
           if clients[i]["client"]==client:
              topic=clients[i]["sub_topic"]
              break
      
        client.subscribe(topic)
    else:
        print("Bad connection Returned code=",rc)
        client.loop_stop()  
def on_disconnect(client, userdata, rc):
   pass
   #print("client disconnected ok")
def on_publish(client, userdata, mid):
   time.sleep(1)
   print("In on_pub callback mid= "  ,mid)


def Create_connections():
   for i in range(nclients):
      cname="client"+str(i)
      t=int(time.time())
      client_id =cname+str(t) #create unique client_id
      client = mqtt.Client(client_id)             #create new instance
      clients[i]["client"]=client 
      clients[i]["client_id"]=client_id
      clients[i]["cname"]=cname
      broker=clients[i]["broker"]
      port=clients[i]["port"]
      try:
         client.connect(broker,port)           #establish connection
      except:
         print("Connection Fialed to broker ",broker)
         continue
      
      #client.on_log=on_log #this gives getailed logging
      client.on_connect = on_connect
      client.on_disconnect = on_disconnect
      #client.on_publish = on_publish
      client.on_message = on_message
      while not client.connected_flag:
         client.loop(0.01) #check for messages
         time.sleep(0.05)


mqtt.Client.connected_flag=False #create flag in class
no_threads=threading.active_count()
print("current threads =",no_threads)
print("Creating  Connections ",nclients," clients")

   
Create_connections()
t = threading.Thread(target=multi_loop,args=(nclients,True))#start multi loop
t.start()
print("All clients connected ")
time.sleep(5)
#
count =0
no_threads=threading.active_count()
print("current threads =",no_threads)
print("Publishing ")
Run_Flag=True
#this is a bad example when using the loop() call as the while loop
#as lots or sleep calls
try:
   while Run_Flag: 
      i=0
      for i in range(nclients):
         client=clients[i]["client"]
         pub_topic=clients[i]["pub_topic"]
         counter=str(count).rjust(6,"0")
         msg="client "+ str(i) +  " "+counter+"XXXXXX "+message
         if client.connected_flag:
            client.publish(pub_topic,msg)
            time.sleep(0.1)
            print("publishing client "+ str(i))
         i+=1
      time.sleep(10)#now print messages
      print("queue length=",len(out_queue))
      for x in range(len(out_queue)):
         print(out_queue.pop())
      count+=1
      #time.sleep(5)#wait
except KeyboardInterrupt:
   print("interrupted  by keyboard")

#client.loop_stop() #stop loop
for client in clients:
   client.disconnect()
multi_loop(flag=False) #stop loop
#allow time for allthreads to stop before existing
time.sleep(10)


