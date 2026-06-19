import type { ControlStatus, Severity, TaskStatus } from '../data/types'

export const statusMeta: Record<ControlStatus, { label: string; color: string; dot: string }> = {
  compliant: { label: 'Compliant', color: 'text-emerald-300', dot: '#22c55e' },
  at_risk: { label: 'At risk', color: 'text-amber-300', dot: '#f59e0b' },
  non_compliant: { label: 'Non-compliant', color: 'text-red-300', dot: '#ef4444' },
  not_applicable: { label: 'N/A', color: 'text-slate-400', dot: '#475569' },
}

export const severityMeta: Record<Severity, { label: string; color: string; bg: string; dot: string }> = {
  critical: { label: 'Critical', color: 'text-red-200', bg: 'bg-red-500/15 border-red-500/30', dot: '#ef4444' },
  high: { label: 'High', color: 'text-orange-200', bg: 'bg-orange-500/15 border-orange-500/30', dot: '#f97316' },
  medium: { label: 'Medium', color: 'text-amber-200', bg: 'bg-amber-500/15 border-amber-500/30', dot: '#f59e0b' },
  low: { label: 'Low', color: 'text-sky-200', bg: 'bg-sky-500/15 border-sky-500/30', dot: '#38bdf8' },
}

export const taskStatusMeta: Record<TaskStatus, { label: string; color: string }> = {
  not_started: { label: 'Not started', color: 'bg-slate-500/20 text-slate-300 border-slate-500/30' },
  in_progress: { label: 'In progress', color: 'bg-sky-500/15 text-sky-300 border-sky-500/30' },
  in_review: { label: 'In review', color: 'bg-violet-500/15 text-violet-300 border-violet-500/30' },
  blocked: { label: 'Blocked', color: 'bg-red-500/15 text-red-300 border-red-500/30' },
  done: { label: 'Done', color: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30' },
}

/** Color ramp for posture scores. */
export function scoreColor(score: number): string {
  if (score >= 90) return '#22c55e'
  if (score >= 80) return '#84cc16'
  if (score >= 70) return '#f59e0b'
  if (score >= 60) return '#f97316'
  return '#ef4444'
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

export function dueLabel(days: number): { text: string; tone: 'crit' | 'warn' | 'ok' } {
  if (days < 0) return { text: `${Math.abs(days)}d overdue`, tone: 'crit' }
  if (days === 0) return { text: 'Due today', tone: 'crit' }
  if (days <= 7) return { text: `Due in ${days}d`, tone: 'warn' }
  return { text: `Due in ${days}d`, tone: 'ok' }
}
