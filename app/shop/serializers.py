from rest_framework import serializers
from shop import models
from user.serializers import UserSerializer
from user.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name')


class CommentSerializer(serializers.ModelSerializer):
    user_added = UserSerializer(read_only=True)
    date_add = serializers.DateField(read_only=True, format='%d %B %Y')

    class Meta:
        model = models.Comment
        fields = ('id', 'content', 'rating', 'date_add',
                  'user_added', 'product')

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be beetwen 1 and 5")
        return value


class ProductSerializer(serializers.ModelSerializer):
    date_added = serializers.DateField(read_only=True, format='%d %B %Y')
    comments = CommentSerializer(read_only=True, many=True, source='comment_set')
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=models.Category.objects.all(), source='category',
                                                  write_only=True)

    class Meta:
        model = models.Product
        fields = ('id', 'name', 'description', 'amount_rating',
                  'rating', 'price', 'stock', 'category','category_id', 'sold_count',
                  'date_added', 'img_url', 'points', 'comments')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("price must be a positive decimal")
        return value

    def validate_points(self, value):
        if value <= 0:
            raise serializers.ValidationError("price must be a positive number")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all(), source='product',
                                                     write_only=True)

    class Meta:
        model = models.OrderItem
        fields = ('id', 'order', 'product','product_id', 'quantity',
                  'price', 'loyalty_p')

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive number")
        return value


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, source='orderitem_set', read_only=True)

    class Meta:
        model = models.Order
        fields = ('id', 'user', 'products', 'total_price', 'total_loyalty', 'address', 'is_paid', 'date_add')
        read_only_fields = ('total_price', 'total_loyalty')
