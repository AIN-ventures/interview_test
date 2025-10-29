"""
Celery tasks for asynchronous pitch deck processing.

Implements async processing task that orchestrates the entire pipeline:
1. Extract information from PDF
2. Analyze with OpenAI
3. Save results to database
"""

import logging
import os
from celery import shared_task
from django.utils import timezone
from core.utils import log_task_execution
from .models import Deal
from .services import extract_deck_info, analyze_opportunity, save_results

logger = logging.getLogger(__name__)


@shared_task
@log_task_execution
def process_deal_async(deal_id):
    """
    Asynchronously process a pitch deck through the complete pipeline.
    
    Args:
        deal_id: UUID string of the deal to process
        
    Returns:
        dict: Processing result with status and details
    """
    try:
        # Get the deal and update status to processing
        deal = Deal.objects.get(id=deal_id)
        deal.status = 'processing'
        deal.error_message = ''
        deal.save()
        
        logger.info(f"Starting processing for deal {deal_id}")
        
        # Check if file exists
        if not deal.pitch_deck or not deal.pitch_deck.path:
            raise Exception("No pitch deck file found")
        
        file_path = deal.pitch_deck.path
        if not os.path.exists(file_path):
            raise Exception(f"Pitch deck file not found at path: {file_path}")
        
        # Step 1: Extract information from PDF
        logger.info(f"Extracting deck info for deal {deal_id}")
        extracted_data = extract_deck_info(file_path)
        
        if not extracted_data.get('extraction_successful'):
            error_msg = extracted_data.get('error_message', 'PDF extraction failed')
            logger.error(f"Extraction failed for deal {deal_id}: {error_msg}")
            
            # Update deal status to failed
            deal.status = 'failed'
            deal.error_message = error_msg
            deal.processed_at = timezone.now()
            deal.save()
            
            return {
                'success': False,
                'error': error_msg,
                'stage': 'extraction'
            }
        
        # Step 2: Analyze opportunity with OpenAI
        logger.info(f"Analyzing opportunity for deal {deal_id}")
        analysis_result = analyze_opportunity(extracted_data)
        
        if not analysis_result.get('analysis_successful'):
            error_msg = analysis_result.get('error_message', 'AI analysis failed')
            logger.error(f"Analysis failed for deal {deal_id}: {error_msg}")
            
            # Update deal status to failed
            deal.status = 'failed'
            deal.error_message = error_msg
            deal.processed_at = timezone.now()
            deal.save()
            
            return {
                'success': False,
                'error': error_msg,
                'stage': 'analysis'
            }
        
        # Step 3: Save results to database
        logger.info(f"Saving results for deal {deal_id}")
        save_success = save_results(deal_id, extracted_data, analysis_result)
        
        if not save_success:
            error_msg = "Failed to save analysis results to database"
            logger.error(f"Save failed for deal {deal_id}: {error_msg}")
            
            return {
                'success': False,
                'error': error_msg,
                'stage': 'saving'
            }
        
        logger.info(f"Successfully completed processing for deal {deal_id}")
        
        return {
            'success': True,
            'deal_id': deal_id,
            'company_name': analysis_result.get('company_info', {}).get('company_name', 'Unknown'),
            'overall_score': analysis_result.get('assessment_scores', {}).get('overall_score', 0),
            'processed_at': timezone.now().isoformat()
        }
        
    except Deal.DoesNotExist:
        error_msg = f"Deal {deal_id} not found"
        logger.error(error_msg)
        return {
            'success': False,
            'error': error_msg,
            'stage': 'initialization'
        }
        
    except Exception as e:
        error_msg = f"Unexpected error processing deal {deal_id}: {str(e)}"
        logger.error(error_msg)
        
        # Try to update deal status to failed
        try:
            deal = Deal.objects.get(id=deal_id)
            deal.status = 'failed'
            deal.error_message = str(e)
            deal.processed_at = timezone.now()
            deal.retry_count += 1
            deal.save()
        except Exception as save_error:
            logger.error(f"Failed to update deal status after error: {str(save_error)}")
        
        return {
            'success': False,
            'error': error_msg,
            'stage': 'unexpected_error'
        }
