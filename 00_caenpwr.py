from CAENDesktopHighVoltagePowerSupply import CAENDesktopHighVoltagePowerSupply # this was originally meant for another power supply type (DT1470et) so i am now slightly uncertain of whether it will work perfectly for ours - it does works
import time
import datetime
import numpy as np

#def main(args):
 #   print("hello world")
  #  return 0
    
def channel_select():   # is this necessary?
    print("Available channels 0 to 3")
    selection = input("Enter desired channel(s) (comma separated) or type all: ").strip().lower()
    if (selection == 'all'):
        return list(range(caen.channels_count))
    else:
        channels = [int(ch.strip()) for ch in selection.split(',')]
        if (all(0 <= ch < caen.channels_count for ch in channels)):
            return channels
        else:
            print("Invalid input")
            return(channel_select())

def monitor_channels(selected_channels):
    while True:
  #     current_time = datetime.now()
  #     print("Power supply output at ", current_time, " :")
        print("Power supply output: ")
        for ch_num in selected_channels:    # slightly unsure how to do multiple channels concurrently
            channel = caen.channels[ch_num]
            voltage_string = channel.get('VMON')
            voltage_clean = ""
            for ch in voltage_string:
                if ch.isnumeric() or ch == '.':
                    voltage_clean += ch
            voltage = int(float(voltage_clean)*10)
            #current = int(float(channel.get('IMON'))*1000)
            current_string = channel.get('IMON')
            # current_clean = ""
            # for ch in current_string:
                # if ch.isnumeric() or ch == '.':
                    # current_clean += ch
            current = int((current_string)*1000)
            print("Channel: ", ch_num)  # presumably we want to do something other than print but not entirely sure what 
            print("Voltage: ", voltage)
            print("Current: ", current)
            print(current_string)
            print(channel.get('VSET'))
        time.sleep(0.5)     # updates every 0.5 s, but will in theory be essentially continous if I remove this

# def ramp_vol(channel_num, target_volt, ramp_speed):
    # if(channel_num < 0 or channel_num >=caen.channels_count):
        # print("Invalid channel")
        # return
    # channel = caen.channels[channel_num]
    # current_volt = channel.Vmon
    # # caen.channels[channel_number].ramp_voltage(target_volt, ramp_speed_VperSec = ramp_speed)
    # caen.channels[0].ramp_voltage(100,ramp_speed_VperSec = 10)
    # # caen.ramp_voltage(voltage = target_volt, channel = channel_num, ramp_speed_VperSec = ramp_speed)
    # while True:
        # print("Current voltage is: ", channel.Vmon)
        # if channel.is_ramping == 'no':
            # break
        # time.sleep(0.5)
    # print("Final voltage is: ", channel.Vmon)
    
def ramp_vol(channel_num, target_volt):
    if(channel_num < 0 or channel_num >=caen.channels_count):
        print("Invalid channel")
        return
    channel = caen.channels[channel_num]
    current_volt = channel.get('VMON')
    # caen.channels[channel_number].ramp_voltage(target_volt, ramp_speed_VperSec = ramp_speed)
    # caen.channels[0].ramp_voltage(100,ramp_speed_VperSec = 10)
    # caen.ramp_voltage(voltage = target_volt, channel = channel_num, ramp_speed_VperSec = ramp_speed)
    speed_change = input("Channel ramps at 5 V/s, press 1 to continue and 2 to modify ramping speed ")
    if speed_change == '1':
        caen.channels[channel_num].V_set = target_volt
        time.sleep(target_volt/5)
    else:
        print("sorry still figuring that out :(")

    # while True:
        # print("Current voltage is: ", channel.Vmon)
        # if channel.is_ramping == 'no':
            # break
        # time.sleep(0.5)
    print("Final voltage is: ", channel.get('VMON'))
    
def main_menu():
    while True:
        choice = input("1 to monitor,  2 to ramp, 3 to exit: ")
        if choice == '1':
            selected_channels = channel_select()
            monitor_channels(selected_channels)
        elif choice == '2':
            channel_num = int(input("Enter channel number: "))
            target_volt = int(input("Enter desired voltage: "))
            # ramp_speed = input("Enter ramp speed in V/s: ")
            ramp_vol(channel_num, target_volt)
        elif choice == '3':
            turn_off = channel_select()
            for chan in turn_off:
                caen.channels[chan].output = "off"
            break
        else:
            print("Invalid choice, try again")

if __name__ == '__main__':
    caen = CAENDesktopHighVoltagePowerSupply(port = '/dev/ttyACM0') # usb port or ethernet IP goes here
    print("connected with: ", caen.idn)
    turn_on = channel_select()
    for chan in turn_on:
        caen.channels[chan].output = "on"
    main_menu()


#Note to self: 
 #   -> read voltage at a given time
  #  -> read current at a given time
   # -> set voltage (ramping)
    #-> set maximum current 
    #Q: status? ISET? VSET? Do things simulataneously?
