import logging
import logging.config

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from libredte.api_client import ApiException
from requests.exceptions import ConnectionError, Timeout

from .auth.router import router as auth_router
from .config import settings
from .db import Base, engine
from .routers.cobros import router as cobros_router
from .routers.contribuyentes import router as contribuyentes_router
from .routers.dte import router as dte_router
from .routers.sistema import router as sistema_router

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Base de datos inicializada")
    yield


app = FastAPI(
    title="LibreDTE API",
    description="Wrapper REST sobre el cliente oficial de LibreDTE",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ApiException)
async def api_exception_handler(request: Request, exc: ApiException):
    status = exc.code if exc.code and 400 <= exc.code < 600 else 502
    return JSONResponse(status_code=status, content={"detail": str(exc)})


@app.exception_handler(Timeout)
async def timeout_handler(request: Request, exc: Timeout):
    return JSONResponse(status_code=504, content={"detail": "LibreDTE no respondió a tiempo"})


@app.exception_handler(ConnectionError)
async def conn_error_handler(request: Request, exc: ConnectionError):
    return JSONResponse(status_code=502, content={"detail": "No se pudo conectar a LibreDTE"})


app.include_router(auth_router)
app.include_router(dte_router)
app.include_router(contribuyentes_router)
app.include_router(cobros_router)
app.include_router(sistema_router)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
