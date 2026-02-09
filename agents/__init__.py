"""
Blog Brain - AI Content Generation System

An autonomous multi-agent system for generating SEO-optimized blog content.
Agents package for Blog Brain.

Contains all AI agent definitions for the content generation workflow.
"""

__version__ = "1.0.0"
__author__ = "Blog Brain Team"

# Import all agent creation functions
from agents.researcher import create_research_agent
from agents.strategist import create_seo_strategist
from agents.writer import create_writer_agent
from agents.editor import create_editor_agent

__all__ = [
    'create_research_agent',
    'create_seo_strategist',
    'create_writer_agent',
    'create_editor_agent'
]
