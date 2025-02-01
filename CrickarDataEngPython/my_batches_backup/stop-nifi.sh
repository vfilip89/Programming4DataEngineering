#!/bin/bash
echo "🛑 Stopping NiFi..."
~/nifi/nifi-1.28.1/bin/nifi.sh stop

echo "🛑 Stopping NiFi Registry..."
~/nifi-registry-2.2.0/bin/nifi-registry.sh stop

echo "✅ All services have been stopped!"
