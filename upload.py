import shutil
import os
import argparse

def copy_to_usb(drive_letter: str, skip_items: set):
    source_dir = os.getcwd()  # Aktuelles Verzeichnis
    destination_dir = f"{drive_letter}:\\"  # USB-Zielverzeichnis
    
    # Feste Ignore-Liste
    ignore_list = {"upload.py", "adafruit_logging.py", "adafruit_hid", "adafruit_httpserver", "keycode_win_de.py"}
    
    # Benutzerdefinierte Skip-Elemente hinzufügen
    ignore_list.update(skip_items)

    if not os.path.exists(destination_dir):
        print(f"Das Zielverzeichnis {destination_dir} existiert nicht. Stelle sicher, dass das USB-Laufwerk eingesteckt ist.")
        return
    
    for item in os.listdir(source_dir):
        if item in ignore_list:
            print(f"Überspringe: {item}")
            continue
        
        source_path = os.path.join(source_dir, item)
        destination_path = os.path.join(destination_dir, item)
        
        try:
            if os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
            else:
                shutil.copy2(source_path, destination_path)
            print(f"Kopiert: {source_path} -> {destination_path}")
        except Exception as e:
            print(f"Fehler beim Kopieren von {source_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kopiere Dateien auf ein USB-Laufwerk, mit der Möglichkeit, bestimmte Dateien/Ordner zu überspringen.")
    parser.add_argument("drive_letter", help="Buchstabe des USB-Laufwerks (z. B. E)")
    parser.add_argument("--skip", nargs="*", default=[], help="Zusätzliche Dateien oder Ordner, die übersprungen werden sollen")
    
    args = parser.parse_args()
    skip_items = set(args.skip)  # Benutzerdefinierte zu ignorierende Dateien/Ordner
    
    copy_to_usb(args.drive_letter, skip_items)
