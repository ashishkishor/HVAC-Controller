'''
This is a Room Heater Module to emulate the Room Heater appliance. The Heater Module simulates the function of Heater and its
states. Also it gets a signed digital certificate to be verified by the AWS during MQTT connection.
The Heater states represent the following

Temperature : Depicts the Room Heater's Temperature
Status : Represents the power status of the Heater
'''
from tkinter import *
from PIL import Image, ImageTk
import os
import threading
from paho.mqtt import client
import ssl
import ast
import time
import datetime
from tkinter import scrolledtext

ca_cert = os.path.realpath("Certificates/ca_cert/AmazonRootCA1.crt")
cert = os.path.realpath("Certificates/heater-certificate.pem.crt")
pkey = os.path.realpath("Certificates/heater-private.pem.key")

aws_broker = 'aqs707es21fx9-ats.iot.eu-west-1.amazonaws.com'
#aws_broker = 'broker.hivemq.com'
PORT = 8883


def on_connect(client, userdata, flags, rc):
    if (rc == 0):
        print("Heater Connected To AWS MQTT Broker\n")
        print("OK ready\n")
    else:
        print("Connection to MQTT Broker Failed\n")


def on_message(client, userdata, message):
    data = ast.literal_eval(message.payload.decode('utf-8'))
    heater_params = data["Heater"]
    current_temp = data['Room_Temp']

    status['text'] = "Current Status : "+heater_params['status']

    if(heater_params['status'] == "ON"):
        status['fg'] = 'green'
    else:
        status['fg'] = 'red'

    temp['text'] = "Temp :"+str(heater_params['temp'])
    temp_label['text'] = temp['text']

    curr_temp['text'] = "Current Room Temp Reported"+str(current_temp)+"^ C"

def mqttProcess():
    heater_client = client.Client("Heater_client")

    heater_client.on_connect = on_connect
    heater_client.on_message = on_message
    heater_client.tls_set(ca_cert, cert, pkey, ssl.CERT_REQUIRED, ssl.PROTOCOL_TLSv1_2, None)
    heater_client.connect(aws_broker, PORT)

    heater_client.subscribe("hvac/room/hub/params")

    heater_client.loop_start()

    while True:
        time.sleep(0.0001)

tk = Tk()   #Creating Tkinter Object

tk.geometry("500x550")
tk.configure(bg='black')
title = Label(tk,text = "Room Heater Appliance",pady = 5,bg='black',fg='white')
title.pack()
ac_image = ImageTk.PhotoImage(Image.open("res/Room_heater.png").resize((500,400)))

bg = Label(tk,image = ac_image,bd=0)
bg.pack()
display_frame = Frame(tk,bd=0, width= 700, height = 700,bg="black")
display_frame.pack()

display_frame.place(x=200, y =50)

temp_label = Label(display_frame,text ="Temp:30^ C",fg="white",bg="black")
temp_label.pack()

display_pane = Frame(tk,bd=1,bg='white',relief = "raised")
display_pane.pack()

status = Label(display_pane,text ="Status : OFF",fg="red",bg="white",padx=5,pady=5)
status.pack()

temp = Label(display_pane,text ="Current Fan Speed : 4",fg="black",bg="white",padx=5,pady=5)
temp.pack()

curr_temp = Label(display_pane, text="Current Room Temprature : 0", fg="black", bg="white", padx=5, pady=5)
curr_temp.pack()

threading.Thread(target=mqttProcess).start()

tk.mainloop()

