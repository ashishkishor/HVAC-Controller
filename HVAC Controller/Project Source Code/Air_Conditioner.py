'''
This is an Air Conditioner Module to emulate the AC appliance. The AC Module simulates the function of AC and its
states. Also it gets a signed digital certificate to be verified by the AWS during MQTT connection.
The AC states represent the following

Temperature : Depicts the Air Conditioners Temperature
Fan Speed : Represents Air Conditioners Fan Speed
Status : Represents the power status of the AC

'''
import time
from tkinter import *
from PIL import Image, ImageTk
import ssl                          #Library required for Certificate authentication during AWS handshake
import os
import threading
from paho.mqtt import client

import ast
aws_broker = 'aqs707es21fx9-ats.iot.eu-west-1.amazonaws.com'  #AWS IOT MQTT Endpoint
#aws_broker = 'broker.hivemq.com'
PORT = 8883

#The following are the certificates and keys of AC device used to verify on the AWS MQTT handshake connection
ca_cert = os.path.realpath("Certificates/ca_cert/AmazonRootCA1.crt")
cert = os.path.realpath("Certificates/ac-certificate.pem.crt")
pkey = os.path.realpath("Certificates/ac-private.pem.key")

def on_connect(client, userdata, flags, rc):
    if (rc==0):
        print("AC Connected to MQTT Broker....OK Ready\n")
    else:
        print("Connection Failed to MQTT Broker\n")
        exit(-1)

#This function is triggered upon recieving the message from Central Hub when it published on the topic, it sets the device state to the parameters received by Central Hub
def on_message(client, userdata, message):
    data = ast.literal_eval(message.payload.decode('utf-8'))
    ac_params = data["AC"]
    current_temp = data['Room_Temp']

    status['text'] = "Current Status :" +ac_params['status']

    if(ac_params['status'] == "ON"):
        status['fg'] = 'green'
    else:
        status['fg'] = 'red'

    temp_label['text'] = "Temp: "+str(ac_params['temp']) +"^ C"
    temp['text'] = temp_label['text']

    fanspeed_label['text'] = "Fan Speed: " + str(ac_params['fan_speed'])
    fanspeed['text'] = fanspeed_label['text']

    curr_temp['text'] = "Current Room Temp Reported" + str(current_temp)+"^ C"

#This is the backend function that initializes and establishes the handshake with AWS MQTT server
def mqttProcess():
    ac_client = client.Client("AC_client")

    ac_client.on_connect = on_connect

    ac_client.tls_set(ca_cert,cert,pkey,ssl.CERT_REQUIRED,ssl.PROTOCOL_TLSv1_2,None)

    ac_client.on_message = on_message

    ac_client.connect(aws_broker, PORT)

    ac_client.subscribe("hvac/room/hub/params")

    ac_client.loop_start()

    while True:
        time.sleep(0.0001)

tk = Tk()
# Creating Tkinter Object
tk.geometry("500x550")
tk.configure(bg='black')
title = Label(tk, text="Air Conditioner (AC) Appliance", pady=5, bg='black', fg='white')
title.pack()
ac_image = ImageTk.PhotoImage(Image.open("res/AC.png").resize((420, 190)))

bg = Label(tk, image=ac_image, bd=0)
bg.pack()

display_frame = Frame(tk, bd=0, width=99, height=100, bg="black")
display_frame.pack()
display_frame.place(x=350, y=100)
temp_label = Label(display_frame, text="Temp:0 C", fg="white", bg="black")
temp_label.pack()

fanspeed_label = Label(display_frame, text="Fan Speed : 0", fg="white", bg="black")
fanspeed_label.pack()

display_pane = Frame(tk, bd=1, bg='white', relief="raised")
display_pane.pack()

status = Label(display_pane, text="Status : OFF", fg="red", bg="white", padx=5, pady=5)
status.pack()

temp = Label(display_pane, text="Current AC Temp:0 C", fg="black", bg="white", padx=5, pady=5)
temp.pack()

fanspeed = Label(display_pane, text="Current Fan Speed : 0", fg="black", bg="white", padx=5, pady=5)
fanspeed.pack()

curr_temp = Label(display_pane, text="Current Room Temprature : 0", fg="black", bg="white", padx=5, pady=5)
curr_temp.pack()

threading.Thread(target=mqttProcess).start()

tk.mainloop()




