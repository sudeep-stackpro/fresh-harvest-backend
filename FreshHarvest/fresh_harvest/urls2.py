from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views2 import CartView, CartViewSet,FarmProductsSearchView,OrderListCreateView,OrderDetailView,FarmProductDetailView,FarmerListView,DiscountDetailView, OrderViewSet, ProductModelViewset
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("product", ProductModelViewset)
router.register("cart",CartViewSet)
router.register("order",OrderViewSet)

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('authtoken/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/cart/', CartView.as_view(), name='cart'),
    # path('product/search/', FarmProductsSearchView.as_view(), name='farm-products-search'),
    path('order/', OrderListCreateView.as_view(), name='orders'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    # path('product/<int:pk>/', FarmProductDetailView.as_view(), name='farmproduct-detail'),
    path('farmers/', FarmerListView.as_view(), name='farmer-list'),
    path('discounts/<str:coupon_code>/', DiscountDetailView.as_view(), name='discount-detail'),
]

urlpatterns += router.urls