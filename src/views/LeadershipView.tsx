import {
  Area,
  AreaChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  BarChart,
  Bar,
} from 'recharts'
import { ShieldCheck, TriangleAlert, Clock, FileCheck2, ArrowUpRight } from 'lucide-react'
import StatCard from '../components/StatCard'
import Panel from '../components/Panel'
import AISummary from '../components/AISummary'
import ScoreGauge from '../components/ScoreGauge'
import { SeverityBadge } from '../components/badges'
import {
  orgScore,
  postureTrend,
  frameworkReadiness,
  statusCounts,
  openOpenItems,
  severityCount,
  overdueOrSoon,
  daysUntil,
} from '../data/metrics'
import { frameworks } from '../data/frameworks'
import { controls as allControls } from '../data/controls'
import { leadershipSummary } from '../data/aiInsights'
import { scoreColor, formatDate } from '../lib/ui'
import { Link } from 'react-router-dom'

const counts = statusCounts(allControls)
const sev = severityCount(openOpenItems)
const readiness = frameworkReadiness()

const donutData = [
  { name: 'Compliant', value: counts.compliant, color: '#22c55e' },
  { name: 'At risk', value: counts.at_risk, color: '#f59e0b' },
  { name: 'Non-compliant', value: counts.non_compliant, color: '#ef4444' },
  { name: 'N/A', value: counts.not_applicable, color: '#475569' },
]

const upcomingAudits = [...frameworks]
  .sort((a, b) => +new Date(a.nextAuditDate) - +new Date(b.nextAuditDate))
  .slice(0, 4)

function ChartTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-lg border border-line bg-ink-850 px-3 py-2 text-xs shadow-xl">
      {label && <div className="mb-1 font-medium text-slate-200">{label}</div>}
      {payload.map((p: any) => (
        <div key={p.name} className="flex items-center gap-2 text-slate-300">
          <span className="h-2 w-2 rounded-full" style={{ background: p.color || p.fill }} />
          {p.name}: <span className="font-mono text-slate-100">{p.value}{p.unit ?? ''}</span>
        </div>
      ))}
    </div>
  )
}

