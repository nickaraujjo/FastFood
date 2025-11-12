from django.shortcuts import render
from orders.models import Order
from menu.models import MenuItem
from customers.models import Customer


def home(request):
    """Página inicial do sistema"""
    total_pedidos = Order.objects.count()
    total_clientes = Customer.objects.count()
    total_itens_menu = MenuItem.objects.count()
    pedidos_pendentes = Order.objects.filter(status='PENDING').count()
    
    context = {
        'total_pedidos': total_pedidos,
        'total_clientes': total_clientes,
        'total_itens_menu': total_itens_menu,
        'pedidos_pendentes': pedidos_pendentes,
    }
    return render(request, 'core/home.html', context)
