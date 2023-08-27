from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from backend import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('stock_management.views')),
    path('api/auth/', include('auth_module.views')),
    path('api/', include('crm.views')),
    path('api/', include('website.views'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
