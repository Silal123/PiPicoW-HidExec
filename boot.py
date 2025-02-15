import storage
import os
import digitalio
import board
import busio
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

led.value = True

remount_button = digitalio.DigitalInOut(board.GP11)
remount_button.switch_to_input(pull=digitalio.Pull.UP)

if remount_button.value:
    print("Remounting USB drive")
    storage.remount("/", readonly=False)

led.value = False

time.sleep(0.5)

led.value = True

disable_usb = digitalio.DigitalInOut(board.GP10)
disable_usb.switch_to_input(pull=digitalio.Pull.UP)

if disable_usb.value:
    print("Disabling USB drive")
    storage.disable_usb_drive()

led.value = False