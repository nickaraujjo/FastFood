from django.db import models
from customers.models import Customer
from menu.models import MenuItem
from django.conf import settings


class Order(models.Model):
    """Modelo para pedidos"""
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('PREPARING', 'Em Preparação'),
        ('READY', 'Pronto para Entrega'),
        ('DELIVERED', 'Entregue'),
        ('CANCELLED', 'Cancelado'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Cliente')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField('Preço Total', max_digits=10, decimal_places=2, default=0)
    notes = models.TextField('Observações', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.customer.name}"
    
    def calculate_total(self):
        """Calcula o total do pedido"""
        total = sum(item.subtotal for item in self.items.all())
        self.total_price = total
        self.save()
        return total
    
    def add_loyalty_points(self):
        """Adiciona pontos de fidelidade ao cliente"""
        points = int(self.total_price * settings.LOYALTY_POINTS_PER_REAL)
        self.customer.loyalty_points += points
        self.customer.save()


class OrderItem(models.Model):
    """Modelo para itens do pedido"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Pedido')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name='Item do Cardápio')
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço Unitário', max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
    
    @property
    def subtotal(self):
        return self.quantity * self.price
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.menu_item.price
        super().save(*args, **kwargs)
