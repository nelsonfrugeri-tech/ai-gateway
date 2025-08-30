# AIGateway — Artificial Intelligence Gateway

HTTP platform based on FastAPI to unify access to GenAI providers (currently Azure/OpenAI), offering endpoints for chat (synchronous and streaming), embeddings, image generation, batch processing, quota management, costs and structured logging.

> The API code base is in `src/`. This README summarizes the architecture, how to run and how to consume the endpoints.

---

## Overview
- Protocol: HTTP/JSON with FastAPI.
- Support for: chat, chat streaming (SSE), embeddings, images, files, batches, quotas and provider list.
- Providers: abstraction via "drives"; current implementation for `azure_openai` using Python OpenAI SDK.
- Observability: structured logs (structlog), correlation via `X-Correlation-Id`, and Datadog integration (ddtrace) for traces/latency.
- Persistence: MongoDB used for the quota module (balance/limit per client and model).

---

## Architecture (high level)
- `src/api/app.py`: FastAPI app creation, lifecycle (Mongo connection), middlewares and exception handlers.
- `src/api/adapter/http/v1`: HTTP layer
  - `endpoint/`: routes (chat, embeddings, images, files, batches, quotas, providers, health, swagger)
  - `header/`: header validation (`BaseHeader`, `QuotaHeader`)
  - `middleware/`: `HeaderMiddleware`, `LogMiddleware`, `QuotaMiddleware`
  - `payload/`: Pydantic request/response models (API contracts)
  - `mapper/`: conversion between domains (providers, quotas, batch file)
  - `handle/`: routing and error handlers
  - `log/`: HTTP log models and logger for quota middleware
- `src/api/adapter/service/provider`: provider integration layer
  - `azure_openai/`: client, domain, and drives (chat, embeddings, images, files, batch)
  - `service_provider.py`: selects the drive by provider name
- `src/api/adapter/database/mongodb`: client, logger and helpers for MongoDB
- `src/api/core`: business rules (business), costs, logs, exceptions and utilities
- `src/api/domain`: domain entities (Provider, Model, Quota, File, etc.)
- `src/api/adapter/cache/simple/provider_cache.py`: in-memory cache of providers/models (based on `ProviderBusiness`).

Key points:
- Middlewares
  - `HeaderMiddleware` saves the `X-Correlation-Id` in context for propagation in logs.
  - `LogMiddleware` generates structured HTTP logs and masks sensitive content (prompt) outside of `LOG_LEVEL=DEBUG`.
  - `QuotaMiddleware` (toggle by env) validates and debits tokens based on usage returned by the provider.
- Exceptions/Errors: dedicated handlers for 400/401/404/429/500 with consistent payloads.
- Costs: `CostClient` calculates text costs from prices configured per model; image still "TODO".

Useful references in the code:
- App: `src/api/app.py:1`
- Routes: `src/api/adapter/http/v1/handle/route_handle.py:1`
- Quotas (business): `src/api/core/business/quota_business.py:1`
- Static providers: `src/api/core/business/provider_business.py:1`
- OpenAI/Azure client: `src/api/adapter/service/provider/azure_openai/client/azure_openai_client.py:1`

---

## Endpoints
Base path configurable via `AIGATEWAY_API_PATH` (default `/ai-gateway`). Below, paths relative to this prefix.

- Health
  - GET `/health` — API status.
- Chat
  - POST `/v1/chat` — text generation.
  - POST `/v1/chat/stream` — SSE streaming of partial responses.
- Embeddings
  - POST `/v1/embeddings` — embedding generation.
- Images
  - POST `/v1/images/generations` — image generation (DALL·E-2/DALL·E-3/GPT‑4o*).
- Files (batch)
  - POST `/v1/files` — creates file (JSONL content in base64) for batch use.
  - GET `/v1/files/{fileId}` — queries file metadata.
- Batches
  - POST `/v1/batches` — creates batch processing (chat completions).
  - GET `/v1/batches/{batchId}` — queries status/result.
- Providers
  - GET `/v1/providers` — lists available providers and models.
