from fastapi import FastAPI
from api.routes import router

app = FastAPI(title = "AI Taskflow")

app.include_router(router)