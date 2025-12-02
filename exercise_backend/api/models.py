# api/models.py
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

from django.utils import timezone

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'user')
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Full custom user model to replace AppUser.
    Uses `username` as the unique identifier (same as original IndexedDB).
    """
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True, db_index=True)
    # password field is provided by AbstractBaseUser (stores hashed password)
    role = models.CharField(max_length=50, default='user', db_index=True)

    # standard Django admin/staff flags
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"


class Progress(models.Model):
    """
    Maps to STORE_PROGRESS.
    param1..param5 map to params.p1..p5 from the original client structure.
    """
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='progresses', db_index=True
    )
    # Choose DateField or DateTimeField depending on original data. Using DateField by default.
    date = models.DateField(db_index=True)
    challenge = models.CharField(max_length=200, blank=True, null=True)
    minutes = models.PositiveIntegerField(default=0)

    # Parameters — numeric, allow null if absent
    param1 = models.FloatField(null=True, blank=True)
    param2 = models.FloatField(null=True, blank=True)
    param3 = models.FloatField(null=True, blank=True)
    param4 = models.FloatField(null=True, blank=True)
    param5 = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'progress'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"Progress {self.id} - {self.user.username} on {self.date}"


class Config(models.Model):
    """
    Maps to STORE_CONFIG. key is primary key; value stored as JSONB (Django JSONField uses JSONB on PG).
    """
    key = models.CharField(max_length=100, primary_key=True)
    value = models.JSONField()

    class Meta:
        db_table = 'config'

    def __str__(self):
        return f"Config: {self.key}"
class Quote(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class DailyQuote(models.Model):
    date = models.DateField(default=timezone.localdate)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.date} – {self.quote.text[:40]}"


class RoutineTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.CharField(max_length=20)  # morning, micro, evening

    emotional = models.BooleanField(default=False)
    mental = models.BooleanField(default=False)
    physical = models.BooleanField(default=False)

    emotional_minutes = models.PositiveIntegerField(default=0)
    mental_minutes = models.PositiveIntegerField(default=0)
    physical_minutes = models.PositiveIntegerField(default=0)

    progress_percent = models.PositiveIntegerField(default=0)  # NEW FIELD

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_time']
