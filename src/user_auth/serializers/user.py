# Framework imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# App level imports
from src.user_auth.models.enums import (RoleType, DeviceType, GenderType)
from src.user_auth.serializers.image import Base64ImageField

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        exclude = ('password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login')


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True, required=True,
        validators=[password_validation.validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    image = Base64ImageField(required=False)

    device_type = serializers.ChoiceField(choices=DeviceType.choices, required=True)
    gender = serializers.ChoiceField(choices=GenderType.choices, default=None, required=False)
    gender_display = serializers.CharField(read_only=True, source="get_gender_display")
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    notification_enabled = serializers.BooleanField(read_only=True)
    role_display = serializers.CharField(read_only=True)
    role = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs['password1'] != password2:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        
        user = User.objects.create_user(
            email=validated_data.pop('email'), password=validated_data.pop('password1'), role=RoleType.USER,
            **validated_data
        )
        return user

    class Meta:
        model = User
        fields = (
            'email', 'password1', 'password2', "first_name", "last_name",
            "device_type", "gender", "date_joined",
            'notification_enabled', 'image', 'role_display', 'role', 'gender_display'
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    is_first_login = serializers.BooleanField(read_only=True, default=False)
    device_type = serializers.ChoiceField(write_only=True, required=True, choices=DeviceType.choices)
    user = serializers.DictField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')
        user = User.get_or_none(Q(email=email))  # check if user exists
        if user is None:
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect password."})
        if not user.is_active:
            raise serializers.ValidationError({"email": "User is not active."})

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data.get('user')
        token, created = Token.objects.get_or_create(user=user)
        utc_now = timezone.now()

        if not created and token.created < (utc_now - settings.AUTH_TOKEN_EXPIRATION):
            token.delete()
            token = Token.objects.create(user=user)

        self.validated_data['is_first_login'] = user.is_first_login

        if user.is_first_login:
            user.is_first_login = False
            user.save()
        
        self.validated_data["user"] = UserSerializer(instance=user).data
        return self.validated_data.update({'token': token.key})


class LogoutSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    message = serializers.CharField(read_only=True)

    def validate(self, attrs):
        return attrs

    def save(self, request, **kwargs):
        request.user.auth_token.delete()
        return None


__all__ = (
    "RegisterSerializer",
    "LoginSerializer",
    "LogoutSerializer",
    "UserSerializer"
)
