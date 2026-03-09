# TeachLoop — Cinematic Landing (Production README)

**One-line summary:** A high-fidelity, production-minded landing page and component design system for an AI-Teacher product — cinematic hero with a large right→left animated headline, media-rich floating tiles, marquee text, responsive gallery, and engineering-grade integration points for RAG + local models.

---

## Banner / Visual Lead

![Banner hero — high-fidelity cinematic media](https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=1600\&q=80\&auto=format\&fit=crop)

**Credit**: Images and demo videos used here are placeholders from Unsplash and Pexels. Replace with your licensed, optimized WebP/AVIF assets for production.

---

# Contents

* [Overview](#overview)
* [Hero & Theme](#hero--theme)
* [Key Features](#key-features)
* [Architecture Diagram](#architecture-diagram)
* [Design System & Visual Tokens](#design-system--visual-tokens)
* [Teacher Component (responsive animation snippet)](#teacher-component-responsive-animation-snippet)
* [Tech Stack & Integrations](#tech-stack--integrations)
* [Performance & Accessibility](#performance--accessibility)
* [CI / CD and Deployment](#ci--cd-and-deployment)
* [Security & Privacy](#security--privacy)
* [Asset Strategy & Licensing](#asset-strategy--licensing)
* [Developer Quick Start](#developer-quick-start)
* [High-level engineering notes (hardwords & techstyle)](#high-level-engineering-notes-hardwords--techstyle)
* [Contributing & Style Guide](#contributing--style-guide)
* [License](#license)

---

## Overview

This repository contains a single-page landing experience and companion patterns built for high visual impact, rapid prototyping, and seamless integration with a Retrieval-Augmented-Generation (RAG) pipeline and local LLMs. The design emphasizes:

* Low-LCP hero delivery
* GPU-friendly motion (transforms + opacity)
* Clear progressive enhancement (reduced-motion, limited animation on low-power devices)
* Modular, testable UI components for engineering reuse

Target audience: product engineers, front-end architects, and ML engineers building an integrated learning product.

---

## Hero & Theme

The hero is engineered for visual hierarchy and measurable performance:

* Headline: large display font (900); animated right → left via `transform` + `opacity` for LCP safety.
* Media Stage: short, looped hero video (low-bitrate H.264) with multiple floating tiles (images / short clips).
* Depth Effects: blurred gradient stripes, radial glow, and a lightweight particle field drawn to canvas at modest frame rate.
* Motion Controls: `prefers-reduced-motion` observer, hover-to-pause marquee and carousel.

Design intent: cinematic, yet engineered for production — hero assets are the single most important optimization target.

---

## Key Features

* Right→left animated headline tuned to be LCP-friendly.
* Floating media stage (video + tiles) with tilt and parallax.
* Continuous marquee and accessible carousel with indicators + keyboard controls.
* RAG-ready structure: isolated vector stores per domain (Database / Python) and an All-Rounder path that conditions a local LLM.
* Accessibility-first: ARIA landmarks, keyboard navigation, and `prefers-reduced-motion` support.
* Performance-first: preload LCP asset, `loading="lazy"` for offscreen images, and suggestions for WebP/AVIF.

---

## Architecture Diagram

Use the diagram below as the canonical integration flow. Copy into a diagram editor (draw.io, Figma, Mermaid) for visuals.

```mermaid
flowchart TD
  Browser[Browser / Landing Page]
  Browser -->|CTA / Chat| Backend[Flask API (optional)]
  Backend -->|embed(query)| EmbedService[Embedding Service]
  EmbedService --> VectorStore[Vector Store (FAISS / Qdrant)]
  VectorStore --> Backend
  Backend -->|context+prompt| Ollama{{Ollama Local LLM}}
  Ollama --> Backend
  Backend --> Browser

  subgraph assets
    A1[Hero Video / Images (CDN)]
  end

  Browser --> A1
```

Alternate textual summary:

1. Browser loads static landing assets from CDN.
2. User triggers a chatbot query -> frontend sends to `/api/query_teacher`.
3. Backend computes embedding -> retrieves top-K documents from vector store (local JSON, FAISS, or Qdrant).
4. Optionally calls local model server (Ollama) for generation using retrieved context.
5. Server returns grounded, citation-aware reply.

---

## Design System & Visual Tokens

Use these tokens as a canonical source:

* Colors: `--accent-a: #5865f2`, `--accent-b: #7dd3fc`, `--bg-1: #050612`, `--muted: #9aa6c7`
* Typography: Display (900) + Inter base. Headline scaled with `clamp()` for responsiveness
* Spacing: 24px base, scale 8/16/24/40/64 for panels
* Elevation: box-shadows tuned for soft cinematic depth
* Motion: durations 180ms (micro), 420ms (mid), 1100ms (headline)

### Colorful info boxes example (use in docs & marketing)

Provide colorful boxed content to highlight features:

```html
<div style="border-radius:12px;padding:16px;background:linear-gradient(90deg,#5865f2, #77a8ff);color:white;">
  <h4>Latency-Optimized Retrieval</h4>
  <p>HNSW-backed ANN retrieval with tuned efSearch for predictable  sub-30ms tail latency.</p>
</div>
```

(For production, move inline styles into CSS variables / classes and keep semantics clean.)

---

## Teacher Component (responsive animation snippet)

This pattern is the interactive “teacher card” used across the site. It supports: collapsed summary → expand (examples/code) with smooth animation, keyboard focus, and code copy button.

**HTML**

```html
<aside class="teacher-card" role="region" aria-label="Database teacher">
  <header class="teacher-head">
    <h3>Database Teacher</h3>
    <button class="toggle" aria-expanded="false">Examples</button>
  </header>
  <div class="teacher-body" hidden>
    <pre class="code-sample">SELECT * FROM users WHERE id = ?;</pre>
    <div class="actions">
      <button class="copy">Copy</button>
    </div>
  </div>
</aside>
```

**CSS (key animation)**

```css
.teacher-body { transition: max-height 380ms cubic-bezier(.2,.9,.3,1), opacity 260ms; overflow:hidden; max-height:0; opacity:0; }
.teacher-card.expanded .teacher-body{ max-height:400px; opacity:1; }
```

**JS (toggle)**

```js
card.querySelector('.toggle').addEventListener('click', () => {
  const expanded = card.classList.toggle('expanded');
  card.querySelector('.toggle').setAttribute('aria-expanded', expanded);
});
```

This animation uses `max-height` + `opacity` to avoid content shift; for complex content prefer `height` calculated via `scrollHeight`.

---

## Tech Stack & Integrations

* Frontend: vanilla HTML/CSS/JS (componentizable to React + Tailwind)
* Backend (optional): Python + Flask (RAG endpoints)
* Vector store options:

  * FAISS — FAISS (HNSW / IVF) for local ANN
  * Qdrant — managed / hosted vector DB option
* Local model server: Ollama (on-prem inference)
* Containerization: Docker for dev parity
* Hosting / static deploy:

  * Vercel or Netlify for static hosting or serverless backends
* Source control and CI: GitHub
* Performance auditing: Lighthouse

> Replace placeholders with your curated production endpoints (models, vector DB, CDN).

---

## Performance & Accessibility

* **LCP priority**: Preload the hero poster image and use a compressed short video for motion. Provide poster fallback for browsers that avoid autoplay.
* **Network hints**: `<link rel="preload" as="image">`, `<link rel="preconnect">` for CDNs.
* **Lazy loading**: `loading="lazy"` for non-critical images.
* **Reduced motion**: Full `prefers-reduced-motion` fallback — disable marquee, tilt, and particle canvas.
* **Accessibility**: semantic landmarks, ARIA labels for dynamic regions, focus-visible styles, keyboard nav & skip links.
* **Metrics to track**: LCP, CLS, TTFB, TBT, interaction latency for chat flows.

---

## CI / CD & Deployment

Recommended pipeline:

1. **Lint & Format**

   * CSS / JS linting (stylelint / eslint)
   * Prettier format
2. **Unit & Integration**

   * Pytest (backend) and Playwright/Cypress (E2E)
3. **Performance Gate**

   * Run a Lighthouse budget step in CI and fail on regressions
4. **Build & Deploy**

   * Build static assets, upload to CDN, invalidate cache
   * Deploy backend container to staging via `Docker` and run smoke tests
5. **Platform**

   * Deploy front-end to Vercel or Netlify; backend to managed cloud or self-hosted k8s.

---

## Security & Privacy

* Sanitize and validate all inputs. Do not directly inject user text into shell or model prompts without escaping.
* Rate-limit public endpoints to prevent abuse.
* For sensitive data, run models locally (Ollama) and keep vector stores private.
* Rotate and store secrets in environment variables or secrets manager (don’t commit them).

---

## Asset Strategy & Licensing

* Use `srcset` + `sizes` with multiple width variants for each hero / gallery image.
* Provide both WebP/AVIF and JPEG fallbacks.
* Short hero video: 2–6s loop, optimized bitrate; provide `poster` attribute for LCP.
* Attribution: demo assets used from Unsplash and Pexels — replace with licensed proprietary assets before production.

---

## Developer Quick Start (local)

1. Clone the repo (or copy files).
2. Static-only preview:

   ```bash
   python -m http.server --directory . 8000
   # open http://localhost:8000/index.html
   ```
3. Optional Flask backend:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   export FLASK_APP=app.py
   flask run
   ```
4. Run Lighthouse and iterate on LCP, TBT.

---

## High-level engineering notes (hardwords & techstyle)

* Embedding dimensionality: choose embedding dimensionality (e.g., 384 / 768 / 1024) matching your embedder and index configuration to balance retrieval accuracy and memory footprint.
* Index topology: HNSW (small-scale latency-sensitive) vs IVF+PQ (very large corpora) — tune `efSearch` for tail latency vs recall trade-offs.
* Retrieval pipeline: chunk size ≈ 500 tokens; use overlap (e.g., 50–100 tokens) to preserve context boundaries.
* Prompt engineering: compose prompts with explicit instruction, system role, and verification step (ask the model to cite the snippet id if it used retrieved context).
* Caching: cache embeddings and hot query responses (use Redis) to reduce repeated inference cost.
* Observability: instrument retrieval latency, model latency, and error rates; alert on 95th/99th percentile spikes.
* Scalability: separate read-heavy static assets (CDN) from compute-heavy inference nodes (horizontal scaling).

---

## Contributing & Style Guide

* Branch naming: `feature/<short>`, `bugfix/<id>`
* Commit style: Conventional Commits (`feat:`, `fix:`, `chore:`)
* PRs should include: short summary, screenshots of visual changes, Lighthouse before/after for performance-impacting PRs.
* Tests: unit tests for backend and E2E for critical user flows.

---

## License

This template is provided under the MIT License. Replace with your organization’s license if required.

---

If you want, I can:

* generate a ready-to-commit `README.md` file in the repository format,
* provide a high-resolution `diagram.svg` (editable) for the architecture,
* create a `design-kit.zip` containing WebP hero images, SVG blobs, and a compressed loop video tailored to the page.

Which of the above should I produce next?
