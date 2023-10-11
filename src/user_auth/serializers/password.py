# Framework imports
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.db.models import Q
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True,
                                         validators=[password_validation.validate_password])
    confirm_new_password = serializers.CharField(required=True, write_only=True,
                                         validators=[password_validation.validate_password])
    user_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=User.objects.filter(is_active=True)
    )
    token = serializers.CharField(read_only=True)
    success = serializers.BooleanField(read_only=True, default=True)
    message = serializers.CharField(read_only=True, default="Password reset successfully")

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("confirm_new_password"):
            raise serializers.ValidationError("Confirm password doesn't match")
        return attrs

    # FIXME : Get user from UserHiddenField
    def save(self, request):
        user = self.validated_data.get("user_id")
        user.set_password(self.validated_data['new_password'])
        user.save()
        return None


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    success = serializers.BooleanField(read_only=True, default=True)
    message = serializers.CharField(read_only=True, default="OTP sent successfully")

    def validate(self, attrs):
        email = attrs.get('email').lower()
        channel = attrs.get("channel")
        user_inst = User.get_or_none(Q(email=email))
        attrs['user'] = user_inst
        if not user_inst:
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        elif user_inst and not user_inst.is_active:
            raise serializers.ValidationError({"email": "The account is deactivated. Please contact Administrator to activate your account"})
        return attrs

    def save(self, **kwargs):
        return self.validated_data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        if not self.context['request'].user.check_password(attrs['old_password']):
            raise serializers.ValidationError("Old password is incorrect")
        return attrs

    def save(self):
        user_obj = self.context['request'].user
        user_obj.set_password(self.validated_data['new_password'])
        user_obj.save()
        user_obj.auth_token.delete()
        token = Token.objects.create(user=user_obj)
        self.validated_data.update({'token': token.key})
        return self.validated_data


all = (
    "ResetPasswordSerializer",
    "ForgetPasswordSerializer",
    "ChangePasswordSerializer"
)