from ADS1x15 import ADS1115
import time
import board
# import busio

# i2c = busio.I2C(board.SCL, board.SDA)

# ads = ADS.ADS1115(i2c)

ads = ADS1115()
ads.gain = 1
ads.data_rate = 128
# chan = AnalogIn(ads, adafruit_ads1x15.ads1115.P0)

while True:
	# print(f"Voltmeter reading: {chan.voltage} V")
	voltage = ads.read_adc(0)*(4.096/32767)
	print(f"Voltmeter reading: {voltage:.3f} V")
	time.sleep(1)
