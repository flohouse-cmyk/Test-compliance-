# Portfolio redesign — handoff brief

Read this first, then redesign. The current homepage works but is plain, and the
`/preview/` concept is AI‑slop. Do it properly this time using the installed skills.

## Goal
A genuinely premium, non‑templated personal site for **Folorunsho "Flo" Ogunyemi,
AI Product Manager**. Audience: recruiters and hiring managers. Must read credible
and designed, not gimmicky.

## Use these skills (now installed under .claude/skills)
- **design-taste-frontend** — primary anti‑slop direction + pre‑flight checklist.
- **emil-design-eng** — polish, component detail, animation decisions.
- **ui-ux-pro-max** — palette/type/system grounding.
- **review-animations** — audit motion before shipping.
- Others available: high-end-visual-design, minimalist-ui, redesign-existing-projects,
  imagegen-frontend-web/mobile (use if an image-gen tool is available), brandkit, etc.
- User is also adding the **impeccable** plugin marketplace (`/plugin marketplace add pbakaus/impeccable`).

## What the user reacted well to (references)
- A **cinematic spotlight hero**: a single subject lit by a real lamp with a
  reflection on a glossy floor (the "flamingo" reel), heavy vignette.
- **Glassmorphism + gradients**, premium/editorial layouts.

## What to AVOID (the current /preview/ failed on all of these)
- AI‑blue/purple glow everywhere (the "Lila rule"). Pick a real accent, lock it.
- Centered hero over a dark mesh as the default. Consider asymmetric/editorial.
- Gradient / liquid‑chrome headline text. Hand‑rolled SVG gimmicks.
- Glass on everything. Em‑dashes anywhere (banned). Decorative dots, eyebrows on
  every section, scroll cues, fake captions.
- Run the design-taste-frontend Pre‑Flight Check before shipping.

## Assets already in repo (public/portfolio/assets/)
- `flo.jpg` — original headshot.
- `flo-cutout.png` — background‑removed cut‑out of Flo (clean subject for a spotlight).
- `og.jpg` — link‑preview card.
- If an image‑generation tool is available, generate real section imagery.

## Content (reuse, do not invent)
Pull copy from the existing pages:
- Home: `public/portfolio/index.html` (name, role, about, experience, skills).
- Résumé: `public/portfolio/resume.html` (word‑for‑word from the user's PDF).
- Projects (4): **ComplyScope** (live demo at /complyscope/), **Voice AI**,
  **AI Chat**, **AI Trading Bot** (+ demo dashboard at /preview path or projects/trading-dashboard.html).

## Confidentiality rules (keep)
- Voice AI and AI Chat **project pages/cards must NOT tag "Judi Health"**.
- The résumé and the Experience timeline DO keep Judi Health (it's the user's history).
- No proprietary data/screenshots; the AI projects are generalized; trading bot is a personal build with sample‑data demo only.

## HOSTING — do not break this (important)
GitHub Pages serves this repo in **branch mode** from the default branch root with
`.nojekyll`. The site is published as **committed built files at the repo root**.
- ComplyScope (Vite app) entry is **`index.vite.html`** (not `index.html`).
- Build: `npm run build` (runs tsc + vite build + `scripts/reorg-pages.mjs`, output in `dist/`:
  portfolio at dist root, ComplyScope at `dist/complyscope/`, plus `dist/preview/`).
- Publish: `cp -r dist/. .` at repo root, then commit. That updates the live site.
- `.github/workflows/deploy.yml` is **manual‑only** on purpose (its configure-pages
  step used to reset the Pages source and break the site). Do NOT re‑add
  `actions/configure-pages` enablement or re‑enable auto deploy.

## Suggested process
1. Redesign on **/preview/** first (public/portfolio/preview/index.html). Get the
   user's sign‑off.
2. Then apply to the real homepage (public/portfolio/index.html + sections),
   rebuild, `cp -r dist/. .`, commit. Keep résumé + 4 project case studies working.
3. Run review-animations + the design-taste Pre‑Flight before declaring done.
