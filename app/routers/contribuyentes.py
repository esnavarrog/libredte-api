from fastapi import APIRouter, Depends

from ..auth.models import User
from ..deps import get_current_user
from ..libredte_client import get_contribuyentes
from ..libredte_error import call_libredte

router = APIRouter(prefix="/contribuyentes", tags=["contribuyentes"])


@router.get("/{rut}")
def info(rut: str, _: User = Depends(get_current_user)):
    """Datos de un contribuyente por RUT (ej: 76192083-9)."""
    client = get_contribuyentes()
    return call_libredte(client.get_contribuyente, rut)
