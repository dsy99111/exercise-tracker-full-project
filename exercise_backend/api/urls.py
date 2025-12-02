from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProgressViewSet, ConfigViewSet, LoginAPIView, get_daily_quote, user_routine_history

from .views import save_routine
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'progress', ProgressViewSet, basename='progress')
router.register(r'config', ConfigViewSet, basename='config')

urlpatterns = [
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("daily-quote/", get_daily_quote, name="daily-quote"),  # 👈 added
    path("save-routine/", save_routine),
    path("routine-history/<int:user_id>/", user_routine_history),


]


urlpatterns += router.urls
