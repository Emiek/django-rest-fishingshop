from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from shop.models import Product, Order, Comment, Category, OrderItem, FavouriteProduct
from shop.serializers import (OrderSerializer, ProductSerializer, FavouriteProductSerializer,
                              CommentSerializer, OrderItemSerializer, CategorySerializer)
from shop.filters import ProductFilter


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    queryset = Category.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    queryset = Product.objects.all()


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ('name', 'description', 'category__name')
    filter_backends = (DjangoFilterBackend, SearchFilter)


class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class FavouriteProductListCreateView(generics.ListCreateAPIView):
    queryset = FavouriteProduct.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = FavouriteProductSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return FavouriteProduct.objects.all()
        else:
            return FavouriteProduct.objects.filter(user=user.id)

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        product_ids = request.data.get('product_ids', [])
        favourites = []
        for product_id in product_ids:
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                return Response({"detail": f"Product with ID {product_id} not found"}, status=status.HTTP_404_NOT_FOUND)

            favourite_product = FavouriteProduct(user=self.request.user, product=product)
            favourite_product.save()
            favourites.append(favourite_product)

        serializer = FavouriteProductSerializer(favourites, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = Order.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=user.id)

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = OrderItem.objects.all()

    def create(self, request, *args, **kwargs):

        data = request.data
        order_id = int(data.get('order', 0))
        product_id = int(data.get('product_id', 0))
        quantity = int(data.get('quantity', 0))


        order_instance = get_object_or_404(Order, pk=order_id)


        order_item = OrderItem(order=order_instance, product_id=product_id, quantity=quantity)
        order_item.save()


        order_instance.sum_price_points()
        order_instance.save(update_fields=['total_price', 'total_loyalty'])

        # Utwórz odpowiedź
        serializer = self.get_serializer(order_item)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user_added=self.request.user)


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
