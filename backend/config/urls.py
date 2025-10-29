"""
URL configuration for pitch deck analyzer.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def api_info(request):
    """Simple API info endpoint for root URL."""
    return JsonResponse({
        'message': 'Pitch Deck Analyzer API',
        'version': '1.0.0',
        'endpoints': {
            'deals': '/api/deals/',
            'admin': '/admin/',
        },
        'status': 'running'
    })

urlpatterns = [
    path('', api_info, name='api_info'),
    path('admin/', admin.site.urls),
    path('api/', include('deals.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


