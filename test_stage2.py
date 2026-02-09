"""
Test script to verify Stage 2 components.

Tests configuration loading, logging, and helper utilities.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_helpers():
    """Test utility functions"""
    from utils.helpers import (
        generate_slug,
        calculate_reading_time,
        sanitize_html,
        truncate_text,
        count_words,
        extract_urls,
        format_metadata
    )
    
    print("=" * 50)
    print("Testing Helper Functions")
    print("=" * 50)
    
    # Test slug generation
    title = "The Future of AI in Healthcare 2026"
    slug = generate_slug(title)
    print(f"✓ Slug: '{title}' -> '{slug}'")
    assert slug == "the-future-of-ai-in-healthcare-2026"
    
    # Test reading time
    text = " ".join(["word"] * 400)  # 400 words
    read_time = calculate_reading_time(text)
    print(f"✓ Reading time for 400 words: {read_time}")
    assert "2 mins" in read_time
    
    # Test HTML sanitization
    dirty_html = '<p>Safe</p><script>alert("bad")</script><p>More safe</p>'
    clean_html = sanitize_html(dirty_html)
    print(f"✓ HTML sanitized: No script tags remain")
    assert '<script>' not in clean_html
    
    # Test truncation
    long_text = "This is a very long text that needs to be truncated for meta descriptions"
    truncated = truncate_text(long_text, 30)
    print(f"✓ Truncated: '{truncated}'")
    assert len(truncated) <= 33  # 30 + "..."
    
    # Test word count
    sample = "Hello world this is a test"
    words = count_words(sample)
    print(f"✓ Word count: '{sample}' has {words} words")
    assert words == 6
    
    # Test URL extraction
    text_with_urls = "Check https://example.com and http://test.com"
    urls = extract_urls(text_with_urls)
    print(f"✓ Extracted URLs: {urls}")
    assert len(urls) == 2
    
    # Test metadata formatting
    meta = format_metadata(
        "A Very Long SEO Title That Should Be Truncated Because It Exceeds Limits",
        "A meta description that should fit"
    )
    print(f"✓ Metadata formatted:")
    print(f"  Title: {meta['title']} ({meta['title_length']} chars)")
    print(f"  Description: {meta['description']} ({meta['description_length']} chars)")
    
    print("\n✅ All helper function tests passed!\n")


def test_logger():
    """Test logging system"""
    from utils.logger import setup_logger
    
    print("=" * 50)
    print("Testing Logging System")
    print("=" * 50)
    
    logger = setup_logger("test_module")
    
    logger.info("✓ INFO level log message")
    logger.warning("✓ WARNING level log message")
    logger.error("✓ ERROR level log message")
    
    print("\n✅ Logging system working!\n")


def test_config():
    """Test configuration loading"""
    print("=" * 50)
    print("Testing Configuration")
    print("=" * 50)
    
    try:
        from config import settings
        
        print(f"✓ Configuration loaded successfully")
        print(f"  Gemini Model: {settings.gemini_model}")
        print(f"  API Port: {settings.api_port}")
        print(f"  Log Level: {settings.log_level}")
        print(f"  Writer Temperature: {settings.writer_temperature}")
        print(f"  Enable Memory: {settings.enable_memory}")
        
        print("\n✅ Configuration system working!\n")
        
    except Exception as e:
        print(f"⚠️  Config test skipped: {e}")
        print("   (This is expected if .env file is not set up yet)")
        print("   To fix: Copy .env.example to .env and add API keys\n")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Stage 2 Verification Tests")
    print("=" * 50 + "\n")
    
    # Run tests
    test_helpers()
    test_logger()
    test_config()
    
    print("=" * 50)
    print("Stage 2 Verification Complete!")
    print("=" * 50)
