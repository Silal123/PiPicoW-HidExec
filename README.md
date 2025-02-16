[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)


# Pi Pico W HID Remote
This is a projekt wich acts like a badusb. You can execute payloads, move the mouse and more!
## Authors

- [@Silal123](https://www.github.com/Sial123)


## Installation

Install this Projekt

#### Clone the git repository
```bash
git clone https://github.com/Silal123/{PROJEKT}
```

#### 1. Prepare thy pi pico W
Copy the **cpy.uf2** to your pi picos storage.
> _If there is a problem with the pi copy the **flash_nuke.uf2** to the storage to completly reset it!_

#### 2. Use the upload.py to upload the code
```bash 
python upload.py {Something like E}
```

#### 3. Restart the py by unpluging it
## Usage/Examples
When you start the pi it will autommaticly open a "wifi hotspot". When you connect to it you can open **192.168.4.1** in your browser. At this ip you can view the Dashboard of the pi. 

Example Script:
```bash
PR WIN r
SLEEP 0.1
TYPE cmd /c start https://youtu.be/dQw4w9WgXcQ?si=e7YQIXwcrGH9m84W && exit
SLEEP 0.1
PR ENTER
RELEASE_ALL
```
This will open your browser and play the youtube video.


## Documentation

#### PR [BUTTONS]
Will press a button and release it like:
```bash
PR WIN r
```

#### PRESS [BUTTONS]
This will only press the buttons, not release them again.
```bash
PRESS WIN
```

#### RELEASE [BUTTONS]
This will release the buttons.
```bash
RELEASE WIN
```

#### SLEEP [SECONDS]
This will pause the programm.
```bash
SLEEP 0.1
```

#### RELEASE_ALL
This will release all keys

#### TYPE [TEXT]
This will type a TEXT
```bash
TYPE Hello, this is a text :D
```

#### MOVE [x] [y]
This will move your mouse
```bash
MOVE 100 100
```

#### CLICK
This will click the left mouse button

#### RIGHT_CLICK
This will click the right mouse button

#### SCROLL [s]
This will scroll the given number
```bash
SCROLL 100
```