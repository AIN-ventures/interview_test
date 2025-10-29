"""
Utility functions provided to candidates.

These helper functions are complete and ready to use.
"""
import logging
from functools import wraps
from django.utils import timezone

logger = logging.getLogger(__name__)


def log_task_execution(func):
    """
    Decorator to log task execution time and status.
    
    Usage:
        @shared_task
        @log_task_execution
        def my_task(arg):
            # task code here
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Starting task: {func.__name__} with args={args}, kwargs={kwargs}")
        start_time = timezone.now()
        try:
            result = func(*args, **kwargs)
            duration = (timezone.now() - start_time).total_seconds()
            logger.info(f"✓ Completed task: {func.__name__} in {duration:.2f}s")
            return result
        except Exception as e:
            duration = (timezone.now() - start_time).total_seconds()
            logger.error(f"✗ Failed task: {func.__name__} after {duration:.2f}s - {str(e)}")
            raise
    return wrapper


def sanitize_text(text):
    """
    Clean and normalize extracted text.
    
    Removes:
    - Excessive whitespace
    - Null bytes
    - Control characters
    
    Args:
        text: Raw text string
        
    Returns:
        str: Cleaned text
        
    Usage:
        raw_text = "Some   text\\x00with   issues"
        clean = sanitize_text(raw_text)
    """
    if not text:
        return ""
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Remove other control characters except newlines and tabs
    text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
    
    # Normalize whitespace (but preserve single newlines)
    lines = text.split('\n')
    cleaned_lines = [' '.join(line.split()) for line in lines]
    text = '\n'.join(line for line in cleaned_lines if line)
    
    return text.strip()


