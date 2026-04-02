# 🏛️ MentorIQ Architecture Overview

MentorIQ is built using a **SaaS-inspired modular architecture** to ensure scalability, ease of testing, and isolation of business logic.

---

### **1. 🛤️ Request Flow**
1.  **Client (Frontend)**: Sends a `GET /api/analyze?username=...` request.
2.  **API Layer (`audit_api.py`)**: Sanitizes input and initiates data fetching.
3.  **Data Fetcher (`github_service.py`)**: 
    - Attempts to pull profile data via REST API.
    - If rate-limited (403/429), it automatically triggers a **BeautifulSoup4-based scraper** fallback to maintain high availability.
    - Fetches the `README.md` and repo file structure for deep context.
4.  **AI Engine (`audit_service.py`)**:
    - Constructs a highly structured prompt (Principcal Engineer Audit).
    - Uses **Llama-3.3-70b (via GROQ)** for deterministic JSON output.
    - Evaluates five key metrics: Code Quality, Architecture, Engineering Practices, Project Depth, and Problem Solving.
5.  **Database Layer (`database.py`)**:
    - Executes a **Weighted Matching Algorithm** between the AI-derived career path and the 25+ industry experts in the SQLite database.
6.  **Response**: Returns a complete audit report with real-time mentor recommendations.

---

### **2. 🗄️ Persistence Layer**
- **SQLite3**: Used to store professional mentor profiles.
- **Dynamic Seeding**: The system automatically initializes and seeds the database with realistic industry mentors (Google, Meta, Uber, etc.) if it's missing or empty.

---

### **3. 🛡️ Fault Tolerance**
- **Graceful Fallback**: If `GROQ_API_KEY` is missing, the service provides an actionable error message (`detail`) instead of a 500 crash.
- **GitHub API Failover**: The application handles rate-limiting gracefully by switching to raw HTML scraping for essential profile info.

---

### **4. 🎨 Design Principles**
- **Single Responsibility**: Scrapers, AI logic, and API routes are strictly separated.
- **Configuration over Hardcoding**: Unified `.env` management via Pydantic Settings throughout the app.
- **Premium UX**: Responsive, glassmorphism-based frontend with real-time loading feedback.
