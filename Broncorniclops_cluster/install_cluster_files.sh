#!/bin/bash

echo "Installing digital gauge cluster files..."

CLUSTER_DIR="/home/pi/digital_cluster"
mkdir -p $CLUSTER_DIR/{ui,logging,sensors,system,docs,logs,exported_logs}

# Move files into place
mv cluster_app.py $CLUSTER_DIR/
mv *.service $CLUSTER_DIR/system/ 2>/dev/null
mv *.sh $CLUSTER_DIR/system/ 2>/dev/null
mv *_panel.py $CLUSTER_DIR/ui/ 2>/dev/null
mv sensor_*.py $CLUSTER_DIR/sensors/ 2>/dev/null
mv can_interface.py $CLUSTER_DIR/sensors/ 2>/dev/null
mv log_*.py $CLUSTER_DIR/logging/ 2>/dev/null
mv usb_exporter.py $CLUSTER_DIR/logging/ 2>/dev/null
mv readme.md structure.txt odometer_override.md $CLUSTER_DIR/docs/ 2>/dev/null

# Set ownership and permissions
chown -R pi:pi $CLUSTER_DIR
chmod +x $CLUSTER_DIR/system/*.sh 2>/dev/null

echo "Files deployed to $CLUSTER_DIR."