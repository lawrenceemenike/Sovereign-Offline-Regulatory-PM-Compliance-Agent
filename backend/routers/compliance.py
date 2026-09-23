from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.database.session import get_db
from backend.database.models import MilestoneAudit, RegulatoryDoc, SubsidiaryPillar, ComplianceStatus
from backend.agents.compliance_agent import get_compliance_agent
from backend.rag.knowledge_base import get_knowledge_base
from backend.rag.ingestion import ingest_pdf_bytes, ingest_raw_text

router = APIRouter(prefix="/api/v1/compliance", tags=["Compliance"])


# -----------------------------------------------------------------------------
# Request & Response Schemas
# -----------------------------------------------------------------------------

class AuditRequest(BaseModel):
    project_name: str = Field(..., json_schema_extra={"example": "Lekki Logistics Hub Expansion"})
    subsidiary_vertical: str = Field(..., json_schema_extra={"example": "Property"})
    submitted_text: str = Field(..., json_schema_extra={"example": "Completed site clearing and ground leveling. Contractor mobilised on site."})
    subsidiary_id: Optional[str] = Field(None, json_schema_extra={"example": "BNH-PROP-02"})


class CitedClause(BaseModel):
    law: str
    section: str
    clause: str
    relevance: str


class AuditReportResponse(BaseModel):
    audit_id: int
    project_name: str
    subsidiary_id: str
    subsidiary_vertical: str
    compliance_status: str
    risk_score: float
    executive_summary: str
    risk_factors: List[str]
    remediation_steps: List[str]
    cited_clauses: List[CitedClause]
    created_at: str


class AuditHistoryItem(BaseModel):
    id: int
    subsidiary_id: str
    subsidiary_vertical: str
    project_name: str
    submitted_text: str
    risk_score: float
    compliance_status: str
    raw_ai_response: Dict[str, Any]
    created_at: str


class PillarMatrixItem(BaseModel):
    id: str
    name: str
    vertical: str
    head_of_compliance: str
    current_risk_rating: str
    compliance_score: float
    total_audits: int
    violations: int
    reviews_required: int
    compliant: int
    last_audit_date: Optional[str]


class RiskMatrixResponse(BaseModel):
    pillars: List[PillarMatrixItem]
    overall_compliance_index: float
    total_audits: int
    active_violations: int
    pending_reviews: int
    indexed_clauses: int


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------

@router.post("/audit", response_model=AuditReportResponse)
def run_compliance_audit(
    payload: AuditRequest,
    db: Session = Depends(get_db)
):
    """
    Evaluates project milestone against sovereign regulatory corpus.
    Stores evaluation in database and updates subsidiary pillar risk metrics.
    """
    agent = get_compliance_agent()
    eval_result = agent.evaluate_milestone(
        project_name=payload.project_name,
        subsidiary_vertical=payload.subsidiary_vertical,
        milestone_text=payload.submitted_text,
        subsidiary_id=payload.subsidiary_id
    )

    # Resolve subsidiary ID if missing
    sub_id = payload.subsidiary_id
    if not sub_id:
        pillar = db.query(SubsidiaryPillar).filter(
            SubsidiaryPillar.vertical.ilike(f"%{payload.subsidiary_vertical}%")
        ).first()
        sub_id = pillar.id if pillar else f"BNH-{payload.subsidiary_vertical.upper()[:4]}-01"

    # Map status to Enum
    raw_status = eval_result.get("compliance_status", "Review Required")
    if raw_status == "Compliant":
        comp_status = ComplianceStatus.COMPLIANT
    elif raw_status == "Non-Compliant Violation":
        comp_status = ComplianceStatus.NON_COMPLIANT_VIOLATION
    else:
        comp_status = ComplianceStatus.REVIEW_REQUIRED

    # Persist in Database
    audit_record = MilestoneAudit(
        subsidiary_id=sub_id,
        subsidiary_vertical=payload.subsidiary_vertical,
        project_name=payload.project_name,
        submitted_text=payload.submitted_text,
        risk_score=eval_result.get("risk_score", 50.0),
        compliance_status=comp_status,
        raw_ai_response=eval_result,
        created_at=datetime.utcnow()
    )
    db.add(audit_record)

    # Update pillar rating and timestamp
    pillar = db.query(SubsidiaryPillar).filter(SubsidiaryPillar.id == sub_id).first()
    if pillar:
        pillar.last_audit_date = datetime.utcnow()
        if comp_status == ComplianceStatus.NON_COMPLIANT_VIOLATION:
            pillar.current_risk_rating = "Critical"
        elif comp_status == ComplianceStatus.REVIEW_REQUIRED:
            pillar.current_risk_rating = "Elevated"
        else:
            pillar.current_risk_rating = "Low"

    db.commit()
    db.refresh(audit_record)

    cited = [
        CitedClause(
            law=c.get("law", "Statutory Reference"),
            section=c.get("section", ""),
            clause=c.get("clause", ""),
            relevance=c.get("relevance", "")
        )
        for c in eval_result.get("cited_clauses", [])
    ]

    return AuditReportResponse(
        audit_id=audit_record.id,
        project_name=payload.project_name,
        subsidiary_id=sub_id,
        subsidiary_vertical=payload.subsidiary_vertical,
        compliance_status=raw_status,
        risk_score=eval_result.get("risk_score", 50.0),
        executive_summary=eval_result.get("executive_summary", ""),
        risk_factors=eval_result.get("risk_factors", []),
        remediation_steps=eval_result.get("remediation_steps", []),
        cited_clauses=cited,
        created_at=audit_record.created_at.isoformat()
    )


