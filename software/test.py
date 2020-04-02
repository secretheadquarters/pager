import hardware
import time

#                 123456789 123456789 123456789 123456789 |
hardware.display("TOP SECRET", "Authorised use only.", "^", "<")

hardware.both_on()
time.sleep(1)
hardware.both_off()
time.sleep(1)
hardware.red_pulse()
time.sleep(10)
hardware.both_blink()
time.sleep(10)

hardware.clear()
