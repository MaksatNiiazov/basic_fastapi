from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiConfig(BaseModel):
    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    url: PostgresDsn = "postgresql+asyncpg://user:password@localhost:5432/db"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class LoggingConfig(BaseModel):
    level: str = "INFO"
    file_enabled: bool = True
    base_dir: str = "../fastapi_app_logs"
    request_dir: str = "requests"
    services_dir: str = "services"
    service_file_name: str = "service.log"
    request_file_name: str = "request.log"
    file_max_bytes: int = 10_000_000
    file_backup_count: int = 5
    console_enabled: bool = True


class CorsConfig(BaseModel):
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.example", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI_CONFIG__",
    )

    run: RunConfig = RunConfig()
    api: ApiConfig = ApiConfig()
    db: DatabaseConfig = DatabaseConfig()
    logging: LoggingConfig = LoggingConfig()
    cors: CorsConfig = CorsConfig()


settings = Settings()
