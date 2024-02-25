"""FastAPI App Settings."""

from typing import List, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Applicator Settings Settings."""

    PROJECT_NAME: str = "Hackathon Backend API"
    PROJECT_DESCRIPTION: str = "Backend API for Hackathon API. Used to control the cell UI."
    PROJECT_VERSION: str = "0.0.1"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    APP_ENV: str = "prod"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, value: Union[str, List[str]]) -> Union[List[str], str]:
        """CORS Origin parsing."""
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        if isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    # class Config:
    #     """General Configurations."""
    #
    #     case_sensitive = True
    #     env_file = ".env"

    # General Configurations
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="allow",
    )
