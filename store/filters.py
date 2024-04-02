import django_filters
from django_filters import DateFilter

from .models import *


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_ordered", lookup_expr='gte')
    end_date = DateFilter(field_name="date_ordered", lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['status']


class MenuFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = ['category']