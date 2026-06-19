import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  Users,
  ListChecks,
  Sparkles,
  ShieldCheck,
  BookCheck,
} from 'lucide-react'
import type { ComponentType } from 'react'

interface NavItem {
  to: string
  label: string
  sub: string
  icon: ComponentType<{ className?: string }>
}

const navItems: NavItem[] = [
  { to: '/leadership', label: 'Leadership', sub: 'Executive posture', icon: LayoutDashboard },
  { to: '/team', label: 'Team Lead', sub: 'Pod-level view', icon: Users },
  { to: '/delivery', label: 'PM / Dev', sub: 'Open items & tasks', icon: ListChecks },
  { to: '/insights', label: 'Insights', sub: 'AI & audit readiness', icon: Sparkles },
  { to: '/frameworks', label: 'Frameworks', sub: 'Controls library', icon: BookCheck },
]

export default function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 flex-col border-r border-line bg-ink-900/80 lg:flex">
      <div className="flex h-16 items-center gap-2.5 border-b border-line px-5">
        <span className="grid h-9 w-9 place-items-center rounded-xl bg-brand-500/15 text-brand-400">
          <ShieldCheck className="h-5 w-5" />
        </span>
        <div className="leading-tight">
          <div className="text-sm font-bold tracking-tight text-slate-50">ComplyScope</div>
          <div className="text-[11px] text-slate-500">Compliance posture</div>
        </div>
      </div>

      <nav className="flex-1 space-y-1 p-3">
        <p className="px-2 pb-1 pt-2 text-[10px] font-semibold uppercase tracking-wider text-slate-500">Views</p>
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-colors duration-200 cursor-pointer ${
                isActive
                  ? 'bg-brand-500/12 text-slate-50 ring-1 ring-brand-500/25'
                  : 'text-slate-400 hover:bg-ink-800 hover:text-slate-200'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <item.icon className={`h-4.5 w-4.5 ${isActive ? 'text-brand-400' : 'text-slate-500 group-hover:text-slate-300'}`} />
                <span className="flex-1">
                  <span className="block font-medium">{item.label}</span>
                  <span className="block text-[11px] text-slate-500">{item.sub}</span>
                </span>
              </>
            )}
          </NavLink>
        ))}
      </nav>

      <div className="m-3 rounded-xl border border-line bg-ink-850 p-3">
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <span className="h-2 w-2 animate-pulse rounded-full bg-brand-500" />
          Live demo data
        </div>
        <p className="mt-1 text-[11px] leading-snug text-slate-500">
          Sample compliance dataset across 5 frameworks &amp; 6 pods.
        </p>
      </div>
    </aside>
  )
}
