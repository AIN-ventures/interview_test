"""
Django admin configuration for deals.
"""
from django.contrib import admin
from .models import Deal, Founder, Assessment


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'status', 'created_at', 'processed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['company_name', 'website', 'location']
    readonly_fields = ['id', 'created_at', 'updated_at', 'processed_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'status', 'pitch_deck')
        }),
        ('Company Information', {
            'fields': ('company_name', 'website', 'location', 'technology_description', 'funding_ask')
        }),
        ('Processing', {
            'fields': ('error_message', 'retry_count', 'created_at', 'updated_at', 'processed_at')
        }),
    )


@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'deal', 'order']
    list_filter = ['deal']
    search_fields = ['name', 'title']


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['deal', 'overall_score', 'team_strength', 'market_opportunity', 'product_innovation', 'business_model']
    list_filter = ['team_strength', 'market_opportunity', 'product_innovation', 'business_model']
    readonly_fields = ['created_at']


