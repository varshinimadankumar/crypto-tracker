from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import CryptoCurrency, PricePoint, Alert
from .forms import AlertForm
from django.views.decorators.http import require_GET

def index(request):
    cryptos = CryptoCurrency.objects.all()
    latest_prices = []
    for c in cryptos:
        latest = c.prices.order_by('-timestamp').first()
        latest_prices.append({
            'id': c.id,
            'name': c.name,
            'symbol': c.symbol,
            'price': float(latest.price) if latest else None,
            'timestamp': latest.timestamp.isoformat() if latest else None
        })
    return render(request, 'tracker/index.html', {'prices': latest_prices, 'cryptos': cryptos, 'alert_form': AlertForm()})

@require_GET
def api_prices(request):
    cryptos = CryptoCurrency.objects.all()
    data = []
    for c in cryptos:
        latest = c.prices.order_by('-timestamp').first()
        data.append({
            'id': c.id,
            'name': c.name,
            'symbol': c.symbol,
            'price': float(latest.price) if latest else None,
            'timestamp': latest.timestamp.isoformat() if latest else None
        })
    return JsonResponse({'prices': data})

@require_GET
def api_chart(request, crypto_id):
    points = PricePoint.objects.filter(crypto_id=crypto_id).order_by('timestamp')[:500]
    labels = [p.timestamp.strftime('%Y-%m-%d %H:%M:%S') for p in points]
    values = [float(p.price) for p in points]
    return JsonResponse({'labels': labels, 'values': values})

def create_alert(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracker:index')
    return redirect('tracker:index')
