import os
import json

LAYOUT_DIR = "data/layouts"

class LayoutProfileManager:
    def __init__(self):
        os.makedirs(LAYOUT_DIR, exist_ok=True)

    def save_profile(self, name, layout_data):
        path = os.path.join(LAYOUT_DIR, f"{name}.json")
        with open(path, "w") as f:
            json.dump(layout_data, f, indent=2)

    def load_profile(self, name):
        path = os.path.join(LAYOUT_DIR, f"{name}.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return []

    def list_profiles(self):
        return [f[:-5] for f in os.listdir(LAYOUT_DIR) if f.endswith(".json")]

    def delete_profile(self, name):
        path = os.path.join(LAYOUT_DIR, f"{name}.json")
        if os.path.exists(path):
            os.remove(path)