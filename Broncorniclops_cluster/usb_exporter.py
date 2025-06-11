import os
import shutil
from datetime import datetime

EXPORT_DIR = "/home/pi/digital_cluster/exported_logs"
MOUNT_BASE = "/media/pi"
USB_LABEL = None  # auto-detect

def detect_usb_mount():
    if not os.path.exists(MOUNT_BASE):
        return None
    for entry in os.listdir(MOUNT_BASE):
        mount_path = os.path.join(MOUNT_BASE, entry)
        if os.path.ismount(mount_path):
            return mount_path
    return None

def export_logs_to_usb():
    usb_path = detect_usb_mount()
    if not usb_path:
        return "No USB drive detected."

    target_dir = os.path.join(usb_path, "cluster_logs_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(target_dir, exist_ok=True)

    if not os.path.exists(EXPORT_DIR):
        return "No exported logs available."

    files = [f for f in os.listdir(EXPORT_DIR) if f.endswith(".log")]
    if not files:
        return "No log files to export."

    for f in files:
        shutil.copy2(os.path.join(EXPORT_DIR, f), os.path.join(target_dir, f))

    return f"Exported {len(files)} logs to: {target_dir}"