from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.profiles.models import Profile
from apps.profiles.exceptions import ProfileNotFound
from apps.ratings.serializers import RatingSerializer

from .models import Rating

User = get_user_model()


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_agent_review(request, profile_id):
    try:
        agent_profile = Profile.objects.get(id=profile_id, is_agent=True)
    except Profile.DoesNotExist:
        raise ProfileNotFound

    data = request.data

    profile_user = User.objects.get(pkid=agent_profile.user.pkid)
    if profile_user.email == request.user.email:
        return Response(
            {"message": "You can't rate yourself"}, status=status.HTTP_403_FORBIDDEN
        )

    already_reviewed = agent_profile.agent_review.filter(
        agent__pkid=profile_user.pkid
    ).exists()

    if already_reviewed:
        return Response(
            {"detail": "Profile already reviewed"}, status=status.HTTP_400_BAD_REQUEST
        )

    elif data["rating"] == 0:
        return Response(
            {"detail": "Please select a rating"}, status=status.HTTP_400_BAD_REQUEST
        )

    else:
        review = Rating.objects.create(
            rater=request.user,
            agent=agent_profile,
            rating=data["rating"],
            comment=data["comment"],
        )
        reviews = agent_profile.agent_review.all()
        agent_profile.num_reviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating
        agent_profile.rating = round(total / len(reviews), 2)
        agent_profile.save()
        return Response("Review Added")
