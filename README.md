# MentorIQ: The AI-Driven Technical Audit Engine

> **Ditch the guesswork. Audit your code. Find your perfect mentor.**

![Dashboard Screenshot](frontend/images/screenshot.png)

---

## 🚀 The Vision

MentorIQ is a diagnostic engine that solves the **"Tutorial Hell" problem**. Instead of relying on inflated, self-reported resumes, MentorIQ performs a deep-dive technical audit of a student's actual GitHub repositories. We provide actionable, data-driven insights that bridge the gap between *"coding hobbyist"* and *"production-ready developer."*

---

## 💡 Why MentorIQ? (Impact)

Most mentorship platforms are flawed because they rely on **resumes** — which are static and often misleading. MentorIQ changes the paradigm:

- **Zero-Config Audit**: No manual profile entry. Just provide your GitHub username.
- **Code-First Truth**: We evaluate the actual repository structure, documentation, and logic.
- **Actionable Growth**: We don't just match you to a mentor; we match you to an archetype that solves your *specific* technical skill gaps.

---

## 🛠 The "Staff Engineer" Audit (Innovation)

Our AI Engine (powered by Llama-3.3/Groq) evaluates every repository against the **5 Pillars of Technical Maturity**:

| Pillar | Signal |
|---|---|
| **DevOps & Environment Awareness** | Docker, CI/CD, `.env` management |
| **Documentation Quality** | README completeness, API docs, setup guides |
| **Modular Architecture** | Separation of concerns, clean code structure |
| **Security & Best Practices** | Auth, config management, error handling |
| **Integration Complexity** | APIs, Database handling, external services |

**The Output**: A **1–10 Maturity Score** and a personalized technical audit report that guides the mentorship matching process.

---

## ⚙️ Tech Stack (Technical Implementation)

Built with a **"Production-First"** mindset:

| Layer | Technology |
|---|---|
| **Backend** | FastAPI — high-performance async microservice |
| **AI Engine** | Groq API (Llama-3.3-70b-versatile) — sub-second code analysis |
| **Frontend** | Vanilla HTML/CSS/JS — zero-dependency, fast |
| **Infrastructure** | Docker & Nginx — fully containerized, production-ready |

---

## 🏗 Architecture

```
[Browser] ──► [Nginx Reverse Proxy]
                      │
                      ▼
              [FastAPI Backend] ──► [GitHub API]  (fetch repos, languages, README)
                      │
                      ▼
              [Groq / Llama-3.3]  ──►  5-Pillar Rubric Audit
                      │
                      ▼
              [Mentor Match Engine]  ──►  Skill Gap → Mentor Archetype
```

---

## 🚀 Getting Started

### Prerequisites
- **Docker & Docker Compose** installed
- A **Groq API Key** (get one at [console.groq.com](https://console.groq.com))

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/khanolkarsujal/MentorIQ
cd MentorIQ
```

**2. Configure Environment:**

Copy the example env file and fill in your key:
```bash
cp .env.example .env
# Then edit .env and set your GROQ_API_KEY
```

**3. Launch with Docker:**
```bash
docker-compose up --build
```

**4. Access the application:**

Navigate to [http://localhost:80](http://localhost:80)

### Run Locally (Without Docker)
```bash
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔮 Future Roadmap

- **Multi-Repo Deep Audit**: Expand from the latest repo to the full portfolio history + commit frequency analysis
- **Live Coding Challenge**: Integrate a code-snippet analyzer to identify specific logic flaws in real-time
- **Mentor Dashboard**: Allow mentors to view a student's "Audit Report" before accepting a mentorship request
- **Skill Graph**: Visual radar chart showing the 5-pillar scores over time as the student improves

---

## 📁 Project Structure

```
MentorIQ/
├── backend/
│   └── main.py          # FastAPI app + GitHub API + Groq AI audit
├── frontend/
│   ├── index.html       # Main UI
│   ├── style.css        # Dark-theme premium design
│   ├── script.js        # Async fetch + dynamic result rendering
│   └── images/
│       └── screenshot.png
├── .env.example         # Environment variable template
├── docker-compose.yml   # Production orchestration
├── Dockerfile           # Container definition
├── nginx.conf           # Reverse proxy config
└── requirements.txt
```

---

*Submitted for **Ignite Hack 2.0***
