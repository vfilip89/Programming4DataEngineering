#!/bin/bash

# Enable strict error handling
set -e

echo "🟢 Starting NiFi and NiFi Registry..."

echo "Starting NiFi..."
~/nifi/nifi-1.28.1/bin/nifi.sh start
sleep 20  # Give NiFi some time to start

# Verify NiFi is running
if pgrep -f "org.apache.nifi.NiFi" > /dev/null; then
    echo "✅ NiFi started successfully!"
else
    echo "❌ ERROR: NiFi failed to start."
    exit 1
fi

echo "Starting NiFi Registry..."
~/nifi-registry-2.2.0/bin/nifi-registry.sh start
sleep 5  # Give Registry some time to start

# Verify NiFi Registry is running
if pgrep -f "org.apache.nifi.registry.NiFiRegistry" > /dev/null; then
    echo "✅ NiFi Registry started successfully!"
else
    echo "❌ ERROR: NiFi Registry failed to start."
    exit 1
fi

echo "🎉 All services started successfully!"

echo "🌍 Opening NiFi and NiFi Registry in Firefox..."

# Open NiFi and NiFi Registry in Firefox
firefox --new-tab "http://localhost:9300/nifi/" --new-tab "http://localhost:18080/nifi-registry" 2>/dev/null &