import django_filters

from shop.models import Category, Product


class ProductFilter(django_filters.rest_framework.FilterSet):
    """Filers for webcam list"""
    category = django_filters.ModelMultipleChoiceFilter(to_field_name='id', queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'category',)
