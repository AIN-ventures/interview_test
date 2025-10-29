"""
Deal API Views

TODO: Complete the create() method to handle pitch deck uploads

Requirements:
1. Validate the uploaded file
2. Save Deal with appropriate status
3. Trigger async processing
4. Return appropriate response

The rest of the ViewSet is complete.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Deal
from .serializers import (
    DealListSerializer,
    DealDetailSerializer,
    DealCreateSerializer,
)


class DealViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Deal operations.
    """
    queryset = Deal.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DealCreateSerializer
        elif self.action == 'list':
            return DealListSerializer
        return DealDetailSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Handle pitch deck upload and trigger processing.
        
        TODO: Implement this method
        
        You need to:
        1. Validate the uploaded file using DealCreateSerializer
        2. Save the Deal instance
        3. Trigger your async processing task
        4. Return appropriate response
        """
        # TODO: Your implementation here
        return Response(
            {"error": "Not implemented"},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
    
    def retrieve(self, request, *args, **kwargs):
        """Get full deal details"""
        deal = self.get_object()
        serializer = self.get_serializer(deal)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        """List all deals with pagination"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """Get current processing status"""
        deal = self.get_object()
        
        return Response({
            'id': deal.id,
            'status': deal.status,
            'company_name': deal.company_name or None,
            'error_message': deal.error_message if deal.status == 'failed' else None,
            'processed_at': deal.processed_at,
        })
