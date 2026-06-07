# AI TaskFlow

Python
FastAPI
PostgreSQL
Redis
RQ
LangChain
License

A lightweight distributed task processing system for AI workloads built with FastAPI, PostgreSQL, Redis, and RQ.

## Overview

AI TaskFlow is a backend system designed to handle long-running AI operations asynchronously. Instead of processing requests synchronously inside the API lifecycle, tasks are persisted, queued, executed by background workers, and tracked from submission to completion.

The project demonstrates practical backend engineering patterns used in production systems: task orchestration, asynchronous processing, queue-based workload distribution, worker architecture, fault isolation, and structured error handling.

---

## Architecture

```
Client
   │
   ▼
FastAPI API  ──→  PostgreSQL (task metadata, results)
   │
   ▼
Redis Queue
   │
   ▼
RQ Worker
   │
   ▼
LangChain / OpenAI
```

### Components


| Layer       | Technology              | Responsibility                           |
| ----------- | ----------------------- | ---------------------------------------- |
| API         | FastAPI                 | Task submission, status retrieval, auth  |
| Persistence | PostgreSQL + SQLAlchemy | Task state, inputs, outputs, errors      |
| Queue       | Redis + RQ              | Job distribution between API and workers |
| Workers     | RQ Worker               | Task execution, processor dispatch       |
| LLM         | LangChain + OpenAI      | AI workload execution                    |


---

## Task Lifecycle

```
pending  →  processing  →  completed
                       ↘  failed
```

1. Client submits a task via `POST /api/v1/tasks`
2. Task is persisted in PostgreSQL with status `pending`
3. Task ID is enqueued in Redis
4. RQ worker picks up the job
5. Status transitions to `processing`
6. Appropriate processor executes the AI workload
7. Result is persisted in PostgreSQL
8. Status transitions to `completed` or `failed`

---

## Supported Task Types

### Summarization — `summarize`

Generates a concise summary from input text.

```json
{
  "task_type": "summarize",
  "input": {
    "text": "The transformer architecture was introduced in the paper Attention is All You Need..."
  }
}
```

### Translation — `translate`

Translates text into a target language.

```json
{
  "task_type": "translate",
  "input": {
    "text": "Hello, how are you?",
    "target_language": "French"
  }
}
```

### Classification — `classify`

Classifies text into a category. Optionally constrain to a set of labels.

```json
{
  "task_type": "classify",
  "input": {
    "text": "Ahmad Raza, CNIC: 34-348538532-7, DOB 9-04-1992",
    "categories": ["ID", "CV", "Bank Statement"]
  }
}
```

If `categories` is omitted, the model picks the most appropriate label.

### Data Extraction — `data_extraction`

Extracts structured fields from unstructured text using a schema.

```json
{
  "task_type": "data_extraction",
  "input": {
    "text": "Ahmad Raza, CNIC: 34-348538532-7, DOB 9-04-1992, Lahore",
    "schema": {
      "name": "string",
      "cnic": "string",
      "dob": "string",
      "city": "string"
    }
  }
}
```

---

## API Reference

All protected routes require the `X-Service-Token` header.

### Authentication


| Header            | Description                        |
| ----------------- | ---------------------------------- |
| `X-Service-Token` | Required on all `/api/v1/*` routes |


### Endpoints

#### `POST /api/v1/tasks`

Submit a new task.

**Request body:** one of the task payloads above.

**Response:**

```json
{
  "id": "45b9f642-664d-424b-b507-84e9598d3003",
  "task_type": "summarize",
  "status": "pending",
  "input": { "text": "..." }
}
```

#### `GET /api/v1/tasks/{id}`

Retrieve task status and result.

**Response:**

```json
{
  "id": "45b9f642-664d-424b-b507-84e9598d3003",
  "task_type": "summarize",
  "status": "completed",
  "input": { "text": "..." },
  "result": "Transformers replaced RNNs by using self-attention...",
  "created_at": "2026-06-07T10:00:00",
  "updated_at": "2026-06-07T10:00:03"
}
```

**Status values:**


| Status       | Meaning                                               |
| ------------ | ----------------------------------------------------- |
| `pending`    | Queued, not yet picked up                             |
| `processing` | Worker is executing                                   |
| `completed`  | Result available                                      |
| `failed`     | Execution failed; `result.error` contains the message |


#### `GET /health`

Health check — no auth required.

---

## Error Handling

The worker distinguishes between permanent and transient errors:


| Error type    | Examples                                | Behaviour                                       |
| ------------- | --------------------------------------- | ----------------------------------------------- |
| **Permanent** | Invalid API key, bad request, not found | Marked `failed` immediately, no retry           |
| **Transient** | Rate limit, timeout, network error      | Retried up to 3 times (10s / 30s / 60s backoff) |


