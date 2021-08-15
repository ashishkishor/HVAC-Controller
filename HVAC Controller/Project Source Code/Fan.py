#This is an Air Conditioner Module to emulate the AC appliance.
'''
This is a Fan Module to emulate the Fan appliance. The Fan Module simulates the function of Fan and its
states. Also it gets a signed digital certificate to be verified by the AWS during MQTT connection.
The Fan states represent the following

Fan Speed : Represents Air Conditioners Fan Speed
Status : Represents the power status of the AC
'''
from tkinter import *
from PIL import Image, ImageTk

import ssl
import os
import threading
from paho.mqtt import client
import datetime
import ast
import time

ca_cert = os.path.realpath("Certificates/ca_cert/AmazonRootCA1.crt")
cert = os.path.realpath("Certificates/fan-certificate.pem.crt")
pkey = os.path.realpath("Certificates/fan-private.pem.key")

aws_broker = 'aqs707es21fx9-ats.iot.eu-west-1.amazonaws.com'
#aws_broker = 'broker.hivemq.com'
PORT = 8883

def on_connect(client, userdata, flags, rc):
    if(rc == 0):
        print("FAN Connected To AWS MQTT Broker\n")
        print("OK Ready\n")
    else:
        print("Connection to MQTT Broker Failed\n")

def on_message(client, userdata, message):
    data = ast.literal_eval(message.payload.decode('utf-8'))
    fan_params = data["Fan"]
    current_temp = data['Room_Temp']

    status['text'] = "Current Status :" + fan_params['status']

    if(fan_params['status'] == "ON"):
        status['fg'] = 'green'
    else:
        status['fg'] = 'red'

    fanspeed['text'] = "Fan Speed :"+str(fan_params['fan_speed'])

    curr_temp['text'] = "Current Room Temp Reported"+str(current_temp)+"^ C"


def mqttProcess():
    fan_client = client.Client("Fan_client")

    fan_client.on_connect = on_connect
    fan_client.on_message = on_message

    fan_client.tls_set(ca_cert, cert, pkey, ssl.CERT_REQUIRED, ssl.PROTOCOL_TLSv1_2, None)
    fan_client.connect(aws_broker, PORT)

    fan_client.subscribe("hvac/room/hub/params")

    fan_client.loop_start()

    while True:
        time.sleep(0.0001)

tk = Tk()   #Creating Tkinter Object

tk.geometry("500x550")
tk.configure(bg='black')
title = Label(tk,text = "FAN Appliance",pady = 5,bg='black',fg='white')
title.pack()
ac_image = ImageTk.PhotoImage(Image.open("res/Fan.png").resize((500,400)))

bg = Label(tk,image = ac_image,bd=0)
bg.pack()

display_pane = Frame(tk,bd=1,bg='white',relief = "raised")
display_pane.pack()

status = Label(display_pane,text ="Status : OFF",fg="red",bg="white",padx=5,pady=5)
status.pack()

fanspeed = Label(display_pane,text ="Current Fan Speed : 0",fg="black",bg="white",padx=5,pady=5)
fanspeed.pack()

curr_temp = Label(display_pane, text="Current Room Temperature : 0", fg="black", bg="white", padx=5, pady=5)
curr_temp.pack()

threading.Thread(target=mqttProcess).start()

tk.mainloop()

