# frameowrk imports
from django.db import models


class TimeStampModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    is_active = models.BooleanField(db_index=True, default=True)

    class Meta:
        abstract = True


__all__ = (
    "TimeStampModel", 
    "ActiveModel"
)