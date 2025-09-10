import requests
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
import logging
from tracker.models import CryptoCurrency, PricePoint, Alert
from tracker.utils import send_alert_email

logger = logging.getLogger('tracker')

COINGECKO_SIMPLE_PRICE = "https://api.coingecko.com/api/v3/simple/price"

class Command(BaseCommand):
    help = "Fetch latest prices from CoinGecko and evaluate alerts (one-shot)."

    def add_arguments(self, parser):
        parser.add_argument('--vs', default='usd', help='fiat currency (default: usd)')

    def handle(self, *args, **options):
        vs = options.get('vs', 'USD')
        cryptos = list(CryptoCurrency.objects.all())
        if not cryptos:
            self.stdout.write(self.style.WARNING("No cryptocurrencies configured. Add via admin."))
            return

        ids = ','.join([c.coingecko_id for c in cryptos])
        params = {'ids': ids, 'vs_currencies': vs}
        try:
            resp = requests.get(COINGECKO_SIMPLE_PRICE, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.exception("Error fetching from CoinGecko")
            self.stdout.write(self.style.ERROR(f"Fetch error: {e}"))
            return

        # save prices
        now = timezone.now()
        for c in cryptos:
            p = data.get(c.coingecko_id, {}).get(vs)
            if p is None:
                logger.info(f"No price for {c.coingecko_id}")
                continue
            price_dec = Decimal(str(p))
            PricePoint.objects.create(crypto=c, price=price_dec)
            logger.info(f"Saved price {c.symbol} {price_dec}")
            self.stdout.write(self.style.SUCCESS(f"{c.symbol}: {price_dec}"))

        # evaluate alerts
        alerts = Alert.objects.filter(active=True)
        for a in alerts:
            latest = PricePoint.objects.filter(crypto=a.crypto).order_by('-timestamp').first()
            if not latest:
                continue
            triggered = False
            if a.direction == 'above' and latest.price >= a.target_price:
                triggered = True
            elif a.direction == 'below' and latest.price <= a.target_price:
                triggered = True

            if triggered:
                # avoid frequent repeats - skip if triggered in last hour
                now = timezone.now()
                if a.last_triggered and (now - a.last_triggered).total_seconds() < 3600:
                    logger.info(f"Alert {a.id} recently triggered; skipping.")
                    continue

                subject = f"[Crypto Alert] {a.crypto.symbol} is {a.direction} {a.target_price}"
                html = f"""
                <p>Hi,</p>
                <p>The alert you set for <strong>{a.crypto.name} ({a.crypto.symbol})</strong> has been triggered.</p>
                <ul>
                <li>Direction: {a.direction}</li>
                <li>Target price: {a.target_price}</li>
                <li>Current price: {latest.price}</li>
                <li>Time: {latest.timestamp}</li>
                </ul>
                <p>— Crypto Tracker</p>
                """
                text = f"{a.crypto.symbol} {a.direction} {a.target_price}. Current: {latest.price} at {latest.timestamp}"

                try:
                    send_alert_email(a.email, subject, html, text)
                    a.last_triggered = now
                    a.save()
                    logger.info(f"Alert sent to {a.email} for {a.crypto.symbol}")
                    self.stdout.write(self.style.SUCCESS(f"Alert sent to {a.email}"))
                except Exception as e:
                    logger.exception("Failed to send alert email")
                    self.stdout.write(self.style.ERROR(f"Email send error: {e}"))

