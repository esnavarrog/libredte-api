from fastapi import HTTPException
from libredte.api_client import ApiException
from requests.exceptions import ConnectionError, Timeout


def libredte_to_http(exc: Exception) -> HTTPException:
    if isinstance(exc, ApiException):
        status = exc.code if exc.code and 400 <= exc.code < 600 else 502
        return HTTPException(status_code=status, detail=str(exc))
    if isinstance(exc, Timeout):
        return HTTPException(status_code=504, detail="LibreDTE no respondió a tiempo")
    if isinstance(exc, ConnectionError):
        return HTTPException(status_code=502, detail="No se pudo conectar a LibreDTE")
    return HTTPException(status_code=502, detail=f"Error externo: {exc}")


def call_libredte(fn, *args, **kwargs):
    """Envuelve una llamada sincrónica al cliente LibreDTE y convierte errores."""
    try:
        response = fn(*args, **kwargs)
        return response.json()
    except (ApiException, Timeout, ConnectionError) as exc:
        raise libredte_to_http(exc) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Error inesperado: {exc}") from exc
