"""
Models for Deal tracking and assessment.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Deal(models.Model):
    """
    Represents a pitch deck submission and analysis.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Upload'),
        ('uploaded', 'Uploaded - Awaiting Processing'),
        ('processing', 'Processing'),
        ('completed', 'Analysis Complete'),
        ('failed', 'Processing Failed'),
    ]
    
    # Primary fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # File
    pitch_deck = models.FileField(upload_to='pitch_decks/', null=True, blank=True)
    
    # Extracted company information
    company_name = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    technology_description = models.TextField(blank=True)
    funding_ask = models.CharField(max_length=100, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Error handling
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.company_name or 'Unknown'} ({self.status})"


class Founder(models.Model):
    """
    Represents a founder extracted from a pitch deck.
    """
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='founders')
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    background = models.TextField(blank=True)  # Education, previous experience
    linkedin_url = models.URLField(blank=True)
    
    order = models.IntegerField(default=0)  # For maintaining order from deck
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.name} - {self.deal.company_name}"


class Assessment(models.Model):
    """
    Investment assessment scores and analysis.
    
    TODO: Candidates must implement the logic to populate these fields.
    """
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, related_name='assessment')
    
    # Four key VC assessment categories (1-10 scale)
    team_strength = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Quality and experience of founding team"
    )
    market_opportunity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Size and growth potential of target market"
    )
    product_innovation = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Technical differentiation and uniqueness"
    )
    business_model = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Revenue viability and scalability"
    )
    
    # Overall score (calculated or AI-generated)
    overall_score = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Weighted average or AI-generated overall score"
    )
    
    # Detailed analysis
    strengths = models.JSONField(default=list)  # List of key strengths
    concerns = models.JSONField(default=list)   # List of concerns/risks
    investment_thesis = models.TextField(blank=True)  # 2-3 paragraph summary
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Assessments"
    
    def __str__(self):
        return f"Assessment for {self.deal.company_name} (Score: {self.overall_score})"


