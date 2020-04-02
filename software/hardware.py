import RPi.GPIO
import RPLCD
import gpiozero

_lcd = RPLCD.CharLCD(pin_rs=25, pin_rw=22, pin_e=24, pins_data=[3, 15, 2, 14], numbering_mode=RPi.GPIO.BCM)
_lcd.clear()

_green = gpiozero.PWMLED(21)
_red = gpiozero.PWMLED(20)

def display(line1, line2, align1 = "<", align2 = "<"):
    display_line1 = ("{: " + align1 + "20}").format(line1)[:21]
    display_line2 = ("{: " + align2 + "20}").format(line2)[:21]
    text = display_line1 + display_line2
    _lcd.write_string(text)

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
