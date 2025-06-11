import os
import shutil
from datetime import datetime

EXPORT_ITEMS = {
    "layouts": "/home/pi/digital_cluster/layouts",
    "logs": "/home/pi/digital_cluster/logs",
    "themes": "/home/pi/digital_cluster/themes",
    "icons": "/home/pi/digital_cluster/icons",
    "pids": "/home/pi/digital_cluster/pids"
}

USB_MOUNT = "/media/pi"

class ConfigExporter:
    def __init__(self):
        self.target_root = self.detect_usb()

    def detect_usb(self):
        if not os.path.exists(USB_MOUNT):
            return None
        for entry in os.listdir(USB_MOUNT):
            path = os.path.join(USB_MOUNT, entry)
            if os.path.ismount(path):
                return os.path.join(path, "digital_cluster_backup")
        return None

    def export_all(self):
        if not self.target_root:
            return "No USB drive detected."

        os.makedirs(self.target_root, exist_ok=True)
        exported = []

        for label, src_path in EXPORT_ITEMS.items():
            if os.path.exists(src_path):
                dst = os.path.join(self.target_root, label)
                shutil.copytree(src_path, dst, dirs_exist_ok=True)
                exported.append(label)

        return f"Exported: {', '.join(exported)}"