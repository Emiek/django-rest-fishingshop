from rest_framework import viewsets
from shop.models import Product
from shop.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

