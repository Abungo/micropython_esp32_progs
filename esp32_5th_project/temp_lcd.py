from microWebSrv import MicroWebSrv
from machine import Pin
from dht import DHT11
import network
sensor = DHT11(Pin(4))   # DHT-22 on GPIO 15
sta_if = network.WLAN(network.STA_IF)

def _httpHandlerDHTGet(httpClient, httpResponse):
    try:
        sensor.measure()   # Poll sensor
        t,h,r = sensor.temperature(),sensor.humidity(),sta_if.status('rssi')
        if all(isinstance(i, int) for i in [t,h,r]):   # Confirm values
            data = 'TEMP:{0:.1f} CHUMID:{1:.1f}%RSSI:{2:.1f}%'.format(t,h,r)
        else:
            data = 'Invalid reading.'
    except:
        data = 'Attempting to read sensor...'
        
    httpResponse.WriteResponseOk(
        headers = ({'Cache-Control': 'no-cache'}),
        contentType = 'text/event-stream',
        contentCharset = 'UTF-8',
        content = 'data: {0}\n\n'.format(data) )

routeHandlers = [ ( "/dht", "GET",  _httpHandlerDHTGet ) ]
srv = MicroWebSrv(routeHandlers=routeHandlers, webPath='/www/')
srv.Start(threaded=True)