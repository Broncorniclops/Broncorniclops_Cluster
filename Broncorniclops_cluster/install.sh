#!/bin/bash

echo "🚀 Starting Broncorniclops Digital Cluster Installation..."

# ===== 1. Update system and install dependencies =====
echo "📦 Updating system and installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-kivy i2c-tools git wmctrl tree

# ===== 2. Enable I2C and SPI =====
echo "🔧 Enabling I2C and SPI..."
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

# ===== 3. Install Python packages =====
echo "🐍 Installing Python packages..."
pip3 install --break-system-packages RPi.GPIO adafruit-blinka adafruit-circuitpython-dht pyserial python-can pyyaml kivy[base]

# ===== 4. Create directory structure =====
echo "📁 Creating project directory structure..."
CLUSTER_DIR="/home/pi/digital_cluster"
mkdir -p $CLUSTER_DIR/{ui,logging,sensors,system,docs,logs,exported_logs,data/system,data/pid_mappings}
chown -R pi:pi $CLUSTER_DIR

# ===== 5. Optional: Create new user =====
read -p "➕ Create new user 'broncorniclops' for dedicated access? (y/n): " CREATE_USER
if [[ "$CREATE_USER" == "y" ]]; then
  USERNAME="broncorniclops"
  PASSWORD="digitalcluster"

  echo "👤 Creating user $USERNAME..."
  sudo adduser --disabled-password --gecos "" $USERNAME
  echo "$USERNAME:$PASSWORD" | sudo chpasswd
  sudo usermod -aG sudo $USERNAME

  echo "📋 Copying SSH keys from pi..."
  sudo mkdir -p /home/$USERNAME/.ssh
  sudo cp -r /home/pi/.ssh/* /home/$USERNAME/.ssh/ 2>/dev/null
  sudo chown -R $USERNAME:$USERNAME /home/$USERNAME/.ssh
fi

# ===== 6. Enable SSH =====
echo "🔐 Enabling SSH service..."
sudo systemctl enable ssh
sudo systemctl start ssh

# ===== 7. Optional: Static IP setup =====
read -p "🌐 Configure static IP (wlan0) to 192.168.1.200? (y/n): " SET_STATIC
if [[ "$SET_STATIC" == "y" ]]; then
  STATIC_IP="192.168.1.200"
  GATEWAY="192.168.1.1"
  DNS="8.8.8.8"

  echo "📡 Configuring static IP on wlan0..."
  if ! grep -q "interface wlan0" /etc/dhcpcd.conf; then
    echo "
interface wlan0
static ip_address=$STATIC_IP/24
static routers=$GATEWAY
static domain_name_servers=$DNS
" | sudo tee -a /etc/dhcpcd.conf
  fi
  sudo systemctl restart dhcpcd
fi

# ===== 8. Install systemd service =====
echo "🛠 Installing systemd service..."
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

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable cluster_app.service

echo "✅ Installation complete. Reboot required to apply all changes."
read -p "🔁 Reboot now? (y/n): " REBOOT
if [[ "$REBOOT" == "y" ]]; then
  sudo reboot
else
  echo "ℹ️ Please reboot manually later to apply changes."
fi
