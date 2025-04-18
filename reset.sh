#!/bin/bash

echo "🧼 Resetting..."
sudo docker container stop phishing-web 2>/dev/null
sudo docker container rm phishing-web 2>/dev/null
sudo docker image rm phishing-analyzer-web phishing-analyzer -f 2>/dev/null
echo "✅ Done. Ready for a clean start."
