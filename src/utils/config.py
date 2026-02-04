from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    name: str = Field(default="app_db")
    user: str = Field(default="postgres")
    password: str = Field(default="password")
    pool_size: int = Field(default=10)
    max_overflow: int = Field(default=25)
    echo: bool = Field(default=False)
    echo_pool: bool = Field(default=False)

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def dsn(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

class LLMSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LLM_")

    api_key: str = Field(default="llm-secret-api-key")
    url: str = Field(default="https://openrouter.ai/api/v1")
    model: str = Field(default="gpt-5-mini")


class TGBotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TG_BOT_")

    token: str = Field(default="tg-bot-secret-token")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    db: DatabaseSettings = DatabaseSettings()
    llm: LLMSettings = LLMSettings()
    bot: TGBotSettings = TGBotSettings()
    environment: str = Field(default="development")


settings = Settings()