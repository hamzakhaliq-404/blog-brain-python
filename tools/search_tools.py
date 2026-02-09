"""
Search tools for Blog Brain using Serper.dev API.

Provides Google search functionality for the research agent.
"""

from crewai_tools import tool
import requests
from config import settings
from utils.logger import setup_logger
from typing import Dict, List, Any, Optional

logger = setup_logger(__name__)


@tool("Google Search Tool")
def google_search(query: str, num_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search Google using Serper.dev API.
    
    This tool performs Google searches and returns organic search results
    including titles, URLs, snippets, and positions.
    
    Args:
        query: Search query string
        num_results: Number of results to return (default 10, max 100)
        
    Returns:
        List of search results with title, link, snippet, and position
        
    Example:
        >>> results = google_search("AI in healthcare 2026", num_results=5)
        >>> print(results[0]['title'])
    """
    url = "https://google.serper.dev/search"
    
    payload = {
        "q": query,
        "num": min(num_results, 100),  # Serper max is 100
        "gl": "us",  # Geographic location
        "hl": "en"   # Language
    }
    
    headers = {
        "X-API-KEY": settings.serper_api_key,
        "Content-Type": "application/json"
    }
    
    try:
        logger.info(f"Searching Google for: '{query}' (requesting {num_results} results)")
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("organic", [])[:num_results]:
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "position": item.get("position", 0)
            })
        
        logger.info(f"Successfully retrieved {len(results)} search results")
        return results
        
    except requests.exceptions.Timeout:
        logger.error(f"Search request timed out for query: {query}")
        return []
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Search API request failed: {str(e)}")
        return []
        
    except KeyError as e:
        logger.error(f"Unexpected API response format: {str(e)}")
        return []
        
    except Exception as e:
        logger.error(f"Unexpected error during search: {str(e)}")
        return []


@tool("News Search Tool")
def news_search(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for recent news articles using Serper.dev API.
    
    Args:
        query: Search query string
        num_results: Number of news results to return (default 5)
        
    Returns:
        List of news articles with title, link, source, date, and snippet
        
    Example:
        >>> news = news_search("latest AI developments", num_results=3)
    """
    url = "https://google.serper.dev/news"
    
    payload = {
        "q": query,
        "num": min(num_results, 50)
    }
    
    headers = {
        "X-API-KEY": settings.serper_api_key,
        "Content-Type": "application/json"
    }
    
    try:
        logger.info(f"Searching news for: '{query}'")
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("news", [])[:num_results]:
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "source": item.get("source", ""),
                "date": item.get("date", ""),
                "snippet": item.get("snippet", "")
            })
        
        logger.info(f"Successfully retrieved {len(results)} news articles")
        return results
        
    except Exception as e:
        logger.error(f"News search error: {str(e)}")
        return []


def search_with_retry(query: str, num_results: int = 10, max_retries: int = 3) -> List[Dict[str, Any]]:
    """
    Search with automatic retry on failure.
    
    Args:
        query: Search query
        num_results: Number of results
        max_retries: Maximum retry attempts
        
    Returns:
        List of search results
    """
    for attempt in range(max_retries):
        results = google_search(query, num_results)
        if results:
            return results
        
        if attempt < max_retries - 1:
            logger.warning(f"Search attempt {attempt + 1} failed, retrying...")
            
    logger.error(f"All {max_retries} search attempts failed")
    return []
