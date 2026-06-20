# PeopleEdge HR Consulting — Website

A professional, multi-page marketing & client-intake website for **PeopleEdge**,
a veteran-owned (SDVOSB-certified) HR and talent-acquisition consulting practice.

**This folder is intentionally isolated** from the ComplyScope app at the
repository root so the two projects never overwrite each other.

## Built to "Claude Code specs" (adapted from the Lovable PRD)

The original PRD targeted Lovable.dev (React + React Router). This implementation
delivers the same product as a **self-contained, multi-page static site** — no
build step, no framework, Tailwind via CDN. That keeps it:

- **Isolated** from the ComplyScope React/Vite app at the repo root
- **Zero-build & easy to maintain** without a developer (a PRD goal)
- **Instantly previewable** (open a file or use the GitHub HTML-preview proxy)
- **Deployable anywhere** (Netlify/Vercel drag-and-drop, any static host)

## Pages

| File | Page | Highlights |
|------|------|-----------|
| `index.html` | Home | Hero, credibility bar, services snapshot, Who We Serve, About teaser, testimonials, CTA |
| `about.html` | About | Bio, expertise, certifications, SDVOSB/veteran badge |
| `services.html` | Services | Business HR services + à la carte career services, with prices/CTAs |
| `pricing.html` | Pricing | Hourly / project / retainer / contingency + à la carte table |
| `book.html` | Book a Consultation | Scheduling embed placeholder + intake form |
| `contact.html` | Contact | Contact form + info + map placeholder |
| `blog.html` | Resources | Phase 2 placeholder |

Shared design system lives in `assets/styles.css` and `assets/main.js`, so the
nav, footer, buttons, cards, and animations stay consistent across every page.

## Design

- **Palette:** navy `#1B2B4B` · gold `#C8A96E` · cream `#F9F7F4` · near-black `#1A1A1A`
- **Type:** Playfair Display (display) + Inter (body)
- **Motion:** IntersectionObserver scroll-reveal, fully disabled under `prefers-reduced-motion`
- Accessible: labelled forms, focus rings, aria, keyboard-friendly nav

## Things to wire up before launch (placeholders)

1. **Brand name / DBA** — currently "PeopleEdge" (swap throughout if different).
2. **Headshot & hero photo** — Unsplash placeholders; replace the `src` URLs.
3. **Scheduling** — replace the placeholder on `book.html` with your Calendly/Cal.com embed (see the comment in that file's source).
4. **Forms** — point the contact/intake forms at a service like Formspree or Basin for inbox delivery.
5. **Real testimonials, email, LinkedIn URL, location.**

## Run it

```bash
open peopleedge/index.html            # macOS
xdg-open peopleedge/index.html        # Linux
# or serve the folder:
cd peopleedge && python3 -m http.server 8000   # http://localhost:8000
```

## Moving it to its own repository

Fully standalone — copy the `peopleedge/` folder anywhere and it just works.
