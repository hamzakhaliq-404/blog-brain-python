"""
Pytest configuration and fixtures for Blog Brain tests.
"""

import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def setup_environment():
    """Setup test environment with API keys."""
    from config import settings
    
    # Set GOOGLE_API_KEY for Gemini
    os.environ['GOOGLE_API_KEY'] = settings.gemini_api_key
    
    yield settings
    
    # Cleanup if needed
    pass


@pytest.fixture
def sample_topic():
    """Sample topic for testing."""
    return "The Future of AI in Healthcare"


@pytest.fixture
def sample_audience():
    """Sample target audience."""
    return "Healthcare professionals"


@pytest.fixture
def sample_tone():
    """Sample tone."""
    return "professional"


@pytest.fixture
def mock_search_results():
    """Mock search results for testing."""
    return [
        {
            "title": "AI in Healthcare: A Comprehensive Review",
            "link": "https://example.com/article1",
            "snippet": "Artificial intelligence is transforming healthcare...",
            "position": 1
        },
        {
            "title": "Machine Learning Applications in Medicine",
            "link": "https://example.com/article2",
            "snippet": "Machine learning algorithms are being used...",
            "position": 2
        }
    ]


@pytest.fixture
def mock_scrape_result():
    """Mock scrape result for testing."""
    return {
        "url": "https://example.com/article",
        "title": "AI Transforming Healthcare",
        "content": "This is sample content about AI in healthcare. " * 50,
        "word_count": 250,
        "success": True
    }
