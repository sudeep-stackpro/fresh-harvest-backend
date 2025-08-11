from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets,permissions
from django.shortcuts import get_object_or_404

from .models import  Farmer, FarmProduct, Cart, CartItem, Discount, Order
from .serializers import (
    CartSerializer, FarmProductWriteSerializer, OrderCreateSerializer,
    CartItemAddSerializer, FarmProductSerializer,
    OrderDetailSerializer, FarmerSerializer, DiscountSerializer,OrderSerializer
)

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


class CartView(APIView):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemAddSerializer(data=request.data)
        if serializer.is_valid():
            farm_product = get_object_or_404(FarmProduct, id=serializer.validated_data['farm_product_id'])
            quantity = serializer.validated_data['quantity']
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=farm_product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            return Response({"message": "Item added to cart successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        serializer = CartItemAddSerializer(data=request.data)
        if serializer.is_valid():
            farm_product = get_object_or_404(FarmProduct, id=serializer.validated_data['farm_product_id'])
            quantity = serializer.validated_data['quantity']
            cart_item = get_object_or_404(CartItem, cart=cart, product=farm_product)
            cart_item.quantity = quantity
            cart_item.save()
            return Response({"message": "Cart item quantity updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        farm_product_id = request.data.get('farm_product_id')

        if not farm_product_id:
            return Response({"error": "farm_product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = get_object_or_404(CartItem, cart=cart, product_id=farm_product_id)
        cart_item.delete()
        return Response({"message": "Cart item removed successfully"}, status=status.HTTP_200_OK)

# class CartViewSet(viewsets.ModelViewSet):
#     serializer_class = CartSerializer
#     queryset = Cart.objects.all()


# class OrderViewSet(viewsets.ModelViewSet):
#     serializer_class = OrderSerializer
#     queryset = Order.objects.all()
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
        


class FarmProductsSearchView(APIView):
    def get(self, request):
        queryset = FarmProduct.objects.all()
        product_name = request.query_params.get('name')
        if product_name:
            queryset = queryset.filter(product__name__icontains=product_name)
        serializer = FarmProductSerializer(queryset, many=True)
        return Response(serializer.data)


class OrderListCreateView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
        serializer = OrderDetailSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)


class FarmProductDetailView(APIView):
    def get(self, request, pk):
        farm_product = get_object_or_404(
            FarmProduct.objects.select_related('farm', 'product').prefetch_related('images', 'reviews'),
            pk=pk
        )
        serializer = FarmProductSerializer(farm_product)
        return Response(serializer.data)


class FarmerListView(APIView):
    def get(self, request):
        farmers = Farmer.objects.all().order_by('name')
        serializer = FarmerSerializer(farmers, many=True)
        return Response(serializer.data)


class DiscountDetailView(APIView):
    def get(self, request, coupon_code):
        discount = get_object_or_404(Discount, coupon_code=coupon_code)
        serializer = DiscountSerializer(discount)
        return Response(serializer.data)
