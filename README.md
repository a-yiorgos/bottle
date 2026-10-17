# bottle

Bottle is a lightweight FastAPI web application designed for educational purposes that tracks visitor hit counts and returns system diagnostic metadata. On each HTTP GET request to the root endpoint, the application increments a counter—persisted in Redis if the `REDIS_URL` environment variable is defined, or maintained in local memory otherwise—and responds with a JSON payload containing the updated visit count (`n`), the server's `hostname`, Unix epoch seconds (`timestamp`), and an ISO 8601 UTC date string (`date`).
