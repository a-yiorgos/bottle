from fastapi import FastAPI
from datetime import datetime, timezone
import os
import socket

app = FastAPI()
local_counter = 0

REDIS_URL = os.getenv("REDIS_URL")
redis_client = None

if REDIS_URL:
    import redis
    redis_client = redis.from_url(REDIS_URL)
    redis_client.setnx("counter", 0)  # initialise only if key absent


def increment_counter() -> int:
    if redis_client:
        return redis_client.incr("counter")
    global local_counter
    local_counter += 1
    return local_counter


@app.get("/")
def root():
    return {
        "n": increment_counter(),
        "hostname": socket.gethostname(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
