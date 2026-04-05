#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

cleanup() {
    echo "Shutting down..."
    kill "$OLLAMA_PID" "$UVICORN_PID" 2>/dev/null
    wait "$OLLAMA_PID" "$UVICORN_PID" 2>/dev/null
    echo "Done."
}
trap cleanup EXIT INT TERM

# Start Ollama server
echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
for i in $(seq 1 30); do
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "Ollama is ready."
        break
    fi
    if [[ $i -eq 30 ]]; then
        echo "Error: Ollama failed to start within 30 seconds."
        exit 1
    fi
    sleep 1
done

# Activate venv and start FastAPI
echo "Starting web UI on http://localhost:8000 ..."
source .venv/bin/activate
uvicorn app:app --host 0.0.0.0 --port 8000 &
UVICORN_PID=$!

echo "Ready. Open http://localhost:8000 in your browser."
echo "Press Ctrl+C to stop."

wait
