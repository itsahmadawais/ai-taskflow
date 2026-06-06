# AI TaskFlow

A lightweight distributed task processing system for AI workloads.

AI TaskFlow enables developers to build scalable AI-powered applications using asynchronous task execution, Redis-backed queues, and worker-based processing. It provides a simple architecture for running LLM workflows, background jobs, and long-running AI tasks outside the request-response lifecycle.

## Features

* Distributed task execution
* Redis-backed job queues
* Asynchronous worker processing
* Task lifecycle tracking
* LangChain integration
* OpenAI-compatible model support
* Environment-based configuration
* FastAPI-powered API layer
* Docker-friendly deployment

---

## Architecture

```text
Client
   │
   ▼
FastAPI API
   │
   ▼
Redis Queue
   │
   ▼
RQ Worker
   │
   ▼
LangChain
   │
   ▼
LLM Provider
   │
   ▼
Result Storage
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/itsahmadawais/ai-taskflow.git
cd ai-taskflow
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

---

## Running Redis

```bash
docker compose up -d
```

Verify Redis is running:

```bash
docker ps
```

---

## Starting the API

```bash
uvicorn api.main:app --reload
```

---

## Starting Workers

Open a separate terminal:

```bash
rq worker tasks
```

---

## Creating a Task

```http
POST /tasks
```

Request:

```json
{
  "prompt": "Summarize the benefits of distributed systems.",
  "task_type": "summarize"
}
```

Response:

```json
{
  "id": "b1a8c8a7",
  "task_type": "summarize",
  "status": "queued",
  "result": null
}
```

---

## Checking Task Status

```http
GET /tasks/{task_id}
```

Response:

```json
{
  "id": "b1a8c8a7",
  "status": "completed",
  "result": "Distributed systems improve scalability..."
}
```

---

## Supported Tasks

Currently supported:

* summarize
* translate
* classify

---

## Project Structure

```text
ai-taskflow/
│
├── api/
│   └── routes.py
│
├── core/
│   ├── ai_engine.py
│   ├── config.py
│   ├── queue.py
│   └── tasks.py
│
├── worker/
│   └── worker.py
│
├── db/
│   └── job_store.py
│
├── .env
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Roadmap

### Upcoming

* Task registration system
* Decorator-based task definitions
* Plugin architecture
* Retry policies
* Dead-letter queue support
* Scheduled jobs
* Multi-worker scaling
* Observability and monitoring

---

## Why AI TaskFlow?

Most AI applications execute LLM calls synchronously inside API requests, leading to poor scalability and poor user experience.

AI TaskFlow separates execution from request handling by introducing asynchronous task processing, allowing AI workloads to run independently and scale horizontally through worker processes.

The architecture follows patterns commonly used in production systems built on Redis, SQS, Kafka, Celery, and distributed worker fleets.

---

## Contributing

Contributions, feature requests, and bug reports are welcome.

Feel free to open an issue or submit a pull request.

---

## License

MIT License
