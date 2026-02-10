"""
Configuration package for Blog Brain.

This package contains all configuration modules including
settings, AI credible sources, and other configurations.
"""

# Import from submodules for easy access
from .ai_credible_sources import (
    AI_CREDIBLE_SOURCES,
    SOURCE_PRIORITY,
    TARGET_SOURCE_DISTRIBUTION,
    get_all_domains,
    get_category_for_domain,
    get_priority_for_domain,
)

# Note: settings is imported from config.py in the parent directory
# This allows: from config import settings
# While also allowing: from config.ai_credible_sources import AI_CREDIBLE_SOURCES

__all__ = [
    'AI_CREDIBLE_SOURCES',
    'SOURCE_PRIORITY',
    'TARGET_SOURCE_DISTRIBUTION',
    'get_all_domains',
    'get_category_for_domain',
    'get_priority_for_domain',
]
