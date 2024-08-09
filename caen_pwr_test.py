from CAENDesktopHighVoltagePowerSupply import CAENDesktopHighVoltagePowerSupply # this was originally meant for another power supply type (DT1470et) so i am now slightly uncertain of whether it will work perfectly for ours
import time
import datetime

caen = CAENDesktopHighVoltagePowerSupply(port = '/dev/ttyACM0') # usb port or ethernet IP goes here
print("connected with: ", caen.idn)

# print(caen.channels[0].output == "on")

caen.channels[0].output = "on"

print("current voltage = ", caen.channels[0].V_mon)

print("voltage = ", caen.channels[0].I_mon)

caen.channels[0].set('RUP', 13)
print(caen.channels[0].get('RUP'))
caen.channels[0].V_set = 32


print(caen.channels[0].get('VMON'))

caen.channels[0].output = "on"

print(caen.channels[0].polarity[0])

print(caen.channels[0].get('VSET'))
print(caen.channels[0].V_set)

current_lim = 10*1000
# caen.channels[0].current_compliance = current_lim/1000

print("look", caen.channels[0].V_mon)

# print(caen.channels[0].current_compliance)
# print(caen.channels[0].get('IMON'))

# print(caen.channels[0].status_byte)
