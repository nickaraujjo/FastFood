from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.customer_list, name='list'),
    path('<int:pk>/', views.customer_detail, name='detail'),
    path('cadastrar/', views.customer_create, name='create'),
    path('<int:pk>/resgatar-pontos/', views.customer_redeem_points, name='redeem_points'),
     path('<int:pk>/editar/', views.customer_edit, name='edit'),
    path('<int:pk>/remover/', views.customer_delete, name='delete'),
]
