import subprocess
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class WiFiSettingsPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        self.add_widget(Label(text="WiFi SSID:"))
        self.ssid_input = TextInput(multiline=False)
        self.add_widget(self.ssid_input)

        self.add_widget(Label(text="Password:"))
        self.password_input = TextInput(multiline=False, password=True)
        self.add_widget(self.password_input)

        self.status = Label(text="", color=(0, 1, 0, 1))
        self.add_widget(self.status)

        save_btn = Button(text="Connect", size_hint=(1, 0.3))
        save_btn.bind(on_press=self.save_wifi)
        self.add_widget(save_btn)

    def save_wifi(self, instance):
        ssid = self.ssid_input.text.strip()
        password = self.password_input.text.strip()
        if ssid and password:
            config = f'''
network={{
    ssid="{ssid}"
    psk="{password}"
    key_mgmt=WPA-PSK
}}
'''
            with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as f:
                f.write(config)
            subprocess.call(["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"])
            self.status.text = f"Connected to {ssid} (pending verification)"
        else:
            self.status.text = "SSID and Password required"