from CAENDesktopHighVoltagePowerSupply import CAENDesktopHighVoltagePowerSupply
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import StartTcpServer
import threading
import time
import datetime

address = ('0.0.0.0', '5020')  # currently using local loopback interface: 127.0.0.1
ch_num = 4
n_hr = 4*ch_num + 1    # set current, set voltage, set ramp speed up and down
n_ir = 2*ch_num + 1    # reading voltage and current
n_coil = 1*ch_num + 1   # set on/off status

def setup_context():
    store = ModbusSlaveContext (
        co = ModbusSequentialDataBlock(0, [0]*n_coil),
        hr = ModbusSequentialDataBlock(0, [0]*n_hr),
        ir = ModbusSequentialDataBlock(0, [0]*n_ir)
    )
    context = ModbusServerContext(slaves = store, single = True)
    return context
    
def server_thread(context, address):
    StartTcpServer(context = context, address = address)
    
def start_server_thread(context, address):

    t = threading.Thread(target = server_thread, args = (context, address), daemon = True)
    t.start()
    return t
    
if __name__ == '__main__':
    
    # connecting to power supply
    caen = CAENDesktopHighVoltagePowerSupply(port = '/dev/ttyACM0') # usb port or ethernet IP goes here
    print("connected with: ", caen.idn)
    
    # setting up modbus server
    context = setup_context()
    start_server_thread(context, address)
    
    # fc as hex for each register type
    fx_co = 5
    fx_hr = 3
    fx_ir = 4
    
    # setting intial current limit as 100 microamps and ramp voltage (up and down) as 5 V/s for all channels
    current_initial = context[0].getValues(fx_hr, ch_num, ch_num)
    current_initial = [cur + 100*100 for cur in current_initial]
    ramp_initial = context[0].getValues(fx_hr, 2*ch_num, 2*ch_num)
    ramp_initial = [ramp + 50 for ramp in ramp_initial]
    initial = current_initial + ramp_initial
    context[0].setValues(fx_hr, ch_num, initial)
    # print(initial)
    # print(context[0].getValues(fx_hr, 0, n_hr))

    
    while True:
        # taking current in units of 10 nanoamps
        # taking voltage in 0.1 volts and ramp speed in 0.1 V/s
        
        # setting on/off status
        on_value = context[0].getValues(fx_co, 0, n_coil)
        for i in range(0, ch_num):
            if on_value[i] == 1: 
                caen.channels[i].output = "on"
            else:
                caen.channels[i].output = "off"
        print("coil: ", context[0].getValues(fx_co, 0, n_coil))
                
        # reading voltage and current
        volt_value = context[0].getValues(fx_ir, 0, ch_num)
        current_value = context[0].getValues(fx_ir, ch_num, ch_num)
        for i in range(0, ch_num):
            channel = caen.channels[i]
            voltage_string = channel.get('VMON')  # power supply gives results with a semicolon at the end
            voltage_clean = ""
            for ch in voltagcaene_string:        
                if ch.isnumeric() or ch == '.':
                    voltage_clean += ch
            volt_value[i] = int(float(voltage_clean)*10)
            current_value[i] = int(channel.get('IMON')*100)
        read_values = volt_value + current_value  # combining all the read values
        # print("Readings: ", read_values)
        context[0].setValues(fx_ir, 0, read_values) # updating registers
        print("inputs: ", context[0].getValues(fx_ir, 0, n_ir))

        
        # setting voltage, current limit, ramp speed
        volt_set = context[0].getValues(fx_hr, 0, ch_num)
        current_lim = context[0].getValues(fx_hr, ch_num, ch_num)
        ramp_speed_up = context[0].getValues(fx_hr, 2*ch_num, ch_num)
        ramp_speed_down = context[0].getValues(fx_hr, 3*ch_num, ch_num)
        # print(current_lim)
        for i in range(0, ch_num):
            channel = caen.channels[i]
            print("ch_num", i)
            # setting voltage
            vset_string = channel.get('VSET')
            vset_clean = ""
            for ch in vset_string:
                if ch.isnumeric() or ch == '.':
                    vset_clean += ch
            vset_val = int(float(vset_clean)*10)
            print(vset_val)
            print(volt_set[i])
            print(volt_set[i]/10)
            if int(volt_set[i]) != vset_val:
                print("changing VSET to", volt_set[i]/10)
                channel.V_set = float(volt_set[i]/10)
                
            # setting current limit
            iset_string = channel.get('ISET')
            iset_clean = ""
            for ch in iset_string:
                if ch.isnumeric() or ch == '.':
                    iset_clean += ch
            iset_val = int(float(iset_clean)*100)
            # print(iset_val)
            # print(current_lim[i])
            # print(current_lim[i]/100)
            if current_lim[i] != iset_val:
                channel.current_compliance = current_lim[i]/100
                
            # setting ramp up voltage    
            rv_string = channel.get('RUP')
            rv_clean = ""
            for ch in rv_string:
                if ch.isnumeric() or ch == '.':
                    rv_clean += ch
            rv_val = int(float(rv_clean)*10)
            if ramp_speed_up[i] != rv_val:
                channel.set('RUP', ramp_speed_up[i]/10)
                
                
            # setting ramp down voltage    
            rvd_string = channel.get('RDW')
            rvd_clean = ""
            for ch in rvd_string:
                if ch.isnumeric() or ch == '.':
                    rvd_clean += ch
            rvd_val = int(float(rvd_clean)*10)
            if ramp_speed_down[i] != rvd_val:
                channel.set('RDW', ramp_speed_down[i]/10)
                
        print("holding: ", context[0].getValues(fx_hr, 0, n_hr))

                
        print("working")
                
        time.sleep(1)
