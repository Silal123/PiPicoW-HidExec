import json

json_data = {}

def file_exists(file: str) -> bool:
    try:
        with open(file, 'r') as f:
            return True
    except:
        return False

#def create():
#    if file_exists('config.json'): return
#    with open('config.json', 'a', encoding="utf-8") as json_file:
#        json.dump({}, json_file, indent=4)

#def save():
#    with open('config.json', 'w', encoding="utf-8") as json_file:
#        json.dump(json_data, json_file, indent=4)

def load():
    global json_data
    if not file_exists('config.json'):
        json_data = {}
        return
    with open('config.json', 'r', encoding="utf-8") as json_file:
        json_data = json.load(json_file)

#def create_default():
#    create()
#    entrys = {
#        "wifi.ssid": "TestESP",
#        "wifi.password": "12345678",
#        }
#    for entry, value in entrys.items():
#        elements = entry.split('.')
#        current_level = json_data
#        
#        for i, element in enumerate(elements):
#            if i == len(elements) - 1:
#                if element not in current_level:
#                    current_level[element] = value
#            else:
#                if element not in current_level:
#                    current_level[element] = {}
#                current_level = current_level[element]
#    save()


def get(key: str):
    elements = key.split('.')
    value = json_data
    for element in elements:
        if not value.get(element): return None
        value = value[element]
    return value

#create()
load()
#create_default()