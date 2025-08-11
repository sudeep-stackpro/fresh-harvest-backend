from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, FarmProductViewSet, OrderViewSet, FarmerViewSet, DiscountViewSet, RecipeViewSet, SearchProductsViewSet, UserCreateViewSet
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router.register('users', UserCreateViewSet, basename='user')
router.register('cart', CartItemViewSet, basename='cart')
router.register('farm-products', FarmProductViewSet, basename='farmproduct')
router.register('orders', OrderViewSet, basename='order')
router.register('farmers', FarmerViewSet, basename='farmer')
router.register('discounts', DiscountViewSet, basename='discount')
router.register('search',SearchProductsViewSet,basename='search')
router.register('recipe',RecipeViewSet,basename='recipe')

urlpatterns += router.urls
