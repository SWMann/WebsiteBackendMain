 
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Add a common prefix to all API endpoints
API_PREFIX = 'websitebackendmain/'

urlpatterns = [
    # Admin panel with prefix
    path(f'{API_PREFIX}admin/', admin.site.urls),

    # API routes with prefix
    path(f'{API_PREFIX}api/auth/', include('authentication.urls')),
    path(f'{API_PREFIX}api/', include('api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)