#!/bin/bash

USERNAME="broncorniclops"
PASSWORD="digitalcluster"
STATIC_IP="192.168.1.200"
GATEWAY="192.168.1.1"
DNS="8.8.8.8"

echo "Creating user $USERNAME..."
sudo adduser --disabled-password --gecos "" $USERNAME
echo "$USERNAME:$PASSWORD" | sudo chpasswd
sudo usermod -aG sudo $USERNAME

echo "Copying SSH keys from pi to $USERNAME..."
sudo mkdir -p /home/$USERNAME/.ssh
sudo cp -r /home/pi/.ssh/* /home/$USERNAME/.ssh/ 2>/dev/null
sudo chown -R $USERNAME:$USERNAME /home/$USERNAME/.ssh

echo "Enabling SSH service..."
sudo systemctl enable ssh
sudo systemctl start ssh

echo "Setting static IP..."
if ! grep -q "interface wlan0" /etc/dhcpcd.conf; then
  echo "
interface wlan0
static ip_address=$STATIC_IP/24
static routers=$GATEWAY
static domain_name_servers=$DNS
" | sudo tee -a /etc/dhcpcd.conf
fi

echo "Setup complete. Please reboot to apply static IP."