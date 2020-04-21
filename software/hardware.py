import RPi.GPIO
import RPLCD
import gpiozero
from itertools import chain, repeat
import time

_width = 20
_width1 = 21
_lcd = RPLCD.CharLCD(pin_rs=25, pin_rw=22, pin_e=24, pins_data=[3, 15, 2, 14], numbering_mode=RPi.GPIO.BCM)
_lcd.clear()

_green = gpiozero.PWMLED(21)
_red = gpiozero.PWMLED(20)

def write(line1, line2, align1 = "<", align2 = "<"):
    display_line1 = ("{: " + align1 + str(_width) + "}").format(line1)[:_width1]
    display_line2 = ("{: " + align2 + str(_width) + "}").format(line2)[:_width1]
    text = display_line1 + display_line2
    _lcd.clear()
    _lcd.write_string(text)

def scroll_top(text, prepad=0, interpad=int(_width/2), postpad=_width, delay=0.2, repeats=1):
    pre_pad = " " * prepad
    inter_pad = " " * interpad
    post_pad = " " * postpad

    sequence = chain(pre_pad, 
                     chain.from_iterable(repeat(text + inter_pad, repeats - 1)),
                     text + post_pad)

    buffer = ""
    for char in sequence:
        buffer = (buffer + char)[-_width:]
        if len(buffer) == _width:
            _lcd.cursor_pos = (0, 0)
            _lcd.write_string(buffer)
            print("'" + buffer + "'")
            time.sleep(delay)

def clear():
    _lcd.clear()

def green_on():
    _green.on()

def green_off():
    _green.off()

def green_pulse():
    _green.pulse()

def green_blink():
    _green.blink()

def red_on():
    _red.on()

def red_off():
    _red.off()

def red_pulse():
    _red.pulse()

def red_blink():
    _red.blink()

def both_on():
    green_on()
    red_on()

def both_off():
    green_off()
    red_off()

def both_pulse():
    green_pulse()
    red_pulse()

def both_blink():
    green_blink()
    red_blink()
