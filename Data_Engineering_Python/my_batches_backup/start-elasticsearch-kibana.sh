#!/bin/bash

# Enable strict error handling
set -e

echo "🟢 Starting Elasticsearch and Kibana as background processes..."

# Start Elasticsearch in the background
cd ~/elasticsearch-8.17.0/bin
./elasticsearch > ~/elasticsearch.log 2>&1 &
echo $! > ~/elasticsearch.pid
echo "✅ Elasticsearch started (PID: $(cat ~/elasticsearch.pid))"

sleep 10  # Allow Elasticsearch some time to initialize

# Start Kibana in the background
cd ~/kibana-8.17.0/bin
./kibana > ~/kibana.log 2>&1 &
echo $! > ~/kibana.pid
echo "✅ Kibana started (PID: $(cat ~/kibana.pid))"

echo "🌍 Opening Kibana dashboard in Firefox..."
echo "⏳ It takes a few seconds..."

sleep 40  # Allow Kibana to initialize

# Open Kibana UI in Firefox
firefox --new-tab "http://localhost:5601" 2>/dev/null &

echo "🎉 Elasticsearch and Kibana started successfully!"
