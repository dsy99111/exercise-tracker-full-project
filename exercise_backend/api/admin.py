# api/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib import messages

from .models import User, Progress, Config, Quote, DailyQuote
import random
from .models import RoutineTracker


# ------------------------
# Custom Admin Action
# ------------------------

@admin.action(description="Set Today's Quote (Random)")
def set_todays_quote(modeladmin, request, queryset):
    """Pick a random Quote and set as DailyQuote for today."""
    quotes = Quote.objects.all()
    if not quotes:
        messages.error(request, "No quotes available to select.")
        return

    chosen = random.choice(quotes)

    dq, created = DailyQuote.objects.get_or_create(date=timezone.now().date())
    dq.quote = chosen
    dq.save()

    messages.success(request, f"Today's quote set to: {chosen.text[:50]}...")


@admin.action(description="Set Selected Quote as Today's Quote")
def set_selected_quote(modeladmin, request, queryset):
    """Admin selects exactly one quote and sets it."""
    if queryset.count() != 1:
        messages.error(request, "Please select exactly ONE quote.")
        return

    quote = queryset.first()

    dq, created = DailyQuote.objects.get_or_create(date=timezone.now().date())
    dq.quote = quote
    dq.save()

    messages.success(request, f"Today's quote updated to: {quote.text[:50]}...")


# ------------------------
# User Admin
# ------------------------

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ()}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'is_staff', 'is_superuser'),
        }),
    )
    list_display = ('username', 'role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'role')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


# ------------------------
# Other Models
# ------------------------

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'challenge', 'minutes', 'created_at')
    list_filter = ('date', 'challenge')
    search_fields = ('user__username', 'challenge')


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('key',)
    search_fields = ('key',)


# ------------------------
# Quote Model with Actions
# ------------------------

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    search_fields = ('text',)
    actions = [set_todays_quote, set_selected_quote]


# ------------------------
# Daily Quote
# ------------------------

@admin.register(DailyQuote)
class DailyQuoteAdmin(admin.ModelAdmin):
    list_display = ('date', 'quote')
    search_fields = ('quote__text',)

@admin.register(RoutineTracker)
class RoutineTrackerAdmin(admin.ModelAdmin):
    list_display = ("user", "section", "start_time", "end_time")
    list_filter = ("section", "user")
