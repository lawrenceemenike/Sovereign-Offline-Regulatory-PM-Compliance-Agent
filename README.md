# LexGuard: Sovereign Offline Regulatory & PM Compliance Agent
### Brendan Nicholas Holdings (BNH) — Office of Institutional Governance & Compliance

LexGuard is an institutional, air-gapped regulatory compliance and project management audit agent built to enforce statutory compliance across the five operational pillars of **Brendan Nicholas Holdings (BNH)**:
1. **BNH Energy & Midstream** (Petroleum Industry Act 2021, NMDPRA regulations, Gas Flare Penalties)
2. **BNH Property & Real Estate Holdings** (Land Use Act 1978, Governor's Consent, EIA Act Cap E12)
3. **BNH GovTech & Sovereign Cloud** (Nigeria Data Protection Act 2023, NDPR, NITDA Sovereign Cloud Policy)
4. **BNH Agribusiness & Food Security** (National Agricultural Seeds Act, Fertilizer Quality Control Act, NAFDAC)
5. **BNH Capital & Infrastructure Projects** (COREN Certification, Urban & Regional Planning Act)

---

## 1. Sovereign Air-Gapped Architecture (Zero-Cloud Leakage)

LexGuard is engineered specifically for sensitive government-sector and high-stakes conglomerate operations where data privacy, national security, and regulatory sovereignty are paramount.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        BNH HOST ENVIRONMENT                            │
│                                                                        │
│  ┌───────────────────────┐          ┌───────────────────────────────┐  │
│  │ Next.js 14 Dashboard  │ ───────> │  FastAPI Compliance Gateway   │  │
│  │ (Executive Dark UI)   │ <─────── │  (Port 8005 / Port 8000)      │  │
│  └───────────────────────┘          └──────────────┬────────────────┘  │
│                                                    │                   │
│                               ┌────────────────────┴────────────────┐  │
│                               ▼                                     ▼  │
│                    ┌─────────────────────┐               ┌───────────┐ │
│                    │ Compliance RAG      │               │PostgreSQL/│ │
│                    │ Agent               │               │SQLite DB  │ │
│                    └──────────┬──────────┘               └───────────┘ │
│                               │                                        │
│               ┌───────────────┴───────────────┐                        │
│               ▼                               ▼                        │
│  ┌────────────────────────┐      ┌─────────────────────────┐           │
│  │ Local FAISS Index      │      │ Local Ollama Service    │           │
│  │ (Dense Embeddings 768) │      │ (gemma:2b / gemma2:2b)  │           │
│  │ Grounded Nigerian Acts │      │ http://127.0.0.1:11434  │           │
│  └────────────────────────┘      └─────────────────────────┘           │
│                                                                        │
│        [Strictly Air-Gapped: Zero External API or Cloud Egress]         │
└────────────────────────────────────────────────────────────────────────┘
```

### Sovereign Guarantees:
- **Zero Third-Party Cloud Transmission**: No data is ever transmitted to OpenAI, Anthropic, AWS Bedrock, or any foreign cloud endpoint.
- **Local In-Memory Inference**: Vector search runs locally via FAISS; LLM token generation runs locally on host hardware via Ollama (`gemma:2b` or `gemma2:2b`).
- **Grounded Statutory Citations**: Every risk flag is explicitly tied to Nigerian statutory provisions (Act name, Section number, legal excerpt, and potential liabilities).

---

## 2. Directory Structure

```
├── backend/
│   ├── agents/
│   │   └── compliance_agent.py      # Sovereign RAG Agent with legal guardrails
│   ├── database/
│   │   ├── migrations/
│   │   │   └── 001_initial_schema.sql # PostgreSQL DDL migration with JSONB & Indexes
│   │   ├── models.py                # SQLAlchemy models (MilestoneAudit, RegulatoryDoc, Pillar)
│   │   └── session.py               # Engine & session manager (Dual-mode Postgres/SQLite)
│   ├── rag/
│   │   ├── ingestion.py             # Document & PDF chunking engine
│   │   ├── knowledge_base.py        # Local FAISS vector index & local embeddings
│   │   └── seed_data.py             # Curated Nigerian statutory legal frameworks
│   ├── routers/
│   │   └── compliance.py            # FastAPI Router (/audit, /history, /matrix, /regulations)
│   ├── tests/
│   │   └── test_compliance.py       # Full automated test suite (Pytest)
│   ├── .env.example                 # Configuration template
│   ├── main.py                      # FastAPI application entrypoint
│   ├── requirements.txt             # Python backend dependencies
│   └── setup_rag.py                 # Vector database & seed initialization script
│
├── frontend/
│   ├── app/
│   │   ├── compliance/
│   │   │   ├── audit/
│   │   │   │   └── page.tsx         # View 2: Milestone Audit Studio with 1-click test scenarios
│   │   │   └── page.tsx             # View 1: Subsidiary Compliance Command Center (Risk Matrix)
│   │   ├── globals.css              # Custom styling & glassmorphic tokens
│   │   ├── layout.tsx               # Institutional header, navigation & air-gap status
│   │   └── page.tsx                 # Root redirect to /compliance
│   ├── next.config.js               # Next.js config with backend API proxy rewrites
│   ├── package.json                 # Next.js 14, Tailwind CSS, TypeScript dependencies
│   ├── postcss.config.js            # PostCSS configuration
│   ├── tailwind.config.js           # Institutional BNH slate/navy color scheme
│   └── tsconfig.json                # TypeScript compiler configuration
│
└── README.md                        # Institutional architecture & deployment manual
```

---

## 3. Quick Start & Setup

### Prerequisites
1. **Python 3.10+**: Ensure `python` or `py` is installed.
2. **Node.js 18+ & npm**: For Next.js executive dashboard.
3. **Ollama**: Installed locally with models `gemma:2b` and `nomic-embed-text`:
   ```bash
   ollama pull gemma:2b
   ollama pull nomic-embed-text
   ```

### Step 1: Initialize the Local Vector Store & Database
Run the automated setup script to index the Nigerian regulatory frameworks into the local FAISS store and create initial database tables:
```bash
# From repository root:
py backend/setup_rag.py
```
*Output confirms: `Indexed 14 regulatory clauses into local FAISS vector store. Sovereign readiness confirmed.`*

### Step 2: Start the FastAPI Backend
```bash
py -m uvicorn backend.main:app --host 127.0.0.1 --port 8005 --reload
```
Interactive OpenAPI documentation will be accessible at: `http://127.0.0.1:8005/docs`

### Step 3: Launch the Executive Dashboard
In a new terminal window:
```bash
cd frontend
npm run dev
# Or for production:
# npm run build
# npx next start -p 3005
```
Open **`http://localhost:3005/compliance`** in your browser.

---

## 4. Institutional Views

### View 1: Subsidiary Compliance Command Center (`/compliance`)
- **Executive KPIs**: Real-time Sovereign Compliance Index, active statutory violations count, pending review alerts, and vector corpus clause density.
- **Operational Risk Matrix**: Tabular telemetry across all 5 BNH operational pillars showing compliance scores, risk tier (`Critical`, `Elevated`, `Low`), audit breakdown (Violations / Reviews / Compliant), and last audit timestamp.
- **Audit Ledger Stream**: Filterable chronological feed of all past milestone audits with one-click report drawer inspection.

### View 2: Milestone Audit Studio (`/compliance/audit`)
- **PM Submission Form**: Project managers submit progress reports, sprint logs, or contractor manifests.
- **1-Click Test Scenarios**: Instant autofill buttons for realistic institutional edge cases:
  1. *GovTech*: Cloud Biometrics Migration to AWS us-east-1 (triggers NDPA Section 41-43 violation).
  2. *Energy*: Pipeline Tie-in with Unmetered Gas Flaring (triggers PIA Section 104 violation).
  3. *Property*: Swamp Clearing & Mobilization prior to Governor's Consent & EIA (triggers Land Use Act review).
  4. *Agribusiness*: Hybrid Maize & Fertilizer Shipment prior to NASC assay (triggers Seed Act review).
  5. *Infrastructure*: Highway Trenching with COREN Certification (models a fully Compliant audit).
- **Statutory Inspector**:
  - Compliance Status Badge (`Compliant`, `Review Required`, `Non-Compliant Violation`)
  - Dynamic Risk Gauge (0 - 100)
  - Itemized Regulatory Gaps & Penalties
  - Mandatory PM Remediation Steps
  - Exact Nigerian Statutory Clause Citations
  - **Copy Sovereign Audit Memo** button for board memos and project dossiers.

---

## 5. REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check verifying FAISS clause count and local Ollama model |
| `GET` | `/api/v1/compliance/matrix` | Returns live compliance metrics across all 5 BNH operational pillars |
| `POST` | `/api/v1/compliance/audit` | Submits milestone text, triggers local RAG, saves to DB, returns JSON risk assessment |
| `GET` | `/api/v1/compliance/history` | Fetches chronological audit history with optional `vertical` and `status` filters |
| `GET` | `/api/v1/compliance/regulations` | Returns indexed regulatory frameworks and clause distribution |
| `POST` | `/api/v1/compliance/ingest` | Uploads and indexes new regulatory PDFs or raw text into FAISS |

### Sample Audit Request:
```bash
curl -X POST "http://127.0.0.1:8005/api/v1/compliance/audit" \
     -H "Content-Type: application/json" \
     -d '{
       "project_name": "Citizen Biometric Central Registry",
       "subsidiary_vertical": "GovTech",
       "submitted_text": "Completed database migration of 4.2 million voter records to overseas cloud storage without local replication.",
       "subsidiary_id": "BNH-TECH-03"
     }'
```

### Sample Structured JSON Response:
```json
{
  "audit_id": 1,
  "project_name": "Citizen Biometric Central Registry",
  "subsidiary_id": "BNH-TECH-03",
  "subsidiary_vertical": "GovTech",
  "compliance_status": "Non-Compliant Violation",
  "risk_score": 92.0,
  "executive_summary": "Sovereign audit for 'Citizen Biometric Central Registry' under GovTech vertical concluded with status: Non-Compliant Violation.",
  "risk_factors": [
    "Violation of NDPA 2023 Section 41-43 and NITDA Sovereign Cloud Policy: Prohibited cross-border transfer of Level 4 citizen biometrics.",
    "Potential liability: Regulatory fine up to 2% of gross annual turnover or ₦10,000,000, plus personal criminal liability."
  ],
  "remediation_steps": [
    "Immediately halt overseas data replication pipelines and isolate outbound database egress endpoints.",
    "Re-route workload to a certified Nigerian Tier-III/Tier-IV Sovereign Cloud provider.",
    "Conduct an emergency Data Protection Impact Assessment (DPIA) and submit disclosure to the NDPC within 72 hours."
  ],
  "cited_clauses": [
    {
      "law": "Nigeria Data Protection Act (NDPA) 2023",
      "section": "NDPA 2023, Part V, Sections 41-43 (Cross-Border Data Flows)",
      "clause": "Cross-Border Transfer of Personal Data & Sovereign Data Custody",
      "relevance": "Matched based on operational vertical [GovTech] with similarity 0.70."
    }
  ],
  "created_at": "2026-09-23T20:30:00"
}
```

---

## 6. PostgreSQL Enterprise Migration

In production, point `DATABASE_URL` in `.env` to a PostgreSQL instance:
```bash
DATABASE_URL=postgresql+psycopg2://lexguard:secret@localhost:5432/lexguard_db
```
Apply the migration script:
```bash
psql -U lexguard -d lexguard_db -f backend/database/migrations/001_initial_schema.sql
```

---

## 7. Verification & Automated Testing

Run the full automated test suite verifying vector search, compliance agent evaluation, and API endpoints:
```bash
py -m pytest backend/tests -v
```

---

## 8. License & Institutional Custody
Proprietary software developed for **Brendan Nicholas Holdings (BNH)**. Strictly prohibited from distribution outside authorized sovereign infrastructure nodes.
