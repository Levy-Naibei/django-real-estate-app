from django.core.mail import send_mail
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from real_estate.settings.development import DEFAULT_FROM_EMAIL

from .models import Enquiry


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def send_enquiry_email(request):
    data = request.data
    try:
        name = data["name"]
        subject = data["subject"]
        email = data["email"]
        from_email = data["email"]
        phone_number = data["phone_number"]
        message = data["message"]
        recipient_list = [DEFAULT_FROM_EMAIL]

        send_mail(from_email, subject, message, recipient_list, fail_silently=True)
        enquiry = Enquiry(
            name=name,
            email=email,
            phone_number=phone_number,
            message=message,
            subject=subject,
        )
        enquiry.save()
        return Response({"Success": "Enquiry email submitted successfully"})

    except Exception:
        return Response({"Error": "Error occured while trying to send"})
