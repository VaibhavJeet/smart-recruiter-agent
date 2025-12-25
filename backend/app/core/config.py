"""Application configuration."""

from typing import List, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "smart-recruiter-agent"
    app_env: str = "development"
    debug: bool = True

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000"]

    llm_provider: Literal["openai", "anthropic", "ollama", "llamacpp"] = "openai"

    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-sonnet-20240229"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    llamacpp_model_path: str = ""
    llamacpp_n_ctx: int = 4096

    database_url: str = "sqlite+aiosqlite:///./data/recruiter.db"
    chroma_persist_dir: str = "./data/chroma"


settings = Settings()