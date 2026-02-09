"""
Research Agent - Senior Research Analyst

This agent is responsible for deep-dive research, data gathering,
and identifying content gaps in competitor articles.
"""

from crewai import Agent
from tools.search_tools import google_search, news_search
from tools.scraper_tools import scrape_website
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


def create_research_agent() -> Agent:
    """
    Create the Senior Research Analyst agent.
    
    This agent is an investigative tech journalist who focuses on:
    - Hard data and verified statistics
    - Recent developments (last 3-6 months)
    - Identifying informational gaps in competitor content
    - Finding authoritative sources
    
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
            "Uncover comprehensive data, recent statistics, and user intent that "
            "generic AI responses miss. Identify informational gaps in existing content "
            "and find unique angles for our article."
        ),
        
        backstory="""You are an investigative tech journalist with 15 years of experience 
        in cutting-edge technology and digital media. You have a reputation for uncovering 
        stories that others miss.
        
        Your Expertise:
        - You hate fluff and superficial content with a passion
        - You only care about hard data, verified statistics, and concrete evidence
        - You always prioritize recent developments (last 3-6 months preferred)
        - You have an instinct for finding what competitors are missing
        
        Your Specialty:
        - Finding the unique angles that make content stand out
        - Identifying emerging trends before they become mainstream
        - Uncovering specific user problems that need solving
        - Locating authoritative sources that add credibility
        
        Your Method:
        - Always cite your sources and verify facts from multiple authoritative sources
        - Focus on data that tells a story, not just numbers
        - Look for informational gaps - what are the top 10 results NOT covering?
        - Seek out recent case studies, expert opinions, and real-world examples
        
        You approach each research task as if you're breaking a major story.""",
        
        tools=[google_search, news_search, scrape_website],
        
        llm=llm,
        verbose=True,
        allow_delegation=False,  # Research agent works independently
        memory=settings.enable_memory
    )
    
    logger.info("Research Agent created successfully")
    return agent
