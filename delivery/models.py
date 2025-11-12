from django.db import models
from orders.models import Order


class DeliveryPerson(models.Model):
    """Modelo para entregadores"""
    STATUS_CHOICES = [
        ('AVAILABLE', 'Disponível'),
        ('BUSY', 'Ocupado'),
        ('OFFLINE', 'Offline'),
    ]
    
    name = models.CharField('Nome', max_length=200)
    phone = models.CharField('Telefone', max_length=20)
    vehicle = models.CharField('Veículo', max_length=100)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Entregador'
        verbose_name_plural = 'Entregadores'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.vehicle}"


class Delivery(models.Model):
    """Modelo para entregas"""
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('ASSIGNED', 'Atribuída'),
        ('IN_TRANSIT', 'Em Trânsito'),
        ('DELIVERED', 'Entregue'),
        ('FAILED', 'Falhou'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name='Pedido')
    delivery_person = models.ForeignKey(
        DeliveryPerson, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Entregador'
    )
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='PENDING')
    delivery_address = models.TextField('Endereço de Entrega')
    estimated_time = models.IntegerField('Tempo Estimado (minutos)', default=30)
    actual_delivery_time = models.DateTimeField('Hora da Entrega', null=True, blank=True)
    notes = models.TextField('Observações', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Entrega #{self.id} - Pedido #{self.order.id}"
