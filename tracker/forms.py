from django import forms
from .models import Alert

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
