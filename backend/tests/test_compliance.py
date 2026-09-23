import os
import sys
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.main import app
from backend.database.session import init_db, SessionLocal
from backend.database.models import MilestoneAudit, SubsidiaryPillar
from backend.rag.knowledge_base import get_knowledge_base
from backend.agents.compliance_agent import get_compliance_agent
from backend.rag.seed_data import SEED_REGULATIONS


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    init_db()
    kb = get_knowledge_base()
    if kb.index.ntotal == 0:
        kb.add_chunks(SEED_REGULATIONS)


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["faiss_clauses_indexed"] > 0


def test_vector_similarity_search():
    kb = get_knowledge_base()
    results = kb.search("biometric citizen sovereign cloud offshore", category="GovTech", k=2)
    assert len(results) > 0
    top = results[0]
    assert "NDPA" in top["framework"] or "NITDA" in top["framework"] or "Data" in top["title"]
    assert top["similarity_score"] > 0


def test_compliance_matrix(client):
    response = client.get("/api/v1/compliance/matrix")
    assert response.status_code == 200
    data = response.json()
    assert "pillars" in data
    assert len(data["pillars"]) >= 5
    assert data["indexed_clauses"] > 0
    assert 0 <= data["overall_compliance_index"] <= 100


def test_audit_endpoint_govtech_violation(client):
    payload = {
        "project_name": "Citizen Biometric Central Registry",
        "subsidiary_vertical": "GovTech",
        "submitted_text": "Completed database export and migrated 5 million biometric voter records to AWS us-east-1 offshore bucket without local replication.",
        "subsidiary_id": "BNH-TECH-03"
    }
    response = client.post("/api/v1/compliance/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["project_name"] == payload["project_name"]
    assert data["subsidiary_vertical"] == "GovTech"
    assert data["compliance_status"] in ["Review Required", "Non-Compliant Violation"]
    assert data["risk_score"] > 40.0
    assert len(data["risk_factors"]) > 0
    assert len(data["remediation_steps"]) > 0
    assert len(data["cited_clauses"]) > 0


def test_audit_endpoint_energy(client):
    payload = {
        "project_name": "Bonny Island Gas Terminal Interconnect",
        "subsidiary_vertical": "Energy",
        "submitted_text": "Contractor completed pipeline welding and commenced continuous unmetered gas flaring pending authority inspection.",
        "subsidiary_id": "BNH-ENG-01"
    }
    response = client.post("/api/v1/compliance/audit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["compliance_status"] in ["Review Required", "Non-Compliant Violation"]
    assert any("flare" in rf.lower() or "pia" in rf.lower() or "regulatory" in rf.lower() for rf in data["risk_factors"])


def test_audit_history(client):
    response = client.get("/api/v1/compliance/history")
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    assert len(history) >= 2


def test_regulations_endpoint(client):
    response = client.get("/api/v1/compliance/regulations")
    assert response.status_code == 200
    data = response.json()
    assert "frameworks" in data
    assert len(data["frameworks"]) > 0
