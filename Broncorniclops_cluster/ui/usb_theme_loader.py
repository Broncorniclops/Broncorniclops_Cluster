import os
import shutil

FONT_DIR = "/home/pi/digital_cluster/fonts"
THEME_DIR = "/home/pi/digital_cluster/themes"
USB_BASE = "/media/pi"

class USBThemeLoader:
    def __init__(self):
        os.makedirs(FONT_DIR, exist_ok=True)
        os.makedirs(THEME_DIR, exist_ok=True)

    def scan_and_import(self):
        usb_path = self.detect_usb()
        if not usb_path:
            return "No USB drive detected"

        imported = []

        for root, _, files in os.walk(usb_path):
            for f in files:
                if f.lower().endswith(".ttf"):
                    shutil.copy2(os.path.join(root, f), FONT_DIR)
                    imported.append(f"Font: {f}")
                elif f.lower().endswith(".json") and "theme" in f.lower():
                    shutil.copy2(os.path.join(root, f), THEME_DIR)
                    imported.append(f"Theme: {f}")

        if not imported:
            return "No fonts or themes found on USB"
        return f"Imported: {', '.join(imported)}"

    def detect_usb(self):
        if not os.path.exists(USB_BASE):
            return None
        for d in os.listdir(USB_BASE):
            path = os.path.join(USB_BASE, d)
            if os.path.ismount(path):
                return path
        return None