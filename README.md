# 🎓 MentorIQ (GitMentor)

> **Stop Guessing. Let Your Code Find Your Mentor.**

MentorIQ is an AI-powered **Staff Engineer Audit** engine that analyzes your GitHub portfolio to find your perfect professional mentor. No resumes, no fluff—just pure code analysis.

---

## ✨ Features
- **🤖 AI Staff Audit**: Deep 5-pillar technical maturity check using Groq & Llama-3.3.
- **📊 1100px Dashboard**: High-density bento-style reports for strengths and skill gaps.
- **🎯 Mentor Matchmaking**: Intelligent pairing with industry pros based on your actual tech stack.
- **🚀 High Availability**: Automatic GitHub API fallback—works even without a personal token!
- **💎 Premium UI**: Sleek dark mode with glassmorphism and smooth animations.

---

## 🚀 Quick Start

### 1. Setup Environment
Clone the repo and create a `.env` file in the root:
```env
GROQ_API_KEY=your_key_here
GITHUB_TOKEN=optional_but_recommended
```

### 2. Run with Docker (Recommended)
```bash
docker-compose up --build
```
Open [http://localhost](http://localhost)

### 3. Local Development (Manual)
```bash
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

---

## 🛠 Tech Stack
- **Backend**: FastAPI (Python)
- **AI**: Groq (Llama-3.3-70B)
- **Frontend**: Vanilla JS, CSS3 (Glassmorphism), HTML5
- **Database**: SQLite3
- **DevOps**: Docker, Nginx

---

## 📁 Structure
- `/backend`: FastAPI server & AI logic.
- `/frontend`: Responsive UI & Dashboard.
- `/docs`: Architecture & Technical deep-dives.

---

### *Ignite Hack 2.0 Submission*
Created with 💻 by [khanolkarsujal](https://github.com/khanolkarsujal)
