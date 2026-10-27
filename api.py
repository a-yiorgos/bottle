import logging
import os
import socket
from datetime import datetime, timezone
from urllib.parse import urlsplit, urlunsplit
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
local_counter = 0


def mangle_redis_url(url: str) -> str:
    if not url:
        return ""
    parsed = urlsplit(url)
    if parsed.password:
        user = parsed.username or ""
        host_port = parsed.netloc.rsplit("@", 1)[-1]
        new_netloc = f"{user}:***@{host_port}"
        parsed = parsed._replace(netloc=new_netloc)
        return urlunsplit(parsed)
    return url


REDIS_URL = os.getenv("REDIS_URL")
redis_client = None

if REDIS_URL:
    import redis

    logger.info(f"Starting with REDIS: {mangle_redis_url(REDIS_URL)}")
    redis_client = redis.from_url(REDIS_URL)
    redis_client.setnx("counter", 0)  # initialise only if key absent
else:
    logger.info("Starting without REDIS")


def increment_counter() -> int:
    if redis_client:
        return redis_client.incr("counter")
    global local_counter
    local_counter += 1
    return local_counter


@app.get("/")
def root():
    now = datetime.now(timezone.utc)
    return {
        "n": increment_counter(),
        "hostname": socket.gethostname(),
        "timestamp": int(now.timestamp()),
        "date": now.isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
