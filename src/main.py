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
from fastapi.middleware.cors import CORSMiddleware

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
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(godot_router)
app.include_router(dev_router, include_in_schema=False)

if __name__ == "__main__":
    try:
        uvicorn.run(
            "main:app", 
            host="0.0.0.0", 
            port=8000, 
            reload=True
        )
    except KeyboardInterrupt:
        logging.info("Application stop Ctrl+C")
        sys.exit(0)