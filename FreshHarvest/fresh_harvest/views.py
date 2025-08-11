from rest_framework import viewsets, status, permissions,mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Farmer, FarmProduct, Cart, CartItem, Discount, Order,User,Recipe
from .serializers import (
    CartSerializer, CartItemAddSerializer, FarmProductSerializer, FarmProductSimpleSerializer,
    OrderCreateSerializer, OrderDetailSerializer, FarmerSerializer,
    DiscountSerializer, OrderSerializer, RecipeSerializer, UserSerializer
)

class UserCreateViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]



class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemAddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart).select_related('product')

    def list(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        farm_product = get_object_or_404(FarmProduct, id=serializer.validated_data['farm_product_id'])
        quantity = serializer.validated_data['quantity']

        cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=farm_product,quantity=quantity)
        cart_item.quantity = quantity
        cart_item.save()
        return Response({"message": "Item added to cart successfully"}, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        quantity = request.data.get('quantity')
        if quantity is not None:
            instance.quantity = quantity
            instance.save()
            return Response({"message":f"Quantity updated susscessfully {quantity}"}, status=status.HTTP_200_OK)
        return Response({"error" : "No fields to Update "},status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Cart item removed successfully"}, status=status.HTTP_200_OK)
      

class FarmProductViewSet(viewsets.ModelViewSet):
        queryset = FarmProduct.objects.select_related('farm', 'product').prefetch_related('images', 'reviews')
        serializer_class = FarmProductSerializer 
        
        def retrieve(self, request, pk=None):
            try:
                product = FarmProduct.objects.get(pk=pk)
            except product.DoesNotExist:
                return Response({"error" : "No Such Product"},status=status.HTTP_204_NO_CONTENT)
            serializer = FarmProductSerializer(product)
            return Response(serializer.data)


class SearchProductsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FarmProductSerializer
    def get_queryset(self):
        queryset = FarmProduct.objects.all()
        product_name = self.request.query_params.get('name')
        if product_name:
            queryset = queryset.filter(product__name__icontains=product_name)
        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderDetailSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FarmerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Farmer.objects.all().order_by('name')
    serializer_class = FarmerSerializer


class DiscountViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'coupon_code'
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
