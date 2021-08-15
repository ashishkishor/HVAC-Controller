'''
This is the central Hub Controller of all the appliances that communicates with the appliances, co-ordinates
the appliances and regulates the temperature according to the Rule Engine based on the temperature from the sensor.
Also the Hub constantly saves the generates the LOGS to the local directory called logs.txt.

Device - ID : 19AX532021
'''
import ast
import datetime
import time
import os
import ssl
import boto3
from paho.mqtt import client

ca_cert = os.path.realpath("Certificates/ca_cert/AmazonRootCA1.crt")
cert = os.path.realpath("Certificates/hub-certificate.pem.crt")
pkey = os.path.realpath("Certificates/hub-private.pem.key")

aws_broker = 'aqs707es21fx9-ats.iot.eu-west-1.amazonaws.com'
#aws_broker = 'broker.hivemq.com'
PORT = 8883

'''
The following is the Rule Engine that initializes the default parameters for all the appliances. And upon receiving 
the temperatures based on the defiend set of rules sets the corresponding states of all the appliances and sends 
the information to all the appliances by publishing it ot the topic hvac/room/hub/params subscribed by all the 
appliances.
'''
class CloudDB:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb',region_name='eu-west-1',aws_access_key_id='AKIAQTN33AHNTAOVSIEZ',aws_secret_access_key='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')
        self.device_table = self.dynamodb.Table('hvac_device')
        #self.user_table = self.dynamodb.Table('user_table')

    def pushDataToDB(self,data):
        self.device_table.put_item(Item ={ "device_id" : '19AX532021',
                                           "room_temp":data['room_temp'],
                                           "AC_temp" : data['AC']['temp'],
                                           "AC_fanspeed": data['AC']['fan_speed'],
                                           "AC_status": data['AC']['status'],
                                           "Fan_fanspeed": data['Fan']['fan_speed'],
                                           "Fan_status": data['Fan']['status'],
                                           "Heater_temp": data['Heater']['temp'],
                                           "Heater_status": data['Heater']['status']})

    def getDataFromDB(self):
        data = self.user_table.get_item(key = {'device_id':'19AX532021'})

cdb = CloudDB()

class RuleEngine:
    def __init__(self):
        self.params = {"AC" : {"status":"ON","temp":25,"fan_speed":3} ,"Fan" : {"status":"ON","fan_speed":3} , "Heater": {"status": "ON","temp":0},"Room_Temp":0}

    def sendParams(self,hub):
        hub.publish("hvac/room/hub/params",str(self.params))

    def intiConditions(self,temp):
        if temp >= 30 and temp <= 35:
            self.params["AC"] = {"status" : "ON" , "temp" :22, "fan_speed": 4}
            self.params["Fan"] = {"status":"ON","fan_speed":4}
            self.params["Heater"] = {"status": "OFF","temp":0}
            self.params["Room_Temp"] = temp
        elif temp >= 35 and temp <=45:
            self.params["AC"] = {"status" : "ON" , "temp" :20, "fan_speed": 4}
            self.params["Fan"] = {"status":"ON","fan_speed":4}
            self.params["Heater"] = {"status": "OFF","temp":0}
            self.params["Room_Temp"] = temp
        elif temp >= 45 and temp <=50:
            self.params["AC"] = {"status" : "ON" , "temp" :18, "fan_speed": 5}
            self.params["Fan"] = {"status":"ON","fan_speed":5}
            self.params["Heater"] = {"status": "OFF","temp":0}
            self.params["Room_Temp"] = temp
        elif temp >= 25 and temp <=30:
            self.params["AC"] = {"status" : "ON" , "temp" :25, "fan_speed": 3}
            self.params["Fan"] = {"status":"ON","fan_speed":3}
            self.params["Heater"] = {"status": "OFF","temp":0}
            self.params["Room_Temp"] = temp
        elif temp >= 20 and temp <=24:
            self.params["AC"] = {"status" : "ON" , "temp" :28, "fan_speed": 2}
            self.params["Fan"] = {"status":"ON","fan_speed":3}
            self.params["Heater"] = {"status": "ON","temp":26}
            self.params["Room_Temp"] = temp
        elif temp >= 15 and temp <=19:
            self.params["AC"] = {"status" : "OFF" , "temp" :0, "fan_speed": 0}
            self.params["Fan"] = {"status":"ON","fan_speed":2}
            self.params["Heater"] = {"status": "ON","temp":30}
            self.params["Room_Temp"] = temp

def on_connect(client, userdata, flags, rc):
    if (rc==0):
        print("Central HUB connected to MQTT Broker....OK Ready\n")
    else:
        print("Connection Failed to MQTT Broker\n")
        exit(-1)

def on_message(client,userdata,message):
    log_file = open("logs.txt", "a")
    temp = ast.literal_eval(message.payload.decode('utf-8'))
    log_file.write("["+str(datetime.datetime.now())+"]"+" Temperature Reported By Sensor : "+str(temp)+"^ C"+"\n")
    re.intiConditions(temp)
    log_file.write("["+str(datetime.datetime.now())+ "]" + "<Parameters>: "+str(re.params)+"\n")
    data =  {"room_temp" : str(temp),"AC": re.params['AC'],"Fan" : re.params['Fan'],"Heater":re.params['Heater']}
    cdb.pushDataToDB(data)
    log_file.close()
    re.sendParams(hub)

hub = client.Client("Central_hub")

hub.on_connect = on_connect
hub.on_message = on_message

hub.tls_set(ca_cert,cert,pkey,ssl.CERT_REQUIRED,ssl.PROTOCOL_TLSv1_2,None)
hub.connect(aws_broker,PORT)  #Connecting The Central HUB to MQTT Broker

re = RuleEngine()   #Initialize the rule engine
re.sendParams(hub)  #Sending Intial Status and defualt states to appliances

hub.subscribe("hvac/room/sensor")

hub.loop_start()

while True:
    time.sleep(0.0001)






