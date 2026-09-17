# LibreDTE API

REST API wrapper sobre el [cliente oficial Python de LibreDTE](https://github.com/LibreDTE/libredte-api-client-python), para exponer documentos tributarios electrónicos (DTE) chilenos como una API interna con autenticación propia.

LibreDTE entrega un cliente Python sincrónico pensado para scripts. Este proyecto lo convierte en un servicio HTTP con autenticación JWT, manejo de errores uniforme y documentación interactiva, sin perder la compatibilidad con el cliente oficial.

## Stack

- **FastAPI** + **uvicorn** (ASGI)
- **libredte** — cliente oficial, módulos `Dte`, `Contribuyentes`, `Cobros`, `Moneda`
- **SQLAlchemy 2.0 async** + **Alembic** — tabla `users` para autenticación
- **python-jose** + **pwdlib[bcrypt]** — JWT HS256 y hashing de contraseñas
- **pytest** — 8 tests de autenticación y de los endpoints de DTE

## Decisiones de diseño

Las tres decisiones que definen el proyecto:

**1. Endpoints síncronos sobre un cliente síncrono.** El cliente oficial de LibreDTE usa `requests`, que bloquea. Declarar sus endpoints como `async def` los ejecutaría en el event loop y bloquearía todo el servidor en cada llamada al SII. Están declarados como `def`, así FastAPI los despacha a su threadpool y el loop queda libre. Los endpoints que solo tocan la base de datos sí son `async def`.

**2. Un solo lugar para los errores del proveedor.** `app/libredte_error.py` traduce las `ApiException` del cliente oficial a respuestas HTTP con forma estable, vía un exception handler global. Los routers no repiten `try/except` y el consumidor recibe siempre el mismo contrato de error, venga de donde venga la falla.

**3. FastAPI en vez de Node.** El resto del ecosistema es TypeScript, pero LibreDTE solo publica cliente oficial para Python. La alternativa era reimplementar a mano el wrapper HTTP contra la API del SII y hacerse cargo de mantenerlo. El costo de introducir un segundo lenguaje era menor que el de mantener esa reimplementación.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env
# Editar .env con tu LIBREDTE_HASH, LIBREDTE_RUT y un JWT_SECRET propio

alembic upgrade head
uvicorn app.main:app --reload
```

Swagger interactivo en `http://localhost:8000/docs`.

## Autenticación

1. `POST /auth/register` → crear usuario
2. `POST /auth/login` → obtener `access_token`
3. Enviar `Authorization: Bearer <token>` en el resto de las llamadas

El `JWT_SECRET` se genera con:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Endpoints

| Método | Path | Descripción |
|--------|------|-------------|
| `POST` | `/auth/register` | Crear usuario |
| `POST` | `/auth/login` | Obtener token JWT |
| `POST` | `/dte/emitidos/buscar` | Buscar DTEs emitidos con filtros |
| `GET`  | `/dte/emitidos/{dte}/{folio}/{emisor}` | Detalle de un DTE real |
| `GET`  | `/dte/emitidos/{dte}/{folio}/{emisor}/pdf` | PDF del DTE |
| `POST` | `/dte/recibidos/buscar` | Buscar DTEs recibidos |
| `POST` | `/dte/temporales/emitir` | Emitir DTE temporal |
| `POST` | `/dte/generar` | Generar DTE real desde uno temporal |
| `GET`  | `/contribuyentes/{rut}` | Información de un contribuyente |
| `POST` | `/cobros/buscar` | Buscar cobros |
| `GET`  | `/sistema/moneda/{to}/{fecha}` | Tasa de cambio USD→{to} |

## Tests

```bash
pytest -q
```

Las llamadas a LibreDTE están mockeadas: los tests corren sin credenciales y sin tocar el SII.

## Docker

```bash
docker build -t libredte-api .
docker run -p 8000:8000 --env-file .env libredte-api
```

## Variables de entorno

Todas están documentadas en `.env.example`. Ninguna credencial vive en el código: la app falla al arrancar si `LIBREDTE_HASH` o `JWT_SECRET` no están definidos.

## Estado

Proyecto funcional, no desplegado en producción. Base de datos SQLite en desarrollo y PostgreSQL en producción vía `DATABASE_URL`.
