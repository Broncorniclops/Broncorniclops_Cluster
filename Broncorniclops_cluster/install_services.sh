#!/bin/bash
echo "Installing cluster services..."

# Install systemd services
sudo cp cluster_app.service /etc/systemd/system/
sudo cp ups_monitor.service /etc/systemd/system/
sudo cp apply_update_schedule.service /etc/systemd/system/

# Enable systemd services
sudo systemctl enable cluster_app.service
sudo systemctl enable ups_monitor.service
sudo systemctl enable apply_update_schedule.service

# Start services immediately
sudo systemctl start cluster_app.service
sudo systemctl start ups_monitor.service
sudo systemctl start apply_update_schedule.service

# Ensure SSH is enabled
sudo systemctl enable ssh
sudo systemctl start ssh

echo "All services installed and started."