#!/bin/bash
echo "Running cluster update..."

cd /home/pi/digital_cluster || exit 1

# Ensure Git is available
if ! command -v git &> /dev/null; then
  echo "Git not found. Install Git first."
  exit 1
fi

# Pull latest changes
git pull origin main

# Update Python dependencies
pip install -r requirements.txt

# Restart the cluster app (systemd service assumed)
sudo systemctl restart cluster_app.service

echo "Update complete."