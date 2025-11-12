from django.db import models
from django.conf import settings


class Customer(models.Model):
    """Modelo para clientes"""
    name = models.CharField('Nome', max_length=200)
    phone = models.CharField('Telefone', max_length=20)
    email = models.EmailField('E-mail', blank=True)
    address = models.TextField('Endereço')
    loyalty_points = models.IntegerField('Pontos de Fidelidade', default=0)
    referred_by = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Indicado por'
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.phone}"
    
    def get_order_history(self):
        """Retorna histórico de pedidos do cliente"""
        return self.order_set.all().order_by('-created_at')
    
    def get_referrals(self):
        """Retorna clientes indicados por este cliente"""
        return Customer.objects.filter(referred_by=self)
    
    def redeem_points(self, points):
        """Resgata pontos de fidelidade"""
        if self.loyalty_points >= points:
            self.loyalty_points -= points
            self.save()
            return True
        return False


class Referral(models.Model):
    """Modelo para rastrear indicações"""
    referrer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='referrals_made',
        verbose_name='Indicador'
    )
    referred = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='referral_received',
        verbose_name='Indicado'
    )
    bonus_points = models.IntegerField('Pontos de Bônus', default=0)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Indicação'
        verbose_name_plural = 'Indicações'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.referrer.name} indicou {self.referred.name}"
    
    def save(self, *args, **kwargs):
        if not self.bonus_points:
            self.bonus_points = settings.REFERRAL_BONUS_POINTS
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            self.referrer.loyalty_points += self.bonus_points
            self.referrer.save()
