"""
Nigerian Institutional Regulatory Knowledge Base Seed Data
Curated for Brendan Nicholas Holdings (BNH) Sovereign Compliance Agent.
"""

from typing import List, Dict, Any

SEED_REGULATIONS: List[Dict[str, Any]] = [
    # -------------------------------------------------------------
    # 1. NIGERIA DATA PROTECTION ACT (NDPA) 2023 & NDPR (GovTech & Enterprise)
    # -------------------------------------------------------------
    {
        "framework": "Nigeria Data Protection Act (NDPA) 2023",
        "category": "GovTech",
        "section": "Part V, Section 41-43",
        "title": "Cross-Border Transfer of Personal Data & Sovereign Data Custody",
        "content": (
            "Cross-Border Transfer of Personal Data: A data controller or processor shall not transfer "
            "personal data from the Federal Republic of Nigeria to another country unless: (a) the recipient "
            "country ensures an adequate level of protection as approved by the Nigeria Data Protection "
            "Commission (NDPC); (b) binding corporate rules or standard contractual clauses approved by the "
            "NDPC are executed; or (c) explicit, documented consent is obtained from the data subject with "
            "adequate risk disclosure. Public sector records, sovereign citizen biometrics, and critical "
            "national infrastructure data are prohibited from offshore transmission without an express waiver "
            "from the National Security Adviser and the Commission."
        ),
        "citation": "NDPA 2023, Part V, Sections 41-43 (Cross-Border Data Flows)",
        "penalties": "Up to 2% of annual gross revenue or ₦10,000,000 (whichever is greater), plus personal liability for Directors."
    },
    {
        "framework": "Nigeria Data Protection Act (NDPA) 2023",
        "category": "GovTech",
        "section": "Part IV, Section 40",
        "title": "Data Protection Impact Assessment (DPIA) & High-Risk Processing",
        "content": (
            "Data Protection Impact Assessment: Where the processing of personal data may result in high "
            "risk to the rights and freedoms of data subjects by virtue of its nature, scope, context, "
            "or use of novel technologies (including biometrics, AI profiling, or surveillance telemetry), "
            "the data controller shall carry out a comprehensive Data Protection Impact Assessment (DPIA) "
            "prior to project launch or deployment. The completed DPIA must be submitted to the NDPC for "
            "formal sign-off before production data ingestion commences."
        ),
        "citation": "NDPA 2023, Part IV, Section 40 (DPIA Mandate)",
        "penalties": "Administrative fines, operational cease-and-desist orders, and suspension of digital processing licenses."
    },
    {
        "framework": "Nigeria Data Protection Regulation (NDPR) & NDPA 2023",
        "category": "GovTech",
        "section": "Section 40(2) & Regulation 2.10",
        "title": "72-Hour Security Incident & Data Breach Notification",
        "content": (
            "Breach Notification Protocols: In the event of a security breach compromising confidentiality, "
            "integrity, or availability of personal data, the data controller or processor must inform "
            "the Commission (NDPC) within 72 hours of becoming aware of the breach. If the breach exposes "
            "high-risk data, affected data subjects must be notified without undue delay with clear "
            "mitigation advisories. Failure to report within the 72-hour statutory window constitutes a "
            "separate statutory violation."
        ),
        "citation": "NDPA 2023, Section 40(2) & NDPR Reg. 2.10 (72-Hour Incident Window)",
        "penalties": "Statutory fine and mandatory public disclosure sanction."
    },

    # -------------------------------------------------------------
    # 2. PETROLEUM INDUSTRY ACT (PIA) 2021 & NMDPRA (Energy & Midstream)
    # -------------------------------------------------------------
    {
        "framework": "Petroleum Industry Act (PIA) 2021",
        "category": "Energy",
        "section": "Part IV, Section 125 & Section 174",
        "title": "Midstream Gas Infrastructure Licensure & Network Code",
        "content": (
            "Licensing of Midstream Operations: No entity shall construct, place in service, expand, or "
            "operate any midstream petroleum pipeline, processing plant, bulk gas distribution facility, "
            "or compression station without an operating license granted by the Nigerian Midstream and "
            "Downstream Petroleum Regulatory Authority (NMDPRA). Open-access network code rules mandate "
            "non-discriminatory tariff structures and strict adherence to technical and safety standards "
            "approved by the Authority."
        ),
        "citation": "Petroleum Industry Act 2021, Sections 125 & 174 (NMDPRA Licensure)",
        "penalties": "Shutdown of facilities, forfeiture of assets, and criminal sanctions under Section 297."
    },
    {
        "framework": "Petroleum Industry Act (PIA) 2021 & Flare Regulations",
        "category": "Energy",
        "section": "Section 104-107",
        "title": "Prohibition of Natural Gas Flaring & Flare Elimination Plans",
        "content": (
            "Gas Flaring Prohibition: A licensee or lessee who produces natural gas shall not flare or vent "
            "natural gas except in emergencies or under an explicit permit granted by the Commission (NUPRC) "
            "or Authority (NMDPRA). Operators must install continuous fiscal metering at all flare points "
            "and submit an annual Flare Gas Elimination Plan. Unmetered or unpermitted flaring incurs "
            "punitive daily penalties of $2.00 per 1,000 SCF flared and may void operating permits."
        ),
        "citation": "PIA 2021, Sections 104-107 (Flare Elimination & Fiscal Metering)",
        "penalties": "Fines of $2.00/1,000 SCF plus liability for environmental remediation costs."
    },
    {
        "framework": "Petroleum Industry Act (PIA) 2021",
        "category": "Energy",
        "section": "Section 108 & 110",
        "title": "Domestic Crude Oil and Gas Supply Obligation (DCSO)",
        "content": (
            "Domestic Supply Mandate: Licensees and operators are legally bound to fulfill their assigned "
            "Domestic Gas Supply Obligation (DGSO) and Domestic Crude Supply Obligation before any volume "
            "may be allocated to export markets. All off-take agreements, interconnections, and pipeline "
            "deliveries must be cleared through the NMDPRA Domestic Gas Clearinghouse to safeguard national "
            "energy security."
        ),
        "citation": "PIA 2021, Sections 108 & 110 (Domestic Supply Quotas)",
        "penalties": "Curtailment of export quotas and civil fines equivalent to unsatisfied domestic volume value."
    },

    # -------------------------------------------------------------
    # 3. LAND USE ACT 1978 & EIA ACT (Property & Infrastructure)
    # -------------------------------------------------------------
    {
        "framework": "Land Use Act 1978 (Cap L5 LFN 2004)",
        "category": "Property",
        "section": "Sections 21 & 22",
        "title": "Mandatory Governor's Consent for Alienation and Transfer of Land",
        "content": (
            "Governor's Consent on Real Property: It shall not be lawful for any holder of a statutory "
            "Right of Occupancy or Certificate of Occupancy (C of O) granted by the Governor to alienate "
            "his right of occupancy or any part thereof by assignment, mortgage, transfer of possession, "
            "sublease or otherwise howsoever without the consent of the Governor first had and obtained. "
            "Any transaction executed without requisite consent is null, void, and unenforceable under Section 26."
        ),
        "citation": "Land Use Act 1978, Sections 21, 22, and 26 (Governor's Consent Mandate)",
        "penalties": "Transaction deemed void ab initio; forfeiture of proprietary claim."
    },
    {
        "framework": "Environmental Impact Assessment (EIA) Act 1992 (Cap E12)",
        "category": "Property",
        "section": "Sections 2, 4, and 13",
        "title": "Mandatory Category 1 EIA Certification Prior to Groundbreaking",
        "content": (
            "Environmental Impact Assessment: Prior to undertaking any public or private development "
            "classified under Mandatory Study Activities (including commercial complexes exceeding 5 hectares, "
            "industrial parks, port facilities, or major highway corridors), the project proponent must "
            "submit an Environmental Impact Statement and obtain an Environmental Impact Assessment (EIA) "
            "Final Approval Certificate from the Federal Ministry of Environment. Ground-breaking or "
            "contractor mobilization without an EIA permit is strictly prohibited."
        ),
        "citation": "EIA Act Cap E12 LFN 2004, Sections 2 & 13 (Mandatory Study Clearance)",
        "penalties": "Immediate site sealing by NESREA/FMEnv, demolition orders, and corporate fines."
    },
    {
        "framework": "Nigerian Urban and Regional Planning Act (Cap N138)",
        "category": "Infrastructure",
        "section": "Sections 27-32",
        "title": "Development Permit, Structural Integrity & Right-of-Way Clearances",
        "content": (
            "Development Permits and Setbacks: No building or engineering works shall be commenced without "
            "obtaining an approved Development Permit from the relevant State Urban Planning and Development "
            "Authority. Designs must include certified structural engineering calculations signed by a COREN-"
            "registered engineer, compliant setback distances from high-tension power corridors, waterways, "
            "and federal trunk roads."
        ),
        "citation": "Urban & Regional Planning Act, Sections 27-32 (COREN Certification & Setbacks)",
        "penalties": "Stop-work notices, contravention notices, and state-mandated demolition."
    },

    # -------------------------------------------------------------
    # 4. NITDA GOVTECH & SOVEREIGN CLOUD POLICY (GovTech & Cloud)
    # -------------------------------------------------------------
    {
        "framework": "NITDA Act 2007 & Nigeria Cloud Computing Policy (NCCP)",
        "category": "GovTech",
        "section": "Guidelines on Sovereign Data Residency, Sections 5 & 8",
        "title": "Sovereign Cloud Data Residency & Public Records Classification",
        "content": (
            "Government Data Residency: All Ministries, Departments, Agencies (MDAs), and contractors "
            "operating on public-sector assignments handling Level 3 (Confidential) and Level 4 (Top Secret/ "
            "Sovereign) data—including citizen biometrics, Treasury Single Account (TSA) telemetry, and "
            "e-governance identity vaults—shall host such data in Tier-III or Tier-IV data center facilities "
            "physically located within the sovereign territory of Nigeria. Cloud architectures relying on "
            "unauthorized international edge points violate National IT Guidelines."
        ),
        "citation": "NITDA Nigeria Cloud Computing Policy (NCCP), Sections 5 & 8 (Data Sovereignty)",
        "penalties": "Revocation of NITDA IT Clearance, blacklisting from Federal procurement, and legal prosecution."
    },
    {
        "framework": "NITDA IT Project Clearance Regulations 2018",
        "category": "GovTech",
        "section": "Regulatory Framework for Federal Public Sector IT Projects",
        "title": "Mandatory Pre-Procurement IT Clearance & Interoperability Standards",
        "content": (
            "NITDA IT Project Clearance: All IT and digital infrastructure initiatives undertaken for public "
            "institutions or funded with public allocations must receive formal IT Clearance from the National "
            "Information Technology Development Agency (NITDA) before budget disbursement and hardware/software "
            "procurement. The system must verify interoperability with the Nigeria e-Government Interoperability "
            "Framework (NeGIF) and Nigeria Government Enterprise Architecture (NGEA)."
        ),
        "citation": "NITDA Regulatory Notice No. NITDA/HQ/REG/01/2018 (Mandatory IT Clearance)",
        "penalties": "Freeze on budgetary disbursements by Office of the Accountant-General of the Federation."
    },

    # -------------------------------------------------------------
    # 5. AGRIBUSINESS & FOOD SECURITY STANDARDS (Agribusiness)
    # -------------------------------------------------------------
    {
        "framework": "National Agricultural Seeds Act (Cap N5 LFN 2004)",
        "category": "Agribusiness",
        "section": "Sections 14-18",
        "title": "NASC Quality Control, Seed Certification & Quarantine Verification",
        "content": (
            "Seed Quality and Certification: No person or corporate body shall produce, condition, pack, "
            "or market any agricultural seed for commercial distribution unless certified by the National "
            "Agricultural Seeds Council (NASC). Imported seed stocks must accompany a Phytosanitary Certificate "
            "issued by the Nigeria Agricultural Quarantine Service (NAQS) confirming freedom from genetically "
            "engineered contaminants and prohibited noxious weed vectors."
        ),
        "citation": "National Agricultural Seeds Act Cap N5, Sections 14-18 (NASC Certification)",
        "penalties": "Confiscation and destruction of seed consignments; criminal fines under Section 21."
    },
    {
        "framework": "Fertilizer Quality Control Act 2019",
        "category": "Agribusiness",
        "section": "Sections 3-7",
        "title": "Fertilizer Blending Facility Registration & Heavy Metal Limits",
        "content": (
            "Fertilizer Quality Assurance: Every commercial fertilizer manufacturer, blender, or importer "
            "must obtain a Certificate of Registration from the Federal Ministry of Agriculture and Food "
            "Security. Formulations must undergo laboratory assay for NPK nutrient balance, and moisture "
            "content must remain below 1.5%. Heavy metal contamination thresholds (Cadmium, Lead, Arsenic) "
            "must not exceed standard permissible parts per million (ppm)."
        ),
        "citation": "Fertilizer Quality Control Act 2019, Sections 3-7 (Blending Standards)",
        "penalties": "Revocation of blending license, impoundment of stock, and heavy administrative fines."
    },
    {
        "framework": "NAFDAC Act (Cap N1 LFN 2004) & Cold-Chain Regulations",
        "category": "Agribusiness",
        "section": "Good Distribution Practice (GDP) Guidelines 2021",
        "title": "Cold-Chain Integrity & Biological Input Transit Standards",
        "content": (
            "Cold-Chain and Perishable Bio-Inputs: Perishable agricultural inputs, veterinary vaccines, "
            "and microbial fertilizers must maintain documented uninterrupted cold-chain telemetry "
            "(2°C to 8°C) from point of port disembarkation to last-mile warehousing. Temperature breach logs "
            "exceeding 2 hours require immediate batch quarantine and independent re-testing prior to farmgate release."
        ),
        "citation": "NAFDAC GDP Guidelines 2021, Schedule 3 (Cold Chain Transit)",
        "penalties": "Immediate revocation of release permit and product condemnation."
    }
]
