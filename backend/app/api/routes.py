"""
FactFlow API Routes.

Thin API layer — all business logic lives in the orchestration graph.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.orchestration.graph import run_factflow

router = APIRouter()


# ── Request / Response Models ──

class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str
    trust_score: float | None = None
    decision: str | None = None
    hallucination: bool | None = None


class HealthResponse(BaseModel):
    status: str
    service: str


# ── Routes ──

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Execute the full FactFlow agentic RAG pipeline."""
    try:
        result = run_factflow(request.query)

        return QueryResponse(
            answer=result.get("answer", ""),
            trust_score=result.get("validation", {}).get("trust_score"),
            decision=result.get("validation", {}).get("decision"),
            hallucination=result.get("hallucination", {}).get("hallucination"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthResponse)
async def health():
    """Service health check."""
    return HealthResponse(status="ok", service="FactFlow")
