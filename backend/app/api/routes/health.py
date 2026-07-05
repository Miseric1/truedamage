"""
Health check lives in its own route module (not bolted onto main.py) because
every future route module (summoners.py, matches.py, ...) will follow this
same pattern: an APIRouter, registered in main.py. Keeping health.py as the
first example makes that convention obvious from day one.
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
