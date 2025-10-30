import logging
from celery import shared_task
from .services import process_pitch_deck
from .models import Deal

logger = logging.getLogger(__name__)

@shared_task
def analyze_pitch_deck(deal_id: int):
    """
    Celery task to run the pitch deck analysis asynchronously.
    """
    logger.info(f"Celery task started for deal_id: {deal_id}")
    try:
        # Call the main function from services.py
        process_pitch_deck(deal_id)
        logger.info(f"Celery task finished for deal_id: {deal_id}")
    except Exception as e:
        logger.error(f"Celery task failed for deal_id {deal_id}: {e}")
        # If a major error happens, mark the deal as failed
        try:
            deal = Deal.objects.get(id=deal_id)
            deal.status = 'failed'
            deal.save()
        except Deal.DoesNotExist:
            logger.error(f"Deal {deal_id} not found when trying to mark as failed.")