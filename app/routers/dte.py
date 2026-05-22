from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..auth.models import User
from ..deps import get_current_user
from ..libredte_client import get_dte
from ..libredte_error import call_libredte

router = APIRouter(prefix="/dte", tags=["dte"])


# ── DTEs emitidos ───────────────────────────────────────────────────────────


class BuscarEmitidosRequest(BaseModel):
    emisor: str
    filtros: dict[str, Any] = {}


@router.post("/emitidos/buscar")
def buscar_emitidos(body: BuscarEmitidosRequest, _: User = Depends(get_current_user)):
    """Busca DTEs emitidos por un RUT emisor con filtros opcionales."""
    client = get_dte()
    return call_libredte(client.get_dte_emitidos, body.emisor, body.filtros)


@router.get("/emitidos/{dte}/{folio}/{emisor}")
def get_emitido(dte: int, folio: int, emisor: str, _: User = Depends(get_current_user)):
    """Detalle de un DTE real emitido."""
    client = get_dte()
    return call_libredte(client.get_dte_real, dte, folio, emisor)


@router.get("/emitidos/{dte}/{folio}/{emisor}/pdf")
def pdf_emitido(dte: int, folio: int, emisor: str, _: User = Depends(get_current_user)):
    """PDF de un DTE real emitido (devuelve bytes en base64)."""
    from fastapi.responses import Response
    from ..libredte_error import libredte_to_http
    from libredte.api_client import ApiException
    from requests.exceptions import ConnectionError, Timeout

    client = get_dte()
    try:
        resp = client.get_pdf_dte_real(dte, folio, emisor)
        return Response(content=resp.content, media_type="application/pdf")
    except (ApiException, Timeout, ConnectionError) as exc:
        raise libredte_to_http(exc) from exc


@router.post("/emitidos/consultar")
def consultar_emitidos(filtros: dict[str, Any], _: User = Depends(get_current_user)):
    """Consulta DTEs emitidos con filtros genéricos."""
    client = get_dte()
    return call_libredte(client.dte_emitidos_consultar, filtros)


# ── DTEs recibidos ──────────────────────────────────────────────────────────


class BuscarRecibidosRequest(BaseModel):
    receptor: str
    filtros: dict[str, Any] = {}


@router.post("/recibidos/buscar")
def buscar_recibidos(body: BuscarRecibidosRequest, _: User = Depends(get_current_user)):
    """Busca DTEs recibidos por un RUT receptor con filtros opcionales."""
    client = get_dte()
    return call_libredte(client.get_dte_recibidos, body.receptor, body.filtros)


@router.get("/recibidos/{emisor}/{dte}/{folio}/{receptor}")
def get_recibido(emisor: str, dte: int, folio: int, receptor: str, _: User = Depends(get_current_user)):
    """Detalle de un DTE recibido."""
    client = get_dte()
    return call_libredte(client.get_dte_recibido, emisor, dte, folio, receptor)


# ── DTEs temporales ─────────────────────────────────────────────────────────


@router.post("/temporales/emitir")
def emitir_temporal(dte_temporal: dict[str, Any], _: User = Depends(get_current_user)):
    """Emite un DTE temporal."""
    client = get_dte()
    return call_libredte(client.emitir_dte_temporal, dte_temporal)


class BuscarTemporalesRequest(BaseModel):
    emisor: str
    filtros: dict[str, Any] = {}


@router.post("/temporales/buscar")
def buscar_temporales(body: BuscarTemporalesRequest, _: User = Depends(get_current_user)):
    """Lista DTEs temporales de un emisor."""
    client = get_dte()
    return call_libredte(client.get_dte_temporales, body.emisor, body.filtros)


@router.get("/temporales/{receptor}/{dte}/{codigo}/{emisor}")
def get_temporal(receptor: str, dte: int, codigo: str, emisor: str, _: User = Depends(get_current_user)):
    """Detalle de un DTE temporal."""
    client = get_dte()
    return call_libredte(client.get_dte_temporal, receptor, dte, codigo, emisor)


# ── Generar DTE real desde temporal ─────────────────────────────────────────


@router.post("/generar")
def generar_real(dte_real: dict[str, Any], _: User = Depends(get_current_user)):
    """Genera un DTE real a partir de un DTE temporal."""
    client = get_dte()
    return call_libredte(client.emitir_dte_real, dte_real)


# ── Email ────────────────────────────────────────────────────────────────────


class EmailRequest(BaseModel):
    data_email: dict[str, Any]


@router.post("/emitidos/{dte}/{folio}/{emisor}/email")
def email_emitido(dte: int, folio: int, emisor: str, body: EmailRequest, _: User = Depends(get_current_user)):
    """Envía por email un DTE real emitido."""
    client = get_dte()
    return call_libredte(client.dte_real_enviar_email, dte, folio, emisor, body.data_email)
