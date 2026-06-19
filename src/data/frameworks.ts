import type { Framework, Team } from './types'

export const frameworks: Framework[] = [
  {
    id: 'SOC2',
    name: 'SOC 2 Type II',
    fullName: 'SOC 2 Type II — Trust Services Criteria',
    description: 'Security, Availability & Confidentiality controls audited over a 12-month window.',
    auditType: 'External attestation (AICPA)',
    nextAuditDate: '2026-09-15',
    totalControls: 64,
  },
  {
    id: 'ISO27001',
    name: 'ISO 27001',
    fullName: 'ISO/IEC 27001:2022 — ISMS',
    description: 'Information Security Management System certification with Annex A controls.',
    auditType: 'Certification (Stage 2 surveillance)',
    nextAuditDate: '2026-11-03',
    totalControls: 93,
  },
  {
    id: 'GDPR',
    name: 'GDPR',
    fullName: 'EU General Data Protection Regulation',
    description: 'Data protection, lawful processing, and data-subject rights for EU residents.',
    auditType: 'Internal DPO assessment',
    nextAuditDate: '2026-07-30',
    totalControls: 41,
  },
  {
    id: 'HIPAA',
    name: 'HIPAA',
    fullName: 'HIPAA Security & Privacy Rule',
    description: 'Safeguards for protected health information (PHI) in the patient-data product.',
    auditType: 'Internal + customer audit',
    nextAuditDate: '2026-08-20',
    totalControls: 38,
  },
  {
    id: 'PCI',
    name: 'PCI DSS 4.0',
    fullName: 'PCI DSS 4.0 — Payment Card Industry',
    description: 'Cardholder data environment controls for the payments platform.',
    auditType: 'QSA assessment (Level 1)',
    nextAuditDate: '2026-10-12',
    totalControls: 51,
  },
]

export const teams: Team[] = [
  { id: 'platform', name: 'Platform & Infra', pod: 'Engineering', lead: 'Marcus Lee', leadInitials: 'ML', headcount: 11 },
  { id: 'payments', name: 'Payments', pod: 'Engineering', lead: 'Priya Nair', leadInitials: 'PN', headcount: 9 },
  { id: 'identity', name: 'Identity & Access', pod: 'Security', lead: 'Sofia Alvarez', leadInitials: 'SA', headcount: 7 },
  { id: 'data', name: 'Data Platform', pod: 'Engineering', lead: 'Tomás Berg', leadInitials: 'TB', headcount: 8 },
  { id: 'clinical', name: 'Clinical Products', pod: 'Product', lead: 'Dr. Aisha Khan', leadInitials: 'AK', headcount: 10 },
  { id: 'corpit', name: 'Corporate IT', pod: 'Operations', lead: 'Derek Owens', leadInitials: 'DO', headcount: 6 },
]

export const frameworkLabel = (id: string) =>
  frameworks.find((f) => f.id === id)?.name ?? id

export const teamLabel = (id: string) => teams.find((t) => t.id === id)?.name ?? id
