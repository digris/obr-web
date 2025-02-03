#!/usr/bin/env python3
import uvicorn
import asyncio
import logging
import json
import threading

from typing import AsyncIterable, List
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

__version__ = "0.0.1"

LOGGER = logging.getLogger(__name__)


class State:
    _lock = threading.Lock()
    _instance = None

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.news = []
        return cls._instance


class News(BaseModel):
    provider: str
    cmd: str


app = FastAPI(title="Contribution UI - Public", version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚀 Track all connected clients
connected_clients: List[asyncio.Queue] = []


@app.post("/publish/news")
async def publish_news(news: News):
    state = State()
    state.news.append(news)

    # 🚀 Notify all connected clients
    for queue in connected_clients:
        await queue.put(json.dumps([n.model_dump() for n in state.news]))

    state.news = []

    return {"message": "ok"}


async def sse_generator(request: Request) -> AsyncIterable[str]:
    queue = asyncio.Queue()
    connected_clients.append(queue)

    try:
        while True:
            if await request.is_disconnected():
                print("Client disconnected")
                break

            # 🚀 Wait for new messages (no sleep required)
            data = await queue.get()
            yield f"data: {data}\n\n"

    finally:
        connected_clients.remove(queue)


@app.get("/sse/news")
async def sse_news(request: Request) -> StreamingResponse:
    return StreamingResponse(sse_generator(request), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5004)
