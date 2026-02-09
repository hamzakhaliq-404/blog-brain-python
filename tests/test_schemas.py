"""
Unit tests for Pydantic schemas (request and response validation).
"""

import pytest
from schemas.request_schema import ContentGenerationRequest, HealthCheckResponse
from schemas.response_schema import (
    ContentGenerationSuccessResponse,
    MetaDataResponse,
    ContentResponse
)
from pydantic import ValidationError


class TestRequestSchema:
    """Tests for request schema validation."""
    
    def test_valid_request(self):
        """Test valid request creation."""
        request = ContentGenerationRequest(
            topic="The Future of AI in Healthcare",
            target_audience="Healthcare professionals",
            tone="professional",
            exclude_keywords=["game-changer"]
        )
        
        assert request.topic == "The Future of AI in Healthcare"
        assert request.target_audience == "Healthcare professionals"
        assert request.tone== "professional"
        assert "game-changer" in request.exclude_keywords
    
    def test_topic_too_short(self):
        """Test topic validation - too short."""
        with pytest.raises(ValidationError) as exc_info:
            ContentGenerationRequest(
                topic="AI",  # Too short
                tone="professional"
            )
        
        # Should have validation error
        assert exc_info.value is not None
    
    def test_topic_too_long(self):
        """Test topic validation - too long."""
        long_topic = "A" * 201  # Over 200 chars
        
        with pytest.raises(ValidationError):
            ContentGenerationRequest(
                topic=long_topic,
                tone="professional"
            )
    
    def test_invalid_tone(self):
        """Test tone validation with invalid value."""
        with pytest.raises(ValidationError):
            ContentGenerationRequest(
                topic="Valid Topic Here",
                tone="invalid_tone"  # Not in allowed values
            )
    
    def test_valid_tones(self):
        """Test all valid tone values."""
        valid_tones = ["professional", "casual", "technical", 
                      "conversational", "formal", "friendly"]
        
        for tone in valid_tones:
            request = ContentGenerationRequest(
                topic="Test Topic",
                tone=tone
            )
            assert request.tone == tone
    
    def test_tone_case_insensitive(self):
        """Test tone validation is case insensitive."""
        request = ContentGenerationRequest(
            topic="Test Topic",
            tone="PROFESSIONAL"  # Uppercase
        )
        
        assert request.tone == "professional"  # Should be lowercased
    
    def test_exclude_keywords_deduplication(self):
        """Test exclude keywords are deduplicated."""
        request = ContentGenerationRequest(
            topic="Test Topic",
            tone="professional",
            exclude_keywords=["test", "test", "word", "test"]
        )
        
        # Should have duplicates removed
        assert len(request.exclude_keywords) == 2
        assert "test" in request.exclude_keywords
        assert "word" in request.exclude_keywords
    
    def test_exclude_keywords_max_limit(self):
        """Test exclude keywords max limit."""
        with pytest.raises(ValidationError):
            ContentGenerationRequest(
                topic="Test Topic",
                tone="professional",
                exclude_keywords=["word"] * 21  # Over limit of 20
            )
    
    def test_optional_fields(self):
        """Test request with only required fields."""
        request = ContentGenerationRequest(
            topic="Test Topic"
        )
        
        assert request.topic == "Test Topic"
        assert request.target_audience is None
        assert request.tone == "professional"  # Default value
        assert request.exclude_keywords == []


class TestResponseSchema:
    """Tests for response schema validation."""
    
    def test_metadata_response(self):
        """Test metadata response creation."""
        metadata = MetaDataResponse(
            seo_title="Test Article Title",
            meta_description="This is a test meta description for an article",
            slug="test-article-title",
            focus_keyword="test keyword",
            estimated_read_time="5 mins",
            word_count=1500,
            published_date="2026-02-09T12:00:00Z"
        )
        
        assert metadata.seo_title == "Test Article Title"
        assert metadata.word_count == 1500
        assert len(metadata.slug) > 0
    
    def test_content_response(self):
        """Test content response creation."""
        content = ContentResponse(
            html_body="<h1>Test</h1><p>Content</p>",
            markdown_body="# Test\n\nContent"
        )
        
        assert "<h1>" in content.html_body
        assert "# Test" in content.markdown_body
    
    def test_health_check_response(self):
        """Test health check response."""
        health = HealthCheckResponse(
            status="healthy",
            service="Blog Brain API",
            version="1.0.0"
        )
        
        assert health.status == "healthy"
        assert health.service == "Blog Brain API"


class TestSchemaExamples:
    """Tests for schema examples."""
    
    def test_request_example_valid(self):
        """Test that request example is valid."""
        from schemas.request_schema import ContentGenerationRequest
        
        # The example from schema should be valid
        example_request = ContentGenerationRequest(
            topic="The Future of AI in Healthcare",
            target_audience="Healthcare professionals",
            tone="professional"
        )
        
        assert example_request is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
