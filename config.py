"""
Configuration management for Blog Brain using Pydantic Settings.

This module handles all environment variables and application settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be configured via .env file or environment variables.
    """
    
    # API Keys
    gemini_api_key: str
    gemini_model: str = "gemini-3-pro-preview"
    serper_api_key: str
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # CORS Settings (can be comma-separated string or list)
    allowed_origins: Union[List[str], str] = ["http://localhost:3000"]
    
    # Logging
    log_level: str = "INFO"
    
    # Agent Temperature Settings (controls creativity vs. determinism)
    researcher_temperature: float = 0.2  # Low for factual accuracy
    strategist_temperature: float = 0.4  # Balanced
    writer_temperature: float = 0.7      # High for creative writing
    editor_temperature: float = 0.3      # Low for consistency
    
    # Research Enhancement for AI Blogs
    enable_domain_filtering: bool = True          # Enable AI credible source filtering
    enable_fact_verification: bool = True         # Enable multi-source verification
    fact_verification_min_sources: int = 3        # Minimum sources for claim verification
    max_sources_per_category: int = 5             # Max results per source category
    prioritize_academic_sources: bool = True      # Prioritize academic over other sources
    
    # CrewAI Settings
    enable_memory: bool = True           # Agents remember context
    enable_delegation: bool = True       # Agents can delegate tasks
    max_iterations: int = 3              # Max task iterations
    
    @field_validator('allowed_origins', mode='before')
    @classmethod
    def parse_origins(cls, v):
        """Parse comma-separated string into list"""
        if isinstance(v, str):
            return [x.strip() for x in v.split(',')]
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra='ignore'
    )


# Global settings instance
settings = Settings()

