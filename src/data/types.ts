export type FrameworkId = 'SOC2' | 'ISO27001' | 'GDPR' | 'HIPAA' | 'PCI'

export type ControlStatus =
  | 'compliant'
  | 'at_risk'
  | 'non_compliant'
  | 'not_applicable'

export type EvidenceStatus = 'collected' | 'partial' | 'missing' | 'expired'

export type Severity = 'critical' | 'high' | 'medium' | 'low'

export type TaskStatus =
  | 'not_started'
  | 'in_progress'
  | 'in_review'
  | 'blocked'
  | 'done'

export type Role = 'leadership' | 'team_lead' | 'dev'

export interface Framework {
  id: FrameworkId
  name: string
  fullName: string
  description: string
  auditType: string
  nextAuditDate: string
  totalControls: number
}

export interface Team {
  id: string
  name: string
  pod: string
  lead: string
  leadInitials: string
  headcount: number
}

export interface Control {
  id: string
  code: string
  frameworkId: FrameworkId
  title: string
  category: string
  status: ControlStatus
  evidence: EvidenceStatus
  ownerTeamId: string
  lastReviewed: string
}

export interface OpenItem {
  id: string
  title: string
  description: string
  /** Plain-language "what is being asked" for the delivery team */
  ask: string
  /** Why it matters, the risk/impact framing */
  why: string
  frameworkId: FrameworkId
  controlCode: string
  teamId: string
  owner: string
  severity: Severity
  status: TaskStatus
  createdDate: string
  dueDate: string
  effortDays: number
}

export interface PosturePoint {
  /** Month label, e.g. "Jan" */
  month: string
  score: number
  target: number
}

export interface FrameworkReadiness {
  frameworkId: FrameworkId
  score: number
  target: number
  controlsCompliant: number
  controlsTotal: number
  openItems: number
}
