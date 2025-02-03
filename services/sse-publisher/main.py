# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fastapi[standard]>=0.115.7",
#     "pydantic-settings>=2.7.1",
#     "uvicorn>=0.34.0",
# ]
# ///
import asyncio
from fastapi import FastAPI, Request, Response, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global list to hold client queues for broadcasting
clients: List[asyncio.Queue] = []
clients_lock = asyncio.Lock()


@app.get("/healthz")
async def health():
    return {"status": "ok"}


async def event_generator(queue: asyncio.Queue, request: Request):
    """
    Generator that yields messages from the queue as SSE formatted events.
    """
    try:
        while True:
            # If the client has disconnected, break out.
            if await request.is_disconnected():
                break

            # Wait for the next message.
            message = await queue.get()
            # SSE event format: "data: <message>\n\n"
            yield f"data: {message}\n\n"
    except asyncio.CancelledError:
        # The generator was cancelled (likely because the client disconnected)
        return


@app.get("/sse/news")
async def sse_endpoint(request: Request, background_tasks: BackgroundTasks):
    """
    SSE endpoint for clients to subscribe to events.
    """
    # Create a new queue for this client.
    client_queue = asyncio.Queue()

    # Add the client queue to the global list in a thread-safe way.
    async with clients_lock:
        clients.append(client_queue)

    async def client_disconnect():
        async with clients_lock:
            if client_queue in clients:
                clients.remove(client_queue)

    # Create the streaming response with SSE media type.
    generator = event_generator(client_queue, request)
    # Add cleanup as a background task so that when the response is finished,
    # the client_disconnect function is called.
    background_tasks.add_task(client_disconnect)

    return StreamingResponse(generator, media_type="text/event-stream")


@app.post("/sse/news")
async def publish(request: Request):
    """
    Publish endpoint to broadcast a message to all connected clients.
    """
    # Read the raw body.
    data = await request.body()
    message = data.decode("utf-8")

    # Broadcast the message to every client's queue.
    async with clients_lock:
        for queue in clients:
            await queue.put(message)

    # Return a No Content response.
    return Response(status_code=204)


if __name__ == "__main__":
    # Run the FastAPI app with uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5004, reload=True)
