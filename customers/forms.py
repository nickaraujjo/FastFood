from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    """Formulário para criar/editar clientes"""
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address', 'loyalty_points', 'referred_by']
        labels = {
            'name': 'Nome',
            'phone': 'Telefone',
            'email': 'E-mail',
            'address': 'Endereço',
            'loyalty_points': 'Pontos de Fidelidade',
            'referred_by': 'Indicado por',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'loyalty_points': forms.NumberInput(attrs={'class': 'form-control'}),
            'referred_by': forms.Select(attrs={'class': 'form-select'}),
        }
