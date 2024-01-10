from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="profile.gender")
    phone_number = PhoneNumberField(source="profile.phone_number")
    profile_photo = serializers.CharField(source="profile.profile_photo")
    country = CountryField(source="profile.country")
    city = serializers.CharField(source="profile.city")
    top_seller = serializers.BooleanField(source="profile.top_seller")
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "gender",
            "phone_number",
            "profile_photo",
            "top_seller",
            "country",
            "city",
        ]
    
    def get_first_name(self, obj):
        return obj.first_name.title()
    
    def get_last_name(self, obj):
        return obj.last_name.title()
    
    # to dynamically put values to serializer fields
    def to_representation(self, instance):
        representation =  super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            # if user is admin, then add admin=True to serializer field
            representation["admin"] = True
        return representation

class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "username", "email", "username", "first_name", "last_name", "password"]
