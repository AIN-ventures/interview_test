"""
Serializers for Deal API.
"""
from rest_framework import serializers
from .models import Deal, Founder, Assessment


class FounderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Founder
        fields = ['id', 'name', 'title', 'background', 'linkedin_url', 'order']


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            'team_strength',
            'market_opportunity', 
            'product_innovation',
            'business_model',
            'overall_score',
            'strengths',
            'concerns',
            'investment_thesis',
        ]


class DealListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list view"""
    class Meta:
        model = Deal
        fields = [
            'id',
            'company_name',
            'status',
            'created_at',
            'processed_at',
        ]


class DealDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail view"""
    founders = FounderSerializer(many=True, read_only=True)
    assessment = AssessmentSerializer(read_only=True)
    
    class Meta:
        model = Deal
        fields = [
            'id',
            'status',
            'company_name',
            'website',
            'location',
            'technology_description',
            'funding_ask',
            'founders',
            'assessment',
            'created_at',
            'updated_at',
            'processed_at',
            'error_message',
        ]


class DealCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new deals"""
    class Meta:
        model = Deal
        fields = ['pitch_deck']
    
    def validate_pitch_deck(self, value):
        """Validate file is PDF and within size limits"""
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed")
        
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise serializers.ValidationError("File size cannot exceed 10MB")
        
        return value


