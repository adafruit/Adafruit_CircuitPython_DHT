"""
example of reading temperature and humidity from a DHT device
and displaying results to the serial port and a 8 digit 7-segment display
the DHT device data wire is connected to board.D2
"""
# import for dht devices
import time
import adafruit_dhtlib
from board import D2

#imports for 7-segment display device
from  adafruit_max7219 import bcddigits
from board import TX, RX, A2
import busio
import digitalio

clk = RX
din = TX
cs = digitalio.DigitalInOut(A2)
spi = busio.SPI(clk, MOSI=din)
display = bcddigits.BCDDigits(spi, cs, nDigits=8)
display.brightness(5)

#initial the dht device
dhtDevice = adafruit_dhtlib.DHT22(D2)

while True:
    try:
        # show the values to the serial port
        temperature = dhtDevice.temperature*9/5+32
        humidity = dhtDevice.humidity
        #print("Temp: {:.1f} F Humidity: {}% ".format(temperature, humidity))

        # now show the values on the 8 digit 7-segment display
        display.clear_all()
        display.show_str(0,'{:5.1f}{:5.1f}'.format(temperature, humidity))
        display.show()

    except RuntimeError as error:
        print(error.args)

    time.sleep(2.0)
    