@router.get("/history", response_model=List[AuditHistoryItem])
def get_audit_history(
    vertical: Optional[str] = Query(None, description="Filter by operational vertical"),
    status: Optional[str] = Query(None, description="Filter by compliance status"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Retrieves chronological milestone audit log across all BNH operational pillars."""
    query = db.query(MilestoneAudit)
    if vertical:
        query = query.filter(MilestoneAudit.subsidiary_vertical.ilike(f"%{vertical}%"))
    if status:
        query = query.filter(MilestoneAudit.compliance_status == status)

    records = query.order_by(desc(MilestoneAudit.created_at)).limit(limit).all()

    return [
        AuditHistoryItem(
            id=r.id,
            subsidiary_id=r.subsidiary_id,
            subsidiary_vertical=r.subsidiary_vertical,
            project_name=r.project_name,
            submitted_text=r.submitted_text,
            risk_score=r.risk_score,
            compliance_status=r.compliance_status.value if hasattr(r.compliance_status, "value") else str(r.compliance_status),
            raw_ai_response=r.raw_ai_response,
            created_at=r.created_at.isoformat()
        )
        for r in records
    ]


@router.get("/matrix", response_model=RiskMatrixResponse)
def get_compliance_matrix(db: Session = Depends(get_db)):
    """Executive live risk matrix across all 5 operational pillars."""
    pillars = db.query(SubsidiaryPillar).all()
    kb = get_knowledge_base()
    all_audits = db.query(MilestoneAudit).all()

    total_audits = len(all_audits)
    total_violations = sum(1 for a in all_audits if a.compliance_status == ComplianceStatus.NON_COMPLIANT_VIOLATION)
    total_reviews = sum(1 for a in all_audits if a.compliance_status == ComplianceStatus.REVIEW_REQUIRED)

    pillar_items = []
    total_score_sum = 0.0

    for p in pillars:
        p_audits = [a for a in all_audits if a.subsidiary_id == p.id or a.subsidiary_vertical.lower() == p.vertical.lower()]
        violations = sum(1 for a in p_audits if a.compliance_status == ComplianceStatus.NON_COMPLIANT_VIOLATION)
        reviews = sum(1 for a in p_audits if a.compliance_status == ComplianceStatus.REVIEW_REQUIRED)
        compliant = sum(1 for a in p_audits if a.compliance_status == ComplianceStatus.COMPLIANT)

        # Calculate compliance score (100 - average risk)
        if p_audits:
            avg_risk = sum(a.risk_score for a in p_audits) / len(p_audits)
            comp_score = max(0.0, min(100.0, 100.0 - avg_risk))
        else:
            comp_score = 95.0

        total_score_sum += comp_score

        pillar_items.append(
            PillarMatrixItem(
                id=p.id,
                name=p.name,
                vertical=p.vertical,
                head_of_compliance=p.head_of_compliance,
                current_risk_rating=p.current_risk_rating,
                compliance_score=round(comp_score, 1),
                total_audits=len(p_audits),
                violations=violations,
                reviews_required=reviews,
                compliant=compliant,
                last_audit_date=p.last_audit_date.isoformat() if p.last_audit_date else None
            )
        )

    overall_index = round(total_score_sum / len(pillar_items), 1) if pillar_items else 95.0

    return RiskMatrixResponse(
        pillars=pillar_items,
        overall_compliance_index=overall_index,
        total_audits=total_audits,
        active_violations=total_violations,
        pending_reviews=total_reviews,
        indexed_clauses=kb.index.ntotal
    )


@router.get("/regulations")
def list_regulatory_frameworks(db: Session = Depends(get_db)):
    """Lists indexed regulatory frameworks and clause distribution."""
    kb = get_knowledge_base()
    docs = db.query(RegulatoryDoc).all()
    summary = kb.get_summary()

    return {
        "summary": summary,
        "frameworks": [
            {
                "id": d.id,
                "title": d.title,
                "category": d.category,
                "chunk_count": d.chunk_count,
                "source": d.source_filename,
                "updated_at": d.updated_at.isoformat()
            }
            for d in docs
        ]
    }


@router.post("/ingest")
async def ingest_regulatory_document(
    file: Optional[UploadFile] = File(None),
    title: str = Form(...),
    category: str = Form(...),
    raw_text: Optional[str] = Form(None)
):
    """Ingests a new regulatory document (PDF or raw text) into the FAISS store."""
    if file:
        content = await file.read()
        res = ingest_pdf_bytes(
            file_bytes=content,
            title=title,
            category=category,
            source_filename=file.filename or "uploaded.pdf"
        )
        return res
    elif raw_text:
        res = ingest_raw_text(
            content=raw_text,
            title=title,
            category=category
        )
        return res
    else:
        raise HTTPException(status_code=400, detail="Must provide either a PDF file or raw_text")
