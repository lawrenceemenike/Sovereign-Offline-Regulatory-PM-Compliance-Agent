import os
import re
import json
import logging
from typing import Dict, Any, List, Optional
import httpx

from backend.rag.knowledge_base import get_knowledge_base

logger = logging.getLogger("lexguard.agent")
logger.setLevel(logging.INFO)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma:2b")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "10.0"))


class ComplianceAgent:
    """
    Sovereign Offline Compliance RAG Agent for Brendan Nicholas Holdings (BNH).
    Grounds milestone audit assessments in local FAISS Nigerian legal frameworks.
    """

    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        self.base_url = base_url
        self.model = model
        self.kb = get_knowledge_base()

    def evaluate_milestone(
        self,
        project_name: str,
        subsidiary_vertical: str,
        milestone_text: str,
        subsidiary_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end sovereign compliance audit:
        1. Query FAISS for localized regulatory clauses.
        2. Prompt local Ollama gemma:2b model.
        3. Parse, ground, and validate structured JSON risk output.
        """
        # Step 1: Retrieve top relevant regulatory clauses
        retrieved_clauses = self.kb.search(
            query=milestone_text,
            category=subsidiary_vertical,
            k=3
        )

        # Build context string
        context_blocks = []
        for i, c in enumerate(retrieved_clauses):
            context_blocks.append(
                f"[Regulatory Reference {i+1}]\n"
                f"Framework: {c.get('framework')}\n"
                f"Section/Citation: {c.get('citation')}\n"
                f"Statutory Provision: {c.get('content')}\n"
                f"Statutory Penalties: {c.get('penalties', 'Standard legal remedies')}\n"
            )
        regulatory_context = "\n".join(context_blocks)

        # Step 2: Construct Institutional Auditor Prompt
        prompt = self._build_prompt(
            project_name=project_name,
            subsidiary_vertical=subsidiary_vertical,
            milestone_text=milestone_text,
            regulatory_context=regulatory_context
        )

        # Step 3: Run Inference via Local Ollama
        raw_response = self._call_ollama(prompt)

        # Step 4: Parse & Ensure Grounded Schema
        structured_report = self._parse_and_validate_response(
            raw_response=raw_response,
            project_name=project_name,
            subsidiary_vertical=subsidiary_vertical,
            milestone_text=milestone_text,
            retrieved_clauses=retrieved_clauses
        )

        return structured_report

    def _build_prompt(
        self,
        project_name: str,
        subsidiary_vertical: str,
        milestone_text: str,
        regulatory_context: str
    ) -> str:
        return f"""You are the Chief Regulatory Auditor for Brendan Nicholas Holdings (BNH), conducting an institutional air-gapped compliance audit.
Analyze the following project milestone log against the retrieved statutory provisions of Nigerian law.

### PROJECT DETAILS:
- Project Name: {project_name}
- Subsidiary Vertical: {subsidiary_vertical}
- Milestone Log:
"{milestone_text}"

### STATUTORY REGULATORY CONTEXT (NIGERIAN LAW):
{regulatory_context}

### AUDIT INSTRUCTIONS:
Evaluate compliance strictly against the cited provisions.
Determine if the project violates Nigerian laws (such as NDPA cross-border data transfer, PIA gas flaring/licensing, Land Use Act Governor's consent, or NITDA cloud residency).
You MUST respond ONLY with a valid JSON object matching the exact schema below. No explanations outside the JSON.

```json
{{
  "project_name": "{project_name}",
  "subsidiary_vertical": "{subsidiary_vertical}",
  "compliance_status": "Compliant" | "Review Required" | "Non-Compliant Violation",
  "risk_score": 0-100,
  "executive_summary": "Concise executive assessment explaining compliance finding.",
  "risk_factors": [
    "Specific regulatory violation or operational risk #1",
    "Specific regulatory violation or operational risk #2"
  ],
  "remediation_steps": [
    "Actionable institutional remediation step #1",
    "Actionable institutional remediation step #2"
  ],
  "cited_clauses": [
    {{
      "law": "Exact law or act name",
      "section": "Section or regulation number",
      "clause": "Summary of statutory mandate",
      "relevance": "Why this milestone triggers this provision"
    }}
  ]
}}
```"""

    def _call_ollama(self, prompt: str) -> str:
        """Invokes local Ollama instance with snappy options and fast fallback."""
        try:
            with httpx.Client(timeout=OLLAMA_TIMEOUT) as client:
                res = client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.1,
                            "top_p": 0.9,
                            "num_predict": 256,
                            "num_ctx": 1024,
                        }
                    },
                )
                if res.status_code == 200:
                    return res.json().get("response", "")
        except Exception as e:
            logger.warning(f"Ollama call timed out or failed ({e}). Engaging deterministic compliance auditor engine.")
        return ""

    def _parse_and_validate_response(
        self,
        raw_response: str,
        project_name: str,
        subsidiary_vertical: str,
        milestone_text: str,
        retrieved_clauses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Safely extracts JSON or applies expert deterministic auditing heuristic."""
        parsed = None

        if raw_response:
            # Strip markdown code blocks
            clean = raw_response.strip()
            match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", clean, re.DOTALL)
            if match:
                clean = match.group(1)
            else:
                match_brace = re.search(r"(\{.*\})", clean, re.DOTALL)
                if match_brace:
                    clean = match_brace.group(1)

            try:
                data = json.loads(clean)
                if isinstance(data, dict) and "compliance_status" in data:
                    parsed = data
            except Exception as e:
                logger.warning(f"Failed to parse model JSON: {e}")

        # If model returned valid JSON, enhance and validate with statutory guardrails
        if parsed:
            status = parsed.get("compliance_status", "Review Required")
            risk_score = float(parsed.get("risk_score", 50.0))
            risk_factors = parsed.get("risk_factors", [])
            remediation_steps = parsed.get("remediation_steps", [])

            # Statutory Guardrail Override for blatant legal triggers
            text_lower = milestone_text.lower()
            if any(term in text_lower for term in ["unmetered gas flaring", "continuous flaring", "gas flaring pending", "flaring without permit"]):
                if status == "Compliant":
                    status = "Non-Compliant Violation"
                    risk_score = max(risk_score, 88.0)
                    risk_factors.append("Statutory Violation: Petroleum Industry Act (PIA) 2021 Section 104 strictly prohibits unmetered and unpermitted gas flaring.")
                    remediation_steps.append("Immediately cease flaring operations and install NMDPRA-certified fiscal gas meters.")

            if any(term in text_lower for term in ["biometric", "voter records", "citizen identity"]) and any(term in text_lower for term in ["aws", "azure", "us-east", "offshore", "overseas"]):
                if status == "Compliant":
                    status = "Non-Compliant Violation"
                    risk_score = max(risk_score, 92.0)
                    risk_factors.append("Statutory Violation: NDPA 2023 Section 41-43 and NITDA Cloud Policy prohibit offshore transmission of sovereign citizen biometrics.")
                    remediation_steps.append("Halt replication to foreign cloud regions and repatriate data to in-country Tier-III sovereign data centers.")

            if any(term in text_lower for term in ["mobilised on site", "groundbreaking", "clearing"]) and not any(term in text_lower for term in ["eia approved", "governor's consent", "c of o granted"]):
                if status == "Compliant":
                    status = "Review Required"
                    risk_score = max(risk_score, 65.0)
                    risk_factors.append("Compliance Gap: Land Use Act & EIA Act require validated Governor's Consent and FMEnv EIA certification prior to ground mobilization.")
                    remediation_steps.append("Verify Governor's consent perfection and obtain formal Ministry of Environment EIA certificate.")

            if status not in ["Compliant", "Review Required", "Non-Compliant Violation"]:
                status = "Review Required"

            risk_score = max(0.0, min(100.0, risk_score))

            cited = parsed.get("cited_clauses", [])
            if not cited and retrieved_clauses:
                for c in retrieved_clauses:
                    cited.append({
                        "law": c.get("framework", "Nigerian Regulatory Act"),
                        "section": c.get("citation", "Statutory Provision"),
                        "clause": c.get("title", "Compliance Clause"),
                        "relevance": f"Grounding match based on semantic proximity score ({c.get('similarity_score', 0):.2f})."
                    })

            return {
                "project_name": project_name,
                "subsidiary_vertical": subsidiary_vertical,
                "compliance_status": status,
                "risk_score": risk_score,
                "executive_summary": parsed.get("executive_summary", "Regulatory audit completed under BNH sovereign framework."),
                "risk_factors": risk_factors or ["Procedural verification recommended."],
                "remediation_steps": remediation_steps or ["Consult BNH Chief Legal Counsel."],
                "cited_clauses": cited
            }

        # Deterministic Expert Fallback Engine
        return self._rule_based_audit(project_name, subsidiary_vertical, milestone_text, retrieved_clauses)

    def _rule_based_audit(
        self,
        project_name: str,
        subsidiary_vertical: str,
        milestone_text: str,
        retrieved_clauses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """High-precision legal rules for standard sovereign operational milestones."""
        text_lower = milestone_text.lower()
        vertical = subsidiary_vertical.lower()

        risk_factors = []
        remediation_steps = []
        status = "Compliant"
        risk_score = 15.0

        # Check GovTech triggers
        if "govtech" in vertical or "tech" in vertical:
            if any(w in text_lower for w in ["aws", "azure", "us-east", "frankfurt", "overseas", "foreign cloud", "ireland", "offshore"]):
                if any(w in text_lower for w in ["biometric", "citizen", "identity", "nin", "voter", "passport", "tax"]):
                    status = "Non-Compliant Violation"
                    risk_score = 94.0
                    risk_factors.append(
                        "Violation of NDPA 2023 Section 41-43 and NITDA Sovereign Cloud Policy: Prohibited cross-border transfer of Level 4 citizen biometrics."
                    )
                    risk_factors.append(
                        "Potential liability: Regulatory fine up to 2% of gross annual turnover or ₦10,000,000, plus personal criminal liability."
                    )
                    remediation_steps.append(
                        "Immediately halt overseas data replication pipelines and isolate outbound database egress endpoints."
                    )
                    remediation_steps.append(
                        "Re-route workload to a certified Nigerian Tier-III/Tier-IV Sovereign Cloud provider (e.g., Galaxy Backbone, MainOne, Rack Centre)."
                    )
                    remediation_steps.append(
                        "Conduct an emergency Data Protection Impact Assessment (DPIA) and submit disclosure to the NDPC within 72 hours."
                    )

        # Check Energy triggers
        if "energy" in vertical:
            if any(w in text_lower for w in ["flare", "flaring", "venting", "interconnect", "pipeline"]) and not any(w in text_lower for w in ["permit", "license", "nmdpra approved"]):
                status = "Non-Compliant Violation" if "flare" in text_lower else "Review Required"
                risk_score = 88.0 if status == "Non-Compliant Violation" else 62.0
                risk_factors.append(
                    "Petroleum Industry Act 2021 Section 104-107: Flaring or constructing midstream infrastructure without NMDPRA authorization."
                )
                remediation_steps.append(
                    "File for formal NMDPRA Facility Construction & Interconnect Permit prior to physical hot-tapping."
                )
                remediation_steps.append(
                    "Submit verified Flare Gas Elimination & Fiscal Metering Plan to the Commission."
                )

        # Check Property triggers
        if "property" in vertical or "real estate" in vertical:
            if any(w in text_lower for w in ["mobiliz", "groundbreak", "clearing", "construction"]) and not any(w in text_lower for w in ["governor's consent", "eia permit", "c of o"]):
                status = "Non-Compliant Violation" if "eia" not in text_lower else "Review Required"
                risk_score = 82.0
                risk_factors.append(
                    "Land Use Act 1978 & EIA Act Cap E12: Commercial mobilization without validated Governor's Consent and FMEnv Category 1 EIA Clearance."
                )
                remediation_steps.append(
                    "Issue immediate stop-work order to civil engineering contractors pending Ministry of Environment EIA certificate."
                )
                remediation_steps.append(
                    "Complete statutory Governor's Consent perfection at State Lands Registry."
                )

        # Check Agribusiness triggers
        if "agri" in vertical:
            if any(w in text_lower for w in ["seed", "fertilizer", "import", "chemical"]) and not any(w in text_lower for w in ["nasc", "certified", "phytosanitary"]):
                status = "Review Required"
                risk_score = 68.0
                risk_factors.append(
                    "National Agricultural Seeds Act & Fertilizer Quality Control Act: Distribution of uncertified genetic material or unregistered blending stocks."
                )
                remediation_steps.append(
                    "Obtain National Agricultural Seeds Council (NASC) batch assay certification."
                )
                remediation_steps.append(
                    "Submit seed stock for NAQS phytosanitary quarantine clearance at port of entry."
                )

        # If no issues found, remain compliant
        if not risk_factors:
            status = "Compliant"
            risk_score = 12.0
            risk_factors.append("Milestone appears aligned with basic statutory operating boundaries.")
            remediation_steps.append("Maintain routine internal compliance logging and audit trails.")

        cited = []
        for c in retrieved_clauses:
            cited.append({
                "law": c.get("framework", "Nigerian Statutory Law"),
                "section": c.get("citation", "Statutory Provision"),
                "clause": c.get("title", "Regulatory Clause"),
                "relevance": f"Matched based on operational vertical [{subsidiary_vertical}] with similarity {c.get('similarity_score', 0):.2f}."
            })

        return {
            "project_name": project_name,
            "subsidiary_vertical": subsidiary_vertical,
            "compliance_status": status,
            "risk_score": risk_score,
            "executive_summary": (
                f"Sovereign audit for '{project_name}' under {subsidiary_vertical} vertical concluded with status: {status}. "
                f"Evaluation detected {len(risk_factors)} primary risk factors requiring institutional oversight."
            ),
            "risk_factors": risk_factors,
            "remediation_steps": remediation_steps,
            "cited_clauses": cited
        }


# Singleton agent instance
compliance_agent_instance = ComplianceAgent()


def get_compliance_agent() -> ComplianceAgent:
    return compliance_agent_instance
