"""
Business logic for pitch deck processing.

Implements functions to:
1. Extract information from PDF pitch decks
2. Use OpenAI API to analyze the deck
3. Generate investment assessment
4. Save results to database

The core.utils module provides helper functions:
- sanitize_text(text): Clean extracted text
- log_task_execution: Decorator for logging (use on your task function)
"""

import json
import logging
from typing import Dict, Any, List
import PyPDF2
from openai import OpenAI
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from core.utils import sanitize_text
from .models import Deal, Founder, Assessment

logger = logging.getLogger(__name__)

# Configure OpenAI client
try:
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        logger.warning("OPENAI_API_KEY not set - OpenAI features will be disabled")
        client = None
    else:
        # Initialize OpenAI client with explicit parameters only
        client = OpenAI(
            api_key=api_key
        )
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None


def extract_deck_info(file_path: str) -> Dict[str, Any]:
    """
    Extract relevant information from pitch deck PDF using PyPDF2.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Dict containing extracted text and metadata
    """
    try:
        extracted_info = {
            'raw_text': '',
            'page_count': 0,
            'extraction_successful': True,
            'error_message': None
        }
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            extracted_info['page_count'] = len(pdf_reader.pages)
            
            # Extract text from all pages
            full_text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num + 1}: {str(e)}")
                    continue
            
            # Clean and sanitize the extracted text
            extracted_info['raw_text'] = sanitize_text(full_text)
            
            if not extracted_info['raw_text'].strip():
                extracted_info['extraction_successful'] = False
                extracted_info['error_message'] = "No text could be extracted from PDF"
                
        return extracted_info
        
    except Exception as e:
        logger.error(f"PDF extraction failed: {str(e)}")
        return {
            'raw_text': '',
            'page_count': 0,
            'extraction_successful': False,
            'error_message': f"PDF extraction failed: {str(e)}"
        }


