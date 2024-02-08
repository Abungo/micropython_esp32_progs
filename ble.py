from machine import Pin, Timer, SoftI2C
from time import sleep_ms
import ubluetooth
from dht import DHT11
sensor=DHT11(Pin(4))
#sensor.measure()
class BLE():
    def __init__(self, name):   
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)

        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.timer2 = Timer(1)
        
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):        
        self.timer1.deinit()
        self.timer2.deinit()
        self.led(0)

    def disconnected(self):        
        self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(1))
        sleep_ms(200)
        self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0))   

    def ble_irq(self, event, data):
        if event == 1:
            '''Central disconnected'''
            self.connected()
            self.led(0)
        
        elif event == 2:
            '''Central disconnected'''
            self.advertiser()
            self.disconnected()
        
        elif event == 3:
            '''New message received'''            
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            print(message)            
            if message == 'red_led':
                red_led.value(not red_led.value())
                print('red_led', red_led.value())
                ble.send('red_led' + str(red_led.value()))
            if message == 'read_temp':
              try:
                sensor.measure()   # Poll sensor
                t, h = sensor.temperature(), sensor.humidity()
                if all(isinstance(i, int) for i in [t, h]):   # Confirm values
                  data = '{0:.1f}&deg;C {1:.1f}%'.format(t, h)
                else:
                  data = 'Invalid reading.'
              except:
                data = 'Attempting to read sensor...'
              ble.send(data)
            if message == 'read_hum':
                print("h")
                ble.send("humidity")
            if message == 'ip':
            	import network
            	sta_if = network.WLAN(network.STA_IF)
            	sta_if.active(True)
            	print('network config:', sta_if.ifconfig())
            	ip=list(sta_if.ifconfig())
            	ble.send(ip[0])
            else:
            	ble.send(message)
           
    def register(self):        
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)
        
# test
#i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
red_led = Pin(2, Pin.OUT)
ble = BLE("ESP32")