import { useMemo, useState } from 'react'
import Panel from '../components/Panel'
import { ControlStatusBadge } from '../components/badges'
import { controls } from '../data/controls'
import { frameworks, teamLabel } from '../data/frameworks'
import { scoreFor, statusCounts } from '../data/metrics'
import { formatDate, scoreColor } from '../lib/ui'

export default function FrameworksView() {
  const [active, setActive] = useState(frameworks[0].id)
  const [q, setQ] = useState('')

  const set = useMemo(() => controls.filter((c) => c.frameworkId === active), [active])
  const counts = statusCounts(set)
  const score = scoreFor(set)
  const fw = frameworks.find((f) => f.id === active)!

  const filtered = useMemo(() => {
    const t = q.trim().toLowerCase()
    if (!t) return set
    return set.filter(
      (c) => c.title.toLowerCase().includes(t) || c.code.toLowerCase().includes(t) || c.category.toLowerCase().includes(t),
    )
  }, [set, q])

  return (
    <div className="space-y-5">
      {/* Framework tabs */}
      <div className="flex flex-wrap gap-2">
        {frameworks.map((f) => {
          const s = scoreFor(controls.filter((c) => c.frameworkId === f.id))
          return (
            <button
              key={f.id}
              onClick={() => setActive(f.id)}
              className={`flex items-center gap-2 rounded-xl border px-3.5 py-2 text-sm font-medium transition-colors cursor-pointer ${
                active === f.id
                  ? 'border-brand-500/40 bg-brand-500/10 text-slate-50'
                  : 'border-line bg-ink-850 text-slate-400 hover:text-slate-200'
              }`}
            >
              <span className="h-2 w-2 rounded-full" style={{ background: scoreColor(s) }} />
              {f.name}
              <span className="font-mono text-xs text-slate-500">{s}%</span>
            </button>
          )
        })}
      </div>

      <div className="card p-5">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="max-w-xl">
            <h2 className="text-lg font-semibold text-slate-50">{fw.fullName}</h2>
            <p className="mt-1 text-sm text-slate-400">{fw.description}</p>
            <p className="mt-2 text-xs text-slate-500">
              {fw.auditType} · Next assessment {formatDate(fw.nextAuditDate)}
            </p>
          </div>
          <div className="flex gap-3">
            <Stat label="Score" value={`${score}%`} color={scoreColor(score)} />
            <Stat label="Compliant" value={`${counts.compliant}`} color="#22c55e" />
            <Stat label="At risk" value={`${counts.at_risk}`} color="#f59e0b" />
            <Stat label="Non-compliant" value={`${counts.non_compliant}`} color="#ef4444" />
          </div>
        </div>
      </div>

      <Panel
        title="Control inventory"
        subtitle={`${filtered.length} of ${set.length} controls`}
        action={
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search controls…"
            aria-label="Search controls"
            className="w-44 rounded-lg border border-line bg-ink-850 px-3 py-1.5 text-sm text-slate-200 placeholder:text-slate-500 outline-none focus:border-brand-500/50"
          />
        }
      >
        <div className="max-h-[28rem] overflow-y-auto">
          <table className="w-full text-left text-sm">
            <thead className="sticky top-0 bg-ink-900 text-xs uppercase tracking-wider text-slate-500">
              <tr>
                <th className="px-3 py-2 font-medium">Code</th>
                <th className="px-3 py-2 font-medium">Control</th>
                <th className="hidden px-3 py-2 font-medium md:table-cell">Category</th>
                <th className="hidden px-3 py-2 font-medium lg:table-cell">Owner</th>
                <th className="px-3 py-2 font-medium">Status</th>
                <th className="hidden px-3 py-2 font-medium sm:table-cell">Reviewed</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((c) => (
                <tr key={c.id} className="border-t border-line/60 hover:bg-ink-850/60">
                  <td className="px-3 py-2 font-mono text-xs text-slate-400">{c.code}</td>
                  <td className="px-3 py-2 text-slate-200">{c.title}</td>
                  <td className="hidden px-3 py-2 text-slate-400 md:table-cell">{c.category}</td>
                  <td className="hidden px-3 py-2 text-slate-400 lg:table-cell">{teamLabel(c.ownerTeamId)}</td>
                  <td className="px-3 py-2"><ControlStatusBadge status={c.status} /></td>
                  <td className="hidden px-3 py-2 text-xs text-slate-500 sm:table-cell">{formatDate(c.lastReviewed)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Panel>
    </div>
  )
}

function Stat({ label, value, color }: { label: string; value: string; color: string }) {
  return (
    <div className="rounded-xl border border-line bg-ink-850 px-4 py-2 text-center">
      <div className="font-mono text-lg font-semibold" style={{ color }}>{value}</div>
      <div className="text-[10px] uppercase tracking-wider text-slate-500">{label}</div>
    </div>
  )
}
