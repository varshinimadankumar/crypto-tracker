from django.shortcuts import render
from tracker.models import CryptoCurrency, PricePoint, Alert
from django.http import JsonResponse

def api_chart(request, crypto_id):
    try:
        coin = CryptoCurrency.objects.get(id=crypto_id)
    except CryptoCurrency.DoesNotExist:
        return JsonResponse({'error': 'Crypto not found'}, status=404)

    points = PricePoint.objects.filter(crypto=coin).order_by('timestamp')
    data = [{'timestamp': p.timestamp.isoformat(), 'price': float(p.price)} for p in points]
    return JsonResponse({'crypto': coin.symbol, 'prices': data})

def api_prices(request):
    coins = CryptoCurrency.objects.all()
    data = {}
    return JsonResponse(data)


def home(request):
    coins = CryptoCurrency.objects.all()

    # Attach latest price dynamically from PricePoint
    coin_data = []
    for coin in coins:
        latest = PricePoint.objects.filter(crypto=coin).order_by('-timestamp').first()
        coin_data.append({
            'name': coin.name,
            'symbol': coin.symbol,
            'price': latest.price if latest else None
        })

    # Get last 5 triggered alerts
    last_alerts = Alert.objects.filter(last_triggered__isnull=False).order_by('-last_triggered')[:5]

    context = {
        'coins': coin_data,
        'last_alerts': last_alerts,
    }

    return render(request, 'tracker/home.html', context)
def create_alert(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alert created successfully!')
            return redirect('tracker:home')
    else:
        form = AlertForm()
    
    return render(request, 'tracker/create_alert.html', {'form': form})