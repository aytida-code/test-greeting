# Checkpoint

## Design decisions
- Stack: Python 3.13.5, FastAPI 0.115.6, Uvicorn; no persistence or messaging.
- Single greeting feature group: `User` domain entity (only `name`), schema DTOs, injected greeting service, thin FastAPI routes.
- Public routes: `POST /greet` and operational `GET /health`; port 8000.
- Error handling: centralized envelope with correlation ID middleware and standard logging.
- Delivery: Docker app service plus PostgreSQL `postgres:17.2`; database is infrastructure-only.

## Progress
- [x] STEP 1: Design and endpoint classification (`POST /greet`: TESTABLE; `GET /health`: TESTABLE; docs/OpenAPI: TESTABLE).
- [ ] STEP 2-7: Application and infrastructure
- [ ] STEP 10-11: Compile, smoke, boot verification
- [ ] STEP 15: Reports
- [ ] Final Docker verification
