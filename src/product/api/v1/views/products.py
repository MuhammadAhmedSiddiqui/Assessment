# Framework imports
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# App level imports
from src.product.serializer import ProductSerializer
from src.product.models import Product


class ProductModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related("created_by").all()
    filter_backends = (SearchFilter, )
    search_fields = ("name", "description", "price", "available_stock")

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