- Quotas
  - POST `/v1/quotas` — creates quota.
  - GET `/v1/quotas` — searches quotas by `useCaseId`, `providerName`, `modelName`.
  - PATCH `/v1/quotas` — enables/disables quota.
- Swagger UI (custom)
  - GET `/swagger` — UI. OpenAPI at `/swagger.json`.

Headers (required in most operations):
- `X-Correlation-Id` (UUID)
- `X-User-Id` (string)
- `client_id` (UUID)
- Quotas admin: add `X-Admin-Auth` with the value of `GENAI_QUOTA_AUTHENTICATION`.

Minimum example — Chat
```bash
curl -X POST "http://localhost:8080/ai-gateway/v1/chat" \
  -H 'Content-Type: application/json' \
  -H 'X-Correlation-Id: 11111111-1111-1111-1111-111111111111' \
  -H 'X-User-Id: demo-user' \
  -H 'client_id: 22222222-2222-2222-2222-222222222222' \
  -d '{
    "provider": {"name": "azure_openai", "model": {"name": "gpt-4o"}},
    "prompt": {
      "messages": [
        {"role": "user", "content": "Say hello in Portuguese."}
      ],
      "parameter": {"temperature": 0.2, "max_tokens": 128}
    }
  }'
```

Example — Embeddings
```bash
curl -X POST "http://localhost:8080/ai-gateway/v1/embeddings" \
  -H 'Content-Type: application/json' \
  -H 'X-Correlation-Id: 11111111-1111-1111-1111-111111111111' \
  -H 'X-User-Id: demo-user' \
  -H 'client_id: 22222222-2222-2222-2222-222222222222' \
  -d '{
    "provider": {"name": "azure_openai", "model": {"name": "text-embedding-ada-002"}},
    "content": {"texts": ["text A", "text B"]}
  }'
```

Example — Quotas (admin)
```bash
curl -X POST "http://localhost:8080/ai-gateway/v1/quotas" \
  -H 'Content-Type: application/json' \
  -H 'X-Correlation-Id: 11111111-1111-1111-1111-111111111111' \
  -H 'X-User-Id: demo-user' \
  -H 'client_id: 22222222-2222-2222-2222-222222222222' \
  -H 'X-Admin-Auth: <value-of-GENAI_QUOTA_AUTHENTICATION>' \
  -d '{
    "unit": "tokens",
    "limit": 100000,
    "useCase": {"id": "case-01", "name": "my-app"},
    "provider": {"name": "azure_openai", "model": {"name": "gpt-4o"}}
  }'
```

Streaming — Chat
- Endpoint: `/v1/chat/stream`
- Header and payload same as synchronous chat
- Response: `text/event-stream` with events containing chunks (`delta`) and, at the end, `usage` (tokens) and calculated cost.

---

## Quotas (middleware)
- Toggle by env: `TOGGLE_QUOTA_MIDDLEWARE` (`true`/`false`).
- Applies to: `POST /v1/chat`, `POST /v1/embeddings`, `POST /v1/similarity`.
- Operation:
  1) Before calling the provider, validates if there is an active quota for `client_id` + `provider` + `model`.
  2) If there is none or balance is 0, returns error (`404` or `429`).
  3) After successful response, debits `usage.total_tokens` from current balance asynchronously.
- Tables: `quotas` collection (MongoDB). Model in `src/api/domain/quota.py:1`.

---

## Cost Calculation
- Implemented for text/embeddings: `src/api/core/cost/cost_client.py:1` + `text_cost.py`.
- Based on prices per model defined in `ProviderBusiness` (tokens per million, currency, etc.).
- Response includes `cost` field when there is a configured price for the model.
- Images: calculation method not yet implemented (`image_cost.py`).

---

## Providers and Models
- Source: `ProviderBusiness.find()` defines the providers/models exposed via API (`/v1/providers`).
- Current provider: `azure_openai` with models like `gpt-4o`, `gpt-4o-mini`, `text-embedding-ada-002`, `dall-e-2`, `dall-e-3`, batch variants, etc.
- Validations: provider/model name, generation type (text/embedding/image), `max_tokens` limits, batch support, etc.

