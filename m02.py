from flask import Flask, jsonify
import paho.mqtt.client as paho
import threading
import random
from datetime import datetime

# Initial values
k = 0.5
adc_min = 0
adc_max = 128

#HiveMQInit
def on_connect(client, userdata, flag, rc, properties=None):
    print("CONNACK received code %s." %rc)

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect=on_connect
client.connect("broker.hivemq.com",1883)

#MQTT Topics
mqttInput1 = "test/iot/input1"
pe = "test/iot/pe"
# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    global k
    sep=";;"
    message = msg.payload.decode()

    if message == "DEC01":
        k -= 0.1
    elif message == "DEC02":
        k -= 0.2
    elif message == "INC01":
        k += 0.1
    elif message == "INC02":
        k += 0.2
    else:
        print(f"Error! Unrecognized Input")
    print(f"Received user input: {message}. Updated k: {k}")

    
client.on_message = on_message
client.subscribe(mqttInput1,qos=1)


# Flask setup
app = Flask(__name__)


# Function to generate temperature using the specified formula
def genTemp(adc_val):
    return k * adc_val + 5


if __name__ == '__main__':

    # Start a thread for MQTT loop
    mqtt_thread = threading.Thread(target=client.loop_forever)
    mqtt_thread.start()

    # Flask route to get sensor state
    @app.route('/sensor2', methods=['GET'])
    def sensor2():
        adc_val = random.randint(adc_min, adc_max)
        temperature = genTemp(adc_val)
        #sendSensorM03(temperature)
        #return "this shit works"
        print(f"K value is {k} and ADCval is {adc_val}")
        return jsonify({"temperature": temperature})

    
    app.run(host='192.168.18.56')