"""
Tests for deals app.

Basic test structure provided. Candidates can expand if desired.
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Deal, Founder, Assessment


class DealModelTest(TestCase):
    """Test Deal model"""
    
    def test_create_deal(self):
        """Test creating a deal instance"""
        deal = Deal.objects.create(
            company_name="Test Company",
            status="pending"
        )
        self.assertEqual(deal.company_name, "Test Company")
        self.assertEqual(deal.status, "pending")
        self.assertIsNotNone(deal.id)
    
    def test_deal_str(self):
        """Test deal string representation"""
        deal = Deal.objects.create(company_name="Acme Inc")
        self.assertIn("Acme Inc", str(deal))


class FounderModelTest(TestCase):
    """Test Founder model"""
    
    def test_create_founder(self):
        """Test creating a founder"""
        deal = Deal.objects.create(company_name="Test Co")
        founder = Founder.objects.create(
            deal=deal,
            name="Jane Doe",
            title="CEO",
            order=0
        )
        self.assertEqual(founder.name, "Jane Doe")
        self.assertEqual(founder.deal, deal)


class AssessmentModelTest(TestCase):
    """Test Assessment model"""
    
    def test_create_assessment(self):
        """Test creating an assessment"""
        deal = Deal.objects.create(company_name="Test Co")
        assessment = Assessment.objects.create(
            deal=deal,
            team_strength=8,
            market_opportunity=7,
            product_innovation=9,
            business_model=6,
            overall_score=7.5,
            strengths=["Strong team", "Large market"],
            concerns=["Early stage"]
        )
        self.assertEqual(assessment.team_strength, 8)
        self.assertEqual(assessment.overall_score, 7.5)


# TODO: Candidates can add more tests
# - Test API endpoints
# - Test service functions
# - Test Celery tasks
# - Test error handling


