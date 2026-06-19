import type { ReactNode } from 'react'

interface Props {
  label: string
  value: ReactNode
  delta?: { value: string; positive: boolean }
  icon?: ReactNode
  hint?: string
  accent?: string
}

export default function StatCard({ label, value, delta, icon, hint, accent = '#22c55e' }: Props) {
  return (
    <div className="card p-4 transition-colors duration-200 hover:border-slate-600">
      <div className="flex items-start justify-between">
        <span className="text-xs font-medium uppercase tracking-wider text-slate-400">{label}</span>
        {icon && (
          <span className="grid h-8 w-8 place-items-center rounded-lg" style={{ background: `${accent}1a`, color: accent }}>
            {icon}
          </span>
        )}
      </div>
      <div className="mt-2 flex items-baseline gap-2">
        <span className="font-mono text-2xl font-semibold tabular-nums text-slate-50">{value}</span>
        {delta && (
          <span className={`text-xs font-medium ${delta.positive ? 'text-emerald-400' : 'text-red-400'}`}>
            {delta.positive ? '▲' : '▼'} {delta.value}
          </span>
        )}
      </div>
      {hint && <p className="mt-1 text-xs text-slate-500">{hint}</p>}
    </div>
  )
}
