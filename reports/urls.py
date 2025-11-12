from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('vendas/', views.sales_report, name='sales'),
    path('entregadores/', views.delivery_performance, name='delivery_performance'),
    path('entregadores/', views.delivery_performance, name='delivery_performance'),
]
