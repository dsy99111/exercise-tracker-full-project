# api/views.py
from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .models import Progress, Config
from .serializers import UserSerializer, ProgressSerializer, ConfigSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from .models import DailyQuote
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import RoutineTracker
from django.utils import timezone

from datetime import date
from .models import User
User = get_user_model()


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin-only write: allow safe methods for everyone; writes only for admin.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # adjust as needed

    # limit creation to admin, or allow anyone? adjust here
    def get_permissions(self):
        if self.action in ['create']:
            # allow any to create (if you want open signup) OR restrict to admins:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.select_related('user').all().order_by('-date')
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        # optionally: set user to request.user if you want
        serializer.save()


class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    permission_classes = [IsAdminOrReadOnly]
# JWT Auth

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)

        return Response({
            "token": str(refresh.access_token),
            "refresh": str(refresh),
            "id": user.id,
            "username": user.username,
            "role": user.role
        })

@api_view(["GET"])
def get_daily_quote(request):
    dq = DailyQuote.objects.first()
    if not dq or dq.date != date.today():
        return Response({"quote": "No quote set for today"}, status=404)

    return Response({"quote": dq.quote.text})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_routine(request):
    data = request.data

    selected_minutes = (
        (data.get("emotionalMinutes") or 0) +
        (data.get("mentalMinutes") or 0) +
        (data.get("physicalMinutes") or 0)
    )

    # Max possible = 3 × 30 = 90
    progress_percent = round((selected_minutes / 90) * 100) if selected_minutes > 0 else 0

    tracker = RoutineTracker.objects.create(
        user=request.user,
        section=data.get("section"),
        emotional=data.get("emotional", False),
        mental=data.get("mental", False),
        physical=data.get("physical", False),

        emotional_minutes=data.get("emotionalMinutes", 0),
        mental_minutes=data.get("mentalMinutes", 0),
        physical_minutes=data.get("physicalMinutes", 0),

        progress_percent=progress_percent,

        start_time=data.get("start"),
        end_time=data.get("end"),
    )

    return Response({
        "message": "Routine saved",
        "id": tracker.id,
        "progress": progress_percent,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_routine_history(request, user_id):
    qs = RoutineTracker.objects.filter(user_id=user_id).order_by('-start_time')

    data = [
        {
            "id": r.id,
            "section": r.section,
            "emotional": r.emotional,
            "mental": r.mental,
            "physical": r.physical,
            "emotional_minutes": r.emotional_minutes,
            "mental_minutes": r.mental_minutes,
            "physical_minutes": r.physical_minutes,
            "progress": r.progress_percent,

            # FIXED → ALWAYS ISO-8601
            "start_time": r.start_time.isoformat() if r.start_time else None,
            "end_time": r.end_time.isoformat() if r.end_time else None,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in qs
    ]

    return Response(data)
