from CAENDesktopHighVoltagePowerSupply import CAENDesktopHighVoltagePowerSupply # this was originally meant for another power supply type (DT1470et) so i am now slightly uncertain of whether it will work perfectly for ours
import time
import datetime

caen = CAENDesktopHighVoltagePowerSupply(port = '/dev/ttyACM0') # usb port or ethernet IP goes here
print("connected with: ", caen.idn)

# print(caen.channels[0].output == "on")

caen.channels[0].output = "on"

print("current voltage = ", caen.channels[0].V_mon)

caen.channels[0].V_set = 10
print("voltage = ", caen.channels[0].I_mon)

print(caen.channels[0].get('VMON'))

caen.channels[0].output = "on"

print(caen.channels[0].polarity)

print(caen.channels[0].get('VSET'))
print(caen.channels[0].V_set)

# print(caen.channels[0].status_byte)
