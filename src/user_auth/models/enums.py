from django.db.models import IntegerChoices, TextChoices


class RoleType(IntegerChoices):
    """
    SUPER_USER : is_superuser =True, is_staff = True and API LOGIN NOT ALLOWED
    USER : is_superuser =False, is_staff = True and API LOGIN ALLOWED
    """
    SUPER_USER = 0, "Super User"
    USER = 50, "User"


class GenderType(TextChoices):
    MALE = 'M', "Male"
    FEMALE = 'F', "Female"
    OTHER = 'O', "Other"


class DeviceType(TextChoices):
    IOS = 'IOS', "IOS"
    ANDROID = 'ANDROID', "ANDROID"
    WEB = 'WEB', "WEB"


__all__ = (
    "RoleType",
    "GenderType",
    "DeviceType"
)
