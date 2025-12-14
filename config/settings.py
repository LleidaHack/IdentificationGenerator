"""
Settings module using Pydantic for type-safe configuration management.
Loads configuration from environment variables with .env file support.
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # Edition Configuration
    EDITION: str = Field(default="2025", description="Event edition year")
    TEST: bool = Field(default=False, description="Test mode flag")
    
    # Database Paths
    DB_PATH_T: str = Field(
        default="hackeps-2025/dev/users",
        description="Test/development database path"
    )
    DB_PATH: str = Field(
        default="hackeps-2025/prod/users",
        description="Production database path"
    )
    
    # API Configuration
    BASE_URL: str = Field(
        default="http://localhost:8000",
        description="Backend API base URL"
    )
    SERVICE_TOKEN: str = Field(
        default="dummy_token",
        description="Service authentication token"
    )
    
    # Folder Paths (with sensible defaults)
    EDITIONS_FOLDER: str = Field(default="editions", description="Editions folder name")
    OUT_FOLDER: str = Field(default="_out_", description="Output folder name")
    RES_FOLDER: str = Field(default="resources", description="Resources folder name")
    FONT_FOLDER: str = Field(default="fonts", description="Fonts folder name")
    
    # File Names
    DATA_FILE: str = Field(default="data.json", description="Data file name")
    DB_CERT: str = Field(
        default="2019_firebase_cert.json",
        description="Firebase certificate file name"
    )
    FONT_FILE: str = Field(
        default="SpaceMono-Regular.ttf",
        description="Regular font file name"
    )
    BOLD_FONT_FILE: str = Field(
        default="SpaceMono-Bold.ttf",
        description="Bold font file name"
    )
    
    # Template Files (relative paths within edition folder)
    BAK_FILE_CONTESTANT: str = Field(
        default="plantilles/participant.png",
        description="Contestant card template"
    )
    BAK_FILE_STAFF: str = Field(
        default="plantilles/organitzador.png",
        description="Staff card template"
    )
    BAK_FILE_EMPRESA: str = Field(
        default="plantilles/patrocinador.png",
        description="Company card template"
    )
    
    @property
    def db_path(self) -> str:
        """Get the appropriate database path based on TEST mode."""
        return self.DB_PATH_T if self.TEST else self.DB_PATH


# Singleton instance
settings = Settings()
