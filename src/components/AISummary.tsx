import { Sparkles } from 'lucide-react'
import type { ReactNode } from 'react'

interface Props {
  title?: string
  headline?: string
  children: ReactNode
  bullets?: string[]
}

/** Branded "AI summary" panel used across views. */
export default function AISummary({ title = 'AI Summary', headline, children, bullets }: Props) {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-violet-500/25 bg-gradient-to-br from-violet-500/10 via-ink-900 to-ink-900 p-5">
      <div className="pointer-events-none absolute -right-10 -top-10 h-40 w-40 rounded-full bg-violet-500/10 blur-3xl" />
      <div className="flex items-center gap-2">
        <span className="grid h-7 w-7 place-items-center rounded-lg bg-violet-500/20 text-violet-300">
          <Sparkles className="h-4 w-4" />
        </span>
        <span className="text-sm font-semibold text-violet-200">{title}</span>
        <span className="rounded-full border border-violet-500/30 bg-violet-500/10 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wider text-violet-300">
          Generated
        </span>
      </div>
      {headline && <p className="mt-3 text-base font-semibold leading-snug text-slate-100">{headline}</p>}
      <div className="mt-2 text-sm leading-relaxed text-slate-300">{children}</div>
      {bullets && bullets.length > 0 && (
        <ul className="mt-3 space-y-1.5">
          {bullets.map((b) => (
            <li key={b} className="flex items-start gap-2 text-sm text-slate-300">
              <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-violet-400" />
              <span>{b}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
