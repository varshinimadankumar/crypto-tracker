# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# tracker/models.py
from django.db import models
from decimal import Decimal

class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    coingecko_id = models.CharField(max_length=50)
    current_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)  # <-- add this


    def __str__(self):
        return self.symbol

class PricePoint(models.Model):
    crypto = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.crypto.symbol} {self.price} @ {self.timestamp}"

class Alert(models.Model):
    DIRECTION_CHOICES = (('above', 'Above'), ('below', 'Below'))
    crypto = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE, related_name='alerts')
    target_price = models.DecimalField(max_digits=20, decimal_places=8)
    direction = models.CharField(max_length=5, choices=DIRECTION_CHOICES)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    last_triggered = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert {self.crypto.symbol} {self.direction} {self.target_price} -> {self.email}"
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolio")
    crypto = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0'))

    class Meta:
        unique_together = ('user', 'crypto')  # One entry per user-crypto pair

    def __str__(self):
        return f"{self.user.username} owns {self.amount} {self.crypto.symbol}"