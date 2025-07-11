import django_filters
from .models import Listing

class ListingFilter(django_filters.FilterSet):
    class Meta:
        model = Listing  # lowercase 'model'
        fields = {'brand': {'exact'}, }  # use a list, not a set
