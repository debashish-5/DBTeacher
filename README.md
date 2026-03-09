# TeachLoop — Cinematic Landing (Production-grade README)

**One-line:** Modern, high-fidelity landing page and component library for an AI-teacher product — cinematic hero with a right→left animated headline, rich media stage, marquee, accessible carousel, and engineering-grade integration patterns for RAG and local model inference.

---

## Banner / Visual Lead

```
████████╗███████╗ █████╗ ██████╗ ██╗     ██╗      ██████╗  ██████╗  ██████╗ 
╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██║     ██║     ██╔═══██╗██╔═══██╗██╔═══██╗
   ██║   █████╗  ███████║██████╔╝██║     ██║     ██║   ██║██║   ██║██║   ██║
   ██║   ██╔══╝  ██╔══██║██╔═══╝ ██║     ██║     ██║   ██║██║   ██║██║   ██║
   ██║   ███████╗██║  ██║██║     ███████╗███████╗╚██████╔╝╚██████╔╝╚██████╔╝
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝ 
```

High-fidelity hero image (replace the demo asset with your production LCP image): use a short, optimized loop and a high-quality poster frame.

---

## Repository summary

* `index.html` — single-file cinematic landing page (production patterns: LCP preloads, `prefers-reduced-motion`, lazy loading).
* `static/css/*` — design tokens, modular styles, animation utilities.
* `static/js/*` — marquee, carousel, tilt, particles, accessibility utilities.
* `templates/*` — optional Flask templates for teacher pages.
* `vector_db/*` — small JSON samples for Database and Python teacher knowledge.
* `app.py` (optional) — Flask RAG endpoints + Ollama wiring.
* `README.md` — this file.

---

## Design goals (modern high quality)

1. **Perceptual performance** — prioritize LCP, minimal blocking scripts, and preloaded hero resources.
2. **Scalable motion** — only animate transforms and opacity, avoid layout thrashing. Respect `prefers-reduced-motion`.
3. **Visual depth** — layered gradients, blurred stripes, animated SVG blobs, soft glows and cinematic shadows.
4. **Component-driven** — teacher card, media stage, carousel, marquee, gallery — each isolated and accessible.
5. **RAG-ready** — two isolated vector DBs (Database / Python) and an All-Rounder path that composes retrieved snippets into a generator prompt.

---

## Key features (short)

* Right→left headline: GPU-accelerated slide + fade for strong entrance, triggered by `IntersectionObserver`.
* Media stage: device mockup (looped video) + floating image tiles with tilt on pointer.
* Continuous marquee and accessible carousel with keyboard interaction and indicators.
* Particle field canvas for subtle motion (low CPU priority).
* Built-in performance & accessibility patterns: LCP preload, lazy loading, `aria-*`, keyboard shortcuts, reduced-motion fallbacks.
* Production notes for asset formats: WebP / AVIF + fallbacks; H.264 MP4 for broad compatibility.

---

## Architecture diagram (copy to a Mermaid editor for visuals)

```mermaid
flowchart TD
  Browser[Browser: Landing page + UI]
  Browser -->|CTA / Query| Backend[Flask API (optional)]
  Backend -->|embed(query)| EmbedService[Embedding service]
  EmbedService --> VectorStore[Vector Store (FAISS / Qdrant)]
  VectorStore --> Backend
  Backend -->|context + prompt| LLM[Local model]
  LLM --> Backend
  Backend --> Browser

  subgraph Assets
    CDN[Hero images & video (CDN)]
  end
  Browser --> CDN
```

Notes:

* Use `Embedding service` to batch embed requests; cache embeddings for repeated queries.
* `Vector Store` choices: FAISS for in-process, Qdrant for managed/scaled deployments.

---

## Technology map (single mention of each major integration)

* Local model inference: Ollama
* Vector index (local): FAISS
* Vector DB (managed): Qdrant
* Static hosting / deployment: Vercel and Netlify (choose one)
* Source control and CI: GitHub
* Containerization: Docker
* Performance audits: Lighthouse
* Media assets (placeholders): Unsplash and Pexels

(Each of the above is referenced once — replace placeholders with your production endpoints and licensed assets.)

---

## Visual tokens & modern theme

**Color palette**

* Primary gradient: `#5865f2 → #7dd3fc`
* Background deep: `#050612 → #0f1836`
* Muted text: `#9aa6c7`
* Glass card: `rgba(255,255,255,0.035)`

**Typography**

* Display (900) for headline; `clamp()` for responsive sizing.
* Body: Inter 16–18px baseline, 1.45 line-height.

**Spacing**

* Base unit: 8px; scale: 8, 16, 24, 40, 64.

**Elevation**

* Soft cinematic shadows: `0 30px 80px rgba(2,6,23,0.65)` for media stage.

---

## Colorful info boxes (examples for README or marketing pages)

Use CSS cards with gradients or left accent bars. Example HTML snippet:

```html
<div class="info-box gradient">
  <h4>Latency-Optimized Retrieval</h4>
  <p>HNSW ANN tuned for sub-30ms tail latency with efSearch optimized for recall/latency tradeoffs.</p>
</div>

<!-- CSS -->
<style>
.info-box.gradient{padding:16px;border-radius:12px;color:#fff;background:linear-gradient(90deg,#5865f2,#77a8ff);box-shadow:0 12px 40px rgba(12,18,50,0.5)}
</style>
```

