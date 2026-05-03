# bajetAI.my — Freelance Landing Page

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a one-page freelance landing site on bajetAI.my introducing Radzy's data analysis/data science services, with a client requirement form (including sample data upload) that captures leads for manual assessment and quotation.

**Architecture:** SvelteKit (Svelte 5) frontend served via Node adapter, lightweight Python (FastAPI) backend via Pixi for form/file handling. Both containerized with Docker. Caddy reverse proxy handles HTTPS on bajetai.my.

**Tech Stack:** SvelteKit + Svelte 5 (frontend), Python 3.12 + FastAPI + Pixi (backend), Docker + Caddy (deployment), SQLite (submissions storage), Postfix (email notifications)

---

## Current State

- `bajetai-app` container STOPPED (was old app on port 8030)
- Caddy config: `bajetai.my` → `host.docker.internal:8030` (needs update)
- New project dir: `/home/pakerole/bajetai-freelance/`
- Domain: `bajetai.my` (DNS via Dynu, Caddy handles TLS)
- Server: Home server with Docker, Caddy container, Postfix relay via Gmail

## Project Structure

```
bajetai-freelance/
├── frontend/                  # SvelteKit app (Svelte 5)
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/    # UI components
│   │   │   │   ├── Hero.svelte
│   │   │   │   ├── About.svelte
│   │   │   │   ├── Services.svelte
│   │   │   │   ├── HowItWorks.svelte
│   │   │   │   ├── ContactForm.svelte
│   │   │   │   └── Footer.svelte
│   │   │   └── api/           # SvelteKit API proxy (optional)
│   │   ├── routes/
│   │   │   ├── +layout.svelte
│   │   │   └── +page.svelte   # One-page layout
│   │   └── app.html
│   ├── static/
│   ├── package.json
│   ├── svelte.config.js
│   ├── vite.config.ts
│   └── Dockerfile
├── backend/                   # Python FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app
│   │   ├── models.py          # Pydantic models
│   │   ├── storage.py         # SQLite submission storage
│   │   ├── email.py           # Email notification via Postfix
│   │   └── schemas.py         # Form validation schemas
│   ├── pixi.toml
│   ├── Dockerfile
│   └── requirements.txt       # Generated from pixi for Docker
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Page Sections (One-Page Scroll)

### 1. Hero Section
- **Name:** Ahmad Fakrul Radzy (Radzy)
- **Tagline:** Data Scientist & Analytics Engineer
- **One-liner:** "Turning complex data into clear decisions"
- CTA button: "Start a Project" → scrolls to contact form
- Clean, minimal design — no stock photos

### 2. About / Background

__Copy for the page:__

> With a strong foundation in Python-driven data analysis and machine learning, I help businesses extract meaningful insights from their data — whether it's cleaning messy datasets, building predictive models, fine-tuning large language models, or creating automated reporting pipelines.
>
> My work spans from telecommunications analytics (network performance, KPI monitoring, log analysis) to applied ML (LLM fine-tuning, computer vision, speech processing). I bring data science techniques to real-world operational problems, not just academic exercises.
>
> Every project starts with understanding your data. I work across industries — from telecom to finance to e-commerce — to build solutions that are practical, scalable, and actually useful.

**Tools & Skills badges:** Python, pandas, NumPy, SQL, Elasticsearch, PyTorch, Scikit-learn, FastAPI, Docker, Git

### 3. Services

**Service 1: Data Analysis & Reporting**
> Raw data won't tell you much until someone asks the right questions. I analyze datasets — from CSV exports to database queries — and produce clear reports with actionable findings. Whether it's sales trends, operational metrics, or customer behavior patterns.

**Service 2: Data Pipelines & Automation**
> Manual data processing is error-prone and slow. I build automated pipelines that ingest, clean, transform, and deliver your data on schedule. Web scraping scripts, ETL jobs, API integrations, report generators — whatever keeps your data flowing.

**Service 3: Data Visualization & Dashboards**
> Numbers are easier to act on when you can see them. I create dashboards and visualizations — static reports or interactive views — that make your data speak at a glance. Matplotlib, Plotly, or custom-built solutions.

**Service 4: Custom Tooling & APIs**
> Sometimes what you need is a tool that doesn't exist yet. I develop custom Python applications, REST APIs, and automation scripts tailored to your specific workflow. From file-processing utilities to full data platforms.

### 4. How It Works

3-step process:
1. **Submit** — Tell me about your project and upload a sample of your data
2. **Assess** — I review the scope, complexity, and feasibility (within 3 business days)
3. **Quote** — You receive a clear quotation with timeline and deliverables

### 5. Contact / Requirement Form

**Fields:**
- Name (required)
- Email (required)
- Company (optional)
- Project type (dropdown: Data Analysis & Reporting, Machine Learning / AI, Data Pipelines & Automation, Data Visualization & Dashboards, Custom Tooling / APIs, Other)
- Description / Requirements (textarea, required)
- Sample data file upload (CSV, Excel, JSON — optional, max 10MB)
- Submit button

**Auto-reply message:** "Thank you for reaching out! I've received your requirements and will review the scope within 3 business days. You'll receive a tailored quotation via email."

### 6. Footer
- © 2026 bajetAI — Ahmad Fakrul Radzy
- Email: hello@bajetai.my (or pakerole@gmail.com)
- No social links for now

---

## Implementation Tasks

### Task 1: Initialize SvelteKit Frontend

**Objective:** Scaffold SvelteKit project with Svelte 5 in frontend/

**Files:**
- Create: `frontend/` (full SvelteKit scaffold)

**Steps:**
1. Run `cd /home/pakerole/bajetai-freelance && npx sv create frontend` (select SvelteKit minimal, TypeScript, no prettier)
2. Verify: `cd frontend && npm install && npm run dev` starts without errors
3. Commit

### Task 2: Initialize Python Backend with Pixi

**Objective:** Set up Pixi-managed Python project with FastAPI

**Files:**
- Create: `backend/pixi.toml`
- Create: `backend/app/__init__.py`
- Create: `backend/app/main.py`

**pixi.toml:**
```toml
[project]
name = "bajetai-freelance-api"
version = "0.1.0"
description = "Backend API for bajetAI.my freelance landing page"
requires-python = ">=3.12"

