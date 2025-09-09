from django.shortcuts import render
from tracker.models import CryptoCurrency, PriceAlert
from tracker.management.commands.fetch_prices import Command as FetchPricesCommand
import logging

logger = logging.getLogger('tracker')

def home(request):
    # Fetch latest prices each time homepage is loaded
    fetcher = FetchPricesCommand()
    fetcher.handle()

    # Get latest prices from database
    coins = CryptoCurrency.objects.all().order_by('name')

    # Optionally, fetch last alerts for display
    last_alerts = PriceAlert.objects.order_by('-timestamp')[:5]  # latest 5 alerts

    context = {
        'coins': coins,
        'last_alerts': last_alerts,
    }
    return render(request, 'tracker/home.html', context)
