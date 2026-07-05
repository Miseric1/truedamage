"""
main.py is intentionally thin: create the app, wire middleware, include
routers. No route logic and no business logic lives here — that keeps this
file readable as the project grows to dozens of routers, instead of becoming
a 2000-line dumping ground.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Every route module gets included here, under a versioned prefix. Versioning
# from day one (/api/v1/...) means a future breaking change gets /api/v2/
# instead of breaking every existing client.
app.include_router(health.router, prefix="/api/v1")
