from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..auth.models import User
from ..deps import get_current_user
from ..libredte_client import get_cobros
from ..libredte_error import call_libredte

router = APIRouter(prefix="/cobros", tags=["cobros"])


class BuscarCobrosRequest(BaseModel):
    emisor: str
    filtros: dict[str, Any] = {}


@router.post("/buscar")
def buscar(body: BuscarCobrosRequest, _: User = Depends(get_current_user)):
    """Busca cobros de un emisor."""
    client = get_cobros()
    return call_libredte(client.get_cobros, body.emisor, body.filtros)


@router.get("/{codigo}/{emisor}")
def info(codigo: str, emisor: str, _: User = Depends(get_current_user)):
    """Detalle de un cobro."""
    client = get_cobros()
    return call_libredte(client.get_cobro_info, codigo, emisor)


class PagarRequest(BaseModel):
    datos: dict[str, Any]


@router.post("/{codigo}/{emisor}/pagar")
def pagar(codigo: str, emisor: str, body: PagarRequest, _: User = Depends(get_current_user)):
    """Realiza el pago de un cobro."""
    client = get_cobros()
    return call_libredte(client.pagar_cobro, codigo, emisor, body.datos)


@router.get("/dte-emitido/{dte}/{folio}/{emisor}")
def cobro_dte_emitido(dte: int, folio: int, emisor: str, _: User = Depends(get_current_user)):
    """Cobro asociado a un DTE real emitido."""
    client = get_cobros()
    return call_libredte(client.get_cobro_dte_real, dte, folio, emisor)


@router.get("/dte-temporal/{receptor}/{dte}/{codigo}/{emisor}")
def cobro_dte_temporal(receptor: str, dte: int, codigo: str, emisor: str, _: User = Depends(get_current_user)):
    """Cobro asociado a un DTE temporal."""
    client = get_cobros()
    return call_libredte(client.get_cobro_dte_temporal, receptor, dte, codigo, emisor)
