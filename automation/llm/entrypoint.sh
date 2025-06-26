#!/usr/bin/env bash

# Start the server in the background
ollama serve &

# Wait a few seconds for server to come up
sleep 5

# Pull the models
# ollama pull deepseek-r1:1.5b
ollama pull phi4-mini:3.8b

# Kill the server and restart it
pkill -f "ollama serve"
ollama serve
