#!/bin/bash

echo "Optimizing Raspberry Pi OS Lite for fast boot and cluster readiness..."

# Enable auto-login for user 'pi'
sudo raspi-config nonint do_boot_behaviour B2
echo "Auto-login enabled."

# Disable unneeded services
DISABLE_SERVICES=(
  triggerhappy
  bluetooth
  hciuart
  avahi-daemon
  dphys-swapfile
  rsyslog
  man-db.timer
  apt-daily.timer
  apt-daily-upgrade.timer
)

for service in "${DISABLE_SERVICES[@]}"; do
  sudo systemctl disable $service 2>/dev/null
done
echo "Disabled unnecessary services."

# Pre-install Python dependencies
sudo apt update
sudo apt install -y python3-kivy python3-can can-utils python3-pip i2c-tools git

# Install optional Python modules
pip3 install adafruit-circuitpython-dht Adafruit-Blinka RPi.GPIO

# Enable I2C and SPI
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

# Set app to run via systemd (cluster_app.service assumed to be installed)
sudo systemctl enable cluster_app.service
echo "Enabled systemd startup for cluster app."

echo "Optimization complete. Reboot recommended."