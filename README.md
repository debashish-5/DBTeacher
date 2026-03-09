# TeachLoop — Cinematic Landing (README)

**One-line summary:** a modern, production-minded landing page for an AI-teacher experience — cinematic hero, large right→left headline animation, floating media tiles, marquee text, responsive gallery, and accessibility + performance best practices.

This README describes the design goals, features, tech stack, recommended assets and optimizations, deployment options, and implementation notes (diagrams, UI components, animation patterns, accessibility, testing, and CI). Use it as a single-source spec for a high-quality, responsive marketing page for an AI-teacher product.

---

## Banner / Hero (what the page delivers)

A bold, cinematic hero section that:

* shows a **big right→left headline** that animates in with smooth easing,
* presents a **video / device mockup** in a media stage with floating image tiles,
* includes a **wide marquee** (large words scrolling horizontally),
* has compact CTA buttons (primary / ghost) and quick feature chips,
* displays a subtle particle field and blurred gradient background to create depth.

Design goals: high perceived quality, strong LCP control, graceful fallback for `prefers-reduced-motion`, and keyboard-friendly CTAs.

---

## Key features (short list)

* Large headline animation (right → left) tuned for perception and LCP.
* Floating media stage: main video + small image tiles + ribbon gallery.
* Marquee and short chips for context and motion.
* Responsive, accessible features grid and gallery carousel (keyboard + indicators).
* Performance-minded defaults: `loading="lazy"`, preloaded LCP assets, reduced-motion handling.
* Ready for Retrieval Augmented Generation (RAG) and local model integration.
* Production deployment guidance and performance testing checklist.

---

## Tech stack and recommended services

* Frontend: plain HTML/CSS/JS (can be ported to React + Tailwind).
* Backend (optional): Python + Flask for RAG endpoints and Ollama integration.
* Local LLM server: Ollama — used for on-prem model generation.
* Vector indexing (optional): FAISS or Qdrant.
* Hosting & CDN: Vercel or Netlify for static hosting.
* Source control: GitHub for repo, issues and CI.
* Images & video (credits / placeholders): Unsplash and Pexels (replace with your licensed assets).
* Containerization: Docker (for consistent dev / staging).
* Performance audit: Lighthouse.

> Note: each of the above appears once in this README — replace placeholder names and endpoints with your production values.

---

## Project layout (example)

```
teachloop/
├─ index.html               # single-page cinematic landing
├─ static/
│  ├─ css/styles.css        # theme, animations
│  ├─ js/main.js            # interactions (marquee, carousel, tilt)
│  └─ assets/               # hero.png, hero.webp, hero.avif, hero.mp4, thumbnails
├─ templates/               # if using Flask, teacher pages
├─ vector_db/               # sample small JSON vector DBs
├─ app.py                   # optional Flask backend (RAG + Ollama endpoints)
├─ README.md                # this file
└─ package.json / requirements.txt
```

---

## Diagram (architectural flow)

Use this visual as a quick map of how frontend → backend → vector store → LLM works. You can copy this to a diagram tool.

```
[Browser / Landing Page]
    ├─ Hero video + tiles (static assets via CDN)
    ├─ Marquee & animations (JS + CSS)
    └─ CTA -> /db-teacher, /py-teacher, /all-rounder
         |
         v
[Flask Backend (optional)]
    ├─ /api/query_teacher  -> loads vector_db/json or FAISS/Qdrant
    ├─ /api/ollama_generate -> calls local Ollama for generation
    └─ Authentication / rate limiting (if public)
         |
         v
[Vector store]
    ├─ Local JSON (small demo)
    ├─ FAISS index (fast local retrieval)
    └─ Qdrant (managed vector DB)
         |
         v
[Local Model / Ollama]
    └─ Generate response conditioned on retrieved context
```

---

## UI / design system recommendations

1. **Typography**

   * Use a heavy display face for headline (900 weight), variable size via `clamp()`.
   * Subtext: Inter / system sans with 18px base for reading.

2. **Color system**

   * Primary blurple gradient `--accent` → `--accent-2`.
   * Muted text `--muted` for descriptions.
   * Use subtle glass cards `--glass` for panels, with faint borders.

3. **Spacing & layout**

   * Max layout width ~1200–1400px.
   * Use CSS grid for hero and feature layouts, flex for card rows.
   * Preserve whitespace: big hero needs breathing room.

4. **Animated components**

   * Headline: transform + opacity animation (right → left). Trigger via IntersectionObserver.
   * Tile tilt: mousemove rotates with `transform: rotateX()/rotateY()`; scale on hover.
   * Ribbon: slow horizontal translation animation (loop) for visual motion.
   * Marquee: clone content in JS to create continuous scrolling; pause on hover.

5. **Colorful boxes and content cards**

   * Small blur glass chips with colored left border or accent line.
   * Use gradient backgrounds or subtle duotone images inside cards.

6. **Teacher animation**

   * For the “teacher” avatar / panel: use a responsive small card with:

     * subtle entrance animation (slide + fade),
     * micro-interactions (hover to reveal “examples”),
     * code snippet preview that toggles syntax-highlighted sample.
   * For production, use a lightweight animation library (or CSS + IntersectionObserver).

---

## Accessibility & semantic best practices

* Provide `role="banner"`, `role="main"`, `role="region"` and `aria-label` where appropriate.
* Make interactive elements keyboard focusable and visible (custom focus outline).
* Respect `prefers-reduced-motion`: reduce or disable animations and particle canvas.
* Use meaningful `alt` text for images. Avoid alt="" for decorative images only.
* Provide `aria-live` regions for dynamic content (chat results).
* Ensure color contrast (WCAG AA): check primary text vs background.

