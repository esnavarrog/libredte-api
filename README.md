# LibreDTE API

REST API wrapper sobre el [cliente oficial Python de LibreDTE](https://github.com/LibreDTE/libredte-api-client-python).

## Stack

- **FastAPI** + **uvicorn** (ASGI)
- **libredte** (cliente oficial, módulos `Dte`, `Contribuyentes`, `Cobros`, `Moneda`)
- **SQLAlchemy 2.0 async** + **Alembic** (tabla `users` para JWT)
- **python-jose** + **passlib[bcrypt]** (autenticación JWT)

## Setup rápido

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env
# Editar .env con tu LIBREDTE_HASH, JWT_SECRET, LIBREDTE_RUT

alembic upgrade head
uvicorn app.main:app --reload
```

Abrir `http://localhost:8000/docs` para el Swagger interactivo.

## Autenticación

1. `POST /auth/register` → crear usuario
2. `POST /auth/login` → obtener `access_token`
3. Agregar header `Authorization: Bearer <token>` en todas las llamadas

## Endpoints principales

| Método | Path | Descripción |
|--------|------|-------------|
| `POST` | `/dte/emitidos/buscar` | Buscar DTEs emitidos con filtros |
| `GET`  | `/dte/emitidos/{dte}/{folio}/{emisor}` | Detalle DTE real |
| `GET`  | `/dte/emitidos/{dte}/{folio}/{emisor}/pdf` | PDF del DTE |
| `POST` | `/dte/recibidos/buscar` | Buscar DTEs recibidos |
| `POST` | `/dte/temporales/emitir` | Emitir DTE temporal |
| `POST` | `/dte/generar` | Generar DTE real desde temporal |
| `GET`  | `/contribuyentes/{rut}` | Info de un contribuyente |
| `POST` | `/cobros/buscar` | Buscar cobros |
| `GET`  | `/sistema/moneda/{to}/{fecha}` | Tasa de cambio USD→{to} |

## Tests

```bash
pip install pytest-mock
pytest -v
```

## Docker

```bash
docker build -t libredte-api .
docker run -p 8000:8000 --env-file .env libredte-api
```

## Variables de entorno

Ver `.env.example` para la lista completa.
