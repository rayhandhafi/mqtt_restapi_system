import paho.mqtt.client as paho
from datetime import datetime

def on_connect(client, userdata, flag, rc, properties=None):
    print("CONNACK received code %s." %rc)

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect=on_connect
client.connect("broker.hivemq.com",1883)


sep = ";;"
def on_message(client, userdata, msg):
    msg = msg.payload.decode("utf-8")
    print("Performance Evaluation (END)> ", msg)
    timeSend = msg.split(sep)[1]
    end = datetime.now().timestamp()
    delay = end - float(timeSend)
    print("delay = ", delay, " seconds")

client.on_message = on_message
client.subscribe("test/iot/pe", qos=1)
client.loop_forever()