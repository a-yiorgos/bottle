from fastapi import FastAPI
from datetime import datetime, timezone
import socket

app = FastAPI()
counter = 0


@app.get("/")
def root():
    global counter
    counter += 1
    return {
        "n": counter,
        "hostname": socket.gethostname(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
