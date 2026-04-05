# Ollama Chat UI

A simple web interface for multi-turn chat with local LLMs served by [Ollama](https://ollama.com).

## Prerequisites

- [Ollama](https://ollama.com) installed with at least one model pulled (e.g. `ollama pull gemma4:27b`)
- Python 3.12+

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Quick start (recommended)

Run both Ollama and the web UI with a single command:

```bash
./start_local.sh
```

Open http://localhost:8000 in your browser.

### Manual start

Start Ollama and the web server separately:

```bash
# Terminal 1
ollama serve

# Terminal 2
source .venv/bin/activate
uvicorn app:app --reload --port 8000
```

## Features

- Multi-turn conversation with full context
- Streaming token-by-token responses
- Thinking block rendering (for models that use `<think>` tags)
- Auto-detects all installed Ollama models
- New Chat button to reset conversation

## Project Structure

```
app.py              # FastAPI backend (proxies to Ollama API)
static/index.html   # Chat UI (vanilla HTML/JS)
requirements.txt    # Python dependencies
start_local.sh      # One-command launcher
```