[dependencies]
fastapi = ">=0.115.0"
uvicorn = ">=0.34.0"
python-multipart = ">=0.0.18"
pydantic = ">=2.10.0"
pydantic-email = ">=2.0.0"
aiosqlite = ">=0.21.0"

[tasks]
dev = "uvicorn app.main:app --reload --host 0.0.0.0 --port 8010"
```

**Steps:**
1. Create pixi.toml and directory structure
2. Run `cd backend && ~/.pixi/bin/pixi install`
3. Verify: `~/.pixi/bin/pixi run dev` starts FastAPI on 8010
4. Commit

### Task 3: Backend — Submission Model & SQLite Storage

**Objective:** Create Pydantic models for form submission and SQLite storage layer

**Files:**
- Create: `backend/app/models.py`
- Create: `backend/app/storage.py`

**Steps:**
1. Define Pydantic model: Submission(name, email, company?, project_type, description, filename?)
2. Create SQLite table: submissions (id, name, email, company, project_type, description, filename, filepath, created_at)
3. CRUD operations: save_submission, get_submissions, get_submission
4. Write tests
5. Commit

### Task 4: Backend — Form Submission Endpoint & File Upload

**Objective:** POST /api/submit endpoint that accepts form data + file upload

**Files:**
- Create: `backend/app/main.py` (routes)
- Create: `backend/uploads/` directory

**Steps:**
1. POST /api/submit — accepts multipart form (fields + optional file)
2. Validate fields with Pydantic
3. Save uploaded file to uploads/ with UUID filename
4. Store submission record in SQLite
5. Return success response
6. Write tests
7. Commit

### Task 5: Backend — Email Notification

**Objective:** Send email notification to owner (pakerole@gmail.com) on new submission

**Files:**
- Create: `backend/app/email.py`

**Steps:**
1. Use subprocess to call /usr/sbin/sendmail (Postfix relay already configured)
2. Format email: client name, email, project type, description, file info
3. Call email.py from submission endpoint
4. Test with a sample submission
5. Commit

### Task 6: Backend — Dockerfile

**Objective:** Create Dockerfile for backend

**Files:**
- Create: `backend/Dockerfile`
- Create: `backend/requirements.txt` (export from pixi)

**Steps:**
1. Export dependencies: `~/.pixi/bin/pixi export requirements > backend/requirements.txt`
2. Multi-stage Dockerfile: build deps, copy app, run with uvicorn
3. Expose 8010
4. Build and verify: `docker build -t bajetai-backend ./backend`
5. Commit

### Task 7: Frontend — One-Page Layout & Design System

**Objective:** Set up the page layout, design tokens (colors, typography, spacing), and component structure

**Files:**
- Modify: `frontend/src/app.html`
- Modify: `frontend/src/routes/+layout.svelte`
- Modify: `frontend/src/routes/+page.svelte`
- Create: `frontend/src/app.css` (design tokens)

**Design Direction:**
- Clean, professional, minimal
- Dark text on light background (trust-building for freelance)
- One accent color (pick from brand or create)
- Mobile-responsive
- Smooth scroll between sections
- No glassmorphism, no gradients, no stock photos

**Steps:**
1. Define CSS custom properties in app.css
2. Set up +layout.svelte with nav (anchor links to sections)
3. Set up +page.svelte with section slots
4. Verify responsive behavior
5. Commit

### Task 8: Frontend — Hero, About, Services Components

**Objective:** Build the three main content sections

**Files:**
- Create: `frontend/src/lib/components/Hero.svelte`
- Create: `frontend/src/lib/components/About.svelte`
- Create: `frontend/src/lib/components/Services.svelte`

**Steps:**
1. Hero: name, tagline, CTA button (scroll to form)
2. About: background paragraph, skills/tools list
3. Services: 4-5 service cards with icon + title + description
4. Wire into +page.svelte
5. Commit

### Task 9: Frontend — HowItWorks & Footer

**Objective:** Build the process explanation and footer sections

**Files:**
- Create: `frontend/src/lib/components/HowItWorks.svelte`
- Create: `frontend/src/lib/components/Footer.svelte`

**Steps:**
1. HowItWorks: 3-step visual flow
2. Footer: copyright, email, social links
3. Wire into +page.svelte
4. Commit

### Task 10: Frontend — ContactForm Component

**Objective:** Build the client requirement form with file upload

**Files:**
- Create: `frontend/src/lib/components/ContactForm.svelte`

**Steps:**
1. Form fields: name, email, company, project_type (select), description (textarea)
2. File upload: accept .csv,.xlsx,.xls,.json, max 10MB
3. Client-side validation
4. Submit via fetch to backend POST /api/submit
5. Loading state, success state, error state
6. Wire into +page.svelte
7. Commit

### Task 11: Frontend — Dockerfile & Adapter

**Objective:** Containerize SvelteKit with Node adapter

**Files:**
- Modify: `frontend/package.json` (add @sveltejs/adapter-node)
- Modify: `frontend/svelte.config.js`
- Create: `frontend/Dockerfile`

**Steps:**
1. Install adapter-node: `npm install -D @sveltejs/adapter-node`
2. Configure svelte.config.js to use adapter-node
3. Multi-stage Dockerfile: build → run with node
4. Expose 3000
5. Build and verify
6. Commit

### Task 12: Docker Compose & Caddy Config

**Objective:** Wire up both containers and update Caddy

**Files:**
- Create: `docker-compose.yml`
- Modify: Caddy config (update bajetai.my to point to new frontend)

**docker-compose.yml:**
```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "8030:3000"
    restart: unless-stopped

  backend:
    build: ./backend
    ports:
      - "8010:8010"
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/data:/app/data
    restart: unless-stopped
