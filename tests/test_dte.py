import pytest
from unittest.mock import MagicMock, patch


@pytest.mark.asyncio
async def test_buscar_emitidos(client, auth_headers):
    mock_resp = MagicMock()
    mock_resp.json.return_value = [{"folio": 1}]

    mock_client = MagicMock()
    mock_client.get_dte_emitidos.return_value = mock_resp

    with patch("app.routers.dte.get_dte", return_value=mock_client):
        r = await client.post(
            "/dte/emitidos/buscar",
            json={"emisor": "76192083-9", "filtros": {}},
            headers=auth_headers,
        )
    assert r.status_code == 200
    assert r.json() == [{"folio": 1}]


@pytest.mark.asyncio
async def test_contribuyente_info(client, auth_headers):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"rut": "76192083-9", "nombre": "Empresa Test"}

    mock_client = MagicMock()
    mock_client.get_contribuyente.return_value = mock_resp

    with patch("app.routers.contribuyentes.get_contribuyentes", return_value=mock_client):
        r = await client.get("/contribuyentes/76192083-9", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["rut"] == "76192083-9"


@pytest.mark.asyncio
async def test_buscar_requiere_auth(client):
    r = await client.post("/dte/emitidos/buscar", json={"emisor": "76192083-9"})
    assert r.status_code == 401
