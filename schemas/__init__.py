"""
Schemas package for Blog Brain API.

Contains Pydantic models for request validation and response formatting.
"""

# Request schemas
from schemas.request_schema import (
    ContentGenerationRequest,
    HealthCheckResponse
)

# Response schemas
from schemas.response_schema import (
    MetaDataResponse,
    ContentResponse,
    QualityChecksResponse,
    ContentDataResponse,
    ExecutionMetadataResponse,
    ContentGenerationSuccessResponse,
    ErrorDetail,
    ContentGenerationErrorResponse
)

__all__ = [
    # Request models
    'ContentGenerationRequest',
    'HealthCheckResponse',
    
    # Response models
    'MetaDataResponse',
    'ContentResponse',
    'QualityChecksResponse',
    'ContentDataResponse',
    'ExecutionMetadataResponse',
    'ContentGenerationSuccessResponse',
    'ErrorDetail',
    'ContentGenerationErrorResponse'
]
