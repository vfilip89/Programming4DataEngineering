#!/bin/bash
echo "🔄 Restarting NiFi..."
~/nifi/nifi-1.28.1/bin/nifi.sh restart

echo "🔄 Restarting NiFi Registry..."
~/nifi-registry-2.2.0/bin/nifi-registry.sh restart

echo "✅ Both NiFi and NiFi Registry have been restarted!"
