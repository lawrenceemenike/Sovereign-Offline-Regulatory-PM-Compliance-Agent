import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Enum, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ComplianceStatus(str, enum.Enum):
    COMPLIANT = "Compliant"
    REVIEW_REQUIRED = "Review Required"
    NON_COMPLIANT_VIOLATION = "Non-Compliant Violation"


class SubsidiaryVertical(str, enum.Enum):
    ENERGY = "Energy"
    PROPERTY = "Property"
    GOVTECH = "GovTech"
    AGRIBUSINESS = "Agribusiness"
    INFRASTRUCTURE = "Infrastructure"


class MilestoneAudit(Base):
    __tablename__ = "milestone_audits"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subsidiary_id = Column(String(64), index=True, nullable=False)
    subsidiary_vertical = Column(String(64), index=True, nullable=False)
    project_name = Column(String(255), index=True, nullable=False)
    submitted_text = Column(Text, nullable=False)
    risk_score = Column(Float, nullable=False, default=0.0)
    compliance_status = Column(Enum(ComplianceStatus), nullable=False, default=ComplianceStatus.REVIEW_REQUIRED)
    raw_ai_response = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class RegulatoryDoc(Base):
    __tablename__ = "regulatory_docs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False, index=True)
    chunk_count = Column(Integer, default=0, nullable=False)
    source_filename = Column(String(255), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SubsidiaryPillar(Base):
    __tablename__ = "subsidiary_pillars"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    vertical = Column(String(64), nullable=False)
    head_of_compliance = Column(String(255), nullable=False)
    operational_jurisdiction = Column(String(255), default="Federal Republic of Nigeria")
    current_risk_rating = Column(String(32), default="Low")
    last_audit_date = Column(DateTime, nullable=True)
