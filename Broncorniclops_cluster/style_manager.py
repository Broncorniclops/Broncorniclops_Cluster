import os
import json

STYLE_CONFIG = "data/system/style_config.json"

class StyleManager:
    def __init__(self):
        self.current_theme = "light"
        self.current_font = "default"
        self.colors = {
            "bg": "#000000",
            "fg": "#FFFFFF",
            "accent": "#00FF00"
        }
        self.textures = {}
        self._load()

    def _load(self):
        if os.path.exists(STYLE_CONFIG):
            with open(STYLE_CONFIG, 'r') as f:
                data = json.load(f)
                self.current_theme = data.get("theme", self.current_theme)
                self.current_font = data.get("font", self.current_font)
                self.colors = data.get("colors", self.colors)
                self.textures = data.get("textures", self.textures)

    def save(self):
        with open(STYLE_CONFIG, 'w') as f:
            json.dump({
                "theme": self.current_theme,
                "font": self.current_font,
                "colors": self.colors,
                "textures": self.textures
            }, f, indent=2)

    def set_theme(self, theme):
        self.current_theme = theme
        self.save()

    def get_icon_path(self, icon_name):
        return f"assets/themes/{self.current_theme}/{icon_name}"

    def set_font(self, font_name):
        self.current_font = font_name
        self.save()

    def get_font(self):
        return self.current_font

    def set_color(self, key, value):
        self.colors[key] = value
        self.save()

    def get_color(self, key):
        return self.colors.get(key)

    def set_texture(self, key, path):
        self.textures[key] = path
        self.save()

    def get_texture(self, key):
        return self.textures.get(key)