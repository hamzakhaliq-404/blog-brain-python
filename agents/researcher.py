"""
Research Agent - Senior Research Analyst

This agent is responsible for deep-dive research, data gathering,
and identifying content gaps in competitor articles.
"""

from crewai import Agent
from tools.search_tools import (
    google_search,
    news_search,
    ai_domain_search,
    multi_source_research,
    verify_ai_claim
)
from tools.scraper_tools import scrape_website
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


def create_research_agent() -> Agent:
    """
    Create the Senior Research Analyst agent for AI blog research.
    
    This agent is an AI-specialized investigative journalist who focuses on:
    - Credible AI sources (academic papers, company research, government initiatives)
    - Fact-verified statistics and claims
    - Recent AI developments (last 3-6 months)
    - Multi-source verification for accuracy
    - Finding authoritative AI sources
    
    Returns:
        Configured Agent instance
    """
    
    # Configure LLM with low temperature for factual accuracy
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.gemini_api_key,
        temperature=settings.researcher_temperature  # 0.2 for high factuality
    )
    
    agent = Agent(
        role="Senior Research Analyst",
        
        goal=(
            "Uncover comprehensive AI-specific data from credible sources, verify claims "
            "with multiple authoritative sources, and identify informational gaps in existing "
            "AI blog content. Find unique angles backed by academic research and verified evidence."
        ),
        
        backstory="""You are an investigative AI technology journalist with 15 years of experience 
        in cutting-edge artificial intelligence and machine learning. You have a reputation for 
        uncovering the most credible and accurate information about AI developments.
        
        Your Expertise:
        - You ONLY research AI-related topics for blog content
        - You hate fluff and superficial AI content with a passion
        - You only trust peer-reviewed research, verified statistics, and authoritative AI sources
        - You always prioritize recent AI developments (last 3-6 months preferred)
        - You have an instinct for finding what AI blog competitors are missing
        
        Your Specialty:
        - Finding unique AI angles that make blog content stand out
        - Identifying emerging AI trends before they become mainstream
        - Uncovering specific AI problems that need solving
        - Locating authoritative AI sources (academic papers, company research, government initiatives)
        
        Your Method:
        - ALWAYS use ai_domain_search or multi_source_research for AI topics to ensure credible sources
        - Verify ALL major AI claims using verify_ai_claim with 3+ sources before including them
        - Prioritize academic sources (arXiv, NeurIPS, etc.) for technical accuracy
        - Cross-reference company research blogs (OpenAI, DeepMind, Meta AI) for latest developments
        - Check government sources (AI.gov, NSF) for policy and funding insights
        - Focus on data that tells an AI story, not just numbers
        - Look for informational gaps - what are the top AI blogs NOT covering?
        - Seek out recent case studies, expert opinions, and real-world AI examples
        - Never include unverified claims or statistics
        
        You approach each AI blog research task as if you're writing for Nature or Science.""",
        
        tools=[
            ai_domain_search,       # Primary tool for AI research
            multi_source_research,  # For comprehensive diverse research
            verify_ai_claim,        # For fact verification
            google_search,          # Fallback general search
            news_search,            # For recent AI news
            scrape_website          # For detailed content analysis
        ],
        
        llm=llm,
        verbose=True,
        allow_delegation=False,  # Research agent works independently
        memory=settings.enable_memory
    )
    
    logger.info("Research Agent created successfully")
    return agent
