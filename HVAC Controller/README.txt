************************************************************************************************************************************
HVAC IOT PROJECT (CS5453 : Internet of Things)

Project Team : 
Tahir Ahmed Shaik (CS20MTECH14007)
Pratik M. Lahase (CS20MTECH11003)
Ashish Kishor (CS20MTECH11002)

Date : 01/05/2021

***********************************************************************************************************************************

Description:

This is a HVAC project that simulates the entire HVAC (Heating, Ventilation and Air Conditioning) system, which through an interactive smart processing of the applicances regualtes the room temperature based on the external environmental conditions. This project includes a set of simulated devices as python modules which include (AC, Fan and the Room Heater) that are connected to a central hub which handles the entire task of monitoring, communication and co-ordination of the applicances. The temperature sensor is a standalone client that constantly sends room temperature levels based on the random genration logic to simulate the real time temperature changes. The communication between all the appliances, central hub and the sensor happens through the MQTT communication standard using AWS IoT core suite. There also exists a interactive - user interface for the user which displays a variety of information, statistical data and provides status monitoring of the appliances. The interafce is web-page dashboard that can be visualized to the user upon registration with the central hub. The enitre back end data for the interface is taken care by the NOSQL database service provided by Amazon Dynamo DB service. The central hub along with publishing the information to the applicances, publishes the data to the Dynamo DB each time. 


Requirements :
1. Python 3.x 
2. HTML5 enabled web browser
3. Python libraries : matplotlib, boto3 (AWS SDK) , paho-mqtt (MQTT client), tkinter (GUI Library)

************************
Running the project 
************************

1. For Windows system

-->run the batch script file "run_iot_windows.bat", it should firstly try to install the required libraries if not available else will execute the program, launching multiple clients interfaces.
--> After running the script, muliple widows open up , which include the interfaces for AC, Fan and the room heater.
--> after all the windows are launched, the interface can be opened up by first opening the index.html file in a web-browser present in the directory. If this is the first time launching , please register account from the register section of the page.

************************************
First TIme Registration
************************************
Click on register link in the main page , fill the user id email , a password and in the device ID provide the device of the central hub, this is to simulate the real time attaching a device to user. The Device ID is a unique id for each central hub device. Click on register.

After registraion , from the main page click on login and login using the registered details. After logging in the dashboard loads up showing all the information.


2. For Linux / Ubuntu System

-->run the bash script file "run_iot_project.sh", it should firstly try to install the required libraries if not available else will execute the program, launching multiple clients interfaces.
--> After running the script, muliple widows open up , which include the interfaces for AC, Fan and the room heater.
--> after all the windows are launched, the interface can be opened up by first opening the index.html file present in the directory. If this is the first time launching , please register account from the register section of the page.

************************************
First TIme Registration
************************************
Click on register link in the main page , fill the user id email , a password and in the device ID provide the device of the central hub, this is to simulate the real time attaching a device to user. The Device ID is a unique id for each central hub device. Click on register.

After registraion , from the main page click on login and login using the registered details. After logging in the dashboard loads up showing all the information.


***************************************************
Tools and Technologies Used
***************************************************
1. Python 3.x programming language
2. AWS IoT core for MQTT protocol
3. AWS Dynamo DB for interface back-end.
4. PyCharm IDE for project development.



\
