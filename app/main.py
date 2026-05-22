import logging
import logging.config

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(auth_router)
app.include_router(dte_router)
app.include_router(contribuyentes_router)
app.include_router(cobros_router)
app.include_router(sistema_router)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
