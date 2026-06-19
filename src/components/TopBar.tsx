import { useLocation, useNavigate } from 'react-router-dom'
import { Search, Bell, Calendar } from 'lucide-react'

const titles: Record<string, { title: string; subtitle: string }> = {
  '/leadership': { title: 'Leadership Overview', subtitle: 'Org-wide compliance posture & audit readiness' },
  '/team': { title: 'Team Lead View', subtitle: 'Posture, gaps and targets for your pod' },
  '/delivery': { title: 'Delivery Workspace', subtitle: 'What is being asked, what to do, and when' },
  '/insights': { title: 'Insights & Audit Readiness', subtitle: 'AI summaries and upcoming audits' },
  '/frameworks': { title: 'Frameworks Library', subtitle: 'Control inventory across all frameworks' },
}

export default function TopBar() {
  const { pathname } = useLocation()
  const navigate = useNavigate()
  const meta = titles[pathname] ?? titles['/leadership']

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center gap-4 border-b border-line bg-ink-950/80 px-4 backdrop-blur-md sm:px-6">
      <button
        onClick={() => navigate(-1)}
        className="lg:hidden grid h-9 w-9 place-items-center rounded-lg border border-line text-slate-300 cursor-pointer"
        aria-label="Back"
      >
        ‹
      </button>
      <div className="min-w-0 flex-1">
        <h1 className="truncate text-base font-semibold text-slate-50 sm:text-lg">{meta.title}</h1>
        <p className="hidden truncate text-xs text-slate-500 sm:block">{meta.subtitle}</p>
      </div>

      <div className="relative hidden md:block">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
        <input
          type="search"
          aria-label="Search controls and findings"
          placeholder="Search controls, findings…"
          className="w-56 rounded-lg border border-line bg-ink-850 py-2 pl-9 pr-3 text-sm text-slate-200 placeholder:text-slate-500 outline-none focus:border-brand-500/50 focus:ring-1 focus:ring-brand-500/30"
        />
      </div>

      <div className="hidden items-center gap-2 rounded-lg border border-line bg-ink-850 px-3 py-2 text-xs text-slate-400 xl:flex">
        <Calendar className="h-4 w-4 text-slate-500" />
        Reporting period: Q2 2026
      </div>

      <button className="relative grid h-9 w-9 place-items-center rounded-lg border border-line text-slate-300 transition-colors hover:bg-ink-800 cursor-pointer" aria-label="Notifications">
        <Bell className="h-4 w-4" />
        <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-red-500 ring-2 ring-ink-950" />
      </button>

      <div className="flex items-center gap-2.5">
        <div className="grid h-9 w-9 place-items-center rounded-full bg-gradient-to-br from-brand-500 to-emerald-700 text-sm font-semibold text-ink-950">
          AC
        </div>
        <div className="hidden leading-tight sm:block">
          <div className="text-sm font-medium text-slate-100">Alex Carter</div>
          <div className="text-[11px] text-slate-500">VP, Security &amp; Compliance</div>
        </div>
      </div>
    </header>
  )
}
