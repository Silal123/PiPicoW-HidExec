import adafruit_logging as logging

logger = logging.getLogger('test')
logger.setLevel(logging.DEBUG)

logger.info("Starting...")

import time

import wifi
from adafruit_httpserver import Server, Request, Response, Websocket, GET, POST, JSONResponse, FileResponse, Redirect
import adafruit_httpserver

import board
import microcontroller
import socketpool
import os
import json
import hashlib
import struct

import usb_hid
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode as AdKeycode
from keycode_win_de import Keycode

from utils.payload import PayloadExecutor
from utils.dns import CaptivePortalDns

logger.info("Imports done")

mouse = Mouse(usb_hid.devices)  
logger.info("Mouse initialized")

keyboard = Keyboard(usb_hid.devices)
logger.info("Keyboard initialized")

logger.info("Running...")
time.sleep(0.5)


# ! Accesspoint

SSID = "TestESP"
PASSWORD = "12345678"

logger.info("Starting accesspoint")

wifi.radio.start_ap(ssid=SSID, password=PASSWORD)

while not wifi.radio.ap_active:
    logger.info("Waiting for accesspoint to start")
    time.sleep(0.5)

logger.info("Accesspoint started")
logger.info(f"SSID: {SSID}")
logger.info(f"Password: {PASSWORD}")
logger.info(f"IP: {wifi.radio.ipv4_gateway_ap}")

# ! Webserver

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)

@server.route("/")
def main(request: Request):
    return FileResponse(request, filename='index.html', root_path='/www')

@server.route("/tailwind")
def tailwind(request: Request):
    return FileResponse(request, filename='tailwind.css', root_path='/www')

@server.route("/exec/payload", POST)
def exec_payload(request: Request):
    data = request.json()
    payload = data["payload"]

    PayloadExecutor(logger, keyboard, mouse).execute_playload(payload)

    return JSONResponse(request, {"status": "executer"})

server.start(str(wifi.radio.ipv4_gateway_ap), 80)

while True:
    server.poll()