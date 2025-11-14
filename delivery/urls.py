from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('', views.delivery_list, name='list'),
    path('<int:pk>/', views.delivery_detail, name='detail'),
    path('<int:pk>/atribuir/', views.delivery_assign, name='assign'),
    path('<int:pk>/status/', views.delivery_update_status, name='update_status'),
    path('create/<int:order_id>/', views.delivery_create, name='create'),


    # CRUD de entregadores
    path('entregadores/', views.delivery_person_list, name='person_list'),
    path('entregadores/novo/', views.delivery_person_create, name='person_create'),
    path('entregadores/editar/<int:pk>/', views.delivery_person_edit, name='person_edit'),
    path('entregadores/remover/<int:pk>/', views.delivery_person_delete, name='person_delete'),
]

