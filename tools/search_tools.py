"""
Search tools for Blog Brain using Serper.dev API.

Provides Google search functionality and AI-focused domain-specific search
for the research agent to find credible sources for AI blog content.
"""

from crewai.tools import tool
import requests
from config import settings  # settings is in root config.py
from research_config.ai_credible_sources import (  # ai_credible_sources is in research_config/ package
    AI_CREDIBLE_SOURCES,
    SOURCE_PRIORITY,
    TARGET_SOURCE_DISTRIBUTION,
    get_category_for_domain,
    get_priority_for_domain,
)
from utils.logger import setup_logger
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
from collections import defaultdict

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


# ============================================================================
# AI-FOCUSED SEARCH TOOLS
# ============================================================================

def extract_domain(url: str) -> str:
    """
    Extract domain from URL.
    
    Args:
        url: Full URL string
        
    Returns:
        Domain string (e.g., 'arxiv.org')
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        # Remove www. prefix
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except Exception:
        return ""


@tool("AI Domain Search")
def ai_domain_search(
    query: str,
    categories: List[str] = None,
    num_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Search credible AI sources for accurate blog research.
    
    This tool searches only trusted AI domains (academic, company research,
    government, etc.) to ensure high-quality, authoritative sources for AI blogs.
    
    Args:
        query: Search query string
        categories: Source categories to search. Options: 'academic', 'government',
                   'company_research', 'industry', 'ai_blogs'.
                   Default: ['academic', 'company_research']
        num_results: Number of results to return (default 10)
        
    Returns:
        List of search results with credibility scores and source categories
        
    Example:
        >>> results = ai_domain_search(
        ...     "transformer architecture explained",
        ...     categories=["academic", "company_research"]
        ... )
        >>> print(results[0]['source_category'], results[0]['credibility_score'])
    """
    if categories is None:
        categories = ["academic", "company_research"]
    
    logger.info(f"AI domain search for: '{query}' in categories: {categories}")
    
    # Collect domains from selected categories
    domains = []
    for category in categories:
        if category in AI_CREDIBLE_SOURCES:
            domains.extend(AI_CREDIBLE_SOURCES[category])
    
    if not domains:
        logger.warning(f"No domains found for categories: {categories}")
        return []
    
    # Build site: operators (limit to 15 domains to avoid query length issues)
    selected_domains = domains[:15]
    site_operators = " OR ".join([f"site:{domain}" for domain in selected_domains])
    enhanced_query = f"{query} ({site_operators})"
    
    logger.info(f"Searching {len(selected_domains)} credible AI domains")
    
    # Use existing google_search with enhanced query
    results = google_search(enhanced_query, num_results * 2)  # Get extra to filter
    
    # Filter and score results
    filtered_results = []
    for result in results:
        domain = extract_domain(result['link'])
        category = get_category_for_domain(domain)
        
        if category:
            result['credibility_score'] = SOURCE_PRIORITY.get(category, 0.3)
            result['source_category'] = category
            filtered_results.append(result)
    
    # Sort by credibility score (academic sources first)
    filtered_results.sort(key=lambda x: x['credibility_score'], reverse=True)
    
    logger.info(f"Filtered to {len(filtered_results)} credible AI sources")
    return filtered_results[:num_results]


@tool("Multi-Source Research")
def multi_source_research(
    query: str,
    num_results: int = 20
) -> List[Dict[str, Any]]:
    """
    Perform comprehensive multi-source AI research with balanced source diversity.
    
    This tool searches across all credible AI source categories and returns
    a balanced mix prioritizing academic and authoritative sources.
    
    Args:
        query: Search query string
        num_results: Total number of results to return (default 20)
        
    Returns:
        List of diverse, credible search results ranked by priority
        
    Example:
        >>> results = multi_source_research("large language models 2026")
        >>> categories = [r['source_category'] for r in results]
        >>> print(f"Academic: {categories.count('academic')}")
    """
    logger.info(f"Multi-source research for: '{query}'")
    
    # Calculate target results per category based on distribution
    category_targets = {
        category: int(num_results * percentage)
        for category, percentage in TARGET_SOURCE_DISTRIBUTION.items()
    }
    
    # Ensure we get at least the target number
    total_to_fetch = sum(category_targets.values()) + 10
    
    # Collect results from all categories
    all_results = []
    seen_urls = set()
    
    for category, target_count in category_targets.items():
        if target_count == 0:
            continue
            
        logger.info(f"Fetching {target_count} results from {category}")
        
        # Search this category
        category_results = ai_domain_search(
            query,
            categories=[category],
            num_results=target_count + 5  # Extra for deduplication
        )
        
        # Deduplicate by URL
        for result in category_results:
            url = result['link']
            if url not in seen_urls:
                seen_urls.add(url)
                all_results.append(result)
    
    # Sort by credibility score (academic sources prioritized)
    all_results.sort(key=lambda x: x['credibility_score'], reverse=True)
    
    # Log source distribution
    category_counts = defaultdict(int)
    for result in all_results[:num_results]:
        category_counts[result['source_category']] += 1
    
    logger.info(f"Source distribution: {dict(category_counts)}")
    
    return all_results[:num_results]


@tool("Verify AI Claim")
def verify_ai_claim(
    claim: str,
    min_sources: int = 3
) -> Dict[str, Any]:
    """
    Verify an AI-related claim against multiple credible sources.
    
    This tool searches for evidence supporting or contradicting a specific
    claim across academic, company research, and government sources.
    
    Args:
        claim: Specific claim or statement to verify
        min_sources: Minimum number of sources to check (default 3)
        
    Returns:
        Dictionary with verification status, evidence, and confidence score
        
    Example:
        >>> result = verify_ai_claim("GPT-4 uses mixture of experts architecture")
        >>> print(result['verification_status'])
        >>> print(result['evidence'])
    """
    logger.info(f"Verifying AI claim: '{claim}'")
    
    # Search for the claim in credible sources
    search_results = ai_domain_search(
        claim,
        categories=["academic", "company_research", "government"],
        num_results=min_sources * 2  # Get extra to analyze
    )
    
    if len(search_results) < min_sources:
        logger.warning(f"Only found {len(search_results)} sources, less than minimum {min_sources}")
    
    # Analyze evidence
    evidence = []
    for result in search_results[:min_sources * 2]:
        evidence.append({
            'title': result['title'],
            'url': result['link'],
            'snippet': result['snippet'],
            'source_category': result['source_category'],
            'credibility_score': result['credibility_score']
        })
    
    # Determine verification status based on evidence quality
    if len(search_results) >= min_sources:
        # Check if we have high-credibility sources
        high_cred_count = sum(1 for r in search_results[:min_sources] 
                             if r['credibility_score'] >= 0.8)
        
        if high_cred_count >= 2:
            status = "Verified"
            confidence = "High"
        elif len(search_results) >= min_sources:
            status = "Partially Verified"
            confidence = "Medium"
        else:
            status = "Unverified"
            confidence = "Low"
    else:
        status = "Unverified"
        confidence = "Low"
    
    result = {
        'claim': claim,
        'verification_status': status,
        'confidence': confidence,
        'sources_checked': len(search_results),
        'evidence': evidence[:min_sources],
        'all_sources': search_results
    }
    
    logger.info(f"Verification status: {status} (confidence: {confidence})")
    logger.info(f"Checked {len(search_results)} sources, {len(evidence)} provide evidence")
    
    return result
