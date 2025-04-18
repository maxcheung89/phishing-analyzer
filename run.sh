#!/bin/bash

set -e

echo "🔐 Checking .env file..."
if [ ! -f .env ]; then
  echo "❌ .env not found!"
  echo "Please create one with your VirusTotal API key like:"
  echo "VT_API_KEY=your_api_key_here"
  exit 1
fi

echo "🔧 Building Docker image..."
docker build -t phishing-analyzer -f Dockerfile .

echo "🚀 Running phishing analyzer on http://localhost:5000"
docker run --rm -p 5000:5000 \
  --cap-add=NET_RAW --cap-add=NET_ADMIN \
  -v "$(pwd)/backend/static/results:/app/static/results" \
  --env-file .env \
  phishing-analyzer &

# 🕒 Give Flask some time to start
sleep 2

# 🌐 Try to open in browser
URL="http://localhost:5000"
echo "🌍 Opening browser to $URL"
if command -v xdg-open >/dev/null; then
  xdg-open "$URL"
elif command -v open >/dev/null; then
  open "$URL"
else
  echo "Please open your browser and go to $URL"
fi
