'use client';

import React, { useState } from 'react';
import Link from 'next/link';

interface CitedClause {
  law: string;
  section: string;
  clause: string;
  relevance: string;
}

interface AuditResponse {
  audit_id: number;
  project_name: string;
  subsidiary_id: string;
  subsidiary_vertical: string;
  compliance_status: string;
  risk_score: number;
  executive_summary: string;
  risk_factors: string[];
  remediation_steps: string[];
  cited_clauses: CitedClause[];
  created_at: string;
}

const PRESET_SCENARIOS = [
  {
    title: 'GovTech: Cloud Biometrics Migration',
    vertical: 'GovTech',
    project: 'National Digital Identity Gateway (NDIG)',
    subId: 'BNH-TECH-03',
    text: 'Completed Sprint 12 migration of 5.8 million citizen biometric profiles (facial vectors and fingerprint templates) to an AWS us-east-1 S3 bucket with multi-region replication for international latency optimization.',
    badge: 'GovTech Breach',
  },
  {
    title: 'Energy: Gas Interconnect & Flaring',
    vertical: 'Energy',
    project: 'Niger Delta Gas Pipeline Spur Interconnect',
    subId: 'BNH-ENG-01',
    text: 'Completed pipeline tie-in at Okpai junction. Commenced continuous unmetered natural gas flaring during hot-commissioning while awaiting NMDPRA meter inspection schedule next month.',
    badge: 'PIA Violation',
  },
  {
    title: 'Property: Lekki Commercial Mobilization',
    vertical: 'Property',
    project: 'Lekki Coastal Logistics Hub Phase 2',
    subId: 'BNH-PROP-02',
    text: 'Contractor mobilized 14 heavy excavators on site and completed 12 hectares of swamp clearing and sand-filling. Awaiting formal Governor\'s Consent endorsement and Federal Ministry of Environment EIA certificate next quarter.',
    badge: 'Land Use Act',
  },
  {
    title: 'Agribusiness: Seed & Fertilizer Distribution',
    vertical: 'Agribusiness',
    project: 'Savannah Hybrid Maize Outgrower Initiative',
    subId: 'BNH-AGRI-04',
    text: 'Dispatched 450 metric tons of imported hybrid maize seeds and custom NPK blend to regional distribution hubs. Awaiting final NASC germination assay report and NAQS quarantine certificate.',
    badge: 'Agri Standards',
  },
  {
    title: 'Infrastructure: High-Tension Fiber Corridor',
    vertical: 'Infrastructure',
    project: 'Western Regional Fiber Optic Ring',
    subId: 'BNH-CAP-05',
    text: 'Finalized trenching along Federal Trunk A road with COREN certified civil engineering plans and approved Ministry of Works Right-of-Way permits in place.',
    badge: 'Compliant Model',
  },
];

