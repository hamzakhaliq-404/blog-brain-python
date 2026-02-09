"""
Logging configuration for Blog Brain.

Provides consistent logging across all modules.
"""

import logging
import sys
from typing import Optional


def setup_logger(name: str, log_level: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with consistent formatting.
    
    Args:
        name: Name of the logger (typically __name__ of the module)
        log_level: Optional log level override (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
        
    Example:
        >>> from utils.logger import setup_logger
        >>> logger = setup_logger(__name__)
        >>> logger.info("Application started")
    """
    
    # Import here to avoid circular dependency
    try:
        from config import settings
        level = log_level or settings.log_level
    except Exception:
        level = log_level or "INFO"
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level.upper())
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level.upper())
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger or create a new one.
    
    Args:
        name: Name of the logger
        
    Returns:
        Logger instance
    """
    return setup_logger(name)
