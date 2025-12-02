import random
from datetime import date
from .models import Quote, DailyQuote

def update_daily_quote():
    quotes = list(Quote.objects.all())
    if not quotes:
        return

    today_quote = random.choice(quotes)

    DailyQuote.objects.update_or_create(
        id=1,
        defaults={
            "quote": today_quote,
            "date": date.today()
        }
    )
