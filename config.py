"""
Configuration management for Blog Brain using Pydantic Settings.

This module handles all environment variables and application settings.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be configured via .env file or environment variables.
    """
    
    # API Keys
    gemini_api_key: str
    gemini_model: str = "gemini-1.5-pro"
    serper_api_key: str
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # CORS Settings
    allowed_origins: List[str] = ["http://localhost:3000"]
    
    # Logging
    log_level: str = "INFO"
    
    # Agent Temperature Settings (controls creativity vs. determinism)
    researcher_temperature: float = 0.2  # Low for factual accuracy
    strategist_temperature: float = 0.4  # Balanced
    writer_temperature: float = 0.7      # High for creative writing
    editor_temperature: float = 0.3      # Low for consistency
    
    # CrewAI Settings
    enable_memory: bool = True           # Agents remember context
    enable_delegation: bool = True       # Agents can delegate tasks
    max_iterations: int = 3              # Max task iterations
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        case_sensitive = False
        
        # Allow parsing comma-separated values for lists
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == 'allowed_origins':
                return [x.strip() for x in raw_val.split(',')]
            return raw_val


# Global settings instance
settings = Settings()
