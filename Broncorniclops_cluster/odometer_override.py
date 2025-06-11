import os
import json
import RPi.GPIO as GPIO

SETTINGS_FILE = "data/system/odometer_protection.json"
LOG_FILE = "logs/odometer_changes.log"
OVERRIDE_PIN = 17

def check_override():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(OVERRIDE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    if GPIO.input(OVERRIDE_PIN) == GPIO.LOW:
        # Reset credentials
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"username": "admin", "password": "admin"}, f, indent=2)
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a") as log:
            log.write("ODOMETER PASSWORD OVERRIDE TRIGGERED: credentials reset to default\n")
        return True
    return False