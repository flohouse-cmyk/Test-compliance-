import type { Control, ControlStatus, EvidenceStatus, FrameworkId } from './types'
import { frameworks, teams } from './frameworks'

/** Small seeded PRNG (mulberry32) so the dataset is stable across reloads. */
function mulberry32(seed: number) {
  return function () {
    seed |= 0
    seed = (seed + 0x6d2b79f5) | 0
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

const categoriesByFramework: Record<FrameworkId, string[]> = {
  SOC2: ['Access Control', 'Change Management', 'Monitoring', 'Risk Mgmt', 'Vendor Mgmt', 'Availability'],
  ISO27001: ['Org Controls', 'People Controls', 'Physical', 'Technological', 'Cryptography', 'Supplier'],
  GDPR: ['Lawful Basis', 'Data Subject Rights', 'Records of Processing', 'Breach Response', 'DPIA'],
  HIPAA: ['Administrative', 'Physical Safeguards', 'Technical Safeguards', 'Breach Notification'],
  PCI: ['Network Security', 'CHD Protection', 'Vuln Mgmt', 'Access Control', 'Monitoring & Test'],
}

const titleVerbs = [
  'Enforce', 'Document', 'Review', 'Encrypt', 'Monitor', 'Restrict', 'Log',
  'Validate', 'Rotate', 'Segregate', 'Audit', 'Backup', 'Classify', 'Patch',
]
const titleNouns = [
  'production access', 'data at rest', 'admin privileges', 'audit logs',
  'encryption keys', 'change approvals', 'vendor risk reviews', 'backup integrity',
  'MFA enrollment', 'network segmentation', 'incident playbooks', 'data retention',
  'vulnerability scans', 'access recertification', 'security awareness training',
]

/** Target distribution of statuses, weighted toward compliant for a believable mature org. */
function pickStatus(r: number): ControlStatus {
  if (r < 0.7) return 'compliant'
  if (r < 0.85) return 'at_risk'
  if (r < 0.94) return 'non_compliant'
  return 'not_applicable'
}

function pickEvidence(status: ControlStatus, r: number): EvidenceStatus {
  if (status === 'compliant') return r < 0.85 ? 'collected' : 'partial'
  if (status === 'at_risk') return r < 0.5 ? 'partial' : 'expired'
  if (status === 'non_compliant') return r < 0.6 ? 'missing' : 'partial'
  return 'collected'
}

function daysAgo(days: number): string {
  const d = new Date('2026-06-19')
  d.setDate(d.getDate() - days)
  return d.toISOString().slice(0, 10)
}

const teamIds = teams.map((t) => t.id)

function buildControls(): Control[] {
  const rand = mulberry32(20260619)
  const out: Control[] = []

  for (const fw of frameworks) {
    const cats = categoriesByFramework[fw.id]
    for (let i = 0; i < fw.totalControls; i++) {
      const category = cats[Math.floor(rand() * cats.length)]
      const status = pickStatus(rand())
      const evidence = pickEvidence(status, rand())
      const verb = titleVerbs[Math.floor(rand() * titleVerbs.length)]
      const noun = titleNouns[Math.floor(rand() * titleNouns.length)]
      const code = `${fw.id === 'ISO27001' ? 'A' : fw.id.slice(0, 3).toUpperCase()}-${String(i + 1).padStart(3, '0')}`
      out.push({
        id: `${fw.id}-${i}`,
        code,
        frameworkId: fw.id,
        title: `${verb} ${noun}`,
        category,
        status,
        evidence,
        ownerTeamId: teamIds[Math.floor(rand() * teamIds.length)],
        lastReviewed: daysAgo(Math.floor(rand() * 180)),
      })
    }
  }
  return out
}

export const controls: Control[] = buildControls()
