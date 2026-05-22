from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    LIBREDTE_HASH: str = ""
    LIBREDTE_URL: str = ""       # vacío = usa la nube de LibreDTE
    LIBREDTE_RUT: str = ""       # RUT contribuyente (sin puntos, sin DV)
    LIBREDTE_AMBIENTE: str = ""  # "produccion" o "pruebas"

    JWT_SECRET: str = "cambia_esto_en_produccion"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = "sqlite+aiosqlite:///./dev.db"

    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]


settings = Settings()
