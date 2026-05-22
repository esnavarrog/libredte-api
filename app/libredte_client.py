from functools import lru_cache

from libredte.api_client import ApiClient
from libredte.api_client.cobros import Cobros
from libredte.api_client.contribuyentes import Contribuyentes
from libredte.api_client.dte import Dte
from libredte.api_client.sistema import Moneda

from .config import settings


def _kwargs() -> dict:
    kw: dict = {"api_hash": settings.LIBREDTE_HASH}
    if settings.LIBREDTE_URL:
        kw["api_url"] = settings.LIBREDTE_URL
    if settings.LIBREDTE_RUT:
        kw["api_rut"] = settings.LIBREDTE_RUT
    return kw


@lru_cache(maxsize=1)
def get_libredte() -> ApiClient:
    url = settings.LIBREDTE_URL or None
    client = ApiClient(hash=settings.LIBREDTE_HASH, url=url)
    if settings.LIBREDTE_RUT:
        client.set_contribuyente(settings.LIBREDTE_RUT)
    if settings.LIBREDTE_AMBIENTE:
        client.set_ambiente_sii(settings.LIBREDTE_AMBIENTE)
    return client


@lru_cache(maxsize=1)
def get_dte() -> Dte:
    return Dte(api_hash=settings.LIBREDTE_HASH, api_url=settings.LIBREDTE_URL or None)


@lru_cache(maxsize=1)
def get_contribuyentes() -> Contribuyentes:
    return Contribuyentes(api_hash=settings.LIBREDTE_HASH, api_url=settings.LIBREDTE_URL or None)


@lru_cache(maxsize=1)
def get_cobros() -> Cobros:
    return Cobros(api_hash=settings.LIBREDTE_HASH, api_url=settings.LIBREDTE_URL or None)


@lru_cache(maxsize=1)
def get_moneda() -> Moneda:
    return Moneda(api_hash=settings.LIBREDTE_HASH, api_url=settings.LIBREDTE_URL or None)
