from django.core.management.base import BaseCommand
from api.tasks import update_daily_quote

class Command(BaseCommand):
    help = "Updates the daily quote"

    def handle(self, *args, **kwargs):
        update_daily_quote()
        self.stdout.write(self.style.SUCCESS("Daily quote updated"))
