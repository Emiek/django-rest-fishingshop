from rest_framework import generics, authentication, permissions, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter
from shop.models import Product
from shop.serializers import ProductSerializer, UserSerializer, AuthTokenSerializer
from shop.filters import ProductFilter

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


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        """Retrieve and return authenticated user"""

        return self.request.user


