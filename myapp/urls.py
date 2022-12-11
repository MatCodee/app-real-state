from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
    path('account/',include('account.urls')),
    path('service/',include('service.urls')),
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
