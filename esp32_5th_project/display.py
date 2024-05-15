"""ILI9341 demo (orientation)."""
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont


def test():
    """Test code."""
    print('Loading Espresso Dolce font...')
    espresso_dolce = XglcdFont('fonts/EspressoDolce18x24.c', 18, 24)
    print('Font loaded.')
    # Baud rate of 40000000 seems about the max
    spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    
    display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17),
					  width=320, height=280, rotation=90)
    display.draw_text(0, 0, 'Abungo Thokchom', espresso_dolce,color565(0, 255, 255))
    #display.cleanup()

test()



