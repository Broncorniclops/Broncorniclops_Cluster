import os
import json
from datetime import datetime

LAYOUT_DIR = "/home/pi/digital_cluster/layouts"
USB_MOUNT = "/media/pi"

class GaugeLayoutSharing:
    def __init__(self, layout_manager):
        self.layout_manager = layout_manager
        os.makedirs(LAYOUT_DIR, exist_ok=True)

    def export_layout(self, name="layout"):
        data = self.layout_manager.get_layout_data()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.json"
        path = os.path.join(LAYOUT_DIR, filename)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        return path

    def import_layout(self, path):
        if not os.path.exists(path):
            return False
        with open(path) as f:
            data = json.load(f)
        self.layout_manager.apply_layout_data(data)
        return True

    def export_to_usb(self):
        usb_path = self._detect_usb()
        if not usb_path:
            return "No USB detected"
        files = [f for f in os.listdir(LAYOUT_DIR) if f.endswith(".json")]
        if not files:
            return "No layout files to export"
        target = os.path.join(usb_path, "shared_layouts")
        os.makedirs(target, exist_ok=True)
        for f in files:
            src = os.path.join(LAYOUT_DIR, f)
            dst = os.path.join(target, f)
            with open(src, "rb") as rf, open(dst, "wb") as wf:
                wf.write(rf.read())
        return f"Exported {len(files)} layouts to {target}"

    def _detect_usb(self):
        if not os.path.exists(USB_MOUNT):
            return None
        for d in os.listdir(USB_MOUNT):
            path = os.path.join(USB_MOUNT, d)
            if os.path.ismount(path):
                return path
        return None