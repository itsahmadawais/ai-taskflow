# AI Taskflow

A lightweight distributed task processing system for AI workloads built with FastAPI, PostgreSQL, Redis, and RQ.

## Overview

AI Taskflow is a backend system designed to handle long-running AI operations asynchronously. Instead of processing requests synchronously and blocking API consumers, tasks are persisted, queued, executed by background workers, and tracked throughout their lifecycle.

The project demonstrates practical backend engineering patterns commonly used in production systems, including task orchestration, asynchronous processing, queue-based workloads, worker architecture, persistence, and fault tolerance.

## Architecture

The system is composed of four primary components:

### API Layer

FastAPI provides REST endpoints for task submission and status retrieval.

### Persistence Layer

PostgreSQL stores task metadata, execution state, inputs, outputs, and failure information.

### Queue Layer

Redis acts as a broker for task distribution between API nodes and background workers.

### Worker Layer

RQ workers consume queued jobs and execute task processors independently from the API lifecycle.

## Task Lifecycle

1. Client submits a task
2. Task is persisted in PostgreSQL
3. Task ID is enqueued in Redis
4. Worker consumes the job
5. Task status transitions to processing
6. Appropriate processor executes business logic
7. Results are persisted
8. Task status transitions to completed or failed

## Supported Task Types

### Summarization

Generate concise summaries from input text.

### Translation

Translate content between languages.

### Classification

Categorize and label input content.

### Data Extraction

Extract structured information from unstructured text.

## Key Engineering Concepts Demonstrated

* Asynchronous task execution
* Background worker architecture
* Queue-based workload distribution
* Repository pattern
* Separation of concerns
* Database session management
* Retry mechanisms
* Fault isolation
* Structured logging
* Stateless API design

## Technology Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Redis
* RQ (Redis Queue)
* Pydantic

## Running Locally

### Start PostgreSQL

```bash
docker compose up postgres -d
```

### Start Redis

```bash
docker compose up redis -d
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start API

```bash
uvicorn main:app --reload
```

### Start Worker

```bash
rq worker tasks
```

## Example Workflow

Create a task:

```http
POST /api/v1/tasks
```

```json
{
  "task_type": "summarize",
  "input": {
    "text": "Long article content..."
  }
}
```

Response:

```json
{
  "id": "45b9f642-664d-424b-b507-84e9598d3003",
  "status": "pending"
}
```

Retrieve status:

```http
GET /api/v1/tasks/{id}
```

## Why This Project

This project was built to explore the architecture behind modern AI and distributed processing systems where work must be decoupled from request-response cycles. It focuses on reliability, maintainability, and clear separation between API, persistence, queueing, and execution concerns.

Rather than optimizing for framework complexity, the goal was to build a simple, understandable system that demonstrates core backend engineering principles used in production environments.
