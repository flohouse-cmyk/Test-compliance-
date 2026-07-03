# Hart & Co. HR Advisory — Website Handoff

Everything is in a **single file**: `index.html`. Images, fonts, styles, and
scripts are all included, so there are no other files to manage.

You can open it right now by double-clicking `index.html` — it works offline.

---

## How to publish it (pick one)

### Option A — Netlify Drop (easiest, free, ~1 minute) ✅ recommended
1. Go to **https://app.netlify.com/drop**
2. Drag `index.html` (or the folder it's in) onto the page.
3. You instantly get a live URL like `https://your-site.netlify.app`.
4. (Optional) Create a free Netlify account to keep it, rename it, or connect
   your own domain (e.g. `hartco-hr.com`) under **Site settings → Domain**.

### Option B — Your existing website host
If you already have a domain/hosting (GoDaddy, Bluehost, Squarespace hosting,
cPanel, etc.), upload `index.html` as the site's home page (usually the
`public_html` or `www` folder). Your host's support can do this in minutes.

### Option C — Vercel
Go to **https://vercel.com**, create a project, and drag the file in — similar
to Netlify.

### Option D — GitHub Pages
Create a repo, add `index.html`, then enable **Settings → Pages**.

---

## Before it goes live — quick things to update
Open `index.html` in any text editor and search/replace:
- **Email:** `hello@hartco-hr.com` → the real address
- **LinkedIn:** the `https://www.linkedin.com` links → the real profile URL
- **Photos:** the hero and portrait are professional stock placeholders — swap
  for real photos when available (or leave as-is).
- **Contact form / booking:** the buttons currently open an email. To collect
  submissions on a form instead, a developer can connect it to a free service
  like Formspree in a few minutes.

That's it — one file, drag it to Netlify, and it's live.
