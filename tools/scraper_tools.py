"""
Web scraping tools for Blog Brain.

Provides functionality to scrape and extract content from web pages.
"""

from crewai_tools import tool
from bs4 import BeautifulSoup
import requests
from typing import Dict, Optional, List
from utils.logger import setup_logger
import time

logger = setup_logger(__name__)


@tool("Website Scraper Tool")
def scrape_website(url: str, max_content_length: int = 5000) -> Dict[str, str]:
    """
    Scrape and extract main content from a webpage.
    
    This tool fetches a webpage and extracts its title and main content,
    removing navigation, scripts, and other non-content elements.
    
    Args:
        url: Website URL to scrape
        max_content_length: Maximum content length in characters (default 5000)
        
    Returns:
        Dictionary with url, title, content, word_count, and error (if any)
        
    Example:
        >>> result = scrape_website("https://example.com/article")
        >>> print(result['title'])
        >>> print(f"Word count: {result['word_count']}")
    """
    try:
        logger.info(f"Scraping website: {url}")
        
        # Set user agent to avoid blocking
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'aside', 'header', 'form']):
            element.decompose()
        
        # Extract title
        title = None
        # Try h1 first
        h1 = soup.find('h1')
        if h1:
            title = h1.get_text(strip=True)
        # Fallback to title tag
        elif soup.title:
            title = soup.title.string.strip() if soup.title.string else ""
        else:
            title = "No title found"
        
        # Extract main content
        # Priority: article > main > body
        content_container = (
            soup.find('article') or 
            soup.find('main') or 
            soup.find('body')
        )
        
        if content_container:
            # Get text from paragraphs and headings
            content_tags = content_container.find_all(['p', 'h2', 'h3', 'h4', 'li'])
            content_parts = [tag.get_text(strip=True) for tag in content_tags if tag.get_text(strip=True)]
            content = ' '.join(content_parts)
        else:
            content = soup.get_text(strip=True)
        
        # Limit content length
        if len(content) > max_content_length:
            content = content[:max_content_length]
            logger.info(f"Content truncated to {max_content_length} characters")
        
        word_count = len(content.split())
        
        logger.info(f"Successfully scraped: {url} ({word_count} words)")
        
        return {
            "url": url,
            "title": title,
            "content": content,
            "word_count": word_count,
            "success": True
        }
        
    except requests.exceptions.Timeout:
        error_msg = f"Request timed out for {url}"
        logger.error(error_msg)
        return {
            "url": url,
            "title": "",
            "content": "",
            "word_count": 0,
            "error": error_msg,
            "success": False
        }
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed for {url}: {str(e)}"
        logger.error(error_msg)
        return {
            "url": url,
            "title": "",
            "content": "",
            "word_count": 0,
            "error": error_msg,
            "success": False
        }
        
    except Exception as e:
        error_msg = f"Scraping error for {url}: {str(e)}"
        logger.error(error_msg)
        return {
            "url": url,
            "title": "",
            "content": "",
            "word_count": 0,
            "error": error_msg,
            "success": False
        }


@tool("Batch Website Scraper")
def scrape_multiple_websites(urls: List[str], delay: float = 1.0) -> List[Dict[str, str]]:
    """
    Scrape multiple websites with rate limiting.
    
    Args:
        urls: List of URLs to scrape
        delay: Delay in seconds between requests (default 1.0)
        
    Returns:
        List of scraping results for each URL
        
    Example:
        >>> urls = ["https://example1.com", "https://example2.com"]
        >>> results = scrape_multiple_websites(urls, delay=1.5)
    """
    results = []
    
    for i, url in enumerate(urls):
        result = scrape_website(url)
        results.append(result)
        
        # Add delay between requests (except for last one)
        if i < len(urls) - 1:
            time.sleep(delay)
    
    successful = sum(1 for r in results if r.get('success', False))
    logger.info(f"Batch scraping complete: {successful}/{len(urls)} successful")
    
    return results


def extract_metadata(url: str) -> Dict[str, Optional[str]]:
    """
    Extract metadata from a webpage (meta tags, Open Graph, etc.).
    
    Args:
        url: Website URL
        
    Returns:
        Dictionary with metadata fields
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        metadata = {
            "title": soup.title.string if soup.title else None,
            "description": None,
            "keywords": None,
            "author": None,
            "og_title": None,
            "og_description": None,
            "og_image": None
        }
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            metadata["description"] = meta_desc.get('content')
        
        # Extract keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            metadata["keywords"] = meta_keywords.get('content')
        
        # Extract author
        meta_author = soup.find('meta', attrs={'name': 'author'})
        if meta_author:
            metadata["author"] = meta_author.get('content')
        
        # Extract Open Graph data
        og_title = soup.find('meta', property='og:title')
        if og_title:
            metadata["og_title"] = og_title.get('content')
        
        og_desc = soup.find('meta', property='og:description')
        if og_desc:
            metadata["og_description"] = og_desc.get('content')
        
        og_image = soup.find('meta', property='og:image')
        if og_image:
            metadata["og_image"] = og_image.get('content')
        
        logger.info(f"Extracted metadata from: {url}")
        return metadata
        
    except Exception as e:
        logger.error(f"Metadata extraction error for {url}: {str(e)}")
        return {}
