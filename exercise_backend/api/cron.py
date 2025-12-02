from datetime import date
from .models import Quote, DailyQuote
import random

def update_daily_quote():
    quotes = Quote.objects.all()
    if not quotes:
        print("No quotes found.")
        return

    quote = random.choice(quotes)

    # Always create/update WITH quote (never NULL)
    dq, created = DailyQuote.objects.get_or_create(
        date=date.today(),
        defaults={"quote": quote}
    )

    if not created:  # already existed? update the quote
        dq.quote = quote
        dq.save()

    print("Daily quote updated:", quote.text[:40])
