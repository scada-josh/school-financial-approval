#!/bin/bash

# School Financial Approval Project — Launcher
# =============================================
# This script starts both the API server and opens the web interface

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_SCRIPT="$SCRIPT_DIR/src/backend/scripts/tor-api.py"
WEB_PAGE="$SCRIPT_DIR/index.html"

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

# Check if web page exists
if [ ! -f "$WEB_PAGE" ]; then
    echo "❌ Error: Web page not found at $WEB_PAGE"
    exit 1
fi

# Start API server in background
echo "📡 Starting API Server on http://localhost:8765"
python3 "$API_SCRIPT" &
API_PID=$!

# Wait for server to start
sleep 2

# Open web interface
echo "🌐 Opening Web Interface"
if command -v open &> /dev/null; then
    # macOS
    open "$WEB_PAGE"
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open "$WEB_PAGE"
elif command -v start &> /dev/null; then
    # Windows
    start "$WEB_PAGE"
else
    echo "ℹ️  Please open $WEB_PAGE manually in your browser"
fi

echo ""
echo "✅ System is running!"
echo ""
echo "📍 URLs:"
echo "   API:    http://localhost:8765"
echo "   Web:    $WEB_PAGE"
echo "   Sheet:  https://docs.google.com/spreadsheets/d/1Plh_0AodTomKLyP8zrBp9FOriHXVm_uGYIO4TVHSozg/edit"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Wait for user interrupt
trap "echo ''; echo '👋 Stopping server...'; kill $API_PID 2>/dev/null; exit 0" INT
wait $API_PID
