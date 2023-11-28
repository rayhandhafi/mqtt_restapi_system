import paho.mqtt.client as paho
import random
import time
from datetime import datetime

#MQTT Topics
mqttTemp1 = "test/iot/temp1"
mqttInput1 = "test/iot/input1"
pe = "test/iot/pe"

#HiveMQInit
def on_connect(client, userdata, flag, rc, properties=None):
    print("CONNACK received code %s." %rc)
client = paho.Client(client_id="", userdata=None,protocol=paho.MQTTv5)
client.connect("broker.hivemq.com", 1883)

def simulate_temperature():
    temperature = random.uniform(-1, 1) * 5 + 40
    client.publish(mqttTemp1, payload=temperature,qos=1)
    print("T1 = ",temperature)

# Function to handle user input and publish to M02 using MQTT
def send_user_input():
    user_input = input("Enter a message to send to M02: ")
    client.publish(mqttInput1, payload=user_input,qos=1)

send_user_input()
simulate_temperature()

mess = ["A"*50,
        "B"*100,
        "C"*150,
        "D"*200,
        "E"*250]
sep = ";;"

for mess in mess:
    start = datetime.now().timestamp()
    msg=mess + sep + str(start)
    client.publish(pe,payload=msg,qos=1)
    print("Performance Evaluation (START): ", msg)
    time.sleep(2)

client.disconnect()
