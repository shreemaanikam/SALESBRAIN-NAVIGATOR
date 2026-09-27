from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.core.exceptions import global_exception_handler
from backend.app.api.v1.router import api_router
from backend.app.services.data_service import data_service

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up SalesBrain Navigator backend")
    try:
        data_service.load()
    except Exception as e:
        logger.error(f"Failed to load dataset on startup: {e}")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, global_exception_handler)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return RedirectResponse(url="/docs")
