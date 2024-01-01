from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('allauth.urls')),


    path('', include('assistant.urls')),

    path('auth/', include('userschema.urls')),
] + static(settings.STATIC_URL, document_root= settings.COMPRESS_ROOT if getattr(settings, 'COMPRESS_ENABLED', False) else settings.STATIC_ROOT,)
