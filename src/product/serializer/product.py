# Framework imports
from rest_framework import serializers

# App level imports
from src.product.models import Product
from src.user_auth.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):

    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ("__all__")
        extra_kwargs = {
            "id": {
                "read_only": True
            }
        }

