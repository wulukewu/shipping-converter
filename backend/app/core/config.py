from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Shipping Converter API"
    VERSION: str = "2.0.0"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # File upload settings
    UPLOAD_FOLDER: str = "uploads"
    MAX_FILE_SIZE: int = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS: set = {"xls", "xlsx", "xlsm"}
    
    # Discord settings
    DISCORD_WEBHOOK_URL: Optional[str] = None
    DISCORD_TOKEN: Optional[str] = None
    DISCORD_GUILD_ID: Optional[int] = None
    DISCORD_CHANNEL_ID: Optional[int] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
    @classmethod
    def from_env(cls):
        """Create settings from environment, handling empty strings"""
        webhook = os.getenv("DISCORD_WEBHOOK_URL", "")
        token = os.getenv("DISCORD_TOKEN", "")
        guild_str = os.getenv("DISCORD_GUILD_ID", "")
        channel_str = os.getenv("DISCORD_CHANNEL_ID", "")
        
        return cls(
            DISCORD_WEBHOOK_URL=webhook if webhook else None,
            DISCORD_TOKEN=token if token else None,
            DISCORD_GUILD_ID=int(guild_str) if guild_str and guild_str.isdigit() else None,
            DISCORD_CHANNEL_ID=int(channel_str) if channel_str and channel_str.isdigit() else None,
        )

settings = Settings.from_env()
