from django.db import models


class MenuItem(models.Model):
    """Modelo para itens do cardápio"""
    CATEGORY_CHOICES = [
        ('BURGER', 'Hambúrguer'),
        ('PIZZA', 'Pizza'),
        ('DRINK', 'Bebida'),
        ('DESSERT', 'Sobremesa'),
        ('SIDE', 'Acompanhamento'),
    ]
    
    name = models.CharField('Nome', max_length=200)
    description = models.TextField('Descrição')
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    category = models.CharField('Categoria', max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField('Imagem', upload_to='menu/', blank=True, null=True)
    available = models.BooleanField('Disponível', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Item do Cardápio'
        verbose_name_plural = 'Itens do Cardápio'
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} - R$ {self.price}"
