import type {
  Control,
  FrameworkId,
  FrameworkReadiness,
  OpenItem,
  PosturePoint,
  Severity,
} from './types'
import { controls } from './controls'
import { openItems } from './openItems'
import { frameworks } from './frameworks'

/** Posture score = compliant / (total - not_applicable), expressed 0–100. */
export function scoreFor(set: Control[]): number {
  const inScope = set.filter((c) => c.status !== 'not_applicable')
  if (inScope.length === 0) return 100
  const compliant = inScope.filter((c) => c.status === 'compliant').length
  // At-risk controls count as half credit, they are passing today but trending down.
  const atRisk = inScope.filter((c) => c.status === 'at_risk').length
  return Math.round(((compliant + atRisk * 0.5) / inScope.length) * 100)
}

export function statusCounts(set: Control[]) {
  return {
    compliant: set.filter((c) => c.status === 'compliant').length,
    at_risk: set.filter((c) => c.status === 'at_risk').length,
    non_compliant: set.filter((c) => c.status === 'non_compliant').length,
    not_applicable: set.filter((c) => c.status === 'not_applicable').length,
  }
}

export const orgScore = scoreFor(controls)

export function frameworkReadiness(): FrameworkReadiness[] {
  return frameworks.map((fw) => {
    const set = controls.filter((c) => c.frameworkId === fw.id)
    const inScope = set.filter((c) => c.status !== 'not_applicable')
    const compliant = set.filter((c) => c.status === 'compliant').length
    return {
      frameworkId: fw.id,
      score: scoreFor(set),
      target: 95,
      controlsCompliant: compliant,
      controlsTotal: inScope.length,
      openItems: openItems.filter((o) => o.frameworkId === fw.id && o.status !== 'done').length,
    }
  })
}

export function controlsForTeam(teamId: string) {
  return controls.filter((c) => c.ownerTeamId === teamId)
}

export function teamScore(teamId: string) {
  return scoreFor(controlsForTeam(teamId))
}

export function openItemsForTeam(teamId: string) {
  return openItems.filter((o) => o.teamId === teamId)
}

export const openOpenItems = openItems.filter((o) => o.status !== 'done')

export function severityCount(items: OpenItem[]): Record<Severity, number> {
  return {
    critical: items.filter((i) => i.severity === 'critical').length,
    high: items.filter((i) => i.severity === 'high').length,
    medium: items.filter((i) => i.severity === 'medium').length,
    low: items.filter((i) => i.severity === 'low').length,
  }
}

export function daysUntil(dateStr: string): number {
  const today = new Date('2026-06-19')
  const due = new Date(dateStr)
  return Math.round((due.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
}

export const overdueOrSoon = openOpenItems.filter((o) => daysUntil(o.dueDate) <= 14)

/** 12-month posture trend, climbing toward target with realistic noise. */
export const postureTrend: PosturePoint[] = [
  { month: 'Jul', score: 71, target: 90 },
  { month: 'Aug', score: 73, target: 90 },
  { month: 'Sep', score: 72, target: 90 },
  { month: 'Oct', score: 76, target: 92 },
  { month: 'Nov', score: 78, target: 92 },
  { month: 'Dec', score: 77, target: 92 },
  { month: 'Jan', score: 80, target: 93 },
  { month: 'Feb', score: 82, target: 93 },
  { month: 'Mar', score: 81, target: 94 },
  { month: 'Apr', score: 84, target: 94 },
  { month: 'May', score: 86, target: 95 },
  { month: 'Jun', score: orgScore, target: 95 },
]

/** Per-team posture vs. their target, for the leadership comparison + team view. */
export const teamTargets: Record<string, number> = {
  platform: 92,
  payments: 95,
  identity: 95,
  data: 90,
  clinical: 93,
  corpit: 88,
}

export function frameworkOpenItems(id: FrameworkId) {
  return openItems.filter((o) => o.frameworkId === id && o.status !== 'done')
}
