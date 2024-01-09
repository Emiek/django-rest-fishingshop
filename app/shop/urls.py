from django.urls import path

from shop import views

app_name = 'shop'

urlpatterns = [
    path('products/', views.ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='products'),
    path('products/all/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='product-detail-admin'),
    path('product_detail/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('user_favourite_products/', views.FavouriteProductListCreateView.as_view(),
         name='favourite-product-list-create'),
    path('orders/', views.OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list'),
    path('orders/<int:pk>/', views.OrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='order-detail'),
    path('order_items/', views.OrderItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list'),
    path('order_items/<int:pk>/',
         views.OrderItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='order-detail'),
    path('comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list-admin'),
    path('comments/<int:pk>/', views.CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='comment-detail-admin'),
    path('comments_list/', views.CommentListView.as_view(), name='comment-list'),
    path('categories/', views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    path('categories/<int:pk>/',
         views.CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='category-detail'),
    path('orders_user/', views.UserOrderListView.as_view(), name='user-order-list'),
]
