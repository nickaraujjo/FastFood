from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Customer, Referral
from django.conf import settings
from .forms import CustomerForm



def customer_list(request):
    """Lista todos os clientes"""
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'customers/customer_list.html', context)


def customer_detail(request, pk):
    """Detalhes de um cliente"""
    customer = get_object_or_404(Customer, pk=pk)
    order_history = customer.get_order_history()
    referrals = customer.get_referrals()
    
    context = {
        'customer': customer,
        'order_history': order_history,
        'referrals': referrals,
    }
    return render(request, 'customers/customer_detail.html', context)

def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('customers:detail', pk=pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'customer': customer})

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('customers:list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})


def customer_create(request):
    """Criar novo cliente"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        referred_by_id = request.POST.get('referred_by')
        
        customer = Customer.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address
        )
        
        if referred_by_id:
            referrer = get_object_or_404(Customer, pk=referred_by_id)
            customer.referred_by = referrer
            customer.save()
            
            Referral.objects.create(
                referrer=referrer,
                referred=customer
            )
        
        messages.success(request, f'Cliente {customer.name} cadastrado com sucesso!')
        return redirect('customers:detail', pk=customer.id)
    
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'customers/customer_create.html', context)


def customer_redeem_points(request, pk):
    """Resgatar pontos de fidelidade"""
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        points = int(request.POST.get('points', 0))
        
        if customer.redeem_points(points):
            discount = points / settings.LOYALTY_POINTS_PER_REAL
            messages.success(
                request, 
                f'{points} pontos resgatados! Desconto de R$ {discount:.2f} aplicado.'
            )
        else:
            messages.error(request, 'Pontos insuficientes!')
        
        return redirect('customers:detail', pk=customer.id)
    
    context = {'customer': customer}
    return render(request, 'customers/customer_redeem_points.html', context)
