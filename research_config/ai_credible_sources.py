"""
AI Credible Sources Configuration

This module defines trusted, authoritative sources for AI blog research.
Sources are categorized by type and assigned priority weights for ranking.

Categories:
- academic: Peer-reviewed research, conference proceedings, academic journals
- government: Government AI initiatives, research funding agencies
- company_research: AI research labs at major tech companies
- industry: Reputable AI/tech industry publications
- ai_blogs: High-quality AI-focused blogs and educational resources

Usage:
    from config.ai_credible_sources import AI_CREDIBLE_SOURCES, SOURCE_PRIORITY
    academic_sources = AI_CREDIBLE_SOURCES['academic']
"""

from typing import Dict, List

# AI Credible Sources organized by category
AI_CREDIBLE_SOURCES: Dict[str, List[str]] = {
    "academic": [
        # Preprint repositories
        "arxiv.org",
        
        # Major AI/ML conferences
        "papers.nips.cc",  # NeurIPS
        "proceedings.mlr.press",  # ICML, ICLR, etc.
        "aclanthology.org",  # ACL (NLP)
        "aaai.org",  # AAAI
        "openreview.net",  # Various conferences
        "proceedings.neurips.cc",
        
        # Academic publishers & journals
        "ieeexplore.ieee.org",  # IEEE
        "dl.acm.org",  # ACM Digital Library
        "jmlr.org",  # Journal of Machine Learning Research
        "springer.com",  # Springer AI journals
        "science.org",  # Science Magazine
        "nature.com",  # Nature journals
        
        # University AI labs
        "ai.stanford.edu",
        "csail.mit.edu",
        "bair.berkeley.edu",
        "ml.cmu.edu",
        "ai.ox.ac.uk",  # Oxford
        "cam.ac.uk",  # Cambridge
        
        # Research institutions
        "distill.pub",  # Distill (interactive ML explanations)
    ],
    
    "government": [
        # US Government AI
        "nsf.gov",  # National Science Foundation
        "ai.gov",  # US AI portal
        "nist.gov",  # National Institute of Standards and Technology
        "nih.gov",  # National Institutes of Health (AI in healthcare)
        
        # International government
        "gov.uk",  # UK Government AI
        "canada.ca",  # Canada AI
        "digital.gov.au",  # Australia
        
        # Research agencies
        "darpa.mil",  # DARPA
        "energy.gov",  # Dept of Energy (AI research)
    ],
    
    "company_research": [
        # Major AI research labs
        "openai.com/research",
        "openai.com/blog",
        "deepmind.google",
        "deepmind.com",
        "ai.meta.com",
        "ai.facebook.com",
        "research.google",
        "ai.google",
        "microsoft.com/en-us/research/research-area/artificial-intelligence",
        "research.microsoft.com",
        
        # AI-first companies
        "huggingface.co/blog",
        "anthropic.com",
        "cohere.com/blog",
        "inflection.ai",
        
        # Tech company AI blogs
        "ai.googleblog.com",
        "engineering.fb.com",
        "netflixtechblog.com",
        "eng.uber.com",
        "aws.amazon.com/blogs/machine-learning",
        "developer.nvidia.com/blog",
    ],
    
    "industry": [
        # Major tech publications with AI focus
        "techcrunch.com/category/artificial-intelligence",
        "venturebeat.com/ai",
        "technologyreview.com",  # MIT Technology Review
        "wired.com/tag/artificial-intelligence",
        "theverge.com/ai-artificial-intelligence",
        
        # AI-specific news
        "artificialintelligence-news.com",
        "aimagazine.com",
        "aibusiness.com",
        
        # Industry analysis
        "thenewstack.io",
        "infoq.com/ai-ml-data-eng",
    ],
    
    "ai_blogs": [
        # Educational AI blogs
        "towardsdatascience.com",
        "machinelearningmastery.com",
        "kdnuggets.com",
        "analyticsvidhya.com",
        
        # Technical AI blogs
        "sebastianraschka.com/blog",
        "lilianweng.github.io",  # Lilian Weng's blog (OpenAI)
        "ruder.io",  # Sebastian Ruder (NLP)
        
        # AI news & analysis
        "analyticsinsight.net",
        "unite.ai",
        "marktechpost.com",
        
        # Community platforms
        "paperswithcode.com",
        "kaggle.com",
    ],
}


# Priority weights for source ranking
# Higher values indicate more credible/authoritative sources
SOURCE_PRIORITY: Dict[str, float] = {
    "academic": 1.0,         # Highest priority - peer-reviewed research
    "government": 0.9,       # Government research and initiatives
    "company_research": 0.8, # Company research labs (OpenAI, DeepMind, etc.)
    "industry": 0.6,         # Industry publications
    "ai_blogs": 0.5,         # High-quality AI blogs
}


# Target distribution for balanced source diversity
# These percentages guide multi_source_research to provide varied sources
TARGET_SOURCE_DISTRIBUTION: Dict[str, float] = {
    "academic": 0.40,        # 40% academic sources
    "government": 0.10,      # 10% government sources
    "company_research": 0.25,# 25% company research
    "industry": 0.15,        # 15% industry publications
    "ai_blogs": 0.10,        # 10% AI blogs
}


def get_all_domains() -> List[str]:
    """
    Get a flat list of all credible AI domains.
    
    Returns:
        List of all domain strings across all categories
    """
    all_domains = []
    for domains in AI_CREDIBLE_SOURCES.values():
        all_domains.extend(domains)
    return all_domains


def get_category_for_domain(domain: str) -> str:
    """
    Find which category a domain belongs to.
    
    Args:
        domain: Domain string to categorize
        
    Returns:
        Category name or empty string if not found
    """
    domain = domain.lower()
    for category, domains in AI_CREDIBLE_SOURCES.items():
        for credible_domain in domains:
            if credible_domain.lower() in domain or domain in credible_domain.lower():
                return category
    return ""


def get_priority_for_domain(domain: str) -> float:
    """
    Get priority score for a domain.
    
    Args:
        domain: Domain string to score
        
    Returns:
        Priority score (0.0-1.0), or 0.3 if unknown domain
    """
    category = get_category_for_domain(domain)
    return SOURCE_PRIORITY.get(category, 0.3)


# Example usage
if __name__ == "__main__":
    print("AI Credible Sources Configuration")
    print("=" * 50)
    
    for category, domains in AI_CREDIBLE_SOURCES.items():
        print(f"\n{category.upper()} ({len(domains)} sources):")
        print(f"Priority: {SOURCE_PRIORITY[category]}")
        print(f"Target distribution: {TARGET_SOURCE_DISTRIBUTION[category]*100}%")
        print(f"Examples: {', '.join(domains[:3])}")
    
    print(f"\n\nTotal domains: {len(get_all_domains())}")
    
    # Test categorization
    print("\n\nTest domain categorization:")
    test_domains = ["arxiv.org", "openai.com", "techcrunch.com"]
    for domain in test_domains:
        category = get_category_for_domain(domain)
        priority = get_priority_for_domain(domain)
        print(f"{domain} -> {category} (priority: {priority})")
