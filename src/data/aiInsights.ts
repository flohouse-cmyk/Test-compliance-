import {
  orgScore,
  overdueOrSoon,
  openOpenItems,
  severityCount,
  teamScore,
  openItemsForTeam,
  teamTargets,
} from './metrics'
import { teams, frameworks } from './frameworks'

export interface Insight {
  tone: 'positive' | 'warning' | 'critical' | 'neutral'
  text: string
}

const sev = severityCount(openOpenItems)

export const leadershipSummary = {
  headline: `Org posture is ${orgScore}%, up 15 points over 12 months, ${95 - orgScore} short of the board target of 95%.`,
  body: `Momentum is positive and four of five frameworks are audit-ready within tolerance. The risk concentration is in the Cardholder Data Environment: ${sev.critical} critical findings remain open, two of which (segmentation testing and MFA on privileged accounts) gate the PCI Level 1 and SOC 2 attestations this autumn. ${overdueOrSoon.length} items are due within 14 days. With current burn-down, leadership should expect 95% by early Q4 provided the Payments and Identity pods clear their critical items on schedule.`,
  bullets: [
    `${sev.critical} critical + ${sev.high} high findings open across ${frameworks.length} frameworks`,
    `Earliest external audit: GDPR DPO assessment on 30 Jul 2026`,
    `Highest-risk pod: Payments (PCI segmentation test 13 months overdue)`,
  ] as string[],
}

export function teamSummary(teamId: string) {
  const team = teams.find((t) => t.id === teamId)!
  const score = teamScore(teamId)
  const target = teamTargets[teamId] ?? 95
  const items = openItemsForTeam(teamId).filter((o) => o.status !== 'done')
  const s = severityCount(items)
  const gap = target - score
  const trend = gap <= 0 ? 'at or above target' : `${gap} points below the ${target}% target`

  let body: string
  if (s.critical > 0) {
    body = `${team.name} is ${trend}. The priority is the ${s.critical} critical finding${s.critical > 1 ? 's' : ''}, these block an upcoming audit and should be cleared before any lower-severity work. ${items.length} open item${items.length === 1 ? '' : 's'} total; clearing the critical and ${s.high} high item${s.high === 1 ? '' : 's'} would move the pod above target.`
  } else if (gap > 0) {
    body = `${team.name} is ${trend} with no critical findings. ${items.length} open item${items.length === 1 ? '' : 's'} remain, mostly ${s.high} high and ${s.medium} medium severity. Steady burn-down this sprint closes the gap.`
  } else {
    body = `${team.name} is ${trend} and holding. ${items.length} open item${items.length === 1 ? '' : 's'} remain, none critical. Focus shifts to evidence freshness and recertification to keep the score from drifting.`
  }

  return {
    headline: `${team.name} posture: ${score}% vs ${target}% target.`,
    body,
  }
}

export const insightFeed: Insight[] = [
  {
    tone: 'critical',
    text: 'PCI segmentation pen-test is 13 months overdue and blocked on vendor scheduling, this is the single largest threat to the October Level 1 attestation.',
  },
  {
    tone: 'critical',
    text: 'Privileged AWS accounts without hardware MFA (CS-1042) and hardcoded CI secrets (CS-1205) are both critical SOC 2 access-control gaps with overlapping owners on the Platform/Identity pods.',
  },
  {
    tone: 'warning',
    text: `${overdueOrSoon.length} open items fall due within 14 days. Three sit with the Payments pod, which is already the lowest-scoring team relative to its 95% target.`,
  },
  {
    tone: 'positive',
    text: 'Org posture has improved every quarter for the past year (+15 pts). GDPR and ISO 27001 are tracking comfortably ahead of their audit dates.',
  },
  {
    tone: 'neutral',
    text: 'Evidence freshness is the quiet risk: ~15% of compliant controls have partial or expired evidence, which can convert to findings during fieldwork even where the control itself is sound.',
  },
]
