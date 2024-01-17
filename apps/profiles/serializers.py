from rest_framework import serializers
from django_countries.serializer_fields import CountryField

from .models import Profile
from apps.ratings.serializers import RatingSerializer

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    country = CountryField(name_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "full_name",
            "gender",
            "email",
            "id",
            "phone_number",
            "profile_photo",
            "about_me",
            "license",
            "country",
            "city",
            "is_buyer",
            "is_seller",
            "is_agent",
            "rating",
            "num_reviews",
            "reviews"
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"
    
    def get_reviews(self, obj):
        # Rating model => agent field => value of related_name prop == agent_reviewed is what points to profile
        reviews = obj.agent_review.all()
        print("====== ", reviews)
        # if many=True, you tell drf that queryset contains mutiple items (a list of items) 
        # so drf needs to serialize each item with serializer class (and serializer.data will be a list)
        serializer = RatingSerializer(reviews, many=True)
        return serializer.data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.top_agent:
            representation["top_agent"] = True
        return representation

class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "gender",
            "phone_number",
            "profile_photo",
            "about_me",
            "license",
            "country",
            "city",
            "is_buyer",
            "is_seller",
            "is_agent"
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.top_agent:
            representation["top_agent"] = True
        return representation
    