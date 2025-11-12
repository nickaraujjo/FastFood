from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import MenuItem


def menu_list(request):
    """Lista todos os itens do cardápio"""
    category = request.GET.get('category')
    if category:
        items = MenuItem.objects.filter(category=category, available=True)
    else:
        items = MenuItem.objects.filter(available=True)
    
    categories = MenuItem.CATEGORY_CHOICES
    context = {
        'items': items,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'menu/menu_list.html', context)


def menu_detail(request, pk):
    """Detalhes de um item do cardápio"""
    item = get_object_or_404(MenuItem, pk=pk)
    context = {'item': item}
    return render(request, 'menu/menu_detail.html', context)
