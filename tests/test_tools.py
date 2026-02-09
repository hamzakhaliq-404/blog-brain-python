"""
Unit tests for Blog Brain tools (search and scraper).
"""

import pytest
from tools.search_tools import google_search, news_search
from tools.scraper_tools import scrape_website
from unittest.mock import patch, MagicMock


class TestSearchTools:
    """Tests for search tools."""
    
    def test_google_search_imports(self):
        """Test that search tools can be imported."""
        assert google_search is not None
        assert news_search is not None
    
    @patch('tools.search_tools.requests.post')
    def test_google_search_success(self, mock_post, setup_environment):
        """Test successful Google search."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "organic": [
                {
                    "title": "Test Article",
                    "link": "https://test.com",
                    "snippet": "Test snippet",
                    "position": 1
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        # Execute search
        results = google_search("test query", num_results=1)
        
        # Verify
        assert len(results) == 1
        assert results[0]["title"] == "Test Article"
        assert results[0]["link"] == "https://test.com"
    
    @patch('tools.search_tools.requests.post')
    def test_news_search_success(self, mock_post, setup_environment):
        """Test successful news search."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "news": [
                {
                    "title": "Breaking News",
                    "link": "https://news.com",
                    "source": "NewsSource",
                    "date": "2026-02-09",
                    "snippet": "News content"
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        # Execute search
        results = news_search("test query", num_results=1)
        
        # Verify
        assert len(results) == 1
        assert results[0]["title"] == "Breaking News"
        assert results[0]["source"] == "NewsSource"
    
    @patch('tools.search_tools.requests.post')
    def test_search_error_handling(self, mock_post):
        """Test search error handling."""
        # Mock API error
        mock_post.side_effect = Exception("API Error")
        
        # Execute search - should return empty list on error
        results = google_search("test query")
        
        # Verify graceful error handling
        assert results == []


class TestScraperTools:
    """Tests for web scraper tools."""
    
    def test_scraper_imports(self):
        """Test that scraper tools can be imported."""
        assert scrape_website is not None
    
    @patch('tools.scraper_tools.requests.get')
    def test_scrape_website_success(self, mock_get):
        """Test successful website scraping."""
        # Mock HTML response
        mock_response = MagicMock()
        mock_response.content = b"""
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Test Title</h1>
                <article>
                    <p>Test paragraph 1.</p>
                    <p>Test paragraph 2.</p>
                </article>
            </body>
        </html>
        """
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Execute scrape
        result = scrape_website("https://test.com")
        
        # Verify
        assert result["success"] is True
        assert result["url"] == "https://test.com"
        assert "Test Title" in result["title"]
        assert result["word_count"] > 0
    
    @patch('tools.scraper_tools.requests.get')
    def test_scrape_timeout_handling(self, mock_get):
        """Test timeout error handling."""
        from requests.exceptions import Timeout
        
        # Mock timeout error
        mock_get.side_effect = Timeout("Request timed out")
        
        # Execute scrape
        result = scrape_website("https://test.com")
        
        # Verify graceful error handling
        assert result["success"] is False
        assert "error" in result
    
    @patch('tools.scraper_tools.requests.get')
    def test_scrape_content_truncation(self, mock_get):
        """Test content truncation to max_content_length."""
        # Mock large HTML response
        mock_response = MagicMock()
        large_content = "<p>" + ("word " * 2000) + "</p>"
        mock_response.content = f"<html><body>{large_content}</body></html>".encode()
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Execute scrape with limit
        result = scrape_website("https://test.com", max_content_length=100)
        
        # Verify content was truncated
        assert result["success"] is True
        assert len(result["content"]) <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
