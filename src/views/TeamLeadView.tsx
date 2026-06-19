import { useState } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  RadialBar,
  RadialBarChart,
  PolarAngleAxis,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { Target, ListTodo, ShieldAlert, ChevronDown } from 'lucide-react'
import Panel from '../components/Panel'
import AISummary from '../components/AISummary'
import StatCard from '../components/StatCard'
import { SeverityBadge, TaskStatusBadge, ControlStatusBadge } from '../components/badges'
import { teams } from '../data/frameworks'
import {
  controlsForTeam,
  teamScore,
  openItemsForTeam,
  statusCounts,
  severityCount,
  teamTargets,
  daysUntil,
} from '../data/metrics'
import { teamSummary } from '../data/aiInsights'
import { scoreColor, formatDate } from '../lib/ui'

function ChartTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-lg border border-line bg-ink-850 px-3 py-2 text-xs shadow-xl">
      {label && <div className="mb-1 font-medium text-slate-200">{label}</div>}
      {payload.map((p: any) => (
        <div key={p.name} className="flex items-center gap-2 text-slate-300">
          <span className="h-2 w-2 rounded-full" style={{ background: p.color || p.fill }} />
          {p.name}: <span className="font-mono text-slate-100">{p.value}</span>
        </div>
      ))}
    </div>
  )
}

