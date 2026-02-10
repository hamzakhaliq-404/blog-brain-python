"""
Research Task Definition

Task specification for the research agent to gather comprehensive
information and identify content opportunities.
"""

from crewai import Task
from agents.researcher import create_research_agent
from typing import Optional


def create_research_task(
    topic: str,
    target_audience: Optional[str] = None
) -> Task:
    """
    Create a research task for analyzing a topic.
    
    Args:
        topic: The blog topic to research
        target_audience: Optional target audience specification
        
    Returns:
        Configured Task instance
    """
    
    # Build the description with optional audience targeting
    audience_context = f" targeting {target_audience}" if target_audience else ""
    
    description = f"""Conduct comprehensive AI-focused research for a blog post on: "{topic}"{audience_context}

Your research MUST include:

1. SEARCH INTENT ANALYSIS
   - What are AI blog readers actually looking for when they search this topic?
   - What AI-specific questions are they trying to answer?
   - What AI problems are they trying to solve?

2. CREDIBLE SOURCE RESEARCH (USE AI DOMAIN SEARCH TOOLS)
   - Use ai_domain_search with categories: ["academic", "company_research", "government"]
   - Search academic sources (arXiv, NeurIPS, ACL, ICML) for technical foundations
   - Search company research blogs (OpenAI, DeepMind, Meta AI, Anthropic) for latest developments
   - Search government sources (AI.gov, NSF, NIH) for policy and funding insights
   - Prioritize sources from the last 6 months for AI topics

3. COMPETITOR AI BLOG ANALYSIS
   - Search for "{topic}" in AI blogs and analyze top 10 results
   - What are they covering well about AI?
   - What AI-specific technical details are they missing? (CRITICAL - find the gaps!)
   - What format are they using? (tutorials, explainers, comparisons, benchmarks)

4. DATA GATHERING & VERIFICATION (MANDATORY)
   - Find recent AI statistics (preferably from the last 6 months)
   - Use verify_ai_claim to verify ALL major claims with 3+ credible sources
   - Locate AI case studies or real-world applications
   - Identify expert AI opinions from authoritative sources
   - Record ALL source URLs for citations

5. TRENDING AI INFORMATION
   - Use news_search filtered for AI sources to find recent developments
   - What's changed in AI in the last 3-6 months?
   - Are there new AI models, techniques, or breakthroughs?
   - What papers were recently published on this topic?

6. AI-SPECIFIC USER QUESTIONS
   - What are the common AI questions for this topic?
   - What are the technical challenges AI practitioners face?
   - What would make this AI blog content truly valuable to AI professionals?

7. COMPETITIVE GAPS IN AI BLOGS
   - What unique AI angle can we take?
   - What technical information is missing from existing AI blogs?
   - How can we provide more AI-specific value than what's already ranking?

CRITICAL GUIDELINES FOR AI BLOG RESEARCH:
- ALWAYS use ai_domain_search or multi_source_research for credible AI sources
- NEVER use generic google_search for primary AI research
- Prioritize academic sources (.edu, arxiv.org, research conferences, academic journals)
- Verify ALL AI statistics and claims with verify_ai_claim (minimum 3 sources)
- Focus on actionable AI information, not just theory
- Look for specific AI examples, benchmarks, and data points
- Keep track of all URLs for proper citation
- Ensure sources are AI-focused and recent (prefer last 6 months)
- Include source credibility scores and categories in your findings

Your research will form the foundation for an authoritative AI blog post.
Be thorough, be specific, and find the unique AI angle that will make this content stand out."""

    expected_output = """A comprehensive research brief in the following format:

## Research Brief: [Topic]

### Search Intent
[What AI blog readers are looking for and why]

### Verified AI Findings
1. [AI Claim/Finding] - Status: Verified ✓
   - Academic Sources: [arXiv URL], [Conference Paper URL]
   - Company Research: [OpenAI/DeepMind URL]
   - Credibility: High (0.9+)
   
2. [AI Claim/Finding] - Status: Partially Verified ⚠
   - Supporting Sources: [URL1 (category)], [URL2 (category)]
   - Needs additional verification
   - Credibility: Medium (0.7-0.8)

[Continue with 8-12 verified findings]

### Recent AI Statistics & Data
- [Statistic] - Verified ✓
  Sources: [Academic URL], [Company Research URL], [Government URL]
  Credibility: 0.95
- [Statistic] - Verified ✓
  Sources: [URL1], [URL2], [URL3]
  Credibility: 0.90
[Include 5-10 verified AI statistics]

### Competitor AI Blog Analysis
**What's Working:**
- [Point about top-ranking AI content]
- [Technical depth they're achieving]

**Content Gaps (Opportunities):**
- [What AI technical details are missing from current top results]
- [Unique AI angle we can take]
- [Underserved AI subtopic]

### AI-Specific User Questions
1. [Technical AI question from practitioners]
2. [Common AI implementation challenge]
[List 5-8 key AI questions]

### Recent AI Developments
[News, updates, or trends from the last 6 months, with sources]

### Expert AI Insights
[Quotes, opinions, or strategies from authoritative AI sources]

### Source Distribution
- Academic: X% (Y sources) - arXiv, NeurIPS, etc.
- Company Research: X% (Y sources) - OpenAI, DeepMind, etc.
- Government: X% (Y sources) - AI.gov, NSF, etc.
- Industry: X% (Y sources)
Total Sources: [Number]

### Source List (Categorized)
**Academic:**
1. [Paper Title] - [URL] (Credibility: 1.0)
2. [Paper Title] - [URL] (Credibility: 1.0)

**Company Research:**
1. [Article Title] - [URL] (Credibility: 0.8)
2. [Article Title] - [URL] (Credibility: 0.8)

[List ALL sources used, minimum 15, grouped by category]

### Recommended Angle
[Your recommendation for the unique AI approach this blog post should take, backed by verified research]"""

    # Create the research agent
    agent = create_research_agent()
    
    # Create and return the task
    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )
    
    return task
