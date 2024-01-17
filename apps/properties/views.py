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
    PropertySerializer,
)

logger = logging.getLogger(__name__)


class PropertyFilter(django_filters.FilterSet):
    advert_type = django_filters.CharFilter(
        lookup_expr="iexact", field_name="advert_type"
    )
    property_type = django_filters.CharFilter(
        lookup_expr="iexact", field_name="property_type"
    )
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


class PropertyViewsAPIView(generics.ListAPIView):
    serializer_class = PropertyViewSerializer
    queryset = PropertyViews.objects.all()


class PropertyDetailAPIView(APIView):
    def get(self, request, slug):
        property = Property.objects.get(slug=slug)

        # whenever user visits this site via proxy-server,
        # then the http_via is the ip addr of proxy server and
        # http_x_forwarded_for is the ip addr fo the actual user who uses the proxy server
        x_forwarded_for = request.META.get("HTTP_FORWARDED_FOR")
        if x_forwarded_for:
            ip_addr = x_forwarded_for.split(",")[0]
        else:
            ip_addr = request.META.get("REMOTE_ADDR")

        if not PropertyViews.objects.filter(property=property, ip=ip_addr).exists():
            PropertyViews.objects.create(property=property, ip=ip_addr)
            # views to property will only increment if user goes to DETAIL_VIEW of property
            # for each unique user using the ip_addr
            property.views += 1
            property.save()

        serializer = PropertySerializer(property, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_property_api_view(request, slug):
    try:
        property = Property.objects.get(slug=slug)
    except Property.DoesNotExist:
        raise PropertyNotFound

    user = request.user
    if property.user != user:
        return Response(
            {"error": "Not your property"}, status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "PUT":
        data = request.data
        serializer = PropertySerializer(property, data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)