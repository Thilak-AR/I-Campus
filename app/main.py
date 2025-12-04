from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db
from app.db.init_db import init_db
from app.api.v1.tenants import router as tenants_router
from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router
from app.api.v1.campuses import router as campuses_router


app = FastAPI(title="I-Campus API", version="0.1.0")


@app.on_event("startup")
def on_startup():
    init_db()


# Routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(tenants_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(campuses_router, prefix="/api/v1")


# Health endpoints (keep as is)
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1 AS test"))
    row = result.scalar()
    return {"db": "ok", "test": row}