export default function TeamLeadView() {
  const [teamId, setTeamId] = useState(teams[1].id) // default Payments — most interesting
  const team = teams.find((t) => t.id === teamId)!
  const score = teamScore(teamId)
  const target = teamTargets[teamId] ?? 95
  const gap = target - score
  const teamControls = controlsForTeam(teamId)
  const teamItems = openItemsForTeam(teamId)
  const openCount = teamItems.filter((i) => i.status !== 'done').length
  const counts = statusCounts(teamControls)
  const sev = severityCount(teamItems.filter((i) => i.status !== 'done'))
  const summary = teamSummary(teamId)

  const gaugeData = [{ name: 'score', value: score, fill: scoreColor(score) }]

  // controls grouped by category for this team
  const byCategory = Object.values(
    teamControls.reduce<Record<string, { category: string; compliant: number; gap: number }>>((acc, c) => {
      acc[c.category] ??= { category: c.category, compliant: 0, gap: 0 }
      if (c.status === 'compliant') acc[c.category].compliant++
      else if (c.status !== 'not_applicable') acc[c.category].gap++
      return acc
    }, {}),
  )

  return (
    <div className="space-y-5">
      {/* Team selector */}
      <div className="flex flex-wrap items-center gap-3">
        <div className="relative">
          <select
            value={teamId}
            onChange={(e) => setTeamId(e.target.value)}
            aria-label="Select team"
            className="appearance-none rounded-xl border border-line bg-ink-850 py-2.5 pl-4 pr-10 text-sm font-medium text-slate-100 outline-none focus:border-brand-500/50 cursor-pointer"
          >
            {teams.map((t) => (
              <option key={t.id} value={t.id}>
                {t.name} — {t.pod}
              </option>
            ))}
          </select>
          <ChevronDown className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
        </div>
        <div className="flex items-center gap-2 text-sm text-slate-400">
          <span className="grid h-8 w-8 place-items-center rounded-full bg-ink-700 text-xs font-semibold text-slate-200">
            {team.leadInitials}
          </span>
          Led by <span className="text-slate-200">{team.lead}</span> · {team.headcount} people
        </div>
      </div>

      {/* Top row: gauge + stats */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <Panel title="Team posture vs. target" subtitle="Where the pod is today and where it needs to be">
          <div className="flex items-center gap-4">
            <div className="relative h-40 w-40 shrink-0">
              <ResponsiveContainer width="100%" height="100%">
                <RadialBarChart innerRadius="72%" outerRadius="100%" data={gaugeData} startAngle={90} endAngle={-270}>
                  <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
                  <RadialBar background={{ fill: '#1e2a44' }} dataKey="value" cornerRadius={8} />
                </RadialBarChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="font-mono text-3xl font-semibold" style={{ color: scoreColor(score) }}>{score}%</span>
                <span className="text-[11px] uppercase tracking-wider text-slate-500">current</span>
              </div>
            </div>
            <div className="flex-1 space-y-3">
              <div className="rounded-xl border border-line bg-ink-850 p-3">
                <div className="text-xs text-slate-500">Target</div>
                <div className="font-mono text-xl text-slate-100">{target}%</div>
              </div>
              <div className="rounded-xl border border-line bg-ink-850 p-3">
                <div className="text-xs text-slate-500">Gap to close</div>
                <div className={`font-mono text-xl ${gap > 0 ? 'text-amber-400' : 'text-emerald-400'}`}>
                  {gap > 0 ? `${gap} pts` : 'On target'}
                </div>
              </div>
            </div>
          </div>
        </Panel>

        <div className="grid grid-cols-2 gap-4 lg:col-span-2">
          <StatCard label="Open items" value={openCount} icon={<ListTodo className="h-4 w-4" />} hint={`${sev.critical} critical · ${sev.high} high`} accent="#f97316" />
          <StatCard label="Controls owned" value={teamControls.length} icon={<Target className="h-4 w-4" />} hint={`${counts.compliant} compliant`} accent="#22c55e" />
          <StatCard label="Non-compliant" value={counts.non_compliant} icon={<ShieldAlert className="h-4 w-4" />} hint="Require remediation" accent="#ef4444" />
          <StatCard label="At risk" value={counts.at_risk} icon={<ShieldAlert className="h-4 w-4" />} hint="Evidence/freshness gaps" accent="#f59e0b" />
        </div>
      </div>

      {/* AI team summary */}
      <AISummary title="AI Team Summary" headline={summary.headline}>
        {summary.body}
      </AISummary>

      {/* Controls by category */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <Panel title="Compliance by control area" subtitle="Compliant vs. remaining gap per category">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={byCategory} layout="vertical" margin={{ top: 4, right: 12, left: 8, bottom: 0 }}>
                <CartesianGrid stroke="#1e2a44" horizontal={false} />
                <XAxis type="number" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis type="category" dataKey="category" stroke="#94a3b8" fontSize={11} width={96} tickLine={false} axisLine={false} />
                <Tooltip content={<ChartTooltip />} cursor={{ fill: '#ffffff08' }} />
                <Bar dataKey="compliant" stackId="a" fill="#22c55e" radius={[4, 0, 0, 4]} name="Compliant" />
                <Bar dataKey="gap" stackId="a" fill="#ef4444" radius={[0, 4, 4, 0]} name="Gap" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Team open items" subtitle="What this pod needs to close, by priority">
          <div className="max-h-64 space-y-2 overflow-y-auto pr-1">
            {teamItems.filter((i) => i.status !== 'done').length === 0 && (
              <p className="text-sm text-slate-500">No open items — this pod is clear.</p>
            )}
            {teamItems
              .filter((i) => i.status !== 'done')
              .sort((a, b) => daysUntil(a.dueDate) - daysUntil(b.dueDate))
              .map((o) => (
                <div key={o.id} className="rounded-xl border border-line bg-ink-850 p-3">
                  <div className="flex items-center gap-2">
                    <SeverityBadge severity={o.severity} />
                    <span className="font-mono text-[11px] text-slate-500">{o.id}</span>
                    <span className="ml-auto text-[11px] text-slate-500">{formatDate(o.dueDate)}</span>
                  </div>
                  <div className="mt-1.5 text-sm text-slate-100">{o.title}</div>
                  <div className="mt-1 flex items-center gap-2">
                    <TaskStatusBadge status={o.status} />
                    <span className="text-[11px] text-slate-500">{o.frameworkId} · {o.controlCode}</span>
                  </div>
                </div>
              ))}
          </div>
        </Panel>
      </div>

      {/* Owned controls table */}
      <Panel title="Controls owned by this team" subtitle={`${teamControls.length} controls mapped to ${team.name}`}>
        <div className="max-h-80 overflow-y-auto">
          <table className="w-full text-left text-sm">
            <thead className="sticky top-0 bg-ink-900 text-xs uppercase tracking-wider text-slate-500">
              <tr>
                <th className="px-3 py-2 font-medium">Control</th>
                <th className="px-3 py-2 font-medium">Category</th>
                <th className="px-3 py-2 font-medium">Framework</th>
                <th className="px-3 py-2 font-medium">Status</th>
                <th className="hidden px-3 py-2 font-medium sm:table-cell">Evidence</th>
              </tr>
            </thead>
            <tbody>
              {teamControls.slice(0, 40).map((c) => (
                <tr key={c.id} className="border-t border-line/60 hover:bg-ink-850/60">
                  <td className="px-3 py-2">
                    <span className="font-mono text-xs text-slate-400">{c.code}</span>
                    <div className="text-slate-200">{c.title}</div>
                  </td>
                  <td className="px-3 py-2 text-slate-400">{c.category}</td>
                  <td className="px-3 py-2 text-slate-400">{c.frameworkId}</td>
                  <td className="px-3 py-2"><ControlStatusBadge status={c.status} /></td>
                  <td className="hidden px-3 py-2 capitalize text-slate-400 sm:table-cell">{c.evidence}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Panel>
    </div>
  )
}
