# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fastapi[standard]>=0.115.7",
#     "pydantic-settings>=2.7.1",
#     "uvicorn>=0.34.0",
# ]
#
# [dependency-groups]
# dev = [
#     "black",
#     "isort",
#     "ruff",
# ]
# ///
import asyncio
import json
import time

import uvicorn
from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Security,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import APIKeyHeader

from config import settings

app = FastAPI(
    title="SSE Publisher",
)


auth_header = APIKeyHeader(
    name="Authorization",
    auto_error=False,
)


def authorize(
    header: str = Security(auth_header),
):

    is_authorized = header and header.removeprefix("Bearer ") == settings.api_token

    if not is_authorized:
        raise HTTPException(
            status_code=403,
            detail="Invalid or missing credentials. Header: Authorization",
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "detail": exc.errors(),
                "body": exc.body,
            }
        ),
    )


clients: list[asyncio.Queue] = []
clients_lock = asyncio.Lock()


@app.get("/health/")
async def health():
    return {"status": "ok"}


async def event_generator(
    queue: asyncio.Queue,
    request: Request,
):

    try:
        while True:
            if await request.is_disconnected():
                break

            try:
                message = await asyncio.wait_for(queue.get(), timeout=30)

                event = message["event"]
                data = json.dumps(message["data"])

                yield f"event: {event}\ndata: {data}\n\n"

            except asyncio.TimeoutError:
                yield ": keep-alive\n\n"


    except asyncio.CancelledError:
        return


    # try:
    #     while True:
    #         if await request.is_disconnected():
    #             break
    #
    #         message = await queue.get()
    #
    #         event = message["event"]
    #         data = json.dumps(message["data"])
    #
    #         yield f"event: {event}\ndata: {data}\n\n"
    #
    # except asyncio.CancelledError:
    #     return


@app.get("/sse/")
async def sse_subscribe(
    request: Request,
    background_tasks: BackgroundTasks,
):
    client_queue = asyncio.Queue()

    async with clients_lock:
        clients.append(client_queue)

    async def client_disconnect():
        async with clients_lock:
            if client_queue in clients:
                clients.remove(client_queue)

    generator = event_generator(client_queue, request)

    background_tasks.add_task(client_disconnect)

    return StreamingResponse(generator, media_type="text/event-stream")


@app.post("/sse/{event}/")
async def publish(
    request: Request,
    event: str,
    _=Depends(authorize),
):

    try:
        data = await request.json()
    except json.JSONDecodeError as e:
        raise RequestValidationError(
            errors=["invalid payload"],
            body={
                "message": str(e),
                "payload": await request.body(),
            },
        ) from e

    message = {
        "event": event,
        "data": data,
    }

    async with clients_lock:
        for queue in clients:
            await queue.put(message)

    return JSONResponse(
        content=message,
        status_code=201,
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa S104
        port=settings.port,
        reload=settings.debug,
    )
