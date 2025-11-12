from django.shortcuts import render
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from orders.models import Order, OrderItem
from delivery.models import DeliveryPerson, Delivery


def sales_report(request):
    """Relatório de vendas"""
    period = request.GET.get('period', 'daily')
    delivery_person_id = request.GET.get('delivery_person')
    
    now = timezone.now()
    
    if period == 'daily':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        period_label = 'Hoje'
    elif period == 'weekly':
        start_date = now - timedelta(days=7)
        period_label = 'Últimos 7 dias'
    elif period == 'monthly':
        start_date = now - timedelta(days=30)
        period_label = 'Últimos 30 dias'
    else:
        start_date = None
        period_label = 'Todo o período'
    
    orders = Order.objects.filter(status='DELIVERED')
    
    if start_date:
        orders = orders.filter(created_at__gte=start_date)
    
    if delivery_person_id:
        orders = orders.filter(delivery__delivery_person_id=delivery_person_id)
    
    total_revenue = orders.aggregate(total=Sum('total_price'))['total'] or 0
    total_orders = orders.count()
    
    # Itens mais vendidos
    best_selling = OrderItem.objects.filter(
        order__in=orders
    ).values(
        'menu_item__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_quantity')[:10]
    
    # Vendas por categoria
    category_sales = OrderItem.objects.filter(
        order__in=orders
    ).values(
        'menu_item__category'
    ).annotate(
        total=Sum('price')
    ).order_by('-total')
    
    delivery_persons = DeliveryPerson.objects.all()
    
    context = {
        'period': period,
        'period_label': period_label,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'best_selling': best_selling,
        'category_sales': category_sales,
        'delivery_persons': delivery_persons,
        'selected_delivery_person': delivery_person_id,
    }
    return render(request, 'reports/sales_report.html', context)


def delivery_performance(request):
    """
    Relatório de desempenho dos entregadores.
    Calcula total de entregas e uma pontuação baseada em entregas concluídas.
    """
    delivery_persons = DeliveryPerson.objects.annotate(
        total_deliveries=Count('delivery', filter=Q(delivery__status='DELIVERED'))
    )

    # Calcular pontuação: 10 pontos por entrega concluída
    for person in delivery_persons:
        person.score = person.total_deliveries * 10  # ajuste conforme sua regra

    context = {
        'delivery_persons': delivery_persons
    }
    return render(request, 'reports/delivery_performance.html', context)