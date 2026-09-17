from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Placeholder shipped in .env.example. Refused at startup so a deployment can
# never run on a secret that is published in this repository.
_JWT_SECRET_PLACEHOLDER = "cambia_esto_por_un_valor_aleatorio_de_64_chars"
_JWT_SECRET_MIN_LENGTH = 32


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    LIBREDTE_HASH: str = ""
    LIBREDTE_URL: str = ""       # vacío = usa la nube de LibreDTE
    LIBREDTE_RUT: str = ""       # RUT contribuyente (sin puntos, sin DV)
    LIBREDTE_AMBIENTE: str = ""  # "produccion" o "pruebas"

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = "sqlite+aiosqlite:///./dev.db"

    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    @field_validator("JWT_SECRET")
    @classmethod
    def _reject_weak_jwt_secret(cls, value: str) -> str:
        if value == _JWT_SECRET_PLACEHOLDER:
            raise ValueError(
                "JWT_SECRET is still the placeholder from .env.example. "
                'Generate one with: python -c "import secrets; print(secrets.token_hex(32))"'
            )
        if len(value) < _JWT_SECRET_MIN_LENGTH:
            raise ValueError(
                f"JWT_SECRET must be at least {_JWT_SECRET_MIN_LENGTH} characters long."
            )
        return value

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]


settings = Settings()
