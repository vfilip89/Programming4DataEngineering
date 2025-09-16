#!/bin/bash

# Enable strict error handling
set -e

echo "🛑 Stopping Kibana and Elasticsearch..."

# Stop Kibana
if [ -f ~/kibana.pid ]; then
    KIBANA_PID=$(cat ~/kibana.pid)
    if kill -0 $KIBANA_PID 2>/dev/null; then
        kill -TERM $KIBANA_PID && sleep 5
        kill -KILL $KIBANA_PID 2>/dev/null || true
        echo "✅ Kibana stopped."
    else
        echo "⚠️ Kibana is not running."
    fi
    rm -f ~/kibana.pid
else
    echo "⚠️ Kibana PID file not found."
fi

# Stop Elasticsearch
if [ -f ~/elasticsearch.pid ]; then
    ELASTIC_PID=$(cat ~/elasticsearch.pid)
    if kill -0 $ELASTIC_PID 2>/dev/null; then
        kill -TERM $ELASTIC_PID && sleep 5
        kill -KILL $ELASTIC_PID 2>/dev/null || true
        echo "✅ Elasticsearch stopped."
    else
        echo "⚠️ Elasticsearch is not running."
    fi
    rm -f ~/elasticsearch.pid
else
    echo "⚠️ Elasticsearch PID file not found."
fi

echo "🎉 All services stopped successfully!"