```

**Steps:**
1. Create docker-compose.yml
2. Update Caddy Caddyfile: bajetai.my → frontend:8030, /api/* → backend:8010
3. Reload Caddy: `docker exec caddy caddy reload --config /etc/caddy/Caddyfile`
4. Test: `docker compose up -d`
5. Verify bajetai.my loads the new page
6. Test form submission
7. Commit

### Task 13: Git Init & GitHub Push

**Objective:** Initialize git repo and push to GitHub

**Files:**
- Create: `.gitignore`
- Create: `README.md`

**Steps:**
1. Create .gitignore (node_modules, .pixi, uploads/, data/*.db, .env, __pycache__)
2. Create README.md with project description
3. `git init && git branch -m main`
4. Add all files and commit
5. Create GitHub repo (bajetai-freelance or similar)
6. Push to GitHub
7. Done

---

## Risks & Open Questions

1. **Content**: Copy drafted above — ready for implementation. Radzy can tweak later.
2. **Branding**: No logo or brand assets yet — proceed with typography-first design
3. **Social links**: Omitted for now (none provided)
4. **Response time**: 3 business days — confirmed
5. **File size limit**: 10MB default — adjust if needed
6. **Backend port conflict**: Old app used 8010 — reuse same port since old container is stopped
7. **Caddy update**: Need to also handle /api/* routing to backend container
8. **Email for contact form**: Use `hello@bajetai.my` as the from/reply-to. Postfix config for this sender address to be fixed later — use `pakerole@gmail.com` as fallback sender during development.

## Deployment Strategy

1. Build both images locally via docker compose
2. Update Caddy config to point bajetai.my to new frontend (port 8030) and /api/* to backend (port 8010)
3. Reload Caddy, verify HTTPS works
4. Test form submission end-to-end
5. Monitor for issues
