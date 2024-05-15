import machine
import time
import pressure
import bme
import realtime_api
backlight_pin=12
pin = machine.Pin(backlight_pin, machine.Pin.OUT)
pin.on()
def my_function(timer1):
    pressure.measure()
    realtime_api.run()
def my_function2(timer2):
    bme.run()
#initial run
pressure.measure()
bme.run()
#time.sleep(5)
# Create a timer object
timer1 = machine.Timer(1)
timer2 = machine.Timer(2)
timer1.init(period=10000, mode=machine.Timer.PERIODIC, callback=my_function)
timer2.init(period=300000, mode=machine.Timer.PERIODIC, callback=my_function2)