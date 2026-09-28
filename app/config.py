from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    app_name: str = "ComicCraft"

    app_host: str = "127.0.0.1"

    app_port: int = 8000

    # Gemini
    gemini_api_key: str | None = None

    gemini_flash_model: str = "gemini-3.8-flash"

    gemini_pro_model: str = "gemini-3.8-flash"

    # Hugging Face
    hf_token: str | None = None

    hf_api_key: str | None = None

    hf_image_model: str = (
        "black-forest-labs/FLUX.1-schnell"
    )

    image_provider: str = "placeholder"

    # Development
    mock_ai: bool = True

    # Directories
    static_dir: Path = BASE_DIR / "static"

    template_dir: Path = BASE_DIR / "templates"

    panel_dir: Path = BASE_DIR / "static" / "panels"

    export_dir: Path = BASE_DIR / "static" / "exports"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def effective_hf_token(self) -> str | None:
        return self.hf_token or self.hf_api_key


@lru_cache
def get_settings() -> Settings:

    settings = Settings()

    settings.panel_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    settings.export_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return settings