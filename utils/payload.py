import time 
from adafruit_hid.keycode import Keycode as AdaKeycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
from keycode_win_de import Keycode

import adafruit_logging as logging

class PayloadExecutor():
    def __init__(self, logger: logging.Logger, keyboard: Keyboard, mouse: Mouse):
        self.logger = logger
        self.keyboard = keyboard
        self.mouse = mouse

        self.special_keys = {
            "ENTER": Keycode.ENTER,
            "SPACE": Keycode.SPACE,
            "TAB": Keycode.TAB,
            "SHIFT": Keycode.SHIFT,
            "CTRL": Keycode.CONTROL,
            "ALT": Keycode.ALT,
            "WIN": Keycode.WINDOWS,
            "F1": Keycode.F1,
            "F2": Keycode.F2,
            "F3": Keycode.F3,
            "F4": Keycode.F4,
            "F5": Keycode.F5,
            "F6": Keycode.F6,
            "F7": Keycode.F7,
            "F8": Keycode.F8,
            "F9": Keycode.F9,
            "F10": Keycode.F10,
            "F11": Keycode.F11,
            "F12": Keycode.F12,
            "UP": Keycode.UP_ARROW,
            "DOWN": Keycode.DOWN_ARROW,
            "LEFT": Keycode.LEFT_ARROW,
            "RIGHT": Keycode.RIGHT_ARROW,
            "PAGEUP": Keycode.PAGE_UP,
            "PAGEDOWN": Keycode.PAGE_DOWN,
            "HOME": Keycode.HOME,
            "END": Keycode.END,
            "INSERT": Keycode.INSERT,
            "DELETE": Keycode.DELETE,
            "BACKSPACE": Keycode.BACKSPACE,
            "ESC": Keycode.ESCAPE,
            "PRINT": Keycode.PRINT_SCREEN,
            "SCROLLLOCK": Keycode.SCROLL_LOCK,
            "PAUSE": Keycode.PAUSE,
            "CAPSLOCK": Keycode.CAPS_LOCK,
            "NUMLOCK": Keycode.KEYPAD_NUMLOCK,
            "MENU": Keycode.APPLICATION,
            "PAUSE": Keycode.PAUSE
        }

        self.special_char = {
            "/": [Keycode.SHIFT, Keycode.SEVEN],
            "\\": [Keycode.ALTGR, Keycode.OEM_102],
            ":": [Keycode.SHIFT, Keycode.PERIOD],
            ".": Keycode.PERIOD,
            ",": Keycode.COMMA,
            "&": [Keycode.SHIFT, Keycode.SIX],
            "=": [Keycode.SHIFT, Keycode.ZERO],
            "?": [Keycode.SHIFT, 0x2D],
            "\"": [Keycode.SHIFT, Keycode.TWO],
            ">": [Keycode.SHIFT, Keycode.OEM_102],
            "<": [Keycode.OEM_102]
        }

        self.numbers = {
            0: "ZERO",
            1: "ONE",
            2: "TWO",
            3: "THREE",
            4: "FOUR",
            5: "FIVE",
            6: "SIX",
            7: "SEVEN",
            8: "EIGHT",
            9: "NINE",
        }
        pass

    def execute_playload(self, payload: str):
        self.logger.info("Executing payload...")
        self.logger.info(payload)

        first_line = True

        for line in payload.split("\n"):
            if not first_line:
                time.sleep(0.1)
            
            first_line = False

            self.logger.info("Executing line: " + line)
            words = line.split(" ")

            command = words[0]
            data = line[(len(command) + 1):]

            if command == "SLEEP":
                self.logger.info(f"Sleeping for {data} seconds!")
                try:
                    time.sleep(float(data))
                except:
                    self.logger.error(f"Could not cast {data} to float in SLEEP command!")
                    pass
                continue

            if command == "PR":
                keys = data.split(" ")

                for key in keys:
                    self.logger.info("Pressing key: " + key)
                    self.keyboard.press(self.translate_key(key))

                time.sleep(0.1)

                for key in keys:
                    self.logger.info("Releasing key: " + key)
                    self.keyboard.release(self.translate_key(key))
                continue
                
            if command == "PRESS":
                keys = data.split(" ")

                for key in keys:
                    self.logger.info("Pressing key: " + key)
                    self.keyboard.press(self.translate_key(key))
                        
                continue
                
            if command == "RELEASE":
                keys = data.split(" ")

                for key in keys:
                    self.logger.info("Releasing key: " + key)
                    self.keyboard.release(self.translate_key(key))

                continue
                
            if command == "RELEASE_ALL":
                self.logger.info("Releasing all keys")
                self.keyboard.release_all()
                continue
                
            if command == "TYPE":
                self.logger.info("Typing: " + data)
                for char in data:
                    self.logger.debug(f"Typing Char: {char}, {self.translate_key(char)}")
                    
                    key = self.translate_key(char)
                    if isinstance(key, list):
                        self.keyboard.send(*self.translate_key(char))
                        continue

                    self.keyboard.send(self.translate_key(char))
                continue

            # ! Mouse commands

            if command == "MOVE":
                self.logger.info("Moving mouse")
                x, y = data.split(" ")
                self.mouse.move(int(x), int(y))
                continue

            if command == "CLICK":
                self.logger.info("Clicking mouse")
                self.mouse.click(Mouse.LEFT_BUTTON)
                continue

            if command == "RIGHT_CLICK":
                self.logger.info("Right clicking mouse")
                self.mouse.click(Mouse.RIGHT_BUTTON)
                continue

            if command == "SCROLL":
                self.logger.info("Scrolling mouse")
                wheel = data.split(" ")[0]
                self.mouse.move(wheel=int(wheel))
                continue
                

            self.logger.debug("Unknown command: " + command)
            continue
                
            
    def translate_key(self, key: str):
        self.logger.debug(f"Translating: {key}, Upper: {key.upper()}")
        if key == " ":
            return Keycode.SPACE
        
        #key = key.strip()

        if key in self.special_keys:
            return self.special_keys.get(key)

        if key in self.special_char:
            return self.special_char.get(key)

        if key.isdigit():
            return getattr(Keycode, self.numbers.get(int(key)))

        if key.isupper():
            return [Keycode.SHIFT, getattr(Keycode, key.upper())]

        return getattr(Keycode, key.upper())