# Framework imports
from django.contrib.auth.models import BaseUserManager

# Framework imports
from src.user_auth.models.enums import RoleType


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, role=RoleType.USER, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=email.lower(),
            role=role,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, *args, **kwargs):
        user = self.create_user(
            email=email,
            password=password,
            role=RoleType.SUPER_USER
        )

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
