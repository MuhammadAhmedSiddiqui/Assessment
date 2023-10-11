# Framework imports
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

# App level imports
from src.user_auth.api.v1.views import *
from src.product.api.v1.views import products

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

# User/Authentication URLs
router.register('auth/login', LoginViewSet, basename='login')

router.register('auth/signup', RegisterViewSet, basename='register')
router.register('auth/logout', LogoutViewSet, basename='logout')
router.register('auth/forget-password', ForgetPasswordViewSet, basename='forget-password')
router.register('auth/reset-password', ResetPasswordViewSet, basename='reset-password')
router.register('auth/change-password', ChangePasswordViewSet, basename='change-password')

# Product URLs
router.register("product", products.ProductModelViewSet, basename="product-viewset")

urlpatterns = router.urls
