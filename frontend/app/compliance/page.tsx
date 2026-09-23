'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

interface PillarItem {
  id: string;
  name: string;
  vertical: string;
  head_of_compliance: string;
  current_risk_rating: string;
  compliance_score: number;
  total_audits: number;
  violations: number;
  reviews_required: number;
  compliant: number;
  last_audit_date: string | null;
}

interface MatrixResponse {
  pillars: PillarItem[];
  overall_compliance_index: number;
  total_audits: number;
  active_violations: number;
  pending_reviews: number;
  indexed_clauses: number;
}

interface AuditHistoryItem {
  id: number;
  subsidiary_id: string;
  subsidiary_vertical: string;
  project_name: string;
  submitted_text: string;
  risk_score: number;
  compliance_status: string;
  raw_ai_response: {
    executive_summary?: string;
    risk_factors?: string[];
    remediation_steps?: string[];
    cited_clauses?: Array<{
      law: string;
      section: string;
      clause: string;
      relevance: string;
    }>;
  };
  created_at: string;
}

export default function ComplianceCommandCenter() {
  const [matrix, setMatrix] = useState<MatrixResponse | null>(null);
  const [history, setHistory] = useState<AuditHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [verticalFilter, setVerticalFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [selectedAudit, setSelectedAudit] = useState<AuditHistoryItem | null>(null);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [matrixRes, historyRes] = await Promise.all([
        fetch('/api/v1/compliance/matrix'),
        fetch('/api/v1/compliance/history'),
      ]);

      if (matrixRes.ok) {
        const matrixData = await matrixRes.json();
        setMatrix(matrixData);
      }

      if (historyRes.ok) {
        const historyData = await historyRes.json();
        setHistory(historyData);
      }
    } catch (err) {
      console.error('Failed to load compliance data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const filteredHistory = history.filter((item) => {
    if (verticalFilter !== 'ALL' && item.subsidiary_vertical.toUpperCase() !== verticalFilter.toUpperCase()) {
      return false;
    }
    if (statusFilter !== 'ALL' && item.compliance_status !== statusFilter) {
      return false;
    }
    return true;
  });

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'Compliant':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            Compliant
          </span>
        );
      case 'Non-Compliant Violation':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded text-[11px] font-semibold bg-red-50 text-red-700 border border-red-200">
            Violation Flagged
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded text-[11px] font-semibold bg-amber-50 text-amber-800 border border-amber-200">
            Review Required
          </span>
        );
    }
  };

  const getRiskColor = (score: number) => {
    if (score >= 70) return 'text-red-600 font-bold';
    if (score >= 35) return 'text-amber-600 font-bold';
    return 'text-emerald-600 font-bold';
  };

  return (
    <div className="space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <div className="flex items-center space-x-3 mb-1">
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">
              Subsidiary Compliance Command Center
            </h1>
            <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-100 border border-slate-200 text-slate-700 font-semibold">
              5 Pillars Monitored
            </span>
          </div>
          <p className="text-sm text-slate-500">
            Real-time regulatory compliance telemetry, statutory breach surveillance, and sovereign risk scoring across Brendan Nicholas Holdings.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={fetchDashboardData}
            className="px-3.5 py-2 rounded-lg text-xs font-semibold text-slate-700 bg-white border border-slate-300 hover:bg-slate-50 shadow-sm transition"
          >
            Refresh Telemetry
          </button>
          <Link
            href="/compliance/audit"
            className="px-4 py-2 rounded-lg text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 shadow-sm border border-blue-700 transition"
          >
            + Run Milestone Audit
          </Link>
        </div>
      </div>

      {/* Executive KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Sovereign Compliance Index</p>
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-2xl font-bold tracking-tight text-emerald-600">
              {matrix ? `${matrix.overall_compliance_index}%` : '--'}
            </span>
            <span className="text-[10px] text-emerald-700 font-mono font-medium">Target ≥ 90%</span>
          </div>
          <div className="mt-2 w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
            <div
              className="bg-emerald-500 h-full rounded-full transition-all duration-500"
              style={{ width: matrix ? `${matrix.overall_compliance_index}%` : '0%' }}
            ></div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Total Milestone Audits</p>
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-2xl font-bold tracking-tight text-slate-900">
              {matrix ? matrix.total_audits : '--'}
            </span>
            <span className="text-[10px] text-slate-500 font-mono">Logged to DB</span>
          </div>
          <p className="mt-1 text-[11px] text-slate-500">Across 5 BNH Subsidiaries</p>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Active Violations</p>
          <div className="mt-2 flex items-baseline justify-between">
            <span className={`text-2xl font-bold tracking-tight ${matrix && matrix.active_violations > 0 ? 'text-red-600' : 'text-slate-900'}`}>
              {matrix ? matrix.active_violations : '--'}
            </span>
            <span className="text-[10px] text-red-600 font-mono font-semibold">High Severity</span>
          </div>
          <p className="mt-1 text-[11px] text-slate-500">Requires Board Notification</p>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Pending Reviews</p>
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-2xl font-bold tracking-tight text-amber-600">
              {matrix ? matrix.pending_reviews : '--'}
            </span>
            <span className="text-[10px] text-amber-700 font-mono font-semibold">Legal Clearance</span>
          </div>
          <p className="mt-1 text-[11px] text-slate-500">Action items assigned to PMs</p>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Vector Corpus Clauses</p>
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-2xl font-bold tracking-tight text-blue-600">
              {matrix ? matrix.indexed_clauses : '--'}
            </span>
            <span className="text-[10px] text-blue-700 font-mono font-semibold">FAISS Store</span>
          </div>
          <p className="mt-1 text-[11px] text-slate-500">NDPA • PIA • LUA • NITDA</p>
        </div>
      </div>

      {/* View 1 Core: Live Risk Matrix across 5 Operational Pillars */}
      <div className="bg-white rounded-xl overflow-hidden border border-slate-200 shadow-sm">
        <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/50">
          <div>
            <h2 className="text-base font-bold text-slate-900">Live Risk Matrix: BNH Operational Pillars</h2>
            <p className="text-xs text-slate-500">Continuous sovereign regulatory compliance status by subsidiary</p>
          </div>
          <span className="text-xs font-mono text-slate-600 bg-white px-2.5 py-1 rounded border border-slate-200 shadow-2xs">
            Jurisdiction: Federal Republic of Nigeria
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-[11px] uppercase tracking-wider text-slate-600 border-b border-slate-200 font-semibold">
              <tr>
                <th className="px-6 py-3.5">Pillar & Identifier</th>
                <th className="px-6 py-3.5">Vertical</th>
                <th className="px-6 py-3.5">Head of Compliance</th>
                <th className="px-6 py-3.5">Compliance Score</th>
                <th className="px-6 py-3.5">Risk Rating</th>
                <th className="px-6 py-3.5">Audits (V / R / C)</th>
                <th className="px-6 py-3.5">Last Audit</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {matrix?.pillars.map((pillar) => (
                <tr key={pillar.id} className="hover:bg-slate-50/80 transition">
                  <td className="px-6 py-4">
                    <div className="font-semibold text-slate-900">{pillar.name}</div>
                    <div className="text-xs font-mono text-slate-500">{pillar.id}</div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-700 border border-slate-200">
                      {pillar.vertical}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-700 text-xs font-medium">{pillar.head_of_compliance}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2">
                      <span className="font-bold text-slate-900 text-xs">{pillar.compliance_score}%</span>
                      <div className="w-16 bg-slate-100 h-1.5 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${
                            pillar.compliance_score >= 80 ? 'bg-emerald-500' : pillar.compliance_score >= 60 ? 'bg-amber-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${pillar.compliance_score}%` }}
                        ></div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded text-[11px] font-semibold border ${
                        pillar.current_risk_rating === 'Critical'
                          ? 'bg-red-50 text-red-700 border-red-200'
                          : pillar.current_risk_rating === 'Elevated' || pillar.current_risk_rating === 'Moderate'
                          ? 'bg-amber-50 text-amber-800 border-amber-200'
                          : 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      }`}
                    >
                      {pillar.current_risk_rating}
                    </span>
                  </td>
                  <td className="px-6 py-4 font-mono text-xs">
                    <span className="text-red-600 font-bold">{pillar.violations}V</span>
                    <span className="mx-1 text-slate-400">/</span>
                    <span className="text-amber-600 font-bold">{pillar.reviews_required}R</span>
                    <span className="mx-1 text-slate-400">/</span>
                    <span className="text-emerald-600 font-bold">{pillar.compliant}C</span>
                  </td>
                  <td className="px-6 py-4 text-xs text-slate-500">
                    {pillar.last_audit_date ? new Date(pillar.last_audit_date).toLocaleDateString() : 'Pending'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Historical Audit Log & Inspection Stream */}
      <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h2 className="text-base font-bold text-slate-900">Sovereign Audit Log Stream</h2>
            <p className="text-xs text-slate-500">Chronological ledger of project milestone submissions and AI legal evaluations</p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            {/* Vertical Filter */}
            <div className="flex items-center space-x-1 bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs">
              <span className="text-slate-500 px-2 font-medium">Vertical:</span>
              {['ALL', 'Energy', 'Property', 'GovTech', 'Agribusiness'].map((v) => (
                <button
                  key={v}
                  onClick={() => setVerticalFilter(v)}
                  className={`px-2.5 py-1 rounded text-xs font-semibold transition ${
                    verticalFilter === v ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {v}
                </button>
              ))}
            </div>

            {/* Status Filter */}
            <div className="flex items-center space-x-1 bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs">
              <span className="text-slate-500 px-2 font-medium">Status:</span>
              {['ALL', 'Compliant', 'Review Required', 'Non-Compliant Violation'].map((s) => (
                <button
                  key={s}
                  onClick={() => setStatusFilter(s)}
                  className={`px-2 py-1 rounded text-xs font-semibold transition ${
                    statusFilter === s ? 'bg-slate-800 text-white shadow-xs' : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {s === 'Non-Compliant Violation' ? 'Violation' : s === 'Review Required' ? 'Review' : s}
                </button>
              ))}
            </div>
          </div>
        </div>

        {filteredHistory.length === 0 ? (
          <div className="text-center py-12 border border-dashed border-slate-200 rounded-xl bg-slate-50/50">
            <p className="text-slate-500 text-sm">No milestone audits matching current filters.</p>
            <Link
              href="/compliance/audit"
              className="mt-3 inline-flex items-center text-xs font-semibold text-blue-600 hover:text-blue-700"
            >
              Run a new milestone audit →
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredHistory.map((item) => (
              <div
                key={item.id}
                onClick={() => setSelectedAudit(item)}
                className="p-4 rounded-xl bg-white border border-slate-200 hover:border-slate-300 hover:shadow-sm cursor-pointer transition flex flex-col md:flex-row md:items-center justify-between gap-4"
              >
                <div className="space-y-1">
                  <div className="flex items-center space-x-3">
                    <span className="font-bold text-slate-900 text-sm">{item.project_name}</span>
                    <span className="text-xs font-mono text-slate-500">[{item.subsidiary_vertical}]</span>
                    {getStatusBadge(item.compliance_status)}
                  </div>
                  <p className="text-xs text-slate-600 line-clamp-1 max-w-2xl">
                    {item.submitted_text}
                  </p>
                </div>

                <div className="flex items-center space-x-6 shrink-0">
                  <div className="text-right">
                    <div className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Risk Score</div>
                    <div className={`font-mono ${getRiskColor(item.risk_score)}`}>
                      {item.risk_score.toFixed(1)} / 100
                    </div>
                  </div>
                  <div className="text-right text-xs text-slate-400 font-mono">
                    {new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                  <button className="px-3 py-1.5 rounded-lg bg-slate-100 text-xs font-semibold text-slate-700 hover:bg-slate-200 border border-slate-200 transition">
                    Inspect Report
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Audit Detail Modal Drawer */}
      {selectedAudit && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white border border-slate-200 w-full max-w-3xl max-h-[85vh] rounded-2xl overflow-hidden flex flex-col shadow-2xl">
            {/* Modal Header */}
            <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
              <div>
                <div className="flex items-center space-x-3">
                  <h3 className="font-bold text-slate-900 text-lg">{selectedAudit.project_name}</h3>
                  {getStatusBadge(selectedAudit.compliance_status)}
                </div>
                <p className="text-xs text-slate-500 mt-0.5">
                  Vertical: {selectedAudit.subsidiary_vertical} • Subsidiary ID: {selectedAudit.subsidiary_id} • Logged: {new Date(selectedAudit.created_at).toLocaleString()}
                </p>
              </div>
              <button
                onClick={() => setSelectedAudit(null)}
                className="w-8 h-8 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-600 hover:text-slate-900 flex items-center justify-center transition"
              >
                ✕
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto space-y-6 text-sm">
              {/* Executive Summary */}
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1.5">
                  Executive Assessment
                </h4>
                <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-200 text-slate-800 text-xs leading-relaxed font-medium">
                  {selectedAudit.raw_ai_response.executive_summary || 'Regulatory audit executed under BNH sovereign framework.'}
                </div>
              </div>

              {/* Submitted Milestone Text */}
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1.5">
                  Original Milestone Log Submitted by Project Manager
                </h4>
                <div className="p-3.5 rounded-lg bg-slate-100/70 border border-slate-200 font-mono text-xs text-slate-800 leading-relaxed">
                  "{selectedAudit.submitted_text}"
                </div>
              </div>

              {/* Risk Factors */}
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-red-700 mb-2">
                  Identified Regulatory Risks & Penalties
                </h4>
                <div className="space-y-2">
                  {selectedAudit.raw_ai_response.risk_factors?.map((rf, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-red-50 border border-red-200 text-xs text-red-800 flex items-start space-x-2">
                      <span className="text-red-600 font-bold shrink-0">⚠️</span>
                      <span className="font-medium">{rf}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Remediation Steps */}
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-emerald-700 mb-2">
                  Prescribed Institutional Remediation
                </h4>
                <div className="space-y-2">
                  {selectedAudit.raw_ai_response.remediation_steps?.map((step, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-start space-x-2">
                      <span className="text-emerald-600 font-bold shrink-0">✓</span>
                      <span className="font-medium">{step}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Cited Localized Clauses */}
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-blue-700 mb-2">
                  Localized Legal Grounding & Statutory Citations
                </h4>
                <div className="space-y-2.5">
                  {selectedAudit.raw_ai_response.cited_clauses?.map((c, idx) => (
                    <div key={idx} className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-1">
                      <div className="flex items-center justify-between text-blue-800 font-semibold">
                        <span>{c.law}</span>
                        <span className="font-mono text-[11px] text-slate-500">{c.section}</span>
                      </div>
                      <p className="text-slate-800 leading-relaxed">{c.clause}</p>
                      <p className="text-[11px] text-slate-500 italic mt-1">{c.relevance}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="px-6 py-3 border-t border-slate-200 bg-slate-50 flex items-center justify-between">
              <span className="text-[11px] text-slate-500 font-mono">
                LexGuard Sovereign Hash: SHA256-AIRGAP-{selectedAudit.id}
              </span>
              <button
                onClick={() => setSelectedAudit(null)}
                className="px-4 py-2 rounded-lg bg-slate-200 hover:bg-slate-300 text-slate-800 text-xs font-semibold transition"
              >
                Close Report
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
