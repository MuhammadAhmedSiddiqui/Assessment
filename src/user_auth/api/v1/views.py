# Framework imports
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

# App level imports
from src.user_auth.serializers import *
from src.utils.response import (error_response, success_response, error_response_account_not_verified)

User = get_user_model()


class LoginViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    authentication_classes = []

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return error_response_account_not_verified(serializer)
        serializer.save()
        return success_response(serializer=serializer, message="Login Successful")


class RegisterViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer=serializer, message="User created successfully", status_code=201)
        return error_response(serializer)


class ForgetPasswordViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )
    serializer_class = ForgetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer=serializer, message="OTP Sent Successfully")
        return error_response(serializer)


class ResetPasswordViewSet(viewsets.ViewSet):
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            return success_response(serializer=serializer, message="Password Reset Successful")
        return error_response(serializer)


class ChangePasswordViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer=serializer, message="Password Changed Successfully")
        return error_response(serializer)


class LogoutViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data={'success': True})
        serializer.save(request)
        return success_response(serializer=serializer, message="Logged Out Successfully", send_data=False)


__all__ = (
    "LoginViewSet",
    "RegisterViewSet",
    "ForgetPasswordViewSet",
    "ResetPasswordViewSet",
    "ChangePasswordViewSet",
    "LogoutViewSet"
)
