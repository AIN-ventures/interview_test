"""
Deal API Views
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
from .tasks import analyze_pitch_deck


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
        """
        # 1. Validate the uploaded file using DealCreateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 2. Save the Deal instance with 'pending' status
        deal = serializer.save(status='pending')
        
        # 3. Trigger async processing task
        analyze_pitch_deck.delay(deal.id)
        
        # 4. Return appropriate response
        return Response(
            {
                'id': deal.id,
                'status': deal.status,
                'message': 'Pitch deck uploaded successfully. Analysis in progress.',
                'created_at': deal.created_at
            },
            status=status.HTTP_201_CREATED
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