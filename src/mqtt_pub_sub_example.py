import paho.mqtt.client as mqtt
# broker_address = "iot.eclipse.org" # doesn't work at the moment somehow
broker_address = "test.mosquitto.org"

print("# 1. Creating new instance.")
client = mqtt.Client("P1")

print("# 2. Connecting to broker")
client.connect(broker_address)

print("# 3. Subscribe to topic", "house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")

print("# 4. Publish message to topic", "house/bulbs/bulb1")
client.publish("house/bulbs/bulb1", "OFF")
