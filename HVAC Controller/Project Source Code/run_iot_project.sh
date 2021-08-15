sudo apt-get install python3-pil python3-pil.imagetk
sudo apt-get install python3-tk
pip install boto3

gnome-terminal -e "python3 Air_Conditioner.py"
gnome-terminal -e "python3 Fan.py"
gnome-terminal -e "python3 Room_Heater.py"
gnome-terminal -e "python3 CentralHub.py"
gnome-terminal -e "python3 Temp_Sensor.py"
