# Odometer Password Override

If the odometer password is lost or forgotten, a secure reset is available using a hidden GPIO button.

## How to Trigger the Override

1. Wire a momentary push button to:
   - **GPIO 17 (Pin 11)**
   - **GND (e.g., Pin 9)**

2. During boot/startup, **press and hold the button**.

3. If the override is detected:
   - Odometer credentials are reset to:
     - Username: `admin`
     - Password: `admin`
   - A log entry is saved to: `logs/odometer_changes.log`
   - A warning popup may display on next startup (optional)

4. You can now log in and change the password in Settings > Odometer Protection.

## Notes
- This is a physical security measure. The button should be placed in a hidden or secure location.
- It only activates during startup.