---

## Running Locally

### 1. Clone and set up environment

```bash
git clone https://github.com/itsahmadawais/ai-taskflow.git
cd ai-taskflow
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=sk-...
SERVICE_TOKEN=your_secret_token

DATABASE_URL=postgresql://postgres:admin123@localhost:5433/ai_taskflow

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

### 3. Start Redis and PostgreSQL

```bash
docker compose up -d
```

### 4. Start the API

```bash
uvicorn api.app:app --reload
```

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Start the worker

Open a separate terminal:

```bash
# Windows (SimpleWorker required — no os.fork support)
python worker/worker.py

# Linux / macOS
rq worker tasks --url redis://localhost:6379/0
```

---

## Batch Processing

RQ does not have a native batch endpoint, but you can submit multiple tasks in parallel and poll each ID:

```python
import httpx

tasks = [
    {"task_type": "summarize", "input": {"text": "Article one..."}},
    {"task_type": "summarize", "input": {"text": "Article two..."}},
    {"task_type": "classify",  "input": {"text": "Invoice #4521", "categories": ["Invoice", "Receipt", "Contract"]}},
]

headers = {"X-Service-Token": "your_secret_token"}

with httpx.Client(base_url="http://localhost:8000") as client:
    responses = [client.post("/api/v1/tasks", json=t, headers=headers) for t in tasks]
    ids = [r.json()["id"] for r in responses]
    print("Submitted:", ids)
```

Poll for results:

```python
import time

while True:
    statuses = [client.get(f"/api/v1/tasks/{id}", headers=headers).json() for id in ids]
    pending = [s for s in statuses if s["status"] in ("pending", "processing")]
    if not pending:
        break
    print(f"{len(pending)} tasks still running...")
    time.sleep(2)

for s in statuses:
    print(s["id"], s["status"], s.get("result", {}).get("error", ""))
```

---

## Project Structure

```
ai-taskflow/
│
├── api/
│   ├── app.py                  # FastAPI app, middleware, lifespan
│   ├── middleware/
│   │   └── auth.py             # Token-based auth middleware
│   └── routes/
│       ├── __init__.py
│       └── tasks.py            # POST /tasks, GET /tasks/{id}
│
├── core/
│   ├── ai_engine.py            # LangChain + OpenAI wrapper
│   ├── config.py               # Settings from .env
│   ├── logger.py               # Structured logging
│   ├── queue.py                # Redis connection, RQ queue
│   ├── retry.py                # Retry with permanent error detection
│   ├── task_executor.py        # Job entry point dispatched by worker
│   └── processors/
│       ├── summarization.py
│       ├── translation.py
│       ├── classification.py
│       └── extraction.py
│
├── db/
│   ├── base.py                 # SQLAlchemy declarative base
│   ├── dependencies.py         # FastAPI DB session dependency
│   ├── init.py                 # Table creation on startup
│   ├── session.py              # Engine and SessionLocal
│   ├── models/
│   │   └── task.py             # Task ORM model
│   └── repository/
│       └── task_repo.py        # CRUD operations
│
├── schemas/
│   └── task_schema.py          # Pydantic request/response models
│
├── worker/
│   └── worker.py               # RQ worker entry point
│
├── .env.example
├── docker-compose.yml
└── requirements.txt
```

---

## Key Engineering Patterns

- **Asynchronous task execution** — API returns immediately; worker processes independently
- **Repository pattern** — DB access isolated from business logic
- **Separation of concerns** — API, queue, execution, and persistence are fully decoupled
- **Structured logging** — Every request and task execution is traceable by ID
- **Fault isolation** — Permanent vs. transient error classification prevents infinite retries
- **Stateless API** — All state lives in PostgreSQL; API nodes are horizontally scalable
- **Token-based auth** — Service-to-service authentication via `X-Service-Token`

---

## Design Decisions

**Why Redis + RQ over Kafka?**
RQ provides sufficient queue semantics for this workload without Kafka's operational overhead. 
Appropriate for services processing thousands of tasks per day rather than millions per second.

**Why PostgreSQL for task state?**
Task results need durability and queryability. 
Redis alone would lose state on restart. 
PostgreSQL gives ACID guarantees for task metadata while Redis handles ephemeral queue coordination.

**Why synchronous SQLAlchemy over async?**
RQ workers run in separate processes — async, SQLAlchemy adds complexity without benefit in this context. Synchronous sessions are simpler, more debuggable, and appropriate for worker processes.

**Why permanent vs transient error separation?**
Retrying authentication failures or invalid requests wastes resources and masks bugs. 
Retrying rate limits and timeouts recovers from infrastructure noise. The distinction matters in production.

---

## Contributing

Contributions, bug reports, and feature requests are welcome. Open an issue or submit a pull request.

---

## License

MIT License