from rest_framework import generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter
from shop.models import Product, Order, Comment, Category, OrderItem
from shop.serializers import (OrderSerializer, ProductSerializer,
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


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Product.objects.all()
