from pathlib import Path

import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

app = FastAPI()

OLLAMA_BASE = "http://localhost:11434"


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: list[Message]


@app.get("/", response_class=HTMLResponse)
async def index():
    return Path("static/index.html").read_text()


@app.get("/api/models")
async def list_models():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{OLLAMA_BASE}/api/tags")
        resp.raise_for_status()
        data = resp.json()
    return [m["name"] for m in data.get("models", [])]


class UnloadRequest(BaseModel):
    model: str


@app.post("/api/unload")
async def unload_model(req: UnloadRequest):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{OLLAMA_BASE}/api/generate",
            json={"model": req.model, "keep_alive": 0},
        )
        resp.raise_for_status()
    return {"status": "unloaded", "model": req.model}


@app.post("/api/chat")
async def chat(req: ChatRequest):
    async def stream():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_BASE}/api/chat",
                json={
                    "model": req.model,
                    "messages": [m.model_dump() for m in req.messages],
                    "stream": True,
                },
            ) as resp:
                resp.raise_for_status()
                async for chunk in resp.aiter_bytes():
                    yield chunk

    return StreamingResponse(stream(), media_type="application/x-ndjson")
