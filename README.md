# GitMentor: The AI-Driven Technical Audit Engine

> **Ditch the Resume. Audit Your Code. Let Your Code Find Your Mentor.**

![Dashboard Screenshot](frontend/images/screenshot.png)

---

## 🚀 The Vision

GitMentor is a diagnostic engine that eliminates the **"Tutorial Hell"** problem. Instead of relying on inflated, self-reported resumes, GitMentor performs a deep-dive AI technical audit of a student's actual GitHub repositories. We provide actionable, data-driven insights that bridge the gap between *"coding hobbyist"* and *"production-ready developer."*

We are purpose-built to align with the **human-led learning ecosystem of Mentozy** — ensuring every student is matched to the right mentor *before* they have their first conversation.

---

## 💡 Why GitMentor?

Mentorship platforms are broken because they rely on **resumes** — static, inflatable, and misleading.

| Traditional Platform | GitMentor |
|---|---|
| Self-reported skill level | AI-audited from actual code |
| Generic mentor browsing | Targeted gap-to-mentor matching |
| Manual profile setup | Zero-config GitHub scan |
| Subjective assessment | 5-Pillar objective diagnostic |

---

## 🛠 The "Staff Engineer" Audit (Innovation)

Our AI Engine (Groq · Llama-3.3-70b-versatile) evaluates every portfolio against the **5 Pillars of Technical Maturity** — the same signals a Staff Engineer checks in a real hiring assessment.

| # | Pillar | Signal |
|---|---|---|
| 1 | **DevOps & Prod-Readiness** | Docker, CI/CD, `.env` management |
| 2 | **Documentation Quality** | README depth, setup guides, diagrams |
| 3 | **Modular Architecture** | Separation of concerns, clean structure |
| 4 | **Security & Best Practices** | Auth, config management, error handling |
| 5 | **Integration Complexity** | Real APIs, databases, external services |

**Output**: A **1–10 Maturity Score** + named strengths, skill gaps, and a matched mentor archetype.

---

## ⚙️ Tech Stack

| Layer | Technology | Reason |
|---|---|---|
| **Backend** | FastAPI | Async performance, native validation, OpenAPI docs |
| **AI Engine** | Groq / Llama-3.3-70b | Sub-second inference with enforced JSON output |
| **Frontend** | Vanilla HTML/CSS/JS | Zero-dependency, instant load, mobile-ready |
| **Deployment** | Docker + Nginx | Fully containerized, production-ready |

---

## 🏗 Architecture

```
[Browser] ──► [Nginx :80] ──► [FastAPI :8000]
                                     │
                          ┌──────────┴──────────┐
                          ▼                     ▼
                    [GitHub API]         [Groq LLM Audit]
                  repos + languages +    5-Pillar Rubric
                  stars + README         JSON-mode enforced
                          │
                          └────► Mentor Match Output
```

See [`docs/architecture.md`](docs/architecture.md) for the full technical breakdown.

---

## 🔧 Technical Challenges Faced & Solutions

| Challenge | Solution |
|---|---|
| LLM model decommissioned mid-development | Detected via `traceback` logging; upgraded to `llama-3.3-70b-versatile` |
| AI hallucinating on sparse profiles | Added 5 contextual signals: language distribution, stars, topics, README, repo count |
| Secret key committed to git | Used `git-filter-repo` to purge all history; rotated key; added `.gitignore` |
| Result UI hanging indefinitely | Missing `#result-display` DOM element — now validated in both HTML and JS |

---

## 🚀 Getting Started

### With Docker (Recommended)
```bash
git clone https://github.com/khanolkarsujal/GitMentor
cd GitMentor
cp .env.example .env   # Add your GROQ_API_KEY
docker-compose up --build
```
Navigate to [http://localhost:80](http://localhost:80)

### Local Development
```bash
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🧪 Testing

We ship with a full test suite targeting a **Staff Engineer's code review standard**.

```bash
pip install pytest httpx
pytest tests/ -v
```

**Test Coverage:**

| Test | What it checks |
|---|---|
| `test_status_endpoint` | API health check returns 200 |
| `test_root_returns_html` | Frontend is served correctly |
| `test_analyze_missing_username` | Invalid input returns 422 |
| `test_analyze_short_username` | Empty username is rejected |
| `test_analyze_returns_required_fields` | All 9 fields present in response |
| `test_maturity_score_range` | Score is integer in range [1, 10] |

---

## 🤝 Mentozy Alignment

GitMentor is designed as a **pre-session intelligence layer** for human-led learning platforms like Mentozy:

- **Before a session**: GitMentor audits the student's portfolio and surfaces their exact skill gaps
- **Mentor selection**: The audit output directly maps to a mentor archetype (e.g., "Senior Systems Architect")
- **Post-match**: The mentor receives the Audit Report — reducing onboarding time by an estimated **40%**

*"We aren't a job board. We are a personalized career bridge — matching students to mentors who specifically address the technical gaps discovered in the audit."*

---

## 📁 Project Structure

```
GitMentor/
├── backend/
│   └── main.py              # FastAPI + GitHub API + Groq LLM + 5-Pillar diagnostic
├── frontend/
│   ├── index.html           # Multi-section premium UI
│   ├── style.css            # Full design system (glassmorphism + animations)
│   ├── script.js            # Async fetch + result rendering
│   └── images/
│       └── screenshot.png
├── tests/
│   └── test_main.py         # 6 unit tests (pytest + httpx)
├── docs/
│   └── architecture.md      # System design + technical challenges
├── .env.example             # Key template
├── docker-compose.yml       # Nginx + FastAPI orchestration
├── Dockerfile               # Container definition
├── nginx.conf               # Reverse proxy config
└── requirements.txt
```

---

## 🔮 Future Roadmap

- **Multi-Repo Deep Audit** — Full portfolio history + commit frequency analysis
- **Mentor Dashboard** — Students' audit reports visible to mentors before accepting
- **Skill Graph** — Radar chart showing 5-pillar scores over time
- **Live Session Insight Generator** — Auto-summarize mentor sessions with action items

---

*Submitted for **Ignite Hack 2.0***
