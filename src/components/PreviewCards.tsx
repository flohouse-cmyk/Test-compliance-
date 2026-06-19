import { orgScore, postureTrend, openOpenItems, teamScore, teamTargets } from '../data/metrics'
import { openItems } from '../data/openItems'

/* Lightweight, presentational mini-dashboards used in the marketing layers.
   They echo the real product surfaces without pulling in Recharts. */

function Ring({ score, size = 84 }: { score: number; size?: number }) {
  const stroke = 9
  const r = (size - stroke) / 2
  const c = 2 * Math.PI * r
  const offset = c - (score / 100) * c
  return (
    <svg width={size} height={size} className="-rotate-90">
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth={stroke} />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={r}
        fill="none"
        stroke="url(#ringGrad)"
        strokeWidth={stroke}
        strokeLinecap="round"
        strokeDasharray={c}
        strokeDashoffset={offset}
      />
      <defs>
        <linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#a78bfa" />
          <stop offset="60%" stopColor="#22d3ee" />
          <stop offset="100%" stopColor="#34d399" />
        </linearGradient>
      </defs>
    </svg>
  )
}

function Spark({ points }: { points: number[] }) {
  const w = 220
  const h = 56
  const min = Math.min(...points)
  const max = Math.max(...points)
  const span = max - min || 1
  const step = w / (points.length - 1)
  const path = points
    .map((p, i) => `${i === 0 ? 'M' : 'L'} ${i * step} ${h - ((p - min) / span) * (h - 8) - 4}`)
    .join(' ')
  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="w-full" preserveAspectRatio="none" height={h}>
      <path d={`${path} L ${w} ${h} L 0 ${h} Z`} fill="url(#sparkFill)" opacity={0.5} />
      <path d={path} fill="none" stroke="#34d399" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round" />
      <defs>
        <linearGradient id="sparkFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#34d399" stopOpacity={0.35} />
          <stop offset="100%" stopColor="#34d399" stopOpacity={0} />
        </linearGradient>
      </defs>
    </svg>
  )
}

const chipBase =
  'rounded-lg border border-white/10 bg-white/5 px-2.5 py-1.5 text-[11px] text-slate-300'

export function LeadershipPreview() {
  return (
    <div className="glass-strong w-full rounded-2xl p-5 shadow-2xl">
      <div className="flex items-center justify-between">
        <span className="text-[11px] font-medium uppercase tracking-widest text-iris">Leadership</span>
        <span className="rounded-full border border-emerald-400/30 bg-emerald-400/10 px-2 py-0.5 text-[10px] text-emerald-300">
          On track
        </span>
      </div>
      <div className="mt-4 flex items-center gap-4">
        <div className="relative grid place-items-center">
          <Ring score={orgScore} />
          <span className="absolute font-display text-xl font-semibold text-white">{orgScore}%</span>
        </div>
        <div className="flex-1">
          <div className="text-xs text-slate-400">Org posture</div>
          <Spark points={postureTrend.map((p) => p.score)} />
        </div>
      </div>
      <div className="mt-4 grid grid-cols-3 gap-2">
        <div className={chipBase}>5 frameworks</div>
        <div className={chipBase}>{openOpenItems.length} open</div>
        <div className={chipBase}>+15 pts / yr</div>
      </div>
    </div>
  )
}

export function TeamLeadPreview() {
  const score = teamScore('payments')
  const target = teamTargets.payments
  return (
    <div className="glass-strong w-full rounded-2xl p-5 shadow-2xl">
      <div className="flex items-center justify-between">
        <span className="text-[11px] font-medium uppercase tracking-widest text-iris">Team Lead · Payments</span>
        <span className="rounded-full border border-amber-400/30 bg-amber-400/10 px-2 py-0.5 text-[10px] text-amber-300">
          {target - score} pts to target
        </span>
      </div>
      <div className="mt-4 flex items-end gap-3">
        <div className="font-display text-4xl font-bold text-white">{score}%</div>
        <div className="mb-1 text-xs text-slate-400">vs {target}% target</div>
      </div>
      <div className="mt-3 space-y-2">
        {[
          { label: 'Network security', v: 82 },
          { label: 'CHD protection', v: 68 },
          { label: 'Monitoring & test', v: 91 },
        ].map((b) => (
          <div key={b.label}>
            <div className="mb-1 flex justify-between text-[11px] text-slate-400">
              <span>{b.label}</span>
              <span className="text-slate-300">{b.v}%</span>
            </div>
            <div className="h-1.5 overflow-hidden rounded-full bg-white/10">
              <div className="h-full rounded-full bg-iris" style={{ width: `${b.v}%` }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

const sevDot: Record<string, string> = {
  critical: '#f87171',
  high: '#fb923c',
  medium: '#fbbf24',
  low: '#38bdf8',
}

export function DevPreview() {
  const items = openItems.filter((o) => o.status !== 'done').slice(0, 4)
  return (
    <div className="glass-strong w-full rounded-2xl p-5 shadow-2xl">
      <div className="flex items-center justify-between">
        <span className="text-[11px] font-medium uppercase tracking-widest text-iris">PM / Dev workspace</span>
        <span className="text-[10px] text-slate-400">{openItems.filter((o) => o.status !== 'done').length} open items</span>
      </div>
      <div className="mt-4 space-y-2">
        {items.map((o) => (
          <div key={o.id} className="flex items-center gap-2.5 rounded-lg border border-white/8 bg-white/5 px-2.5 py-2">
            <span className="h-2 w-2 shrink-0 rounded-full" style={{ background: sevDot[o.severity] }} />
            <span className="truncate text-[11px] text-slate-200">{o.title}</span>
            <span className="ml-auto shrink-0 font-mono text-[10px] text-slate-500">{o.controlCode}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
