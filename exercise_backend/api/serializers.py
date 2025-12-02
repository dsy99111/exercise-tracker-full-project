# api/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Progress, Config
from .models import RoutineTracker
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'role', 'is_staff', 'is_superuser', 'date_joined')
        read_only_fields = ('id', 'date_joined', 'is_staff', 'is_superuser')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ProgressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Progress
        fields = ('id', 'user', 'date', 'challenge', 'minutes',
                  'param1', 'param2', 'param3', 'param4', 'param5', 'created_at')
        read_only_fields = ('id', 'created_at')


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ('key', 'value')


class RoutineTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineTracker
        fields = "__all__"
