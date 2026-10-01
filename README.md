# Greeting API

A minimal FastAPI service that accepts a user name and returns a greeting.

## Run locally

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./start.sh
```

The service listens on `0.0.0.0:8000` by default. Set `APP_HOST` and `APP_PORT` to configure the bind address and port.

## API

- `POST /greet` with `{"name":"Alice"}` returns `{"message":"Hello Alice"}`.
- `GET /health` returns the unauthenticated operational status.
- `GET /docs` provides Swagger UI and `GET /openapi.json` provides the OpenAPI document.

## Containers

Copy `.env.example` to `.env` and replace the development database password before deployment. The compose file includes the application and the required PostgreSQL 17.2 infrastructure service:

```sh
docker compose up --build
```
