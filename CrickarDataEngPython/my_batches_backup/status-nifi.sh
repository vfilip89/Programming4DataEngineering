#!/bin/bash
echo "🔎 Checking NiFi status..."
~/nifi/nifi-1.28.1/bin/nifi.sh status

echo "🔎 Checking NiFi Registry status..."
~/nifi-registry-2.2.0/bin/nifi-registry.sh status
