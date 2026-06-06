#!/bin/bash

# School Financial Approval Project — Launcher
# =============================================
# This script starts both the API server and opens the web interface

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_SCRIPT="$SCRIPT_DIR/src/backend/scripts/tor-api.py"
WEB_URL="http://localhost:8765"
ENV_FILE="$SCRIPT_DIR/src/backend/config/env.local"

echo "🏫 School Financial Approval Project"
echo "====================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

# Check if API script exists
if [ ! -f "$API_SCRIPT" ]; then
    echo "❌ Error: API script not found at $API_SCRIPT"
    exit 1
fi

# Service account JSON path
SERVICE_ACCOUNT_FILE="$SCRIPT_DIR/src/backend/config/gen-lang-client-0476777034-d38efeabd270.json"

# Load service account JSON if exists
if [ -f "$SERVICE_ACCOUNT_FILE" ]; then
    echo "🔐 Loading service account from $SERVICE_ACCOUNT_FILE"
    export GOOGLE_SERVICE_ACCOUNT_JSON=$(cat "$SERVICE_ACCOUNT_FILE")
else
    echo "⚠️  Warning: No service-account.json found at $SERVICE_ACCOUNT_FILE"
    echo "   Falling back to env.local (if available)..."
    if [ -f "$ENV_FILE" ]; then
        echo "🔐 Loading environment from $ENV_FILE"
        set -a
        source "$ENV_FILE"
        set +a
    fi
fi

# Export Google credentials for the API
export GOOGLE_SERVICE_ACCOUNT_EMAIL
export GOOGLE_PRIVATE_KEY
export SPREADSHEET_ID
export GOOGLE_API_KEY

# Start API server in background
echo "📡 Starting API Server on $WEB_URL"
python3 "$API_SCRIPT" &
API_PID=$!

# Wait for server to start
sleep 3

# Test if server is up
if ! curl -s "$WEB_URL" > /dev/null; then
    echo ""
    echo "⚠️  Warning: Server may not be ready yet. Waiting 2 more seconds..."
    sleep 2
fi

# Open web interface
echo "🌐 Opening Web Interface at $WEB_URL"
if command -v open &> /dev/null; then
    # macOS
    open "$WEB_URL"
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open "$WEB_URL"
elif command -v start &> /dev/null; then
    # Windows
    start "$WEB_URL"
else
    echo "ℹ️  Please open $WEB_URL manually in your browser"
fi

echo ""
echo "✅ System is running!"
echo ""
echo "📍 URLs:"
echo "   Web:    $WEB_URL"
echo "   API:    $WEB_URL/api"
echo "   Sheet:  https://docs.google.com/spreadsheets/d/1Plh_0AodTomKLyP8zrBp9FOriHXVm_uGYIO4TVHSozg/edit"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Wait for user interrupt
trap "echo ''; echo '👋 Stopping server...'; kill $API_PID 2>/dev/null; exit 0" INT
wait $API_PID
