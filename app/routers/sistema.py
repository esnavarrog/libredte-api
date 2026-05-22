from fastapi import APIRouter, Depends

from ..auth.models import User
from ..deps import get_current_user
from ..libredte_client import get_moneda
from ..libredte_error import call_libredte

router = APIRouter(prefix="/sistema", tags=["sistema"])


@router.get("/moneda/{to}/{fecha}")
def tasa_cambio(to: str, fecha: str, _: User = Depends(get_current_user)):
    """Tasa de cambio USD→{to} en la fecha YYYY-MM-DD indicada."""
    client = get_moneda()
    return call_libredte(client.get_moneda_cambios, to, fecha)
