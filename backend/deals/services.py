# backend/deals/services.py

import os
import json
import logging
from PyPDF2 import PdfReader
from io import BytesIO
from openai import OpenAI

from .models import Deal, Founder, Assessment

# Setup logging
logger = logging.getLogger(__name__)

# DO NOT initialize OpenAI client here - it will be initialized in the function


def extract_text_from_pdf(pdf_file) -> str:
    """Extracts raw text from a PDF file."""
    text = ""
    try:
        # Open the PDF file in binary read mode
        with pdf_file.open('rb') as f:
            # Create a BytesIO object to handle the file in memory
            pdf_in_memory = BytesIO(f.read())
            reader = PdfReader(pdf_in_memory)
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            
            logger.info(f"Extracted {len(text)} characters from PDF: {pdf_file.name}")
            return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF {pdf_file.name}: {e}")
        return ""


def get_ai_analysis_prompt(deck_text: str) -> tuple:
    """Creates the system and user prompts for the AI, asking for JSON output."""
    
    system_prompt = """
    You are an expert venture capital analyst. Your task is to analyze a pitch deck text
    and provide a concise investment analysis. Respond ONLY with a valid JSON object.
    
    The JSON structure MUST be:
    {
      "company_name": "String",
      "website": "String (or 'N/A' if not found)",
      "location": "String (City, State/Country or 'N/A')",
      "founders": [
        {
          "name": "String",
          "bio": "String (1-2 sentence summary of background/experience)"
        }
      ],
      "market_analysis": "String (TAM/SAM/SOM, growth, competition summary)",
      "product_analysis": "String (Differentiation, technical moats, innovation)",
      "traction_analysis": "String (Revenue, users, growth metrics, or 'Early' if none)",
      "business_model": "String (Unit economics, scalability)",
      "investment_score": "Integer (1-10, 1=low, 10=high potential)",
      "strengths": "String (Bulleted list of 3-5 key strengths, start each with '*')",
      "concerns": "String (Bulleted list of 3-5 key concerns/risks, start each with '*')"
    }
    """
    
    user_prompt = f"Here is the pitch deck text. Analyze it and return the JSON object:\n\n{deck_text}"
    
    return system_prompt, user_prompt


def analyze_deck_with_ai(deck_text: str) -> dict:
    """Sends text to OpenAI and gets a structured JSON response."""
    if not deck_text:
        logger.warning("No text provided to AI for analysis.")
        return {}

    # Initialize OpenAI client HERE, not at module level
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    system_prompt, user_prompt = get_ai_analysis_prompt(deck_text)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using gpt-4o-mini for faster and cheaper analysis
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        analysis_json = json.loads(response.choices[0].message.content)
        logger.info("Successfully received AI analysis.")
        return analysis_json
        
    except Exception as e:
        logger.error(f"Error during AI analysis: {e}")
        return {}


def process_pitch_deck(deal_id: int):
    """
    Main service function: orchestrates the entire process.
    This is what the Celery task will call.
    """
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        logger.error(f"Deal with id {deal_id} not found.")
        return

    # 1. Update status and extract text
    logger.info(f"Starting processing for Deal {deal_id}...")
    deal.status = 'processing'
    deal.save()
    
    raw_text = extract_text_from_pdf(deal.pitch_deck)
    
    if not raw_text:
        deal.status = 'failed'
        deal.save()
        logger.error(f"Failed to extract text for Deal {deal_id}.")
        return

    # 2. Analyze with AI
    analysis_data = analyze_deck_with_ai(raw_text)
    
    if not analysis_data:
        deal.status = 'failed'
        deal.save()
        logger.error(f"Failed to get AI analysis for Deal {deal_id}.")
        return

    # 3. Save to Database
    try:
        # Update the Deal object
        deal.company_name = analysis_data.get('company_name', 'N/A')
        deal.website = analysis_data.get('website', 'N/A')
        deal.location = analysis_data.get('location', 'N/A')
        
        # Create the Assessment object
        # Use update_or_create to avoid duplicates if task re-runs
        assessment, _ = Assessment.objects.update_or_create(
            deal=deal,
            defaults={
                'market_analysis': analysis_data.get('market_analysis', ''),
                'product_analysis': analysis_data.get('product_analysis', ''),
                'traction_analysis': analysis_data.get('traction_analysis', ''),
                'business_model': analysis_data.get('business_model', ''),
                'investment_score': analysis_data.get('investment_score', 0),
                'strengths': analysis_data.get('strengths', ''),
                'concerns': analysis_data.get('concerns', ''),
            }
        )
        
        # Clear existing founders and create new ones
        deal.founders.all().delete()
        for founder_data in analysis_data.get('founders', []):
            Founder.objects.create(
                deal=deal,
                name=founder_data.get('name', 'N/A'),
                bio=founder_data.get('bio', '')
            )
            
        deal.status = 'completed'
        deal.save()
        logger.info(f"Successfully processed and saved Deal {deal_id}.")

    except Exception as e:
        deal.status = 'failed'
        deal.save()
        logger.error(f"Error saving analysis to DB for Deal {deal_id}: {e}")