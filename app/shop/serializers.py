from rest_framework import serializers
from shop import models
from user.serializers import UserSerializer
from user.models import User


class CommetSerializer(serializers.ModelSerializer):
    user_added = UserSerializer(read_only=True)
    date_add = serializers.DateField(read_only=True, format='%d %B %Y')
    class Meta:
        model = models.Comment
        field = ('content', 'rating', 'date_add',
                 'user_added', 'product')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('name', 'description','amount_rating',
                  'rating', 'price', 'stock', 'category',
                  'date_added', 'img_url','points')


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    order = serializers.PrimaryKeyRelatedField(queryset=models.Order.objects.all())
    class Meta:
        model = models.OrderItem
        fields = ('order', 'product', 'quantity',
                  'price', 'loyalty_p')

class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = models.Order
        fields = ('user','products', 'total_price', 'total_loyalty', 'address', 'is_paid')