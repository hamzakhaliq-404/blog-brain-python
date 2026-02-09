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
    
    description = f"""Conduct comprehensive research on the topic: "{topic}"{audience_context}

Your research MUST include:

1. SEARCH INTENT ANALYSIS
   - What are users actually looking for when they search this topic?
   - What questions are they trying to answer?
   - What problems are they trying to solve?

2. TOP-RANKING CONTENT ANALYSIS
   - Search for "{topic}" and analyze the top 10 results
   - What are they covering well?
   - What are they missing? (CRITICAL - find the gaps!)
   - What format are they using? (listicles, how-to, guides, etc.)

3. DATA GATHERING
   - Find recent statistics (preferably from the last 6 months)
   - Locate case studies or real-world examples
   - Identify expert opinions or authoritative sources
   - Record ALL source URLs for citations

4. TRENDING INFORMATION
   - Use news search to find recent developments
   - What's changed in the last 3-6 months?
   - Are there new tools, techniques, or approaches?

5. USER QUESTIONS
   - What are the "People Also Ask" questions for this topic?
   - What are the common pain points or challenges?
   - What would make this content truly valuable?

6. COMPETITIVE GAPS
   - What unique angle can we take?
   - What information is missing from existing content?
   - How can we provide more value than what's already ranking?

IMPORTANT GUIDELINES:
- Prioritize authoritative sources (.edu, .gov, established publications)
- Always verify facts from multiple sources
- Focus on actionable information, not just theory
- Look for specific examples and data points
- Keep track of all URLs for proper citation

Your research will form the foundation for the entire article.
Be thorough, be specific, and find the unique angle that will make this content stand out."""

    expected_output = """A comprehensive research brief in the following format:

## Research Brief: [Topic]

### Search Intent
[What users are looking for and why]

### Key Findings
1. [Main finding with source URL]
2. [Main finding with source URL]
3. [Main finding with source URL]
[Continue with 8-12 key findings]

### Recent Statistics & Data
- [Statistic] (Source: [URL])
- [Statistic] (Source: [URL])
[Include 5-10 relevant statistics]

### Competitor Analysis
**What's Working:**
- [Point about top-ranking content]
- [Point about top-ranking content]

**Content Gaps (Opportunities):**
- [What's missing from current top results]
- [Unique angle we can take]
- [Underserved subtopic]

### User Questions
1. [Question from PAA or common search]
2. [Question from PAA or common search]
[List 5-8 key questions]

### Recent Developments
[Any news, updates, or trends from the last 6 months]

### Expert Insights
[Quotes, opinions, or strategies from authoritative sources]

### Source List
1. [Article Title] - [URL]
2. [Article Title] - [URL]
[List ALL sources used, minimum 10]

### Recommended Angle
[Your recommendation for the unique approach this article should take]"""

    # Create the research agent
    agent = create_research_agent()
    
    # Create and return the task
    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )
    
    return task
