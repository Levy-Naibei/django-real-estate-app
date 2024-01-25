from django.urls import path

from .views import send_enquiry_email

urlpatterns = [path("mail/", send_enquiry_email, name="enquiry-mail")]
