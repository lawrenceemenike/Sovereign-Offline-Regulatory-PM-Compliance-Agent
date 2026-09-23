import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.compliance import router as compliance_router
from backend.database.session import init_db
from backend.rag.knowledge_base import get_knowledge_base
from backend.rag.seed_data import SEED_REGULATIONS


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    kb = get_knowledge_base()
    if kb.index.ntotal == 0:
        kb.add_chunks(SEED_REGULATIONS)
    yield
    # Shutdown logic if needed


app = FastAPI(
    title="LexGuard - Sovereign Regulatory Compliance Engine",
    description="Offline Air-Gapped Compliance & PM Regulatory Agent for Brendan Nicholas Holdings (BNH)",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Next.js Executive Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Compliance Endpoints
app.include_router(compliance_router)


@app.get("/")
def root():
    return {
        "organization": "Brendan Nicholas Holdings",
        "system": "LexGuard Sovereign Compliance Agent",
        "status": "Operational",
        "air_gapped": True,
        "docs_url": "/docs"
    }


@app.get("/health")
def health_check():
    kb = get_knowledge_base()
    return {
        "status": "healthy",
        "faiss_clauses_indexed": kb.index.ntotal,
        "ollama_host": os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
        "model": os.getenv("OLLAMA_MODEL", "gemma:2b")
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
