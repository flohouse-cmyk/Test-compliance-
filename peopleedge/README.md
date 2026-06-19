# PeopleEdge HR Consulting — Website

A self-contained, single-file marketing website for the PeopleEdge HR
consulting business. **This folder is intentionally isolated** from the
ComplyScope app at the repository root so the two projects never overwrite
each other.

## What's here

- `index.html` — the entire site. No build step, no dependencies to install.
  Tailwind is loaded via CDN and fonts via Google Fonts.

## Sections

Navbar · Hero · Client logos · Services · **Who We Serve** · How It Works ·
Results · Team · Credentials · FAQ · Contact · Footer.

### Who We Serve (audience segments)

| Audience | Description |
|----------|-------------|
| Small-to-mid-size businesses | Companies without in-house HR that need fractional support |
| Chemical / manufacturing companies | Leveraging prior KAI industry experience |
| Government contractors | Needing HR compliance — SDVOSB set-aside eligible |
| Individuals | Job seekers needing career coaching, resume help, or interview prep |
| Companies building intern programs | Need structured onboarding and early career program design |

## Run it

Just open the file in a browser:

```bash
open peopleedge/index.html      # macOS
xdg-open peopleedge/index.html  # Linux
```

Or serve the folder:

```bash
cd peopleedge && python3 -m http.server 8000
# visit http://localhost:8000
```

## Moving it to its own repository

This site is fully standalone. To give it a dedicated repo, copy the
`peopleedge/` folder out and push it anywhere — nothing here depends on the
rest of this repository.
