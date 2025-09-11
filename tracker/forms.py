from django import forms
from .models import Alert
from .models import Portfolio

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['crypto', 'direction', 'target_price', 'email']
        widgets = {
            'crypto': forms.Select(attrs={'class': 'form-control'}),
            'direction': forms.Select(attrs={'class': 'form-control'}),
            'target_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['crypto', 'amount']
        widgets = {
            'crypto': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'}),
        }