Important about the provider client:
- The current client instantiates `OpenAI()` (standard SDK) in `azure_openai_client.py`.
- There is a factory ready for Azure (`AzureOpenAIFactoryClient`) with control by deployment/api_version, but it's commented out. If you want to use native Azure OpenAI, you'll need to adjust this point in the code.

---

## Environment Variables
Main variables (see example in `src/example.env:1`):
- App/API
  - `AIGATEWAY_API_TITLE`, `AIGATEWAY_API_DESCRIPTION`
  - `AIGATEWAY_API_PATH` (e.g., `/ai-gateway`)
  - `AIGATEWAY_SERVER_HOST` and `AIGATEWAY_SERVER_PORT`
- MongoDB
  - `MONGODB_USER`, `MONGODB_PASSWORD`, `MONGODB_DATABASE`, `MONGODB_CONNECTION`
- Auth (Quotas)
  - `GENAI_QUOTA_AUTHENTICATION` (UUID) for `X-Admin-Auth`
- Logging/Tracing
  - `LOG_LEVEL` (INFO/DEBUG), `DD_*` (ddtrace)
- Feature toggle
  - `TOGGLE_QUOTA_MIDDLEWARE` (`true`/`false`)
- Azure/OpenAI (if using Azure factory)
  - `AZURE_OPENAI_WEST_US_API_KEY`, `AZURE_OPENAI_WEST_US_ENDPOINT`
  - `AZURE_OPENAI_EAST_US_API_KEY`, `AZURE_OPENAI_EAST_US_ENDPOINT`
  - `HTTPX_CLIENT_VERIFY` (`True`/`False`)

Startup observation: the app validates Mongo configs on startup; missing ones trigger `StartupErrorException`.

---

## Execution
Prerequisites:
- Python 3.12+
- MongoDB running (accessible as per `MONGODB_CONNECTION`)
- API keys from the provider (OpenAI/Azure) as per client used

Dependency installation (example):
```bash
python -m venv .venv && source .venv/bin/activate
pip install -U fastapi uvicorn pydantic pydantic-settings python-dotenv \
  openai httpx structlog ddtrace motor pymongo tiktoken numpy typing_extensions
```

Local execution (without Docker):
```bash
# Export environment variables or create a .env in the current directory
python src/api/app.py
# or, with uvicorn
uvicorn src.api.app:api --factory --host 0.0.0.0 --port 8080
```

Swagger UI:
- Access `http://localhost:8080/ai-gateway/swagger`

### Docker
There is a basic `Dockerfile`. Notes:
- It expects a `requirements.txt` (not included in this repository). Create one with the dependencies above or adjust the Dockerfile to install via `pip install ...`.

Build and run (example):
```bash
docker build -t aigateway .
# Pass necessary envs (-e) or a --env-file
docker run --rm -p 8080:8080 \
  -e AIGATEWAY_API_PATH=/ai-gateway \
  -e MONGODB_CONNECTION='mongodb://usr:pwd@host:27017/db?authSource=db' \
  -e MONGODB_USER=usr -e MONGODB_PASSWORD=pwd -e MONGODB_DATABASE=db \
  aigateway
```

---

## Best Practices and Limitations
- Prompt log redaction: content is masked at different levels of `LOG_LEVEL` to reduce risk of leakage.
- Image costs: implementation pending.
- Azure client: factory ready but not used by default; requires code adjustment if necessary.
- `requirements.txt`: missing — create/align according to your needs.

---

## Folder Structure (summary)
```
src/
  api/
    app.py
    adapter/
      http/v1/ ... (endpoints, headers, payloads, middleware, mappers, logs)
      service/provider/azure_openai/... (client, drives, domains)
      database/mongodb/... (client and logger)
      cache/simple/provider_cache.py
    core/ ... (business, cost, log config, exceptions, files)
    domain/ ... (entities)
  example.env
```

---

## License
No explicit license. Check with maintainers before public use/distribution.
