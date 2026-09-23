import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base, SubsidiaryPillar

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lexguard.db")

# SQLite connection args for thread safety in FastAPI
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Seed 5 BNH Operational Pillars if not present
        existing = db.query(SubsidiaryPillar).first()
        if not existing:
            default_pillars = [
                SubsidiaryPillar(
                    id="BNH-ENG-01",
                    name="BNH Energy & Midstream",
                    vertical="Energy",
                    head_of_compliance="Engr. Aliyu Bello",
                    current_risk_rating="Moderate",
                ),
                SubsidiaryPillar(
                    id="BNH-PROP-02",
                    name="BNH Property & Real Estate Holdings",
                    vertical="Property",
                    head_of_compliance="Barr. Chidinma Okafor",
                    current_risk_rating="Low",
                ),
                SubsidiaryPillar(
                    id="BNH-TECH-03",
                    name="BNH GovTech & Sovereign Cloud",
                    vertical="GovTech",
                    head_of_compliance="Dr. Femi Adeleke",
                    current_risk_rating="High",
                ),
                SubsidiaryPillar(
                    id="BNH-AGRI-04",
                    name="BNH Agribusiness & Food Security",
                    vertical="Agribusiness",
                    head_of_compliance="Hajiya Zainab Usman",
                    current_risk_rating="Low",
                ),
                SubsidiaryPillar(
                    id="BNH-CAP-05",
                    name="BNH Capital & Infrastructure Projects",
                    vertical="Infrastructure",
                    head_of_compliance="Tariq Al-Mansoor",
                    current_risk_rating="Low",
                ),
            ]
            db.add_all(default_pillars)
            db.commit()
    finally:
        db.close()
