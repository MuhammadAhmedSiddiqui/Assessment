# Framework imports
from django.db import models
from django.contrib.auth import get_user_model

# App level imports
from src.user_auth.models.abstract import (TimeStampModel, ActiveModel)

USER = get_user_model()


class Product(TimeStampModel, ActiveModel):
    name = models.CharField(max_length=31, unique=True)
    description = models.TextField()
    price = models.FloatField()
    available_stock = models.IntegerField()
    created_by = models.ForeignKey(to=USER, on_delete=models.CASCADE, related_name="get_user_products")

    class Meta:
        db_table = "products"

