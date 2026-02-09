"""
API Response Schema - Pydantic Models

Defines the structure for API responses from the content generation endpoint.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class MetaDataResponse(BaseModel):
    """Metadata for the generated content."""
    
    seo_title: str = Field(
        ...,
        description="SEO-optimized title (55-60 characters)",
        example="How AI Transforms Customer Service: Complete 2026 Guide"
    )
    
    meta_description: str = Field(
        ...,
        description="Meta description (150-160 characters)",
        example="Discover how AI is revolutionizing customer service in 2026. Learn implementation strategies, ROI metrics, and best practices for businesses."
    )
    
    slug: str = Field(
        ...,
        description="URL-friendly slug",
        example="ai-customer-service-2026-guide"
    )
    
    focus_keyword: str = Field(
        ...,
        description="Primary SEO keyword",
        example="AI customer service"
    )
    
    estimated_read_time: str = Field(
        ...,
        description="Estimated reading time",
        example="8 mins"
    )
    
    word_count: int = Field(
        ...,
        description="Total word count",
        example=1850
    )
    
    published_date: Optional[str] = Field(
        None,
        description="Publication date in ISO format",
        example="2026-02-09T12:00:00"
    )


class ContentResponse(BaseModel):
    """Content data including HTML and Markdown."""
    
    html_body: str = Field(
        ...,
        description="Full article in HTML format",
        example="<h1>How AI Transforms Customer Service</h1><p>Introduction...</p>"
    )
    
    markdown_body: str = Field(
        ...,
        description="Full article in Markdown format",
        example="# How AI Transforms Customer Service\n\nIntroduction..."
    )


class QualityChecksResponse(BaseModel):
    """Quality assurance checks performed."""
    
    ai_isms_removed: bool = Field(
        ...,
        description="Whether AI-sounding phrases were removed",
        example=True
    )
    
    citations_count: int = Field(
        ...,
        description="Number of citations/sources included",
        example=12
    )
    
    readability_score: str = Field(
        ...,
        description="Overall readability assessment",
        example="good"
    )
    
    seo_compliance: str = Field(
        ...,
        description="SEO requirements compliance status",
        example="passed"
    )
    
    human_sounding: bool = Field(
        ...,
        description="Whether content sounds authentically human",
        example=True
    )


class ContentDataResponse(BaseModel):
    """Main content data structure."""
    
    metadata: MetaDataResponse = Field(
        ...,
        description="SEO metadata and article information"
    )
    
    content: ContentResponse = Field(
        ...,
        description="Article content in HTML and Markdown"
    )
    
    sources: List[str] = Field(
        ...,
        description="List of source URLs cited in the article",
        example=[
            "https://example.com/ai-trends-2026",
            "https://research.com/customer-service-study"
        ]
    )
    
    quality_checks: Optional[QualityChecksResponse] = Field(
        None,
        description="Quality assurance check results"
    )
    
    editor_notes: Optional[str] = Field(
        None,
        description="Notes from the editorial review",
        example="Excellent article with strong citations"
    )


class ExecutionMetadataResponse(BaseModel):
    """Execution metadata for the generation process."""
    
    execution_time_seconds: float = Field(
        ...,
        description="Total execution time in seconds",
        example=45.2
    )
    
    topic: str = Field(
        ...,
        description="Original topic requested",
        example="The Future of AI in Healthcare"
    )
    
    target_audience: Optional[str] = Field(
        None,
        description="Target audience specification",
        example="Healthcare professionals"
    )
    
    tone: str = Field(
        ...,
        description="Writing tone used",
        example="professional"
    )
    
    timestamp: str = Field(
        ...,
        description="Generation timestamp",
        example="2026-02-09 12:30:45"
    )


class ContentGenerationSuccessResponse(BaseModel):
    """
    Success response for content generation.
    
    This is the main response model when content generation succeeds.
    """
    
    status: str = Field(
        default="success",
        description="Response status",
        example="success"
    )
    
    data: ContentDataResponse = Field(
        ...,
        description="Generated content and metadata"
    )
    
    execution_metadata: Optional[ExecutionMetadataResponse] = Field(
        None,
        description="Execution metadata and timing information"
    )
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "metadata": {
                        "seo_title": "How AI Transforms Customer Service: Complete Guide",
                        "meta_description": "Discover how AI revolutionizes customer service. Learn strategies, ROI metrics, and best practices.",
                        "slug": "ai-customer-service-guide",
                        "focus_keyword": "AI customer service",
                        "estimated_read_time": "8 mins",
                        "word_count": 1850,
                        "published_date": "2026-02-09T12:00:00"
                    },
                    "content": {
                        "html_body": "<h1>Title</h1><p>Content...</p>",
                        "markdown_body": "# Title\n\nContent..."
                    },
                    "sources": [
                        "https://example.com/source1",
                        "https://example.com/source2"
                    ],
                    "quality_checks": {
                        "ai_isms_removed": True,
                        "citations_count": 12,
                        "readability_score": "good",
                        "seo_compliance": "passed",
                        "human_sounding": True
                    }
                },
                "execution_metadata": {
                    "execution_time_seconds": 45.2,
                    "topic": "AI in Customer Service",
                    "tone": "professional",
                    "timestamp": "2026-02-09 12:30:45"
                }
            }
        }


class ErrorDetail(BaseModel):
    """Detailed error information."""
    
    error_type: Optional[str] = Field(
        None,
        description="Type of error that occurred",
        example="ValidationError"
    )
    
    error_message: str = Field(
        ...,
        description="Detailed error message",
        example="Topic field is required and must be between 5-200 characters"
    )


class ContentGenerationErrorResponse(BaseModel):
    """
    Error response for content generation.
    
    This is returned when content generation fails.
    """
    
    status: str = Field(
        default="error",
        description="Response status",
        example="error"
    )
    
    message: str = Field(
        ...,
        description="Error message",
        example="Content generation failed"
    )
    
    detail: Optional[ErrorDetail] = Field(
        None,
        description="Detailed error information"
    )
    
    execution_metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Execution metadata if available"
    )
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "status": "error",
                "message": "Content generation failed",
                "detail": {
                    "error_type": "APIError",
                    "error_message": "Serper API key is invalid"
                },
                "execution_metadata": {
                    "execution_time_seconds": 5.3,
                    "topic": "Test Topic",
                    "timestamp": "2026-02-09 12:30:45"
                }
            }
        }
