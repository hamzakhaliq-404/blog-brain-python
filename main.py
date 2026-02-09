"""
Blog Brain - FastAPI Server

Main application entry point for the Blog Brain content generation API.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from schemas.request_schema import ContentGenerationRequest, HealthCheckResponse
from schemas.response_schema import (
    ContentGenerationSuccessResponse,
    ContentGenerationErrorResponse
)
from crew import ContentGenerationCrew
from config import settings
from utils.logger import setup_logger
import time
from typing import Union

# Initialize logger
logger = setup_logger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Blog Brain API",
    description="AI-powered content generation system using multi-agent CrewAI architecture",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize crew instance
crew_instance = ContentGenerationCrew()


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("=" * 60)
    logger.info("🚀 Blog Brain API Starting...")
    logger.info(f"   Version: 1.0.0")
    logger.info(f"   Environment: {settings.gemini_model}")
    logger.info(f"   CORS Origins: {settings.allowed_origins}")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("=" * 60)
    logger.info("🛑 Blog Brain API Shutting Down...")
    logger.info("=" * 60)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information.
    
    Returns basic information about the API.
    """
    return {
        "service": "Blog Brain API",
        "version": "1.0.0",
        "description": "AI-powered content generation system",
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "generate": "/api/v1/generate-post"
        }
    }


@app.get(
    "/health",
    response_model=HealthCheckResponse,
    tags=["Health"]
)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current health status of the API.
    """
    return HealthCheckResponse(
        status="healthy",
        service="Blog Brain API",
        version="1.0.0"
    )


@app.post(
    "/api/v1/generate-post",
    response_model=Union[ContentGenerationSuccessResponse, ContentGenerationErrorResponse],
    tags=["Content Generation"],
    summary="Generate blog post",
    description="Generate a complete, SEO-optimized blog post using AI agents"
)
async def generate_post(
    request: ContentGenerationRequest
) -> Union[ContentGenerationSuccessResponse, ContentGenerationErrorResponse]:
    """
    Generate a complete blog post.
    
    This endpoint orchestrates multiple AI agents to:
    1. Research the topic comprehensively
    2. Create an SEO-optimized outline
    3. Write engaging, human-sounding content
    4. Perform editorial review and quality checks
    
    Args:
        request: ContentGenerationRequest with topic and parameters
        
    Returns:
        ContentGenerationSuccessResponse with generated content and metadata
        or ContentGenerationErrorResponse if generation fails
        
    Raises:
        HTTPException: For validation errors or server errors
        
    Example:
        POST /api/v1/generate-post
        {
            "topic": "The Future of AI in Healthcare",
            "target_audience": "Healthcare professionals",
            "tone": "professional"
        }
    """
    
    start_time = time.time()
    
    try:
        logger.info("=" * 60)
        logger.info(f"📝 New content generation request")
        logger.info(f"   Topic: {request.topic}")
        logger.info(f"   Audience: {request.target_audience or 'General'}")
        logger.info(f"   Tone: {request.tone}")
        logger.info("=" * 60)
        
        # Generate content using the crew
        result = crew_instance.generate_content(
            topic=request.topic,
            target_audience=request.target_audience,
            tone=request.tone,
            exclude_keywords=request.exclude_keywords
        )
        
        execution_time = time.time() - start_time
        
        # Check if generation was successful
        if result.get('status') == 'success':
            logger.info("=" * 60)
            logger.info(f"✅ Content generation successful")
            logger.info(f"   Execution time: {execution_time:.2f}s")
            logger.info("=" * 60)
            return result
        else:
            # Generation failed
            logger.error("=" * 60)
            logger.error(f"❌ Content generation failed")
            logger.error(f"   Error: {result.get('message', 'Unknown error')}")
            logger.error(f"   Execution time: {execution_time:.2f}s")
            logger.error("=" * 60)
            
            return ContentGenerationErrorResponse(
                status="error",
                message=result.get('message', 'Content generation failed'),
                execution_metadata=result.get('execution_metadata')
            )
    
    except ValueError as e:
        # Validation error
        logger.error(f"❌ Validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": "Invalid request parameters",
                "error": str(e)
            }
        )
    
    except Exception as e:
        # Unexpected server error
        execution_time = time.time() - start_time
        logger.error("=" * 60)
        logger.error(f"❌ Unexpected server error: {str(e)}")
        logger.error(f"   Execution time: {execution_time:.2f}s")
        logger.error("=" * 60)
        
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Internal server error",
                "error": str(e),
                "execution_time": round(execution_time, 2)
            }
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An unexpected error occurred",
            "error": str(exc)
        }
    )


# Run the application
if __name__ == "__main__":
    import uvicorn
    
    logger.info("\n" + "=" * 60)
    logger.info("Starting Blog Brain API Server")
    logger.info(f"Host: {settings.api_host}")
    logger.info(f"Port: {settings.api_port}")
    logger.info(f"Reload: {settings.api_reload}")
    logger.info(f"Docs: http://{settings.api_host}:{settings.api_port}/docs")
    logger.info("=" * 60 + "\n")
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )
