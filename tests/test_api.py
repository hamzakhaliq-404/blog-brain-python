"""
Unit tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestAPIEndpoints:
    """Tests for API endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Blog Brain API"
        assert data["version"] == "1.0.0"
        assert "endpoints" in data
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Blog Brain API"
    
    @patch('main.crew_instance.generate_content')
    def test_generate_post_success(self, mock_generate, client):
        """Test successful post generation."""
        # Mock successful generation
        mock_generate.return_value = {
            "status": "success",
            "data": {
                "metadata": {
                    "seo_title": "Test Title",
                    "meta_description": "Test description",
                    "slug": "test-title",
                    "word_count": 1500
                },
                "content": {
                    "html_body": "<h1>Test</h1>",
                    "markdown_body": "# Test"
                },
                "sources": ["https://example.com"],
                "quality_checks": {
                    "ai_isms_removed": True,
                    "citations_count": 10
                }
            }
        }
        
        # Make request
        response = client.post(
            "/api/v1/generate-post",
            json={
                "topic": "The Future of AI",
                "target_audience": "Tech professionals",
                "tone": "professional"
            }
        )
        
        # Verify
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data
        assert data["data"]["metadata"]["seo_title"] == "Test Title"
    
    def test_generate_post_validation_error(self, client):
        """Test request validation."""
        # Missing required field
        response = client.post(
            "/api/v1/generate-post",
            json={
                "target_audience": "Tech professionals"
                # Missing 'topic'
            }
        )
        
        # Should return validation error
        assert response.status_code == 422
    
    def test_generate_post_topic_too_short(self, client):
        """Test topic length validation."""
        response = client.post(
            "/api/v1/generate-post",
            json={
                "topic": "AI",  # Too short (min 5 chars)
                "tone": "professional"
            }
        )
        
        # Should return validation error
        assert response.status_code == 422
    
    def test_generate_post_invalid_tone(self, client):
        """Test tone validation."""
        response = client.post(
            "/api/v1/generate-post",
            json={
                "topic": "The Future of AI in Healthcare",
                "tone": "invalid_tone"  # Not in allowed values
            }
        )
        
        # Should return validation error
        assert response.status_code == 422
    
    @patch('main.crew_instance.generate_content')
    def test_generate_post_server_error(self, mock_generate, client):
        """Test server error handling."""
        # Mock server error
        mock_generate.side_effect = Exception("Internal error")
        
        # Make request
        response = client.post(
            "/api/v1/generate-post",
            json={
                "topic": "The Future of AI",
                "tone": "professional"
            }
        )
        
        # Should return 500 error
        assert response.status_code == 500
        data = response.json()
        assert data["status"] == "error"


class TestCORSConfiguration:
    """Tests for CORS configuration."""
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present."""
        response = client.options(
            "/api/v1/generate-post",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
