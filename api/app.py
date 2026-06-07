from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routes import tasks_router
from api.middleware.auth import AuthMiddleware

from db.init import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AI Taskflow",
    version="1.0.0",
    description="A lightweight distributed task processing system for AI workloads.",
    lifespan=lifespan,
)

app.add_middleware(AuthMiddleware)

app.include_router(
    tasks_router,
    prefix="/api/v1",
    tags=["tasks"],
)


@app.get("/", tags=["health"])
def root():
    return {
        "status": "ok",
        "message": "AI Taskflow is running",
    }


@app.get("/health", tags=["health"])
def health():
    return {
        "status": "ok"
    }
