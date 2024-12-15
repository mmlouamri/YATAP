from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_TITLE: str
    DATABASE_URL: str

    API_VERSION: str = "v1"
    API_PREFIX: str = "api"

    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    PASSWORD_RESET_EXPIRE_MINUTES: int


config = Config()  # type: ignore
