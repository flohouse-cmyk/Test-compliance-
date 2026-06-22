# Folorunsho “Flo” Ogunyemi — Portfolio

A premium digital résumé & portfolio for **Folorunsho “Flo” Ogunyemi**, AI Product Manager.

Bright, vibrant "Aurora" design — intentionally its own universe, separate from the
projects it links out to (each project keeps its own look & feel).

## Structure

```
.
├── index.html               # Home — hero, about, experience, skills, projects, contact
├── resume.html              # Digital, print-to-PDF résumé
├── projects/
│   └── complyscope.html     # ComplyScope case study + live demo embed
└── assets/
    └── flo.jpg              # Profile photo
```

No build step — pure HTML + Tailwind (CDN) + Google Fonts. Just open `index.html`.

## Deploy (GitHub Pages)

1. Push these files to a repo.
2. **Settings → Pages → Build and deployment → Deploy from a branch**, pick the branch and `/ (root)`.
3. Site goes live at `https://<user>.github.io/<repo>/`.

## Adding a new project ("universe")

1. Copy `projects/complyscope.html` to `projects/<your-project>.html` and edit the content.
2. Add a card for it in the **Projects** section of `index.html` (duplicate the ComplyScope card).
3. Point its links at the project's live demo / repo.

## Customize

- **Photo:** replace `assets/flo.jpg` (portrait, ~900px wide works well).
- **Colors:** the gradient is defined once as `--grad` in each file's `<style>`.
- **Content:** all copy is inline in the HTML, clearly sectioned.