export default function LeadershipView() {
  return (
    <div className="space-y-5">
      {/* KPI row */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard
          label="Org posture"
          value={`${orgScore}%`}
          delta={{ value: '+9 pts QoQ', positive: true }}
          icon={<ShieldCheck className="h-4 w-4" />}
          hint="Target 95% by Q4"
          accent="#22c55e"
        />
        <StatCard
          label="Open findings"
          value={openOpenItems.length}
          delta={{ value: '-6 this month', positive: true }}
          icon={<TriangleAlert className="h-4 w-4" />}
          hint={`${sev.critical} critical · ${sev.high} high`}
          accent="#f97316"
        />
        <StatCard
          label="Due ≤ 14 days"
          value={overdueOrSoon.length}
          icon={<Clock className="h-4 w-4" />}
          hint="Across all pods"
          accent="#f59e0b"
        />
        <StatCard
          label="Audit-ready frameworks"
          value={`${readiness.filter((r) => r.score >= 90).length}/${frameworks.length}`}
          icon={<FileCheck2 className="h-4 w-4" />}
          hint="Scoring ≥ 90%"
          accent="#38bdf8"
        />
      </div>

      {/* AI executive summary */}
      <AISummary
        title="AI Executive Summary"
        headline={leadershipSummary.headline}
        bullets={leadershipSummary.bullets}
      >
        {leadershipSummary.body}
      </AISummary>

      {/* Trend + gauge */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <Panel
          title="Posture trend"
          subtitle="Org compliance score vs. target — trailing 12 months"
          className="lg:col-span-2"
        >
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={postureTrend} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="scoreFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#22c55e" stopOpacity={0.35} />
                    <stop offset="100%" stopColor="#22c55e" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="#1e2a44" vertical={false} />
                <XAxis dataKey="month" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis domain={[60, 100]} stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip content={<ChartTooltip />} />
                <Area type="monotone" dataKey="target" stroke="#475569" strokeDasharray="4 4" fill="none" strokeWidth={1.5} name="Target" />
                <Area type="monotone" dataKey="score" stroke="#22c55e" strokeWidth={2.5} fill="url(#scoreFill)" name="Score" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Control health" subtitle={`${allControls.length} controls in scope`}>
          <div className="flex flex-col items-center">
            <div className="h-48 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={donutData} dataKey="value" innerRadius={52} outerRadius={78} paddingAngle={2} stroke="none">
                    {donutData.map((d) => (
                      <Cell key={d.name} fill={d.color} />
                    ))}
                  </Pie>
                  <Tooltip content={<ChartTooltip />} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-2 grid w-full grid-cols-2 gap-2">
              {donutData.map((d) => (
                <div key={d.name} className="flex items-center gap-2 text-xs text-slate-400">
                  <span className="h-2.5 w-2.5 rounded-sm" style={{ background: d.color }} />
                  {d.name} <span className="ml-auto font-mono text-slate-200">{d.value}</span>
                </div>
              ))}
            </div>
          </div>
        </Panel>
      </div>

      {/* Framework readiness + audits */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <Panel title="Framework readiness" subtitle="Posture score by framework vs. 95% target" className="lg:col-span-2">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={readiness.map((r) => ({ name: r.frameworkId, score: r.score, target: r.target }))} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                <CartesianGrid stroke="#1e2a44" vertical={false} />
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis domain={[0, 100]} stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip content={<ChartTooltip />} cursor={{ fill: '#ffffff08' }} />
                <Bar dataKey="score" radius={[6, 6, 0, 0]} name="Score">
                  {readiness.map((r) => (
                    <Cell key={r.frameworkId} fill={scoreColor(r.score)} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Upcoming audits" subtitle="Next external & internal assessments">
          <ul className="space-y-3">
            {upcomingAudits.map((fw) => {
              const d = daysUntil(fw.nextAuditDate)
              return (
                <li key={fw.id} className="flex items-center gap-3 rounded-xl border border-line bg-ink-850 p-3">
                  <ScoreGauge score={readiness.find((r) => r.frameworkId === fw.id)!.score} size={52} />
                  <div className="min-w-0 flex-1">
                    <div className="truncate text-sm font-medium text-slate-100">{fw.name}</div>
                    <div className="text-xs text-slate-500">{fw.auditType}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs font-medium text-slate-200">{formatDate(fw.nextAuditDate)}</div>
                    <div className={`text-[11px] ${d <= 45 ? 'text-amber-400' : 'text-slate-500'}`}>in {d}d</div>
                  </div>
                </li>
              )
            })}
          </ul>
        </Panel>
      </div>

      {/* Top risks */}
      <Panel
        title="Top organizational risks"
        subtitle="Highest-severity open findings driving audit exposure"
        action={
          <Link to="/delivery" className="inline-flex items-center gap-1 text-xs font-medium text-brand-400 hover:text-brand-300 cursor-pointer">
            View all open items <ArrowUpRight className="h-3.5 w-3.5" />
          </Link>
        }
      >
        <div className="space-y-2">
          {openOpenItems
            .filter((o) => o.severity === 'critical' || o.severity === 'high')
            .sort((a, b) => daysUntil(a.dueDate) - daysUntil(b.dueDate))
            .slice(0, 5)
            .map((o) => (
              <div key={o.id} className="flex items-center gap-3 rounded-xl border border-line bg-ink-850 px-3 py-2.5">
                <SeverityBadge severity={o.severity} />
                <div className="min-w-0 flex-1">
                  <div className="truncate text-sm text-slate-100">{o.title}</div>
                  <div className="text-xs text-slate-500">
                    {o.frameworkId} · {o.controlCode} · {o.owner}
                  </div>
                </div>
                <div className="hidden text-right sm:block">
                  <div className="text-xs text-slate-400">{formatDate(o.dueDate)}</div>
                  <div className={`text-[11px] ${daysUntil(o.dueDate) <= 7 ? 'text-red-400' : 'text-slate-500'}`}>
                    {daysUntil(o.dueDate) < 0 ? `${Math.abs(daysUntil(o.dueDate))}d overdue` : `in ${daysUntil(o.dueDate)}d`}
                  </div>
                </div>
              </div>
            ))}
        </div>
      </Panel>
    </div>
  )
}
