# ComplyScope — Compliance Posture Platform

A modern, Datadog-style observability platform for **compliance posture**. It gives
each stakeholder exactly the visibility they need to understand the **current state vs.
the needed future state** across frameworks, teams, and individual findings.

Built as a presentation-ready demo with realistic sample data spanning **5 frameworks**
(SOC 2, ISO 27001, GDPR, HIPAA, PCI DSS) and **6 delivery pods**.

## Three role-based views

| View | Audience | What it answers |
|------|----------|-----------------|
| **Leadership** (`/leadership`) | Org leaders | High-level posture, trend, audit readiness and top risks — no noise. Includes an AI executive summary. |
| **Team Lead** (`/team`) | Pod / team leads | "Where is *my* pod's posture, and where does it need to be?" Score vs. target, control areas, and the team's open items. |
| **PM / Dev** (`/delivery`) | Delivery teams | The detailed work: **what** is being asked, **why** it matters, **who** owns it and **when** it's due — filterable by framework, team, severity and status. |

Plus:

- **Insights** (`/insights`) — AI insight feed and per-framework **audit readiness** (readiness score, evidence freshness, timeline). This is the view designed to present to leadership on posture, audit readiness, and open items.
- **Frameworks** (`/frameworks`) — searchable control inventory across all frameworks.

## AI summaries

Each view surfaces a short, generated-style summary (executive, team, and an insight
feed) framing the data into a narrative: what's improving, what's at risk, and what to
do next. In this demo the summaries are derived deterministically from the live metrics;
the panels are designed to drop in a real LLM call (e.g. the Claude API) without UI
changes.

## Tech stack

- **React 18** + **TypeScript** + **Vite 6**
- **Tailwind CSS v4** (dark observability aesthetic)
- **Recharts** for data visualization
- **lucide-react** icons, **react-router** for the role-based views

## Sample data

All data lives in `src/data/`:

- `frameworks.ts` — frameworks & teams/pods
- `controls.ts` — ~287 controls generated deterministically (seeded) so the dataset is stable across reloads
- `openItems.ts` — hand-authored findings with plain-language *ask* and *why* per item
- `metrics.ts` — posture scoring, trends, readiness selectors
- `aiInsights.ts` — generated-style summaries

## Run it

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # production build
npm run preview  # serve the build
```
