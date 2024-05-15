# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import uftpd
import webrepl
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('OnePlus 6T', '12345678')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig(),sta_if.status('rssi'))
    # Write IP address to file
    with open('ip.txt', 'w') as file:
        file.write(sta_if.ifconfig()[0])
do_connect()
uftpd.restart()
webrepl.start()