from CAENDesktopHighVoltagePowerSupply import CAENDesktopHighVoltagePowerSupply
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import StartTcpServer
import threading
import time
import datetime

address = ('127.0.0.1', '5020')  # currently using local loopback interface
ch_num = 4
n_hr = 2*ch_num     # set current, set voltage - TODO: could add polarity and set ramp_speed (still need to figure this out)
n_ir = 2*ch_num     # currently just reading voltage and current- TODO: could add on/off status and polarity
n_coil = 1*ch_num   # set on/off status

def setup_context():
    store = ModbusSlaveContext (
        co = ModbusSequentialDataBlock(0, [0]*n_coil),
        hr = ModbusSequentialDataBlock(0, [0]*n_hr),
        ir = ModbusSequentialDataBlock(0, [0]*n_ir)
    )
    context = ModbusServerContext(slaves = store, single = true)
    
def server_thread(context, address):
    StartTcpServer(context = context, address = address)
    
def start_server_thread(context, address):
    t = threading.Thread(target = server_thread, args = (context, address), daemon = True)
    t.start()
    return t
    
if __name__ == "__main___":
    context = setup_context()
    start_server_thread(context, address)
    fx_co = 5
    fx_hr = 3
    fx_ir = 2
    
    while True:
        # DONE: need to figure out integer vs float - register is easier to do with integers - voltage is fine but current is currently decimal microamps 
        # taking current in nanoamps - truncating further decimal places
        # taking voltage in 0.1 volts
        
        # setting on/off status - TODO ideally we would check current status and update only if needed, but for some reason I am having trouble checking the status - the current version works I am just unsure if it is the best possible approach for the power supply
        on_value = context[0].getValues(fx_co, 0, n_coil)
        for i in range(0, n_coil):
            if on_value[i] == 1: 
                caen.channels[i].output = "on"
            else:
                caen.channels[i].output = "off"
                
        # reading voltage and current
        volt_value = context[0].getValues(fx_ir, 0, ch_num)
        current_value = context[0].getValues(fx_ir, ch_num, ch_num)
        for i in range(0, ch_num):
            channel = caen.channels[i]
            voltage_string = channel.get('VMON')
            voltage_clean = ""
            for ch in voltage_string:
                if ch.isnumeric() or ch == '.':
                    voltage_clean += ch
            volt_value[i] = int(float(voltage_clean)*10)
            current_value[i] = channel.get('IMON')*1000
        read_values = volt_value + current_value
        context[0].setValues(fx_ir, 0, read_values)
        
        # setting voltage, current limit, ramp speed
        volt_set = context[0].getValues(fx_hr, 0, ch_num)
        current_lim = context[0].getValues(fx_hr, ch_num, ch_num)
        for i in range(0, ch_num):
            channel = caen.channels[i]
            vset_string = channel.get('VMON')
            vset_clean = ""
            for ch in vset_string:
                if ch.isnumeric() or ch == '.':
                    vset_clean += ch
            vset_val = int(float(voltage_clean)*10)
            if volt_set[i] != vset_val:
                channel.V_set = volt_set[i]/10
            if current_lim[i] != (channel.get('ISET')*1000):
                channel.current_compliance = current_lim[i]/1000
                
        time.sleep(1)
                
        
    


# #def main(args):
 # #   print("hello world")
  # #  return 0
    
# def channel_select():   # is this necessary?
    # print("Available channels 0 to 3")
    # selection = input("Enter desired channel(s) (comma separated) or type all: ").strip().lower()
    # if (selection == 'all'):
        # return list(range(caen.channels_count))
    # else:
        # channels = [int(ch.strip()) for ch in selection.split(',')]
        # if (all(0 <= ch < caen.channels_count for ch in channels)):
            # return channels
        # else:
            # print("Invalid input")
            # return(channel_select())

# def monitor_channels(selected_channels):
    # while True:
  # #     current_time = datetime.now()
  # #     print("Power supply output at ", current_time, " :")
        # print("Power supply output: ")
        # for ch_num in selected_channels:    # slightly unsure how to do multiple channels concurrently
            # channel = caen.channels[ch_num]
            # voltage = channel.get('VMON')
            # current = channel.I_mon
            # print("Channel: ", ch_num)  # presumably we want to do something other than print but not entirely sure what 
            # print("Voltage: ", voltage)
            # print("Current: ", current)
        # time.sleep(0.5)     # updates every 0.5 s, but will in theory be essentially continous if I remove this

# # def ramp_vol(channel_num, target_volt, ramp_speed):
    # # if(channel_num < 0 or channel_num >=caen.channels_count):
        # # print("Invalid channel")
        # # return
    # # channel = caen.channels[channel_num]
    # # current_volt = channel.Vmon
    # # # caen.channels[channel_number].ramp_voltage(target_volt, ramp_speed_VperSec = ramp_speed)
    # # caen.channels[0].ramp_voltage(100,ramp_speed_VperSec = 10)
    # # # caen.ramp_voltage(voltage = target_volt, channel = channel_num, ramp_speed_VperSec = ramp_speed)
    # # while True:
        # # print("Current voltage is: ", channel.Vmon)
        # # if channel.is_ramping == 'no':
            # # break
        # # time.sleep(0.5)
    # # print("Final voltage is: ", channel.Vmon)
    
# def ramp_vol(channel_num, target_volt):
    # if(channel_num < 0 or channel_num >=caen.channels_count):
        # print("Invalid channel")
        # return
    # channel = caen.channels[channel_num]
    # current_volt = channel.get('VMON')
    # # caen.channels[channel_number].ramp_voltage(target_volt, ramp_speed_VperSec = ramp_speed)
    # # caen.channels[0].ramp_voltage(100,ramp_speed_VperSec = 10)
    # # caen.ramp_voltage(voltage = target_volt, channel = channel_num, ramp_speed_VperSec = ramp_speed)
    # speed_change = input("Channel ramps at 5 V/s, press 1 to continue and 2 to modify ramping speed ")
    # if speed_change == '1':
        # caen.channels[channel_num].V_set = target_volt
        # time.sleep(target_volt/5)
    # else:
        # print("sorry still figuring that out :(")

    # # while True:
        # # print("Current voltage is: ", channel.Vmon)
        # # if channel.is_ramping == 'no':
            # # break
        # # time.sleep(0.5)
    # print("Final voltage is: ", channel.get('VMON'))
    
# def main_menu():
    # while True:
        # choice = input("1 to monitor,  2 to ramp, 3 to exit: ")
        # if choice == '1':
            # selected_channels = channel_select()
            # monitor_channels(selected_channels)
        # elif choice == '2':
            # channel_num = int(input("Enter channel number: "))
            # target_volt = int(input("Enter desired voltage: "))
            # # ramp_speed = input("Enter ramp speed in V/s: ")
            # ramp_vol(channel_num, target_volt)
        # elif choice == '3':
            # turn_off = channel_select()
            # for chan in turn_off:
                # caen.channels[chan].output = "off"
            # break
        # else:
            # print("Invalid choice, try again")

# if __name__ == '__main__':
    # caen = CAENDesktopHighVoltagePowerSupply(port = '/dev/ttyACM0') # usb port or ethernet IP goes here
    # print("connected with: ", caen.idn)
    # turn_on = channel_select()
    # for chan in turn_on:
        # caen.channels[chan].output = "on"
    # main_menu()


#Note to self: 
 #   -> read voltage at a given time
  #  -> read current at a given time
   # -> set voltage (ramping)
    #-> set maximum current 
    #Q: status? ISET? VSET? Do things simulataneously?
