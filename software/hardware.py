import RPi.GPIO
import RPLCD

lcd = RPLCD.CharLCD(pin_rs=25, pin_rw=22, pin_e=24, pins_data=[3, 15, 2, 14], numbering_mode=RPi.GPIO.BCM)
lcd.clear()

def write_string(text):
    lcd.write_string(text)

