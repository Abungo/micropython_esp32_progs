import machine
import time
from machine import Pin
import bme280_float as bme280
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont
i2c = machine.I2C(0,sda=machine.Pin(21),scl=machine.Pin(22))
bme = bme280.BME280(i2c=i2c)
espresso_dolce = XglcdFont('fonts/Unispace12x24.c', 12, 24)
print('Font loaded.')
# Baud rate of 40000000 seems about the max
spi = SPI(1, baudrate=40000000, sck=Pin(14),mosi=Pin(13))
display = Display(spi, dc=Pin(4), cs=Pin(16),rst=Pin(17),width=320,height=280, rotation=90)
try:
    with open('ip.txt', 'r') as file:
        ip_address = file.read().strip()
except OSError:
    print("Error: Unable to read from ip.txt")
def measure():
    temp,hpa,hum = bme.values
    alti = bme.altitude
    dew = bme.dew_point
    display.draw_text(10,10,f"IP Addr:{ip_address}",espresso_dolce,color565(0,255,255))
    display.draw_text(10,36,f"Temperature:{temp}",espresso_dolce,color565(0,255,255))
    display.draw_text(10,60,f"Pressure: {hpa}",espresso_dolce,color565(0, 255, 255))
    display.draw_text(10,86,f"Humidity: {hum}",espresso_dolce,color565(255, 255, 255))
    display.draw_text(10,112,f"Altitude: {alti}",espresso_dolce,color565(255, 255, 255))
    display.draw_text(10,138,f"Dew Point: {dew}",espresso_dolce,color565(255, 255, 255))
    #display.cleanup()