def analyze_opportunity(deck_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use OpenAI API to analyze the pitch deck and return structured JSON assessment.
    
    Args:
        deck_info: Dictionary containing extracted deck information
        
    Returns:
        Dict containing structured analysis and scores
    """
    # Check if OpenAI client is available
    if client is None:
        return {
            'analysis_successful': False,
            'error_message': 'OpenAI client not available - check API key configuration'
        }
    
    if not deck_info.get('extraction_successful') or not deck_info.get('raw_text'):
        return {
            'analysis_successful': False,
            'error_message': 'No valid text extracted from deck for analysis'
        }
    
    try:
        # Prepare the prompt for OpenAI analysis
        analysis_prompt = f"""
        You are a senior venture capital analyst. Analyze this pitch deck text and provide a comprehensive investment assessment.

        PITCH DECK TEXT:
        {deck_info['raw_text'][:8000]}  # Limit text to avoid token limits

        Please provide your analysis in the following JSON format:

        {{
            "company_info": {{
                "company_name": "extracted company name or 'Unknown'",
                "website": "company website if mentioned or ''",
                "location": "company location if mentioned or ''",
                "technology_description": "brief description of the technology/product",
                "funding_ask": "funding amount requested or ''"
            }},
            "founders": [
                {{
                    "name": "founder name",
                    "title": "founder title/role",
                    "background": "relevant background/experience",
                    "linkedin_url": "linkedin URL if mentioned or ''"
                }}
            ],
            "assessment_scores": {{
                "team_strength": 7,
                "market_opportunity": 8,
                "product_innovation": 6,
                "business_model": 7,
                "overall_score": 7.0
            }},
            "analysis": {{
                "strengths": ["strength 1", "strength 2", "strength 3"],
                "concerns": ["concern 1", "concern 2", "concern 3"],
                "investment_thesis": "2-3 paragraph investment thesis explaining the opportunity, risks, and recommendation"
            }}
        }}

        SCORING CRITERIA (1-10 scale):
        - team_strength: Quality and experience of founding team
        - market_opportunity: Size and growth potential of target market  
        - product_innovation: Technical differentiation and uniqueness
        - business_model: Revenue viability and scalability
        - overall_score: Weighted average considering all factors

        Provide only valid JSON in your response, no additional text.
        """
        
        # Call OpenAI API with structured JSON response format
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior VC analyst. Respond only with valid JSON."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.3,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        analysis_text = response.choices[0].message.content.strip()
        
        # Clean up the response to ensure it's valid JSON
        if analysis_text.startswith('```json'):
            analysis_text = analysis_text[7:]
        if analysis_text.endswith('```'):
            analysis_text = analysis_text[:-3]
        
        analysis_result = json.loads(analysis_text)
        analysis_result['analysis_successful'] = True
        
        return analysis_result
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse OpenAI JSON response: {str(e)}")
        return {
            'analysis_successful': False,
            'error_message': f'Failed to parse AI analysis: {str(e)}'
        }
    except Exception as e:
        logger.error(f"OpenAI analysis failed: {str(e)}")
        return {
            'analysis_successful': False,
            'error_message': f'AI analysis failed: {str(e)}'
        }


@transaction.atomic
def save_results(deal_id: str, extracted_data: Dict[str, Any], analysis: Dict[str, Any]) -> bool:
    """
    Save analysis results to database.
    
    Args:
        deal_id: UUID of the deal to update
        extracted_data: Raw extraction data
        analysis: Structured analysis from OpenAI
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get the deal instance
        deal = Deal.objects.get(id=deal_id)
        
        if not analysis.get('analysis_successful'):
            # Mark as failed if analysis wasn't successful
            deal.status = 'failed'
            deal.error_message = analysis.get('error_message', 'Analysis failed')
            deal.processed_at = timezone.now()
            deal.save()
            return False
        
        # Update deal with company information
        company_info = analysis.get('company_info', {})
        deal.company_name = company_info.get('company_name', '')
        deal.website = company_info.get('website', '')
        deal.location = company_info.get('location', '')
        deal.technology_description = company_info.get('technology_description', '')
        deal.funding_ask = company_info.get('funding_ask', '')
        
        # Create founder records
        founders_data = analysis.get('founders', [])
        for idx, founder_data in enumerate(founders_data):
            if founder_data.get('name'):  # Only create if name exists
                Founder.objects.create(
                    deal=deal,
                    name=founder_data.get('name', ''),
                    title=founder_data.get('title', ''),
                    background=founder_data.get('background', ''),
                    linkedin_url=founder_data.get('linkedin_url', ''),
                    order=idx
                )
        
        # Create assessment record
        scores = analysis.get('assessment_scores', {})
        analysis_details = analysis.get('analysis', {})
        
        Assessment.objects.create(
            deal=deal,
            team_strength=max(1, min(10, scores.get('team_strength', 5))),
            market_opportunity=max(1, min(10, scores.get('market_opportunity', 5))),
            product_innovation=max(1, min(10, scores.get('product_innovation', 5))),
            business_model=max(1, min(10, scores.get('business_model', 5))),
            overall_score=max(1.0, min(10.0, scores.get('overall_score', 5.0))),
            strengths=analysis_details.get('strengths', []),
            concerns=analysis_details.get('concerns', []),
            investment_thesis=analysis_details.get('investment_thesis', '')
        )
        
        # Update deal status
        deal.status = 'completed'
        deal.processed_at = timezone.now()
        deal.error_message = ''
        deal.save()
        
        logger.info(f"Successfully saved analysis results for deal {deal_id}")
        return True
        
    except Deal.DoesNotExist:
        logger.error(f"Deal {deal_id} not found")
        return False
    except Exception as e:
        logger.error(f"Failed to save results for deal {deal_id}: {str(e)}")
        # Try to update deal status to failed
        try:
            deal = Deal.objects.get(id=deal_id)
            deal.status = 'failed'
            deal.error_message = f'Failed to save results: {str(e)}'
            deal.processed_at = timezone.now()
            deal.save()
        except:
            pass
        return False