---

## Performance checklist (high-impact)

1. Preload LCP image (`<link rel="preload" as="image">`).
2. Serve hero images as WebP/AVIF with `srcset` and `sizes`.
3. Short looped MP4 for hero; keep < 2–4s and use a small bitrate.
4. Defer non-critical JS (load `<script defer>` or inline minimal bootstrap).
5. Lazy-load offscreen images (`loading="lazy"`).
6. Compress static assets and enable Brotli/Gzip on the server/CDN.
7. Use a CDN for heavy media and set long cache headers for immutable files.
8. Run audits with Lighthouse and fix LCP / TBT hotspots.

---

## Security & privacy notes

* Validate all user inputs on the backend; never pass raw user input into shell commands.
* Rate-limit model generation endpoints to prevent abuse.
* If using local LLM (Ollama), keep the service behind a firewall for private data.
* Store API keys and credentials using environment variables (don’t commit to Git).

---

## Production deployment & CI

* Build pipeline:

  * Lint HTML / CSS / JS (prettier / stylelint / eslint).
  * Run unit / integration tests for backend.
  * Bundle static assets (optional).
* Example CI flow (GitHub Actions):

  1. `on: push` run linters and tests.
  2. Build artifacts and deploy to Vercel or Netlify.
  3. Upload static assets to CDN & invalidate cache.
* Use Docker (Docker) for dev parity:

  * `docker build .` -> `docker run -p 5000:5000 teachloop:latest`

---

## RAG & LLM integrations (high level)

* Data pipeline:

  1. Collect docs (markdown, text, PDFs).
  2. Chunk into ~500 token passages, embed with a sentence embedder.
  3. Index into FAISS or Qdrant (Qdrant).
  4. Query: embed user prompt → nearest neighbors → compose prompt for model.
* Backend flow:

  * `/api/query_teacher` — compute embedding, retrieve top-K, return snippets.
  * `/api/ollama_generate` — combine retrieved context + user prompt → send to local model (Ollama).
* Always include provenance: show which snippets were used and their score.

---

## Developer tips (hard words & tech style)

* Use `LCP` (largest contentful paint), `CLS` (cumulative layout shift), and `TBT` (total blocking time) metrics to prioritize perf fixes.
* Prefer `partial hydration` or `islands architecture` if migrating to React to keep interactivity localised.
* For vector search: use HNSW index in FAISS for sub-100ms retrieval at scale.
* Use `batching` for embedding calls and keep a cache layer (Redis) for hot queries.
* Use `content-encoding: br` and set a `stale-while-revalidate` policy for near-immediate content updates.

---

## Testing & QA

* Unit tests for backend (Pytest).
* E2E tests for critical flows (Playwright or Cypress): hero LCP, CTA navigation, chat flow.
* Accessibility tests: `axe-core` integration in CI.
* Performance: Lighthouse via CI on staging with budgets.

---

## Design assets & production checklist

* Replace remote demo images with WebP/AVIF versions sized for 1x, 2x, and 3x screens. Provide `srcset` and `sizes`.
* Generate 2 hero video files: short MP4 H.264 fallback and optimized WebM/AV1 for modern browsers (if possible).
* Provide a “poster” image for hero (LCP-friendly).
* Provide SVG blobs and small icons as inline SVGs (avoid external requests).
* Prepare an assets folder with a manifest and hashed filenames for cache busting.

---

## How to run quickly (dev)

1. Clone the repo.
2. If static-only:

   * `python -m http.server --directory . 8000` and open `http://localhost:8000/index.html`.
3. If using Flask backend:

   * `python -m venv venv && source venv/bin/activate`
   * `pip install -r requirements.txt`
   * `export FLASK_APP=app.py && flask run`
4. Run `Lighthouse` locally and iterate on LCP.

---

## Contribution & style guide

* Branch naming: `feature/<short-descriptor>`, `fix/<issue-id>`.
* Commit messages: conventional commits (`feat:`, `fix:`, `chore:`).
* PRs: describe visual changes, link to screenshots, include Lighthouse baseline.
* Code style: follow Prettier / ESLint / Stylelint rules shipped with repo.

---

## Credits & resources

* Hero, gallery and demo media: Unsplash and Pexels (use your own licensed assets for production).
* Tools and libraries mentioned above (Flask, FAISS, Qdrant, Ollama, React, Tailwind, Docker, GitHub, Vercel/Netlify, Lighthouse).

---

## License

This project template is provided under the MIT license unless your organization requires another license. Replace with the appropriate license file before publishing.

---

## Final notes — high-level engineer checklist

* Focus on LCP: optimize hero image/video first.
* Keep animations GPU-friendly and mindful of `prefers-reduced-motion`.
* Build a small local RAG pipeline first (JSON vector store) then scale to FAISS/Qdrant.
* Use local model inference (Ollama) for private data or managed APIs when you need scale.
* Automate testing & performance regression in CI (fail on major regressions).

---

If you want, I can:

* produce a `design-kit.zip` with sample WebP hero images, SVG blobs, and a short optimized hero video (LCP-friendly),
* add a `diagram.svg` (editable) showing the RAG + Ollama flow, or
* scaffold a GitHub Actions CI workflow (lint, test, Lighthouse audit, deploy to Vercel).

Tell me which one to generate next and I’ll create it.
