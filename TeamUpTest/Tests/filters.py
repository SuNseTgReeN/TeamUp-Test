import django_filters
from .models import Poll


class PollFilterSet(django_filters.FilterSet):
    secret_key = django_filters.CharFilter(field_name='secret_key', lookup_expr='exact')

    class Meta:
        model = Poll
        fields = ('secret_key',)
