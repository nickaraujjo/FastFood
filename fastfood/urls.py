"""
URL configuration for fastfood project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('menu/', include('menu.urls')),
    path('pedidos/', include('orders.urls')),
    path('entregas/', include('delivery.urls')),
    path('clientes/', include('customers.urls')),
    path('relatorios/', include('reports.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
