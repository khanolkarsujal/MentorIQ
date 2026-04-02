import os
from pathlib import Path
from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from fastapi.responses import FileResponse # type: ignore
from app.api.endpoints import audit_api
from app.db import database
from app.core.config import settings

# 1. Initialize DB
database.init_db()

# 2. Setup App
app = FastAPI(title=settings.PROJECT_NAME)

# 3. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Paths & Mount
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
frontend_path = PROJECT_ROOT / "frontend"
html_path = frontend_path / "index.html"

app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

# 5. Routes
app.include_router(audit_api.router, prefix=settings.API_V1_STR)

@app.get("/")
async def serve_home():
    return FileResponse(html_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

