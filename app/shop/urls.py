from django.urls import path
from rest_framework.routers import SimpleRouter

from shop import views

app_name = 'shop'

router = SimpleRouter()

router.register('products', views.ProductViewSet, basename='products')

urlpatterns = router.urls
