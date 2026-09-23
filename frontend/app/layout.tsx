import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.css';

export const metadata: Metadata = {
  title: 'LexGuard | Brendan Nicholas Holdings Compliance Engine',
  description: 'Offline Sovereign Regulatory & PM Compliance Agent for Institutional Governance',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col text-slate-900 bg-[#f8fafc]">
        {/* Top Sovereign Institutional Header */}
        <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/95 backdrop-blur-md shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <Link href="/compliance" className="flex items-center space-x-3 group">
                <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-700 to-indigo-800 border border-blue-600 flex items-center justify-center shadow-md">
                  <span className="font-bold text-white tracking-widest text-sm">LG</span>
                </div>
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-slate-900 tracking-wide text-base">LEXGUARD</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-blue-50 border border-blue-200 text-blue-700 uppercase tracking-wider font-semibold">
                      Sovereign Core
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-500 font-medium">Brendan Nicholas Holdings • Office of Chief Compliance</p>
                </div>
              </Link>

              {/* Navigation Links */}
              <nav className="hidden md:flex items-center space-x-1 pl-4 border-l border-slate-200">
                <Link
                  href="/compliance"
                  className="px-3 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition"
                >
                  Subsidiary Command Center
                </Link>
                <Link
                  href="/compliance/audit"
                  className="px-3 py-1.5 rounded-md text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition"
                >
                  Milestone Audit Studio
                </Link>
              </nav>
            </div>

            {/* Sovereign Security & Engine Badges */}
            <div className="flex items-center space-x-3">
              <div className="hidden sm:flex items-center space-x-2 px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-[11px] font-mono font-medium">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>AIR-GAP SECURED</span>
              </div>
              <div className="hidden lg:flex items-center space-x-2 px-2.5 py-1 rounded-full bg-slate-100 border border-slate-200 text-slate-700 text-[11px] font-mono font-medium">
                <span className="text-slate-400">LLM:</span>
                <span className="text-amber-700 font-semibold">gemma:2b</span>
              </div>
              <div className="hidden lg:flex items-center space-x-2 px-2.5 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-800 text-[11px] font-mono font-medium">
                <span className="text-blue-500">VDB:</span>
                <span className="text-blue-700 font-semibold">FAISS</span>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content Viewport */}
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {children}
        </main>

        {/* Institutional Footer */}
        <footer className="border-t border-slate-200 bg-white py-6 text-slate-500 text-xs">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
            <div>
              <p className="font-semibold text-slate-700">LexGuard Regulatory Engine v1.0.0-SOVEREIGN</p>
              <p className="text-[11px] text-slate-500">Strictly confidential. Operating in air-gapped memory mode within BNH sovereign infrastructure.</p>
            </div>
            <div className="flex items-center space-x-6 text-[11px] font-medium text-slate-600">
              <span>NDPA 2023 Compliant</span>
              <span>PIA 2021 Aligned</span>
              <span>Zero-Cloud Retention</span>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
