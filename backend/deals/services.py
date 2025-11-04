"""
Business logic for pitch deck processing.

TODO: Implement functions to:
1. Extract information from PDF pitch decks
2. Use OpenAI API to analyze the deck
3. Generate investment assessment
4. Save results to database

You have complete creative freedom in your approach:
- Decide what information to extract
- Design your data structure
- Choose your extraction method (PyPDF2, vision models, etc.)
- Create your assessment criteria
- Structure your prompts

The core.utils module provides helper functions:
- sanitize_text(text): Clean extracted text
- log_task_execution: Decorator for logging (use on your task function)

Note on OpenAI:
- Use 'gpt-4o' or 'gpt-4-turbo' models (they support JSON response format)
- The older 'gpt-4' model does NOT support response_format={"type": "json_object"}
"""

import logging
from openai import OpenAI
from django.conf import settings
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)

# Configure OpenAI client
# Note: Using custom httpx client to avoid proxy-related initialization errors
try:
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        logger.warning("OPENAI_API_KEY not set - OpenAI features will be disabled")
        client = None
    else:
        import httpx
        
        # Create httpx client without proxy to avoid initialization issues
        http_client = httpx.Client(
            timeout=60.0,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        
        client = OpenAI(
            api_key=api_key,
            http_client=http_client
        )
        logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None


# TODO: Implement your processing functions here
#
# Example structure (adapt as needed):
#
# def extract_deck_info(file_path):
#     """Extract relevant information from pitch deck PDF"""
#     pass
#
# def analyze_opportunity(deck_info):
#     """Analyze investment opportunity using AI"""
#     pass
#
# @transaction.atomic
# def save_results(deal_id, extracted_data, analysis):
#     """Save results to database"""
#     pass
