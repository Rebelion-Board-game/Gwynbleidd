# src/main.py
import uvicorn
import logging
import coloredlogs
import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fun.database import init_db, db_pool, get_db
from fun.api_developer import dev_router
from fun.api_godot import godot_router
from fun.limiter import limiter
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.staticfiles import StaticFiles


logging_level = os.getenv("logging_level","INFO")

coloredlogs.install(
    level=logging_level,
    fmt="%(levelname)s:     %(message)s",
    level_styles={
        "debug": {"color": "magenta"},
        "info": {"color": "blue"},
        "warning": {"color": "yellow"},
        "error": {"color": "red"},
    },
    field_styles={},
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before startup
    init_db()
    yield
    # After shutdown
    db_pool.close()



app = FastAPI(
    title="Gwynbleidd SaaS Backend", 
    description="High-performance connection-pooled SaaS backend",
    lifespan=lifespan,
    docs_url="/docs/godot",
    redoc_url="/docs/godot/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(godot_router)
app.include_router(dev_router, include_in_schema=False)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    try:
        uvicorn.run(
            "main:app", 
            host="0.0.0.0", 
            port=4443, 
            reload=True
        )
    except KeyboardInterrupt:
        logging.info("Application stop Ctrl+C")
        sys.exit(0)