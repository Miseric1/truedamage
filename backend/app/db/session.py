"""
Engine + session factory only. No models here on purpose — model definitions
and Alembic migrations are their own session's work. This file exists now so
the DB layer has a clear home (app/db/) from the start, instead of being
invented ad hoc later and fought over where it should live.

get_db() is a generator dependency: FastAPI calls it per-request, hands the
yielded session to the route, then runs the `finally` block to close it once
the request is done — even if the route raises. This is the standard
SQLAlchemy + FastAPI dependency-injection pattern.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
