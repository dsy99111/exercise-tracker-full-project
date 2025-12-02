from datetime import date
from .models import DailyQuote, Quote
import random

def update_daily_quote():
    # Pick random quote
    all_quotes = Quote.objects.all()
    if not all_quotes:
        return "No quotes available"

    quote = random.choice(all_quotes)

    # Overwrite today's daily quote
    dq, _ = DailyQuote.objects.get_or_create(date=date.today())
    dq.quote = quote
    dq.save()

    return f"Quote updated: {quote.text}"
