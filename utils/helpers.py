"""
Helper utility functions for Blog Brain.

Common functions used across the application.
"""

import re
from typing import Dict, Any


def generate_slug(title: str) -> str:
    """
    Generate a URL-friendly slug from a title.
    
    Args:
        title: The title to convert to a slug
        
    Returns:
        URL-friendly slug string
        
    Example:
        >>> generate_slug("The Future of AI in Healthcare")
        'the-future-of-ai-in-healthcare'
    """
    # Convert to lowercase
    slug = title.lower()
    
    # Remove any characters that aren't alphanumeric, spaces, or hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    
    # Replace spaces and underscores with hyphens
    slug = re.sub(r'[\s_-]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug


def calculate_reading_time(text: str, words_per_minute: int = 200) -> str:
    """
    Calculate estimated reading time for text content.
    
    Args:
        text: The text content to analyze
        words_per_minute: Average reading speed (default: 200 WPM)
        
    Returns:
        Formatted reading time string (e.g., "5 mins")
        
    Example:
        >>> calculate_reading_time("This is a short article...")
        '1 min'
    """
    # Count words
    words = len(text.split())
    
    # Calculate minutes (minimum 1 minute)
    minutes = max(1, round(words / words_per_minute))
    
    # Format output
    return f"{minutes} min{'s' if minutes > 1 else ''}"


def sanitize_html(html: str) -> str:
    """
    Basic HTML sanitization to remove potentially harmful content.
    
    Args:
        html: HTML string to sanitize
        
    Returns:
        Sanitized HTML string
        
    Example:
        >>> sanitize_html("<p>Safe content</p><script>alert('bad')</script>")
        '<p>Safe content</p>'
    """
    # Remove script tags and their content
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove iframe tags
    html = re.sub(r'<iframe[^>]*>.*?</iframe>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove style tags (optional - uncomment if needed)
    # html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove onclick and other event handlers
    html = re.sub(r'\s*on\w+\s*=\s*["\'][^"\']*["\']', '', html, flags=re.IGNORECASE)
    
    return html


def truncate_text(text: str, max_length: int = 160, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length, adding suffix if truncated.
    
    Args:
        text: Text to truncate
        max_length: Maximum length (default: 160 for meta descriptions)
        suffix: Suffix to add if truncated (default: "...")
        
    Returns:
        Truncated text string
        
    Example:
        >>> truncate_text("This is a very long article about AI...", 20)
        'This is a very lo...'
    """
    if len(text) <= max_length:
        return text
    
    # Truncate to max_length minus suffix length
    truncated = text[:max_length - len(suffix)]
    
    # Try to break at a space to avoid cutting words
    last_space = truncated.rfind(' ')
    if last_space > max_length * 0.8:  # Only if we're not losing too much
        truncated = truncated[:last_space]
    
    return truncated + suffix


def count_words(text: str) -> int:
    """
    Count words in text content.
    
    Args:
        text: Text to count words in
        
    Returns:
        Word count as integer
        
    Example:
        >>> count_words("Hello world, this is a test.")
        6
    """
    return len(text.split())


def extract_urls(text: str) -> list[str]:
    """
    Extract all URLs from text content.
    
    Args:
        text: Text containing URLs
        
    Returns:
        List of extracted URLs
        
    Example:
        >>> extract_urls("Check out https://example.com and http://test.com")
        ['https://example.com', 'http://test.com']
    """
    # URL pattern
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    
    urls = re.findall(url_pattern, text)
    
    return urls


def format_metadata(title: str, description: str) -> Dict[str, str]:
    """
    Format and validate metadata for SEO.
    
    Args:
        title: SEO title
        description: Meta description
        
    Returns:
        Dictionary with formatted metadata
        
    Example:
        >>> format_metadata("My Title", "A short description")
        {'title': 'My Title', 'description': 'A short description', 'title_length': 8, 'description_length': 19}
    """
    # Truncate title to 60 characters
    formatted_title = truncate_text(title, 60, "...")
    
    # Truncate description to 160 characters
    formatted_description = truncate_text(description, 160, "...")
    
    return {
        "title": formatted_title,
        "description": formatted_description,
        "title_length": len(formatted_title),
        "description_length": len(formatted_description)
    }
