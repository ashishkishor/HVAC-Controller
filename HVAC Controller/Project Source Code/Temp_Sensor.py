'''
This is the Temperature Sensor Module to emulate the room temperature scenarios. It uses the random number logic to generate
a set of temperatures between the range 15^ C to 50^ C that are real time temperatures in the environment. The sensor
module senses and genrates the temperature for every interval of 5 minutes and published the temperature to a topic
hvac/room/sensor. This topic is subscribed by the Central Hub that recieves this sensed tempearture, and based on a rule
engine decides the set of parameter states for each applicance to regulate the temperature.
'''

import random
import time
import ssl

import os
import paho.mqtt.client as mqtt_client

aws_broker = 'aqs707es21fx9-ats.iot.eu-west-1.amazonaws.com'
#aws_broker = 'broker.hivemq.com'
PORT = 8883

ca_cert = os.path.realpath("Certificates/ca_cert/AmazonRootCA1.crt")
cert = os.path.realpath("Certificates/sensor-certificate.pem.crt")
pkey = os.path.realpath("Certificates/sensor-private.pem.key")

def on_connect(client, userdata, flags, rc):
    if(rc == 0):
        print("SENSOR Connected To AWS MQTT Broker\n")
        print("SENSOR RUNNING")
    else:
        print("Connection to MQTT Broker Failed\n")

sensor = mqtt_client.Client("Sensor")

sensor.on_connect = on_connect

sensor.tls_set(ca_cert,cert,pkey,ssl.CERT_REQUIRED,ssl.PROTOCOL_TLSv1_2,None)

sensor.connect(aws_broker,PORT)

sensor.loop_start()

while True:
    temp = random.randint(15,50)

    sensor.publish("hvac/room/sensor",str(temp))

    time.sleep(5)




