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
        fields = ["advert_type", "property_type", "price"]


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


class ListAgentsPropertiesAPIView(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
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
        print("agent ==== ", user)
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

        if not PropertyViews.objects.filter(property=property, ip_address=ip_addr).exists():
            PropertyViews.objects.create(property=property, ip_address=ip_addr)
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
            {"error": "Not your property. You can't update it."}, status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "PUT":
        data = request.data
        serializer = PropertySerializer(property, data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_property_api_view(request):
    user = request.user
    data = request.data
    data["user"] = request.user.pkid
    serializer = PropertyCreateSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        logger.info(
            f"Property {serializer.data.get('title')} created by {user.username}"
        )
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_property_api_view(request, slug):
    try:
        property = Property.objects.get(slug=slug)
    except Property.DoesNotExist:
        raise PropertyNotFound

    user = request.user
    if property.user != user:
        return Response(
            {"error": "Not your property. You can't delete!"}, status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "DELETE":
        delete_operation = property.delete()
        data = {}
        if delete_operation:
            data["success"] = "Delete successful!"
        else:
            data["failure"] = "Delete failed!"
        return Response(data=data)


@api_view(["POST"])
def upload_property_image(request):
    data = request.data
    print("property image ==== ", data)
    property_id = data["property_id"]
    property = Property.objects.get(id=property_id)
    property.cover_photo = request.FILES.get("cover_photo")
    property.photo1 = request.FILES.get("photo1")
    property.photo2 = request.FILES.get("photo2")
    property.photo3 = request.FILES.get("photo3")
    property.photo4 = request.FILES.get("photo4")
    property.save()
    return Response("Image(s) upload")


class PropertySearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PropertyCreateSerializer

    def post(self, request):
        queryset = Property.objects.filter(published_status=True)

        data = request.data
        advert_type = data["avert_type"]
        queryset = Property.objects.filter(advert_type__iexact=advert_type)

        property_type = data["property_type"]
        queryset = Property.objects.filter(advert_type__iexact=property_type)

        price = data["price"]
        if price == "$0":
            price = 0
        elif price == "$50,000":
            price = 50000
        elif price == "$100,000":
            price = 100000
        elif price == "$200,000":
            price = 200000
        elif price == "$400,000":
            price = 400000
        elif price == "$600,000":
            price = 600000
        elif price == "Any":
            price = -1

        if price != -1:
            queryset.filter(price__gte=price)

        bedrooms = data["bedrooms"]
        if bedrooms == "0+":
            bedrooms = 0
        elif bedrooms == "1+":
            bedrooms = 1
        elif bedrooms == "2+":
            bedrooms = 2
        elif bedrooms == "3+":
            bedrooms = 3
        elif bedrooms == "4+":
            bedrooms = 4
        elif bedrooms == "5+":
            bedrooms = 5

        queryset.filter(bedrooms__gte=bedrooms)

        bathrooms = data["bathrooms"]
        if bathrooms == "0+":
            bathrooms = 0.0
        elif bathrooms == "1+":
            bathrooms = 1.0
        elif bathrooms == "2+":
            bathrooms = 2.0
        elif bathrooms == "3+":
            bathrooms = 3.0
        elif bathrooms == "4+":
            bathrooms = 4.0

        queryset = queryset.filter(bathrooms__gte=bathrooms)

        catch_phrase = data["catch_phrase"]
        queryset = queryset.filter(description_icontains=catch_phrase)
        serializer = PropertySerializer(queryset, many=True)
        return Response(serializer.data)
