import os
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from config.db import get_db
from routes.auth import router as auth_router
from routes.students import router as students_router


app = FastAPI(title="School Management API")

cors_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
# app.include_router(students_router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/health/db")
def database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        ) from exc

    return {"status": "ok", "database": "connected"}


FRONTEND_DIST = Path(__file__).resolve().parents[1] / "frontend" / "dist"


@app.get("/{frontend_path:path}")
def serve_frontend(frontend_path: str):
    if frontend_path == "api" or frontend_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")

    if not FRONTEND_DIST.is_dir():
        raise HTTPException(
            status_code=503,
            detail=(
                "React build not found. Run `npm run build` from the frontend "
                "directory before starting the production server."
            ),
        )

    requested_file = (FRONTEND_DIST / frontend_path).resolve()
    try:
        requested_file.relative_to(FRONTEND_DIST.resolve())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc

    if requested_file.is_file():
        return FileResponse(requested_file)

    index_file = FRONTEND_DIST / "index.html"
    if not index_file.is_file():
        raise HTTPException(
            status_code=503,
            detail="React build is incomplete: frontend/dist/index.html is missing.",
        )

    return FileResponse(index_file)
