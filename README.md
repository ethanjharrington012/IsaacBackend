# Simplomation — Static Site (GitHub Pages + Tailwind CDN)

A simple, fast landing page for **Simplomation** with:
- Tailwind via CDN (no build step)
- Hero section and features
- Email signup form (Formspree-ready)
- SVG logo
- Works on GitHub Pages out of the box

## Deploy on GitHub Pages

1. Create (or open) your repo. For a *user site* at `ethanjharrington012.github.io`, put these files in the repo root.
2. Commit all files and push to `main`.
3. In GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, then choose `main` and `/ (root)`.
4. Open your Pages URL once GitHub finishes deploying.

## Connect the email form

This project uses a static form that can be wired to **Formspree** (free tier):
1. Go to https://formspree.io/ and create a form. Copy your endpoint (looks like `https://formspree.io/f/xxxxx`).
2. Open `assets/app.js` and paste the endpoint into `FORM_ENDPOINT`.
3. Commit/push; test the form on your Pages URL.

> Until you set an endpoint, the form “submits” to `localStorage` and shows a success message so you can demo the flow.

## Customize

- Colors/gradients and typography are set via Tailwind classes in `index.html`.
- Replace the logo in `assets/logo.svg` once you finalize your mark.
- Update copy in **Features** and **About** sections to match your offers.

---

**Made for Simplomation — “Work less, grow more.”**
