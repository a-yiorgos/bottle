FROM python:3.14-rc-slim

WORKDIR /app

RUN groupadd -r appgroup && useradd -r -g appgroup -u 1001 appuser

RUN pip install --no-cache-dir fastapi uvicorn redis

COPY --chown=appuser:appgroup api.py .

USER appuser

ENV PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "exec uvicorn api:app --host 0.0.0.0 --port ${PORT}"]
