"""
AXIOMAI API — FastAPI entry point.

Run with:
    uvicorn app.main:app --reload
"""
import sys

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AXIOMAI API",
    description="Production-oriented Agentic RAG System",
    version="1.0.0",
)

app.include_router(router)
