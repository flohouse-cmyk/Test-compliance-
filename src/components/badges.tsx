import type { ControlStatus, Severity, TaskStatus } from '../data/types'
import { severityMeta, statusMeta, taskStatusMeta } from '../lib/ui'

export function SeverityBadge({ severity }: { severity: Severity }) {
  const m = severityMeta[severity]
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border px-2 py-0.5 text-xs font-medium ${m.bg} ${m.color}`}>
      <span className="h-1.5 w-1.5 rounded-full" style={{ background: m.dot }} />
      {m.label}
    </span>
  )
}

export function TaskStatusBadge({ status }: { status: TaskStatus }) {
  const m = taskStatusMeta[status]
  return <span className={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium ${m.color}`}>{m.label}</span>
}

export function ControlStatusBadge({ status }: { status: ControlStatus }) {
  const m = statusMeta[status]
  return (
    <span className={`inline-flex items-center gap-1.5 text-xs font-medium ${m.color}`}>
      <span className="h-2 w-2 rounded-full" style={{ background: m.dot }} />
      {m.label}
    </span>
  )
}