export default function MilestoneAuditStudio() {
  const [projectName, setProjectName] = useState('');
  const [vertical, setVertical] = useState('GovTech');
  const [subsidiaryId, setSubsidiaryId] = useState('BNH-TECH-03');
  const [milestoneText, setMilestoneText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AuditResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [copiedMemo, setCopiedMemo] = useState(false);

  const applyScenario = (sc: typeof PRESET_SCENARIOS[0]) => {
    setProjectName(sc.project);
    setVertical(sc.vertical);
    setSubsidiaryId(sc.subId);
    setMilestoneText(sc.text);
    setResult(null);
    setError(null);
  };

  const handleRunAudit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!projectName.trim() || !milestoneText.trim()) {
      setError('Please provide both Project Name and Milestone Text.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch('/api/v1/compliance/audit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_name: projectName,
          subsidiary_vertical: vertical,
          submitted_text: milestoneText,
          subsidiary_id: subsidiaryId,
        }),
      });

      if (!res.ok) {
        throw new Error(`Audit request failed with status: ${res.status}`);
      }

      const data: AuditResponse = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Failed to complete sovereign compliance audit.');
    } finally {
      setLoading(false);
    }
  };

  const copyComplianceMemo = () => {
    if (!result) return;
    const memo = `===============================================================
BRENDAN NICHOLAS HOLDINGS • OFFICE OF CHIEF COMPLIANCE
SOVEREIGN REGULATORY AUDIT MEMORANDUM [STRICTLY CONFIDENTIAL]
===============================================================
AUDIT ID: BNH-SEC-${result.audit_id}
TIMESTAMP: ${new Date(result.created_at).toUTCString()}
PROJECT: ${result.project_name}
SUBSIDIARY: ${result.subsidiary_id} (${result.subsidiary_vertical})
STATUS: ${result.compliance_status.toUpperCase()}
RISK SCORE: ${result.risk_score} / 100

EXECUTIVE SUMMARY:
${result.executive_summary}

SUBMITTED MILESTONE LOG:
"${milestoneText}"

IDENTIFIED REGULATORY RISK FACTORS:
${result.risk_factors.map((rf, i) => `${i + 1}. ${rf}`).join('\n')}

MANDATORY REMEDIATION STEPS:
${result.remediation_steps.map((step, i) => `${i + 1}. ${step}`).join('\n')}

STATUTORY CITATIONS:
${result.cited_clauses.map((c) => `- ${c.law} (${c.section}): ${c.clause}`).join('\n')}
===============================================================`;

    navigator.clipboard.writeText(memo);
    setCopiedMemo(true);
    setTimeout(() => setCopiedMemo(false), 2500);
  };

  return (
    <div className="space-y-8">
      {/* Studio Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <div className="flex items-center space-x-3 mb-1">
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">
              Milestone Regulatory Audit Studio
            </h1>
            <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-blue-50 border border-blue-200 text-blue-700 font-semibold">
              Offline RAG Engine
            </span>
          </div>
          <p className="text-sm text-slate-500">
            Submit milestone updates, sprint logs, or procurement records for immediate air-gapped evaluation against Nigerian regulatory instruments.
          </p>
        </div>

        <Link
          href="/compliance"
          className="self-start md:self-auto px-3.5 py-2 rounded-lg text-xs font-semibold text-slate-700 bg-white border border-slate-300 hover:bg-slate-50 shadow-sm transition"
        >
          ← Return to Command Center
        </Link>
      </div>

      {/* Preset Institutional Scenario Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-600">
            Test Scenarios (1-Click Autofill)
          </span>
          <span className="text-[11px] text-slate-500 font-mono">Select a scenario to simulate subsidiary updates</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5">
          {PRESET_SCENARIOS.map((sc, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => applyScenario(sc)}
              className="text-left p-2.5 rounded-lg bg-slate-50 border border-slate-200 hover:border-blue-500 hover:bg-blue-50/40 transition group"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-[10px] font-mono text-slate-500 font-bold">{sc.subId}</span>
                <span className="text-[9px] px-1.5 py-0.5 rounded bg-white border border-slate-200 text-slate-700 font-medium group-hover:text-blue-700">
                  {sc.badge}
                </span>
              </div>
              <p className="text-xs font-semibold text-slate-800 group-hover:text-blue-700 line-clamp-1">
                {sc.title}
              </p>
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Submission Studio Form */}
        <div className="lg:col-span-6 space-y-6">
          <form onSubmit={handleRunAudit} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-5">
            <h2 className="text-base font-bold text-slate-900 border-b border-slate-200 pb-3">
              Milestone Submission Form
            </h2>

            {/* Project Name */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                Project Name / Capital Initiative
              </label>
              <input
                type="text"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="e.g., Lekki Coastal Logistics Hub Phase 2"
                className="w-full px-3.5 py-2.5 rounded-lg bg-white border border-slate-300 text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600 transition"
              />
            </div>

            {/* Subsidiary Vertical & ID */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Operational Vertical
                </label>
                <select
                  value={vertical}
                  onChange={(e) => {
                    setVertical(e.target.value);
                    const mapping: Record<string, string> = {
                      GovTech: 'BNH-TECH-03',
                      Energy: 'BNH-ENG-01',
                      Property: 'BNH-PROP-02',
                      Agribusiness: 'BNH-AGRI-04',
                      Infrastructure: 'BNH-CAP-05',
                    };
                    setSubsidiaryId(mapping[e.target.value] || 'BNH-GEN-01');
                  }}
                  className="w-full px-3.5 py-2.5 rounded-lg bg-white border border-slate-300 text-slate-900 text-sm focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600 transition"
                >
                  <option value="GovTech">GovTech & Sovereign Cloud</option>
                  <option value="Energy">Energy & Midstream</option>
                  <option value="Property">Property & Real Estate</option>
                  <option value="Agribusiness">Agribusiness & Food Security</option>
                  <option value="Infrastructure">Infrastructure & Capital</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Subsidiary Entity ID
                </label>
                <input
                  type="text"
                  value={subsidiaryId}
                  onChange={(e) => setSubsidiaryId(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-lg bg-white border border-slate-300 text-slate-900 font-mono text-sm focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600 transition"
                />
              </div>
            </div>

            {/* Milestone Text Area */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="text-xs font-semibold text-slate-700">
                  Milestone Log / Sprint Progress Narrative
                </label>
                <span className="text-[11px] text-slate-400 font-mono">
                  {milestoneText.length} characters
                </span>
              </div>
              <textarea
                rows={6}
                value={milestoneText}
                onChange={(e) => setMilestoneText(e.target.value)}
                placeholder="Paste the raw milestone progress update, engineering timeline, deployment notes, or procurement records..."
                className="w-full px-3.5 py-3 rounded-lg bg-white border border-slate-300 text-slate-900 placeholder-slate-400 text-sm font-sans focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600 transition leading-relaxed resize-y"
              ></textarea>
            </div>

            {error && (
              <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-xs font-medium">
                {error}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 px-4 rounded-xl text-sm font-bold text-white shadow-md transition flex items-center justify-center space-x-2 ${
                loading
                  ? 'bg-slate-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700 border border-blue-700'
              }`}
            >
              {loading ? (
                <>
                  <span className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin"></span>
                  <span>Executing Sovereign RAG Audit via Gemma...</span>
                </>
              ) : (
                <>
                  <span>Run Institutional Compliance Audit</span>
                  <span className="text-xs font-mono opacity-80">→</span>
                </>
              )}
            </button>
          </form>

          {/* Air-Gap Guarantee Card */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-600 space-y-2">
            <div className="flex items-center space-x-2 text-slate-900 font-bold">
              <span className="text-emerald-600">🛡️</span>
              <span>Institutional Sovereign Air-Gap Guarantee</span>
            </div>
            <p className="text-[11px] leading-relaxed text-slate-500">
              In accordance with BNH National Security protocols, milestone logs are evaluated on-device without telemetry, third-party API queries, or off-premise vector synchronization. All embeddings and token generations execute locally on host loopback.
            </p>
          </div>
        </div>

        {/* Right Column: Live Audit Results Inspector */}
        <div className="lg:col-span-6 space-y-6">
          {!result && !loading && (
            <div className="bg-white p-12 rounded-2xl border border-dashed border-slate-300 text-center flex flex-col items-center justify-center min-h-[460px] shadow-sm">
              <div className="w-14 h-14 rounded-2xl bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-400 text-2xl mb-4">
                ⚖️
              </div>
              <h3 className="text-base font-bold text-slate-800 mb-1">
                Awaiting Milestone Input
              </h3>
              <p className="text-xs text-slate-500 max-w-sm leading-relaxed mb-6">
                Paste a milestone report or click one of the pre-set institutional test scenarios above to trigger instant sovereign RAG verification.
              </p>
              <div className="flex items-center space-x-4 text-[11px] text-slate-500 font-mono font-medium">
                <span>NDPA 2023</span>
                <span>•</span>
                <span>PIA 2021</span>
                <span>•</span>
                <span>Land Use Act</span>
                <span>•</span>
                <span>NITDA Policy</span>
              </div>
            </div>
          )}

          {loading && (
            <div className="bg-white p-12 rounded-2xl border border-slate-200 text-center flex flex-col items-center justify-center min-h-[460px] space-y-4 shadow-sm">
              <div className="w-12 h-12 rounded-full border-4 border-blue-200 border-t-blue-600 animate-spin"></div>
              <h3 className="text-base font-bold text-slate-900">Analyzing Milestone Regulations</h3>
              <div className="space-y-1 text-xs text-slate-500">
                <p>1. Querying FAISS index for Nigerian statutory clauses...</p>
                <p>2. Grounding provisions in sovereign jurisdiction...</p>
                <p>3. Synthesizing risk factors via local Gemma 2B model...</p>
              </div>
            </div>
          )}

          {result && (
            <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-md space-y-6 p-6">
              {/* Result Header & Score Gauge */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-mono text-slate-500 font-bold">AUDIT #{result.audit_id}</span>
                    <span className="text-xs font-mono text-slate-300">•</span>
                    <span className="text-xs font-medium text-slate-600">{result.subsidiary_vertical}</span>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 mt-0.5">{result.project_name}</h3>
                </div>

                {/* Status Badge */}
                <div className="flex items-center space-x-3">
                  {result.compliance_status === 'Compliant' && (
                    <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-300">
                      COMPLIANT
                    </span>
                  )}
                  {result.compliance_status === 'Review Required' && (
                    <span className="px-3 py-1 rounded-full text-xs font-bold bg-amber-50 text-amber-800 border border-amber-300">
                      REVIEW REQUIRED
                    </span>
                  )}
                  {result.compliance_status === 'Non-Compliant Violation' && (
                    <span className="px-3 py-1 rounded-full text-xs font-bold bg-red-50 text-red-700 border border-red-300">
                      VIOLATION FLAGGED
                    </span>
                  )}
                </div>
              </div>

              {/* Risk Score Meter */}
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                <div className="flex items-baseline justify-between mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-600">
                    Statutory Risk Metric
                  </span>
                  <span
                    className={`font-mono text-base font-bold ${
                      result.risk_score >= 70
                        ? 'text-red-600'
                        : result.risk_score >= 35
                        ? 'text-amber-600'
                        : 'text-emerald-600'
                    }`}
                  >
                    {result.risk_score.toFixed(1)} / 100
                  </span>
                </div>
                <div className="w-full bg-slate-200 h-2.5 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-700 ${
                      result.risk_score >= 70
                        ? 'bg-red-500'
                        : result.risk_score >= 35
                        ? 'bg-amber-500'
                        : 'bg-emerald-500'
                    }`}
                    style={{ width: `${Math.max(5, result.risk_score)}%` }}
                  ></div>
                </div>
              </div>

              {/* Executive Summary */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-600 mb-1.5">
                  Executive Legal Assessment
                </h4>
                <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-800 leading-relaxed font-medium">
                  {result.executive_summary}
                </div>
              </div>

              {/* Flagged Risk Factors */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-red-700 mb-2 flex items-center space-x-1.5">
                  <span>⚠️ Flagged Regulatory Gaps & Penalties</span>
                </h4>
                <div className="space-y-2">
                  {result.risk_factors.map((rf, idx) => (
                    <div
                      key={idx}
                      className="p-3 rounded-lg bg-red-50 border border-red-200 text-xs text-red-800 leading-relaxed font-medium"
                    >
                      {rf}
                    </div>
                  ))}
                </div>
              </div>

              {/* Mandatory Remediation Steps */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-700 mb-2 flex items-center space-x-1.5">
                  <span>✓ Mandatory Institutional Remediation Steps</span>
                </h4>
                <div className="space-y-2">
                  {result.remediation_steps.map((step, idx) => (
                    <div
                      key={idx}
                      className="p-3 rounded-lg bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 leading-relaxed flex items-start space-x-2 font-medium"
                    >
                      <span className="font-bold text-emerald-700 shrink-0">{idx + 1}.</span>
                      <span>{step}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Localized Clause Citations */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-blue-700 mb-2 flex items-center space-x-1.5">
                  <span>📜 Grounded Statutory Clauses (Nigerian Law)</span>
                </h4>
                <div className="space-y-2.5">
                  {result.cited_clauses.map((c, idx) => (
                    <div
                      key={idx}
                      className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-1.5"
                    >
                      <div className="flex items-center justify-between text-blue-800 font-semibold">
                        <span>{c.law}</span>
                        <span className="font-mono text-[11px] text-slate-500">{c.section}</span>
                      </div>
                      <p className="text-slate-800 leading-relaxed font-normal">{c.clause}</p>
                      <p className="text-[11px] text-slate-500 italic border-t border-slate-200 pt-1">
                        Application: {c.relevance}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Actions: Export Compliance Memo */}
              <div className="pt-2 border-t border-slate-200 flex items-center justify-between">
                <button
                  type="button"
                  onClick={copyComplianceMemo}
                  className="px-4 py-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-xs font-semibold text-slate-800 border border-slate-300 transition flex items-center space-x-2"
                >
                  <span>{copiedMemo ? '✓ Memo Copied to Clipboard!' : '📋 Copy Sovereign Audit Memo'}</span>
                </button>

                <span className="text-[10px] text-slate-500 font-mono">
                  Report verified by local Ollama engine
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
