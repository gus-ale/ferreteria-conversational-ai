import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from openai import AsyncOpenAI
from prometheus_client import make_asgi_app

import app.models  # noqa: F401
from app.api.router import api_router
from app.core.config import settings
from app.core.errors import DomainError
from app.db.base import Base
from app.db.session import AsyncSessionLocal, engine
from app.middleware import RequestContextMiddleware
from app.repositories.knowledge import seed_knowledge
from app.repositories.products import seed_products

logger = logging.getLogger("ferreteria_conversational")
STATIC_DIR = Path(__file__).parent / "static"


def build_openai_client() -> AsyncOpenAI | None:
    if settings.ai_provider != "openai":
        return None
    return AsyncOpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
        timeout=settings.openai_timeout_seconds,
        max_retries=settings.openai_max_retries,
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    app.state.openai_client = build_openai_client()

    if settings.auto_create_tables:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    if settings.seed_demo_data:
        async with AsyncSessionLocal() as session:
            await seed_products(session)
            await seed_knowledge(session)

    logger.info(
        "application_started environment=%s provider=%s realtime=%s",
        settings.app_env,
        settings.ai_provider,
        settings.realtime_enabled,
    )
    yield

    if app.state.openai_client is not None:
        await app.state.openai_client.close()
    await engine.dispose()
    logger.info("application_stopped")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Asistente conversacional de portfolio con texto, voz Realtime, "
        "function calling, memoria, RAG, guardrails y derivación humana."
    ),
    lifespan=lifespan,
)

app.add_middleware(RequestContextMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Admin-Key", "X-Request-ID"],
)


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "request_id": getattr(request.state, "request_id", None),
            }
        },
    )


@app.exception_handler(Exception)
async def unexpected_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "unhandled_application_error request_id=%s",
        getattr(request.state, "request_id", None),
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_error",
                "message": "Ocurrió un error inesperado.",
                "request_id": getattr(request.state, "request_id", None),
            }
        },
    )


@app.get("/", include_in_schema=False)
async def web_app() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.include_router(api_router, prefix=settings.api_v1_prefix)
app.mount("/metrics", make_asgi_app())
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
