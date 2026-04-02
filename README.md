# 🛡️ MentorIQ (SaaS Architecture)

> **Principal Engineer Refactor: Production-Ready SaaS Architecture**

MentorIQ is an AI-powered GitHub auditing and mentor matchmaking platform. This version features a modular, service-oriented backend built for scalability, security, and high availability.

---

### **🏗️ SaaS Architecture Breakdown**

| **Directory** | **Responsibility** | **Key Patterns Used** |
| :--- | :--- | :--- |
| `backend/app/main.py` | FastAPI Entrypoint | App initialization & Middleware setup |
| `backend/app/api/endpoints/` | Controllers / Routers | Separation of routing from business logic |
| `backend/app/services/` | Business Logic | Isolated AI, Scraper, and Data Logic |
| `backend/app/core/` | Configuration | Pydantic Settings for .env management |
| `backend/app/db/` | Persistence | Modular SQLite initialization and queries |
| `backend/app/models/` | Data Transfer Objects | Pydantic schemas for API consistency |

---

### **🚀 Core Objective Met**
- **Decoupled Architecture**: Scrapers, AI Scoring, and Routes are no longer mixed.
- **High Availability**: Automatic HTML fallback if GitHub API rate-limits the app.
- **Scalable Config**: Unified `.env` management with validation.
- **Judge-Ready**: Clean folder structure, production-grade logic.

---

### **🛠 Quick Start**

#### **1. Environment Setup**
Ensure your `.env` contains:
```env
GROQ_API_KEY=your_key_here
GITHUB_TOKEN=optional_but_helps
```

#### **2. Running the SaaS Backend**
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

---

### **📂 Project Structure**
```text
MentorIQ/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── core/
│   │   ├── db/
│   │   └── main.py
│   └── data/            # Persistence Layer
├── frontend/            # Glassmorphism UI
└── .env                 # Global Config
```

---
*Refactored by Principal Engineer for Ignite Hack 2.0*
