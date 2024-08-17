from CAENDesktopHighVoltagePowerSupply import CAENDesktopHighVoltagePowerSupply # this was originally meant for another power supply type (DT1470et) so i am now slightly uncertain of whether it will work perfectly for ours
import time
import datetime

caen = CAENDesktopHighVoltagePowerSupply(port = '/dev/ttyACM0') # usb port or ethernet IP goes here
print("connected with: ", caen.idn)

# print(caen.channels[0].output == "on")

# caen.channels[0].set('ISET', 100)

caen.channels[0].set('TRIP', 1)
print(caen.channels[0].current_compliance)
# caen.channels[0].current_compliance = 100

caen.channels[0].set('',0)

caen.channels[0].output = "off"

# caen.channels[0].current_compliance = 100


print("current voltage = ", caen.channels[0].V_mon)

print("voltage = ", caen.channels[0].I_mon)

caen.channels[0].set('RUP', 13)
print(caen.channels[0].get('RUP'))
caen.channels[0].V_set = 8

print(caen.channels[0].output)
print(caen.channels[0].is_ramping)
print(caen.channels[0].there_was_overcurrent)

print(caen.channels[0].get('VMON'))

caen.channels[0].output = "on"

print(caen.channels[0].polarity)

print(caen.channels[0].get('VSET'))
print(caen.channels[0].V_set)

current_lim = 10*1000
# caen.channels[0].current_compliance = current_lim/1000

print("look", caen.channels[0].V_mon)

caen.channels[0].output = "off"

# print(caen.channels[0].current_compliance)
# print(caen.channels[0].get('IMON'))

# print(caen.channels[0].status_byte)
