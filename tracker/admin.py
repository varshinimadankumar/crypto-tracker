from django.contrib import admin
from .models import CryptoCurrency, PricePoint, Alert

@admin.register(CryptoCurrency)
class CryptoAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'coingecko_id')

@admin.register(PricePoint)
class PricePointAdmin(admin.ModelAdmin):
    list_display = ('crypto', 'price', 'timestamp')
    list_filter = ('crypto',)

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('crypto', 'direction', 'target_price', 'email', 'active', 'last_triggered')
    list_filter = ('active', 'crypto')
