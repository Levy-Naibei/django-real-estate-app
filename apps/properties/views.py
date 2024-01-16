import logging

import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import PropertyNotFound
from .pagination import PropertyPagination
from .models import Property, PropertyViews
from .serializers import (
    PropertyCreateSerializer,
    PropertyViewSerializer,
    PropertySerializer
)

logger = logging.getLogger(__name__)

class PropertyFilter(django_filters.FilterSet):
    advert_type = django_filters.CharFilter(lookup_expr="iexact", field_name="advert_type")
    property_type = django_filters.CharFilter(lookup_expr="iexact", field_name="property_type")
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Property
        field = ["advert_type", "property_type", "price"]

class ListAllPropertiesAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all().order_by("-created_at")
    pagination_class = PropertyPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PropertyFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]

class ListAgentsPropertyAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PropertyFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]
    
    # to change the queryset of list_api_view, use get_queryset method
    def get_queryset(self):
        user = self.request.user
        queryset = Property.objects.filter(user=user).order_by("-created_at")
        return queryset
    