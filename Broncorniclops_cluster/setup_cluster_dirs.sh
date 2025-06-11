#!/bin/bash

echo "Setting up digital gauge cluster directory structure..."

CLUSTER_DIR="/home/pi/digital_cluster"

# Create core directories
mkdir -p $CLUSTER_DIR/{ui,logging,sensors,system,docs,logs,exported_logs}

# Set permissions
chown -R pi:pi $CLUSTER_DIR

echo "Directory structure created under $CLUSTER_DIR:"
tree $CLUSTER_DIR || ls -R $CLUSTER_DIR

echo "Ready for file deployment."