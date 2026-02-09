"""
API Request Schema - Pydantic Models

Defines the structure and validation rules for API requests
to the content generation endpoint.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List


class ContentGenerationRequest(BaseModel):
    """
    Request model for the content generation endpoint.
    
    This model validates incoming requests and ensures all required
    fields are present with valid values.
    """
    
    topic: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="The blog topic to write about",
        example="How AI is Transforming Customer Service in 2026"
    )
    
    target_audience: Optional[str] = Field(
        None,
        max_length=100,
        description="Optional target audience specification",
        example="Small business owners"
    )
    
    tone: str = Field(
        default="professional",
        description="Writing tone for the article",
        example="professional"
    )
    
    exclude_keywords: Optional[List[str]] = Field(
        default=None,
        description="Optional list of keywords/phrases to avoid",
        example=["game-changer", "revolutionary"]
    )
    
    @validator('topic')
    def validate_topic(cls, v):
        """Validate topic field."""
        if not v or v.strip() == "":
            raise ValueError("Topic cannot be empty")
        
        # Remove extra whitespace
        v = " ".join(v.split())
        
        return v
    
    @validator('tone')
    def validate_tone(cls, v):
        """Validate tone field."""
        allowed_tones = [
            "professional",
            "casual",
            "technical",
            "conversational",
            "formal",
            "friendly"
        ]
        
        v_lower = v.lower()
        if v_lower not in allowed_tones:
            raise ValueError(
                f"Tone must be one of: {', '.join(allowed_tones)}"
            )
        
        return v_lower
    
    @validator('exclude_keywords')
    def validate_exclude_keywords(cls, v):
        """Validate exclude_keywords field."""
        if v is None:
            return v
        
        # Remove empty strings and duplicates
        cleaned = list(set([kw.strip() for kw in v if kw.strip()]))
        
        # Limit to 20 keywords
        if len(cleaned) > 20:
            raise ValueError("Maximum 20 exclude keywords allowed")
        
        return cleaned
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "topic": "The Future of AI in Healthcare",
                "target_audience": "Healthcare professionals",
                "tone": "professional",
                "exclude_keywords": ["game-changer", "revolutionary"]
            }
        }


class HealthCheckResponse(BaseModel):
    """
    Response model for the health check endpoint.
    """
    
    status: str = Field(
        ...,
        description="Health status",
        example="healthy"
    )
    
    service: str = Field(
        ...,
        description="Service name",
        example="Blog Brain API"
    )
    
    version: str = Field(
        ...,
        description="API version",
        example="1.0.0"
    )
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "status": "healthy",
                "service": "Blog Brain API",
                "version": "1.0.0"
            }
        }
