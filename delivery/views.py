from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Delivery, DeliveryPerson
from orders.models import Order
from .forms import DeliveryPersonForm


def delivery_list(request):
    """Lista todas as entregas"""
    status = request.GET.get('status')
    if status:
        deliveries = Delivery.objects.filter(status=status)
    else:
        deliveries = Delivery.objects.all()
    
    context = {
        'deliveries': deliveries,
        'status_choices': Delivery.STATUS_CHOICES,
        'selected_status': status,
    }
    return render(request, 'delivery/delivery_list.html', context)


def delivery_detail(request, pk):
    """Detalhes de uma entrega"""
    delivery = get_object_or_404(Delivery, pk=pk)
    context = {'delivery': delivery}
    return render(request, 'delivery/delivery_detail.html', context)


def delivery_assign(request, pk):
    """Atribuir entregador a uma entrega"""
    delivery = get_object_or_404(Delivery, pk=pk)
    
    if request.method == 'POST':
        person_id = request.POST.get('delivery_person')
        delivery_person = get_object_or_404(DeliveryPerson, pk=person_id)
        
        delivery.delivery_person = delivery_person
        delivery.status = 'ASSIGNED'
        delivery.save()
        
        delivery_person.status = 'BUSY'
        delivery_person.save()
        
        messages.success(request, f'Entrega atribuída a {delivery_person.name}!')
        return redirect('delivery:detail', pk=delivery.id)
    
    available_persons = DeliveryPerson.objects.filter(status='AVAILABLE')
    context = {
        'delivery': delivery,
        'available_persons': available_persons,
    }
    return render(request, 'delivery/delivery_assign.html', context)


def delivery_update_status(request, pk):
    """Atualizar status da entrega"""
    delivery = get_object_or_404(Delivery, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        delivery.status = new_status
        
        if new_status == 'DELIVERED':
            delivery.actual_delivery_time = timezone.now()
            delivery.order.status = 'DELIVERED'
            delivery.order.save()
            
            if delivery.delivery_person:
                delivery.delivery_person.status = 'AVAILABLE'
                delivery.delivery_person.save()
        
        delivery.save()
        messages.success(request, 'Status da entrega atualizado!')
        return redirect('delivery:detail', pk=delivery.id)
    
    context = {
        'delivery': delivery,
        'status_choices': Delivery.STATUS_CHOICES,
    }
    return render(request, 'delivery/delivery_update_status.html', context)


def delivery_person_list(request):
    """Lista todos os entregadores"""
    persons = DeliveryPerson.objects.all()
    context = {'persons': persons}
    return render(request, 'delivery/delivery_person_list.html', context)
from .forms import DeliveryPersonForm

# Criar novo entregador
def delivery_person_create(request):
    """Cria um novo entregador"""
    if request.method == 'POST':
        form = DeliveryPersonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entregador cadastrado com sucesso!')
            return redirect('delivery:person_list')
    else:
        form = DeliveryPersonForm()
    return render(request, 'delivery/delivery_person_form.html', {'form': form, 'title': 'Adicionar Entregador'})


# Editar entregador existente
def delivery_person_edit(request, pk):
    """Editar um entregador"""
    person = get_object_or_404(DeliveryPerson, pk=pk)
    if request.method == 'POST':
        form = DeliveryPersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entregador atualizado com sucesso!')
            return redirect('delivery:person_list')
    else:
        form = DeliveryPersonForm(instance=person)
    return render(request, 'delivery/delivery_person_form.html', {'form': form, 'title': 'Editar Entregador'})


# Remover entregador
def delivery_person_delete(request, pk):
    """Remover um entregador"""
    person = get_object_or_404(DeliveryPerson, pk=pk)
    if request.method == 'POST':
        person.delete()
        messages.success(request, 'Entregador removido com sucesso!')
        return redirect('delivery:person_list')
    return render(request, 'delivery/delivery_person_confirm_delete.html', {'person': person})
    
def delivery_create(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    delivery = Delivery.objects.create(order=order, status='PENDING')
    messages.success(request, "Entrega criada com sucesso!")
    return redirect('delivery:assign', pk=delivery.id)

