from django.shortcuts import render
from tracker.models import CryptoCurrency, PricePoint, Alert,Portfolio
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import PortfolioForm
from decimal import Decimal
import requests

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


@login_required
def home(request):
    # Fetch crypto prices
    cryptos = CryptoCurrency.objects.all()
    ids = ",".join([c.coingecko_id for c in cryptos])
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"

    try:
        response = requests.get(url, timeout=10).json()
    except Exception:
        response = {}

    coin_data = []
    for crypto in cryptos:
        price = response.get(crypto.coingecko_id, {}).get("usd", 0)
        coin_data.append({
            "id": crypto.id,
            "name": crypto.name,
            "symbol": crypto.symbol,
            "price": price,
        })

    # Handle portfolio form
    total_value = 0
    coin_values = []
    if request.method == "POST":
        for crypto in cryptos:
            price = response.get(crypto.coingecko_id, {}).get("usd", 0)
            amount = float(request.POST.get(f"amount_{crypto.id}") or 0)
            value = amount * price
            total_value += value

            coin_values.append({
                "id": crypto.id,
                "name": crypto.name,
                "symbol": crypto.symbol,
                "price": price,
                "amount": amount,
                "value": value
            })

    return render(request, "tracker/home.html", {
        "coin_data": coin_data,
        "coin_values": coin_values,
        "total_value": total_value,
    })


def create_alert(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alert created successfully!')
            return redirect('tracker:home')
    else:
        form = AlertForm()
    
@login_required
def add_to_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            portfolio_entry, created = Portfolio.objects.get_or_create(
                user=request.user,
                crypto=form.cleaned_data['crypto'],
                defaults={'amount': form.cleaned_data['amount']}
            )
            if not created:
                portfolio_entry.amount += form.cleaned_data['amount']
                portfolio_entry.save()
            return redirect('tracker:portfolio')
    else:
        form = PortfolioForm()
    return render(request, 'tracker/add_to_portfolio.html', {'form': form})


