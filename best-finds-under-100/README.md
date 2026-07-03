# 💸 Best Finds Under $100 — Faceless AI Content Engine

A complete, deployable web app that runs a faceless short-form content business
around affordable product finds (under $100) for **TikTok** and **YouTube Shorts**,
with optional Pinterest support.

**Built audience-first and monetization-ready:** it needs **zero** affiliate
accounts, API keys, or payment setup to work. Every product is stored as a
*concept + search term* (not a URL), so the moment you're approved for Amazon
Associates, TikTok Shop, or land a brand deal, you plug the links in — nothing
is blocked while you wait.

## What this app does

| Module | What it gives you |
|---|---|
| **Dashboard** | Totals for products, scripts, captions, prompts, calendar items; top categories; recent scripts; API status; today's automation checklist; latest report; one-click automation buttons |
| **Product Idea Engine** | Generates under-$100 product ideas with price range, audience, problem solved, video angle, and 7 scores (viral, visual, giftability, impulse, TikTok, YouTube, overall) |
| **Link Manager** | Placeholder search links today; fields for manual, affiliate, sponsored, and digital-product links later; `monetization_status` tracking; automatic disclosure switching |
| **TikTok Script Generator** | 5 hooks, voiceover, on-screen text, shot list, caption, hashtags, CTA, length, background style, AI prompts, disclosure |
| **YouTube Shorts Generator** | Title, hook, voiceover, on-screen text, shot list, description, hashtags, pinned comment, CTA, length, disclosure |
| **Video Prompt Generator** | Product/background/b-roll/thumbnail prompts, cover text, editing style, music, pacing, CapCut + Canva notes — for Runway, Pika, Kling, etc. |
| **Content Calendar** | 7-day and 30-day plans across TikTok / YouTube Shorts (+ optional Pinterest) with per-item status workflow |
| **Automation Engine** | One-click daily pipeline: 10 ideas → score → top 5 → 5 TikTok + 5 Shorts scripts → prompts → captions → 7-day calendar → daily report |
| **Daily Report** | New content, top opportunities, missing keys, monetization readiness, recommended next actions |
| **Public Link Hub** | Your future link-in-bio page: featured finds, category sections, platform links, disclosure page. Works with search links today |
| **Admin Area** | Full CRUD on products, links, scripts, prompts, calendar, settings |

## Run it in Replit

1. Create a new Repl → **Import from GitHub** (or upload this `best-finds-under-100/` folder
   as its own Repl — it is fully self-contained).
2. Replit reads `.replit` and runs `python main.py` automatically. If asked for an
   install step: `pip install -r requirements.txt`.
3. Click **Run**. The app seeds itself with demo data on first launch and serves:
   - Admin: `/` (dashboard)
   - Public link hub: `/hub`

Run locally instead:

```bash
cd best-finds-under-100
pip install -r requirements.txt
python main.py     # → http://localhost:5000
```

## Run it without Replit (e.g. PythonAnywhere — works from an iPad)

The app is a plain Flask app; Replit is optional. PythonAnywhere's free tier is a
good fit: browser-only setup, persistent SQLite storage, a public URL, and one
free daily scheduled task for the automation.

1. Sign up at pythonanywhere.com (free "Beginner" plan).
2. Open **Consoles → Bash** and run:
   ```bash
   git clone https://github.com/flohouse-cmyk/flohouse-cmyk.github.io.git
   cd flohouse-cmyk.github.io
   git checkout claude/best-finds-content-engine-5eksi5   # until merged to main
   pip install --user -r best-finds-under-100/requirements.txt
   ```
3. **Web tab → Add a new web app → Manual configuration → Python 3.11** (any 3.10+).
4. Open the WSGI configuration file it shows you, delete its contents, and paste
   (replace YOUR_USERNAME):
   ```python
   import sys
   sys.path.insert(0, '/home/YOUR_USERNAME/flohouse-cmyk.github.io/best-finds-under-100')
   from wsgi import application
   ```
5. Optional: in the Web tab, set an environment variable `SECRET_KEY` to any random
   string. Hit **Reload** — your app is live at `https://YOUR_USERNAME.pythonanywhere.com`
   (admin at `/`, public link hub at `/hub`).
6. **Tasks tab** → add a daily task:
   ```bash
   python3 /home/YOUR_USERNAME/flohouse-cmyk.github.io/best-finds-under-100/run_automation.py
   ```
7. To update later, open a Bash console and `git pull`, then Reload the web app.

Any other host with a persistent disk works the same way via `wsgi.py`
(`gunicorn wsgi:application`). Avoid free tiers with ephemeral filesystems
(e.g. Render free) — the SQLite database would reset on every restart.

## Demo mode (default)

