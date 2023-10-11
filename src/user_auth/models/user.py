
# Framework level imports
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import (EmailField, Q)
from django.utils.translation import gettext_lazy as _

# App level imports
from src.user_auth.models.enums import RoleType, GenderType, DeviceType
from src.user_auth.models.managers import UserManager
from src.user_auth.models.abstract import TimeStampModel

# Other imports
import logging
from typing import Any


class User(AbstractUser, TimeStampModel):
    username = None
    email = EmailField(unique=True, verbose_name=_("Email"), db_index=True)
    role = models.PositiveSmallIntegerField(
        choices=RoleType.choices, verbose_name=_("Role"), default=RoleType.USER
    )
    gender = models.CharField(
        choices=GenderType.choices, verbose_name="Gender", default=None,
        null=True, blank=True, max_length=1
    )
    notification_enabled = models.BooleanField(default=True)
    image = models.ImageField(null=True)
    is_first_login = models.BooleanField(default=True)
    device_type = models.CharField(max_length=10, choices=DeviceType.choices, default=None, null=True)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = []

    objects: BaseUserManager[Any] = UserManager()

    @property
    def role_display(self):
        return self.get_role_display()

    @classmethod
    def get_or_none(cls, query: Q):
        try:
            return cls.objects.get(query)
        except cls.DoesNotExist:
            return None
        except cls.MultipleObjectsReturned:
            logging.error(f"Multiple objects returned for query {query}")
            return None

    class Meta:
        db_table = "users"


class UserFailedLogin(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="failed_logins")
    updated_at = None

    class Meta:
        verbose_name = _("User Failed Login")
        ordering = ("-created_at",)
        db_table = "user_failed_login"

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"
