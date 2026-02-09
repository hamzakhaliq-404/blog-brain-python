"""
Tasks package for Blog Brain.

Contains all task definitions for the multi-agent content generation workflow.
"""

# Import all task creation functions
from tasks.research_task import create_research_task
from tasks.strategy_task import create_strategy_task
from tasks.writing_task import create_writing_task
from tasks.editing_task import create_editing_task

__all__ = [
    'create_research_task',
    'create_strategy_task',
    'create_writing_task',
    'create_editing_task'
]