---

## Teacher component (responsive animated pattern)

**Purpose:** a focused, interactive teacher card that expands to show examples, code snippets, and citations for retrieved context.

**HTML**

```html
<aside class="teacher-card" role="region" aria-label="Database teacher">
  <header class="teacher-head">
    <div><strong>Database Teacher</strong><div class="meta">SQL, ACID, Indexing</div></div>
    <button class="toggle" aria-expanded="false" aria-controls="teacher-1-details">Examples</button>
  </header>

  <div id="teacher-1-details" class="teacher-body" hidden>
    <pre class="code-sample" aria-live="polite">SELECT name, email FROM users WHERE active = 1;</pre>
    <div class="teacher-footer">
      <button class="copy">Copy</button>
      <span class="provenance">Sources: snippet_23, snippet_7</span>
    </div>
  </div>
</aside>
```

**Key CSS pattern**

```css
.teacher-body{overflow:hidden; max-height:0; opacity:0; transition:max-height 360ms cubic-bezier(.2,.9,.3,1), opacity 220ms}
.teacher-card.expanded .teacher-body{max-height:420px; opacity:1}
```

**Behavior**

* Toggle expands/collapses with `aria-expanded` state.
* On expand, focus moves to the first interactive element inside.
* Provide explicit provenance lines showing which retrieved snippets were used.

---

## Retrieval pipeline (high-level)

1. **Document ingestion** — chunk text (≈500 tokens) with overlap (≈50–100 tokens).
2. **Embedding** — batch embeddings (e.g., `all-MiniLM-L6-v2` or larger) and persist vectors.
3. **Index** — HNSW for interactive latency; IVF+PQ for very large corpora. Tune `efSearch` vs `efConstruction`.
4. **Query** — embed user prompt → nearest neighbor retrieval (top-k) → build context window → call generator with context.
5. **Post-process** — extract citations, generate summary and suggested follow-ups. Cache popular queries.

---

## Production checklist (engineer level)

* **LCP**: Preload hero image; ensure hero poster is first meaningful paint.
* **Images**: Provide `srcset` and `sizes`; serve WebP/AVIF.
* **Video**: Short loop (2–6s), H.264 MP4 + WebM; provide a poster image.
* **Scripts**: Defer non-critical JS; inline bootstrap only.
* **Caching**: CDN for assets; long TTL for immutable resources with hashed filenames.
* **Observability**: instrument retrieval latency, model latency, and 95/99 percentiles; integrate with logging/metrics.
* **Security**: sanitize prompts; rate-limit endpoints; secrets in vault.
* **Accessibility**: axe and manual keyboard testing; color-contrast tests.
* **Testing**: unit tests + E2E (Playwright) + Lighthouse in CI.

---

## CI / CD (recommended workflow)

1. `push` → run linters (ESLint, Stylelint), unit tests, and format checks.
2. Build assets & run Lighthouse audit (fail on regressions beyond threshold).
3. On main branch, deploy static assets to CDN via `Vercel` or `Netlify`; deploy backend containers via `Docker` image to a managed cluster or server pool.
4. Post deployment: run smoke tests and synthetic RUM measurement.

---

## Hardwords & engineering annotations (high-level)

* **efSearch**: HNSW search parameter controlling recall vs latency — increase for higher recall at tail latency cost.
* **IVF+PQ**: index topology for billion-scale corpora; trades memory for storage and approximate quality.
* **Partial hydration / islands architecture**: keep static markup and progressively hydrate interactive islands to reduce JS payload.
* **LCP budget**: set a numeric budget in CI to avoid regressions; optimize hero assets first.
* **Provenance**: always show which snippet IDs or document fragments were used to answer a query to enable user verification.

---

## Asset & licensing strategy

* Provide three sizes for each hero and gallery image (1x/2x/3x) in WebP/AVIF and JPEG fallback.
* Two hero videos: optimized WebM + H.264 MP4 fallback; short loop and a lightweight poster for LCP.
* Replace demo assets (Unsplash / Pexels) with licensed proprietary assets before production.

---

## Run locally (quick)

Static preview:

```bash
python -m http.server --directory . 8000
# open http://localhost:8000/index.html
```

Optional backend (Flask with RAG endpoints):

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask run
```

---

## Observability & operational notes

* **Metrics**: Ingest retrieval latency, model latency, request rate, error rate, and resource usage.
* **Alerts**: Alert on spikes in 95th/99th percentile model latency or increased error rates.
* **Telemetry**: correlate frontend LCP/TBT with backend retrieval/model times to identify perf bottlenecks.

---

## Contribution & governance

* Repo conventions: Conventional commits, PRs with visual diffs, Lighthouse baseline.
* Branch strategy: `feature/*`, `fix/*`, `hotfix/*`.
* Review checklist: accessibility, performance, security, regression tests.

---

## Next deliverables I can produce for you (pick one)

* an **editable SVG architecture diagram** (Mermaid → SVG with layers).
* a **design kit**: WebP hero + poster + compressed loop video + SVG blobs (ready for production).
* a **React + Tailwind** migration scaffold with componentized teacher card, carousel and utilities.
* production **CI workflow** (GitHub Actions) with Lighthouse gating and deployment to Vercel.

Tell me which one you want next and I will generate it.
