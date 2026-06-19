import { scoreColor } from '../lib/ui'

interface Props {
  score: number
  size?: number
  label?: string
  sublabel?: string
}

/** Radial posture gauge drawn with a single SVG arc. */
export default function ScoreGauge({ score, size = 160, label, sublabel }: Props) {
  const stroke = size * 0.09
  const r = (size - stroke) / 2
  const c = 2 * Math.PI * r
  const pct = Math.max(0, Math.min(100, score))
  const offset = c - (pct / 100) * c
  const color = scoreColor(score)

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90" role="img" aria-label={`${label ?? 'Posture score'}: ${score} percent`}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e2a44" strokeWidth={stroke} />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={offset}
          style={{ transition: 'stroke-dashoffset 800ms cubic-bezier(0.22,1,0.36,1)' }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-mono font-semibold tabular-nums" style={{ color, fontSize: size * 0.26 }}>
          {score}
          <span style={{ fontSize: size * 0.12 }}>%</span>
        </span>
        {sublabel && <span className="mt-0.5 text-[11px] uppercase tracking-wider text-slate-400">{sublabel}</span>}
      </div>
    </div>
  )
}
