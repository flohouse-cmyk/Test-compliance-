import { Sparkles, TriangleAlert, CheckCircle2, Info, Flame } from 'lucide-react'
import Panel from '../components/Panel'
import AISummary from '../components/AISummary'
import { insightFeed, leadershipSummary } from '../data/aiInsights'
import { frameworkReadiness } from '../data/metrics'
import { frameworks } from '../data/frameworks'
import { controls } from '../data/controls'
import { formatDate, scoreColor } from '../lib/ui'
import { daysUntil } from '../data/metrics'
import type { Insight } from '../data/aiInsights'

const toneMeta: Record<Insight['tone'], { icon: typeof Info; color: string; ring: string }> = {
  positive: { icon: CheckCircle2, color: 'text-emerald-400', ring: 'border-emerald-500/25 bg-emerald-500/5' },
  warning: { icon: TriangleAlert, color: 'text-amber-400', ring: 'border-amber-500/25 bg-amber-500/5' },
  critical: { icon: Flame, color: 'text-red-400', ring: 'border-red-500/25 bg-red-500/5' },
  neutral: { icon: Info, color: 'text-sky-400', ring: 'border-sky-500/25 bg-sky-500/5' },
}

const readiness = frameworkReadiness()

function evidenceFreshness(fwId: string) {
  const set = controls.filter((c) => c.frameworkId === fwId && c.status !== 'not_applicable')
  const fresh = set.filter((c) => c.evidence === 'collected').length
  return Math.round((fresh / Math.max(set.length, 1)) * 100)
}

export default function InsightsView() {
  return (
    <div className="space-y-5">
      <AISummary
        title="AI Executive Summary"
        headline={leadershipSummary.headline}
        bullets={leadershipSummary.bullets}
      >
        {leadershipSummary.body}
      </AISummary>

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-5">
        {/* Insight feed */}
        <Panel
          title="AI insight feed"
          subtitle="Auto-generated observations ranked by impact"
          className="lg:col-span-2"
        >
          <div className="space-y-3">
            {insightFeed.map((ins, i) => {
              const m = toneMeta[ins.tone]
              const Icon = m.icon
              return (
                <div key={i} className={`flex gap-3 rounded-xl border p-3 ${m.ring}`}>
                  <Icon className={`mt-0.5 h-4.5 w-4.5 shrink-0 ${m.color}`} />
                  <p className="text-sm leading-relaxed text-slate-300">{ins.text}</p>
                </div>
              )
            })}
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-[11px] text-slate-500">
            <Sparkles className="h-3.5 w-3.5 text-violet-400" />
            Summaries refresh as control statuses and findings change.
          </div>
        </Panel>

        {/* Audit readiness */}
        <Panel
          title="Audit readiness"
          subtitle="Readiness score, evidence freshness and timeline per framework"
          className="lg:col-span-3"
        >
          <div className="space-y-3">
            {frameworks.map((fw) => {
              const r = readiness.find((x) => x.frameworkId === fw.id)!
              const fresh = evidenceFreshness(fw.id)
              const d = daysUntil(fw.nextAuditDate)
              return (
                <div key={fw.id} className="rounded-xl border border-line bg-ink-850 p-4">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div>
                      <div className="text-sm font-semibold text-slate-100">{fw.fullName}</div>
                      <div className="text-xs text-slate-500">{fw.auditType}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-xs text-slate-400">{formatDate(fw.nextAuditDate)}</div>
                      <div className={`text-[11px] font-medium ${d <= 45 ? 'text-amber-400' : 'text-slate-500'}`}>in {d} days</div>
                    </div>
                  </div>

                  <div className="mt-3 space-y-2.5">
                    <Bar label="Readiness" value={r.score} color={scoreColor(r.score)} />
                    <Bar label="Evidence freshness" value={fresh} color="#38bdf8" />
                  </div>

                  <div className="mt-3 flex items-center gap-4 text-xs text-slate-400">
                    <span>{r.controlsCompliant}/{r.controlsTotal} controls compliant</span>
                    <span className="text-slate-600">·</span>
                    <span className={r.openItems > 0 ? 'text-amber-400' : 'text-emerald-400'}>{r.openItems} open items</span>
                  </div>
                </div>
              )
            })}
          </div>
        </Panel>
      </div>
    </div>
  )
}

function Bar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="mb-1 flex items-center justify-between text-xs">
        <span className="text-slate-400">{label}</span>
        <span className="font-mono text-slate-200">{value}%</span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-ink-700">
        <div className="h-full rounded-full transition-all duration-700" style={{ width: `${value}%`, background: color }} />
      </div>
    </div>
  )
}
