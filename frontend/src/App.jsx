import React from 'react'

export default function App() {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col items-center justify-center p-6">
      <div className="max-w-md w-full bg-slate-800 rounded-xl shadow-2xl p-6 border border-slate-700 text-center">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent mb-2">
          Vision-Agentic Scraper
        </h1>
        <p className="text-sm text-slate-400 mb-4">
          Phase 1: React + Vite + Tailwind v4 + PostCSS is officially configured!
        </p>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          Stack Online & Compiling
        </div>
      </div>
    </div>
  )
}
