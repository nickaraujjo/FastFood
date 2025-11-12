from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order, OrderItem
from customers.models import Customer
from menu.models import MenuItem
from delivery.models import DeliveryPerson, Delivery
from django.utils import timezone
from datetime import timedelta  # necessário para calcular diferença de tempo


def order_list(request):
    """Lista todos os pedidos"""
    status = request.GET.get('status')
    if status:
        orders = Order.objects.filter(status=status)
    else:
        orders = Order.objects.all()

    # 🕒 Marcação para animações
    now = timezone.now()
    for order in orders:
        # Novo = criado há menos de 5 minutos
        order.is_new = (now - order.created_at) < timedelta(minutes=5)
        # Atrasado = pendente há mais de 30 minutos
        order.is_late = (
            order.status == 'PENDING'
            and (now - order.created_at) > timedelta(minutes=30)
        )

    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'selected_status': status,
    }
    return render(request, 'orders/order_list.html', context)



def order_detail(request, pk):
    """Detalhes de um pedido"""
    order = get_object_or_404(Order, pk=pk)
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)


def order_create(request):
    """Criar novo pedido e atribuir entregador disponível automaticamente"""
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        customer = get_object_or_404(Customer, pk=customer_id)
        
        order = Order.objects.create(customer=customer)
        
        # Adicionar itens ao pedido
        item_ids = request.POST.getlist('items')
        quantities = request.POST.getlist('quantities')
        
        for item_id, quantity in zip(item_ids, quantities):
            if item_id and quantity:
                menu_item = get_object_or_404(MenuItem, pk=item_id)
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=int(quantity),
                    price=menu_item.price
                )
        
        # Calcular total e adicionar pontos de fidelidade
        order.calculate_total()
        order.add_loyalty_points()
        
        # Buscar um entregador disponível
        delivery_person = DeliveryPerson.objects.filter(status='AVAILABLE').first()
        if delivery_person:
            # Criar entrega e atribuir entregador
            delivery = Delivery.objects.create(
                order=order,
                delivery_person=delivery_person,
                status='ASSIGNED'
            )
            # Atualizar status do entregador
            delivery_person.status = 'BUSY'
            delivery_person.save()
        else:
            # Criar entrega sem entregador
            delivery = Delivery.objects.create(
                order=order,
                status='PENDING'
            )
        
        messages.success(request, f'Pedido #{order.id} criado com sucesso!')
        return redirect('orders:detail', pk=order.id)
    
    # Se for GET, renderiza o formulário de criação
    customers = Customer.objects.all()
    menu_items = MenuItem.objects.filter(available=True)
    context = {
        'customers': customers,
        'menu_items': menu_items,
    }
    return render(request, 'orders/order_create.html', context)


def order_update_status(request, pk):
    """Atualizar status do pedido"""
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, f'Status do pedido #{order.id} atualizado!')
        return redirect('orders:detail', pk=order.id)
    
    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'orders/order_update_status.html', context)
    
