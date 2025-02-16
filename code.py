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
import supervisor

import usb_hid
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode as AdKeycode
from keycode_win_de import Keycode

from utils.payload import PayloadExecutor
from utils.dns import CaptivePortalDns
from utils import config

logger.info("Imports done")

mouse = Mouse(usb_hid.devices)  
logger.info("Mouse initialized")

keyboard = Keyboard(usb_hid.devices)
logger.info("Keyboard initialized")

logger.info("Running...")
time.sleep(0.5)

if config.get('onplugin'):
    logger.info("ONPLUGIN found!")
    action = config.get('onplugin.action')
    logger.info(f"Onplugin Action: {action}")

    if action == "FILE":
        if config.get('onplugin.file'):
            file = config.get('onplugin.file')
            logger.info("File: " + file)
            with open(file, 'r') as file:
                data = ""
                for x in file:
                    data += x.strip() + "\n"
                data.strip()

                logger.info(f"File data: {data.replace(" ", ".").replace("\n", "!NEXTLINE!\n")}")
                try:
                    PayloadExecutor(logger, keyboard, mouse).execute_playload(data)
                except Exception as e:
                    logger.error(e)
                keyboard.release_all()

    elif action == "TEMPLATE":
        if config.get('onplugin.template'):
            template = config.get('onplugin.template')
            logger.info("Template: " + template)
            templates_d = config.get('templates')
            if template in templates_d:
                try:
                    PayloadExecutor(logger, keyboard, mouse).execute_playload("\n".join(templates_d[template]))
                except Exception as e:
                    logger.error(e)
                keyboard.release_all()



# ! Accesspoint

SSID = config.get("wifi.ssid") if config.get("wifi.ssid") else "TestESP"
PASSWORD = config.get("wifi.password") if config.get("wifi.password") else "12345678"

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

@server.route("/payload")
def payload(request: Request):
    return FileResponse(request, filename='payload.html', root_path='/www')

@server.route("/mouse")
def mouse_req(request: Request):
    return FileResponse(request, filename='mouse.html', root_path='/www')

@server.route("/tailwind")
def tailwind(request: Request):
    return FileResponse(request, filename='tailwind.css', root_path='/www')

@server.route("/templates")
def templates(request: Request):
    templates = config.get("templates")
    return JSONResponse(request, templates)

@server.route("/reload")
def restart(request: Request):
    supervisor.reload()
    return Response(request, "")

@server.route("/config", GET)
def config_r(request: Request):
    return FileResponse(request, filename='config.html', root_path='/www')

@server.route("/config/data", GET)
def config_get(request: Request):
    try:
        with open(config.file, 'r') as file:
            return JSONResponse(request, file.read())
    except Exception as e:
        logger.error(f"Error reading config: {e}")

@server.route("/config/data", POST)
def config_post(request: Request):
    data = request.json()
    try:
        with open(config.file, 'w') as file:
            file.write(data)
    except Exception as e:
        return Response(request, "", status=adafruit_httpserver.FORBIDDEN_403)

@server.route("/exec/payload", POST)
def exec_payload(request: Request):
    data = request.json()
    payload = data["payload"]

    PayloadExecutor(logger, keyboard, mouse).execute_playload(payload)

    return JSONResponse(request, {"status": "executer"})

@server.route("/mouse/move", POST)
def mouse_move(request: Request):
    data = request.json()

    if not "action" in data:
        return Response(request, "", status=adafruit_httpserver.BAD_REQUEST_400)
    
    if data["action"] == "MOVE":
        if not "x" and "y" in data:
            return Response(request, "", status=adafruit_httpserver.BAD_REQUEST_400)
        
        try:
            x = int(data["x"])
            y = int(data["y"])
            scroll = int(data["scroll"])
        except Exception as e:
            logger.error(f"Error in mouse move: {e}")

        mouse.move(x, y, scroll)
        return Response(request, "", status=adafruit_httpserver.OK_200)
    
    if data["action"] == "CLICK":
        if not "button" in data:
            return Response(request, "", status=adafruit_httpserver.BAD_REQUEST_400)
        
        button = data["button"]

        if button == "LEFT":
            mouse.click(Mouse.LEFT_BUTTON)

        if button == "RIGTH":
            mouse.click(Mouse.RIGHT_BUTTON)

        return Response(request, "", status=adafruit_httpserver.OK_200)

server.start(str(wifi.radio.ipv4_gateway_ap), 80)

while True:
    server.poll()