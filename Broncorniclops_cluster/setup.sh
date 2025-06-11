#!/bin/bash

echo "🚀 Setting up Broncorniclops Digital Cluster Environment..."

# Update and install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-kivy i2c-tools git

# Enable I2C and SPI
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

# Install Python packages
pip3 install RPi.GPIO adafruit-blinka adafruit-circuitpython-dht     pyserial python-can pyyaml kivy[base] --break-system-packages

# Create directories
mkdir -p ~/digital_cluster/{logs,data,layouts,themes,icons,pids,config}
mkdir -p ~/digital_cluster/data/system

# Enable auto-login for 'pi' user
sudo raspi-config nonint do_boot_behaviour B2

# Configure systemd service
cat <<EOF | sudo tee /etc/systemd/system/cluster_app.service
[Unit]
Description=Digital Cluster App
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/digital_cluster/cluster_app.py
WorkingDirectory=/home/pi/digital_cluster
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable cluster_app.service

echo "✅ Setup complete. Reboot to start the cluster automatically."

# Reboot automatically to apply changes
sudo reboot