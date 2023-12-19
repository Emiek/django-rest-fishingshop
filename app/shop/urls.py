from django.urls import path
from rest_framework.routers import SimpleRouter

from shop import views

app_name = 'shop'

urlpatterns = [
    path('products/', views.ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='products'),
    path('products/all/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='product-detail'),
    path('user/create/', views.CreateUserView.as_view(), name='create'),
    path('user/token/', views.CreateTokenView.as_view(), name='token'),
    path('user/profile/', views.ManageUserView.as_view(), name='profile'),
]
