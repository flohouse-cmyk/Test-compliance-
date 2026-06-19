import { useMemo, useState } from 'react'
import { Filter, CalendarClock, FileText, Target, X, CircleHelp } from 'lucide-react'
import Panel from '../components/Panel'
import StatCard from '../components/StatCard'
import { SeverityBadge, TaskStatusBadge } from '../components/badges'
import { openItems } from '../data/openItems'
import { frameworks, teams, teamLabel } from '../data/frameworks'
import { daysUntil } from '../data/metrics'
import { formatDate, dueLabel } from '../lib/ui'
import type { OpenItem, Severity, TaskStatus } from '../data/types'

const severities: Severity[] = ['critical', 'high', 'medium', 'low']
const statuses: TaskStatus[] = ['not_started', 'in_progress', 'in_review', 'blocked', 'done']

const dueTone: Record<'crit' | 'warn' | 'ok', string> = {
  crit: 'text-red-400',
  warn: 'text-amber-400',
  ok: 'text-slate-400',
}

export default function DevView() {
  const [fw, setFw] = useState<string>('all')
  const [team, setTeam] = useState<string>('all')
  const [sev, setSev] = useState<string>('all')
  const [status, setStatus] = useState<string>('open')
  const [selected, setSelected] = useState<OpenItem | null>(null)

  const filtered = useMemo(() => {
    return openItems
      .filter((o) => (fw === 'all' ? true : o.frameworkId === fw))
      .filter((o) => (team === 'all' ? true : o.teamId === team))
      .filter((o) => (sev === 'all' ? true : o.severity === sev))
      .filter((o) =>
        status === 'all' ? true : status === 'open' ? o.status !== 'done' : o.status === status,
      )
      .sort((a, b) => daysUntil(a.dueDate) - daysUntil(b.dueDate))
  }, [fw, team, sev, status])

  const totalEffort = filtered.reduce((s, o) => s + o.effortDays, 0)
  const overdue = filtered.filter((o) => daysUntil(o.dueDate) < 0 && o.status !== 'done').length

  const selectClass =
    'appearance-none rounded-lg border border-line bg-ink-850 py-2 pl-3 pr-8 text-sm text-slate-200 outline-none focus:border-brand-500/50 cursor-pointer'

  return (
    <div className="space-y-5">
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard label="Matching items" value={filtered.length} icon={<FileText className="h-4 w-4" />} accent="#38bdf8" />
        <StatCard label="Overdue" value={overdue} icon={<CalendarClock className="h-4 w-4" />} accent="#ef4444" hint="Past due date" />
        <StatCard label="Est. effort" value={`${totalEffort}d`} icon={<Target className="h-4 w-4" />} accent="#a78bfa" hint="Engineer-days remaining" />
        <StatCard
          label="Critical open"
          value={filtered.filter((o) => o.severity === 'critical' && o.status !== 'done').length}
          icon={<CircleHelp className="h-4 w-4" />}
          accent="#f97316"
        />
      </div>

      {/* Filters */}
      <div className="card flex flex-wrap items-center gap-3 p-4">
        <span className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider text-slate-400">
          <Filter className="h-4 w-4" /> Filters
        </span>
        <Select value={fw} onChange={setFw} className={selectClass} label="Framework">
          <option value="all">All frameworks</option>
          {frameworks.map((f) => (
            <option key={f.id} value={f.id}>{f.name}</option>
          ))}
        </Select>
        <Select value={team} onChange={setTeam} className={selectClass} label="Team">
          <option value="all">All teams</option>
          {teams.map((t) => (
            <option key={t.id} value={t.id}>{t.name}</option>
          ))}
        </Select>
        <Select value={sev} onChange={setSev} className={selectClass} label="Severity">
          <option value="all">All severities</option>
          {severities.map((s) => (
            <option key={s} value={s} className="capitalize">{s}</option>
          ))}
        </Select>
        <Select value={status} onChange={setStatus} className={selectClass} label="Status">
          <option value="open">Open only</option>
          <option value="all">All statuses</option>
          {statuses.map((s) => (
            <option key={s} value={s}>{s.replace('_', ' ')}</option>
          ))}
        </Select>
      </div>

      <div className="grid grid-cols-1 gap-5 xl:grid-cols-3">
        {/* Items table */}
        <Panel title="Open items" subtitle="Click a row for the full ask, rationale and timing" className="xl:col-span-2">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="text-xs uppercase tracking-wider text-slate-500">
                <tr>
                  <th className="px-2 py-2 font-medium">ID</th>
                  <th className="px-2 py-2 font-medium">Item</th>
                  <th className="px-2 py-2 font-medium">Sev</th>
                  <th className="px-2 py-2 font-medium">Status</th>
                  <th className="px-2 py-2 font-medium">Due</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((o) => {
                  const d = dueLabel(daysUntil(o.dueDate))
                  const isSel = selected?.id === o.id
                  return (
                    <tr
                      key={o.id}
                      onClick={() => setSelected(o)}
                      className={`cursor-pointer border-t border-line/60 transition-colors hover:bg-ink-850/70 ${isSel ? 'bg-brand-500/8' : ''}`}
                    >
                      <td className="px-2 py-2.5 font-mono text-xs text-slate-500">{o.id}</td>
                      <td className="px-2 py-2.5">
                        <div className="text-slate-100">{o.title}</div>
                        <div className="text-[11px] text-slate-500">{o.frameworkId} · {o.controlCode} · {teamLabel(o.teamId)}</div>
                      </td>
                      <td className="px-2 py-2.5"><SeverityBadge severity={o.severity} /></td>
                      <td className="px-2 py-2.5"><TaskStatusBadge status={o.status} /></td>
                      <td className="px-2 py-2.5">
                        <span className={`text-xs ${o.status === 'done' ? 'text-slate-500' : dueTone[d.tone]}`}>
                          {o.status === 'done' ? 'Closed' : d.text}
                        </span>
                      </td>
                    </tr>
                  )
                })}
                {filtered.length === 0 && (
                  <tr>
                    <td colSpan={5} className="px-2 py-8 text-center text-sm text-slate-500">No items match these filters.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </Panel>

        {/* Detail panel */}
        <div className="xl:col-span-1">
          {selected ? (
            <DetailCard item={selected} onClose={() => setSelected(null)} />
          ) : (
            <div className="card flex h-full min-h-64 flex-col items-center justify-center p-8 text-center">
              <FileText className="h-8 w-8 text-slate-600" />
              <p className="mt-3 text-sm font-medium text-slate-300">Select an open item</p>
              <p className="mt-1 text-xs text-slate-500">
                See exactly what is being asked, why it matters, who owns it and when it is due.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function Select({
  value,
  onChange,
  children,
  className,
  label,
}: {
  value: string
  onChange: (v: string) => void
  children: React.ReactNode
  className: string
  label: string
}) {
  return (
    <div className="relative">
      <select aria-label={label} value={value} onChange={(e) => onChange(e.target.value)} className={className}>
        {children}
      </select>
      <svg className="pointer-events-none absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="m6 9 6 6 6-6" />
      </svg>
    </div>
  )
}

function DetailCard({ item, onClose }: { item: OpenItem; onClose: () => void }) {
  const d = dueLabel(daysUntil(item.dueDate))
  return (
    <div className="card sticky top-20 overflow-hidden">
      <div className="flex items-start justify-between gap-2 border-b border-line p-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="font-mono text-xs text-slate-500">{item.id}</span>
            <SeverityBadge severity={item.severity} />
          </div>
          <h3 className="mt-1.5 text-base font-semibold leading-snug text-slate-50">{item.title}</h3>
        </div>
        <button onClick={onClose} aria-label="Close detail" className="grid h-7 w-7 shrink-0 place-items-center rounded-lg text-slate-400 hover:bg-ink-800 hover:text-slate-200 cursor-pointer">
          <X className="h-4 w-4" />
        </button>
      </div>

      <div className="space-y-4 p-4">
        <Field label="What is being asked">
          <p className="text-sm leading-relaxed text-slate-200">{item.ask}</p>
        </Field>
        <Field label="Why it matters">
          <p className="text-sm leading-relaxed text-slate-300">{item.why}</p>
        </Field>

        <div className="grid grid-cols-2 gap-3">
          <Meta label="Owner" value={item.owner} />
          <Meta label="Team" value={teamLabel(item.teamId)} />
          <Meta label="Framework" value={item.frameworkId} />
          <Meta label="Control" value={item.controlCode} mono />
          <Meta label="Effort" value={`${item.effortDays} day${item.effortDays > 1 ? 's' : ''}`} />
          <Meta label="Opened" value={formatDate(item.createdDate)} />
        </div>

        <div className="rounded-xl border border-line bg-ink-850 p-3">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-[11px] uppercase tracking-wider text-slate-500">Due date</div>
              <div className="text-sm font-medium text-slate-100">{formatDate(item.dueDate)}</div>
            </div>
            <span className={`text-sm font-semibold ${item.status === 'done' ? 'text-emerald-400' : dueTone[d.tone]}`}>
              {item.status === 'done' ? 'Closed' : d.text}
            </span>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-xs text-slate-500">Current status</span>
          <TaskStatusBadge status={item.status} />
        </div>
      </div>
    </div>
  )
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <div className="mb-1 text-[11px] font-semibold uppercase tracking-wider text-brand-400">{label}</div>
      {children}
    </div>
  )
}

function Meta({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <div className="rounded-lg border border-line bg-ink-850 p-2.5">
      <div className="text-[10px] uppercase tracking-wider text-slate-500">{label}</div>
      <div className={`mt-0.5 text-sm text-slate-200 ${mono ? 'font-mono text-xs' : ''}`}>{value}</div>
    </div>
  )
}
