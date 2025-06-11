# Raspberry Pi Digital Gauge Cluster

This project is a fully customizable, touchscreen-based digital instrument cluster for a Ford Bronco, powered by a Raspberry Pi 3B and a 1024x600 IPS display. It integrates CAN bus vehicle data, supports custom gauge layouts, fan/thermal management, and secure odometer handling.

---

## Features

- Full CAN-based data integration (PID support)
- Swipe gesture navigation and toolbar access
- Layout editor with drag-and-drop and profile saving
- Auto-dimming display and night/day themes
- Digital and analog gauge styles (bar, needle, numeric)
- Fault code (DTC) reading, logging, and clearing
- Dual PWM fan control (CPU + ambient temp)
- Secure odometer with logging and password protection
- Modular design with theme support (fonts, icons, textures)
- UPS integration and safe shutdown logic

---

## Core Modules

| File | Purpose |
|------|---------|
| `cluster_app.py` | Main entry point that initializes the UI and logic |
| `layout_editor.py` | Draggable layout system for gauges |
| `gauge_renderer.py` | Rendering logic for gauge visual styles |
| `layout_mode_toggle.py` | Enables or disables edit mode |
| `layout_profile_manager.py` | Save/load multiple layout presets |
| `layout_profile_popup.py` | GUI for managing saved layouts |
| `layout_saver.py` | Auto-load/save default layout file |
| `toolbar.py` | Top menu with settings and layout access |
| `auto_hide_toolbar.py` | Auto-hiding gesture-activated toolbar wrapper |
| `settings_popup.py` | Central UI for all configurable features |
| `gesture_manager.py` | Swipe and tap gesture control |
| `style_manager.py` | Font, color, and texture manager |
| `style_settings_panel.py` | UI for changing visual styles |
| `odometer_display.py` | Displays odometer and trip meters |
| `odometer_manager.py` | Secures odometer edits with password and logs |
| `odometer_settings_popup.py` | Settings panel to set odometer credentials |
| `dtc_manager.py` | Reads and monitors diagnostic trouble codes |
| `dtc_popup.py` | Displays DTCs with expandable icons and logs |
| `diagnostics_overlay.py` | CPU, fan, and ambient diagnostics overlay |
| `fan_controller.py` | Controls dual PWM fans with hysteresis |
| `ambient_temp_sensor.py` | Reads temperature from AM2302 sensor |

---

## Data Sources

- **CAN bus** via Waveshare dual-channel HAT
- **Ambient temp** from DHT22/AM2302 sensor
- **CPU temp** from Pi system
- **Fuel sensor** via analog ADC (future)
- **Gear (PRNDL)** via CAN
- **All alerts and diagnostics** auto-logged and icon displayed

---

## Layout Persistence

- Default layout auto-loads on startup
- Layouts saved when exiting edit mode
- Profiles can be managed in the UI

---

## Odometer Protection

- Trip reset button
- Odometer editing requires username + password
- All odometer changes are logged and undeletable

---

## File Structure

See `structure.txt` for the full directory and file map.

## MPG Calculation

- **Instant MPG** is calculated using smoothed speed and fuel rate (via CAN).
- **Trip MPG** is averaged from start/reset.
- Displayed in a dedicated panel accessible via:
  - Swipe up gesture
  - Layout editor (can be positioned/saved)
- Trip MPG can be reset programmatically via `.reset_trip()`.

## MPG and Trip Reset

- **Current MPG** (smoothed) and **Trip MPG** are displayed in a panel.
- **Reset Trip** button clears both the trip odometer and trip MPG.
- Panel is draggable in layout editor and toggleable with swipe gesture.

## UPS and Shutdown Overlay

- The system monitors the vehicle's ACC signal and UPS battery voltage using `ups_monitor.py`.
- If ACC turns off, the app shows a **"Shutdown pending..."** overlay.
- If battery voltage drops below safe levels, a shutdown is immediately triggered.
- Communication between the UPS monitor and the UI occurs over a UNIX socket.
- Key Files:
  - `ups_monitor.py`: Background daemon that manages shutdown logic
  - `shutdown_overlay.py`: UI overlay triggered via socket
  - `ups_monitor.service`: Systemd service for the monitor

## Manual Shutdown Button

- Accessible from the Settings panel
- Triggers a safe system shutdown
- Works alongside UPS-triggered shutdown behavior