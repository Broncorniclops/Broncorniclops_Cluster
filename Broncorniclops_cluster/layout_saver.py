import json
import os

LAYOUT_PATH = "data/layouts/"

class LayoutSaver:
    def __init__(self):
        os.makedirs(LAYOUT_PATH, exist_ok=True)

    def save_layout(self, layout_name, layout_data):
        path = os.path.join(LAYOUT_PATH, f"{layout_name}.json")
        with open(path, "w") as f:
            json.dump(layout_data, f, indent=2)

    def load_layout(self, layout_name):
        path = os.path.join(LAYOUT_PATH, f"{layout_name}.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return {}

    def list_layouts(self):
        return [f[:-5] for f in os.listdir(LAYOUT_PATH) if f.endswith(".json")]