With no API keys, the app runs in **demo mode** (badge in the header):

- All generation uses built-in original template pools — scripts, hooks, captions,
  hashtags, prompts, calendars, and reports all work.
- First launch seeds: 25 product ideas, 10 TikTok scripts, 10 Shorts scripts,
  10 video prompts, a 7-day calendar, 1 daily report, and placeholder search links.
- Nothing is ever blocked because a key is missing.

## Adding API keys later

Add keys as **Replit Secrets** (Tools → Secrets) or in a local `.env`
(copy `.env.example`). All keys are optional:

| Key | What it unlocks |
|---|---|
| `OPENAI_API_KEY` | AI-written voiceovers (also `pip install openai`). Any AI failure falls back to templates |
| `AMAZON_ASSOCIATE_TAG` | Amazon search links automatically include your tag |
| `TIKTOK_ACCESS_TOKEN` | Stored + shown as connected; for future TikTok API posting |
| `YOUTUBE_API_KEY` / `YOUTUBE_CLIENT_ID` / `YOUTUBE_CLIENT_SECRET` | For future YouTube upload integration |
| `PINTEREST_ACCESS_TOKEN` | For future Pinterest pin creation |

### Adding Amazon Associates later
1. Get approved at affiliate-program.amazon.com.
2. Add `AMAZON_ASSOCIATE_TAG` as a secret — new Amazon search links include your tag.
3. For specific products: **Links → Edit** → paste your SiteStripe/affiliate URL into
   *Future affiliate link* and set status to **Affiliate link added**. The affiliate
   disclosure switches on automatically for that product's content and the hub.

### Adding TikTok Shop links later
Once you have TikTok Shop Affiliate access, paste each product's TikTok Shop link
into the link manager (*Future affiliate link*, platform: "TikTok Shop") and set
the status to **Affiliate link added**.

### Connecting YouTube later
Create a Google Cloud project, enable the YouTube Data API, and add the three
`YOUTUBE_*` secrets. Today the app tracks connection status; auto-upload is a
future integration (see "What the app cannot automate yet").

## Daily automation

**Manual:** Dashboard → **Run Daily Automation** (or any individual button).

**Scheduled (Replit Scheduled Deployments):**
1. Deploy → **Scheduled Deployment**.
2. Command: `python run_automation.py`
3. Schedule: once daily (e.g. every day at 7:00 AM).

The script runs the full pipeline headlessly and prints a JSON summary.
Note: point the scheduled deployment at the same persistent storage/Repl so it
shares `bestfinds.db` with the web app.

## What manual setup is still required

- Create the TikTok / YouTube (and optional Pinterest) accounts and set your
  handles in **Settings**.
- Record/assemble and post the videos yourself (CapCut/Canva/Runway etc.) using the
  generated scripts + prompts — then mark calendar items **Posted**.
- Apply for monetization programs when eligible (YouTube Partner Program,
  TikTok Creator Rewards, Amazon Associates, TikTok Shop Affiliate).
- Put your deployed `/hub` URL in your TikTok/YouTube bios.

## What the app cannot automate yet

- **Posting videos** — TikTok/YouTube/Pinterest upload APIs need approved developer
  apps and OAuth; the keys are supported but no auto-posting is wired up yet.
- **Rendering videos** — it generates scripts and AI-tool prompts, not final MP4s.
- **Analytics ingestion** — views/followers aren't pulled automatically yet.
- **Affiliate link creation** — links must be pasted manually once approved.

## Safety & compliance (baked in)

No guaranteed-earnings or fake-review claims; no "I tested this" unless actually
tested; no copied retailer descriptions; no scraping restricted sites; no
copyrighted characters, celebrity likenesses, or brand logos in prompts; no
medical/financial/safety claims; "prices and availability may change" everywhere;
affiliate disclosure only when affiliate links are actually used.

## Project structure

```
best-finds-under-100/
├── main.py              # Replit entrypoint
├── app.py               # Flask app + all routes (admin + public hub)
├── config.py            # env vars, categories, statuses, compliance copy
├── db.py                # SQLite schema + helpers (9 tables)
├── content_data.py      # original product concept pools & template banks
├── generators.py        # idea/script/prompt generators (+ optional OpenAI)
├── automation.py        # calendar, daily pipeline, reports
├── seed.py              # demo-mode seeding on first run
├── run_automation.py    # headless daily run for Scheduled Deployments
├── templates/           # Jinja templates (admin + hub)
├── static/              # style.css, app.js
├── requirements.txt
├── .env.example
└── .replit
```

Database tables: `product_ideas`, `monetization_links`, `tiktok_scripts`,
`youtube_scripts`, `video_prompts`, `content_calendar`, `automation_runs`,
`reports`, `settings`.
