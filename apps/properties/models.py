import random
import string

from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_countries.serializer_fields import CountryField
from django.core.validators import MinValueValidator

from apps.common.models import TimestampedUUIDModel

User = get_user_model()

class PropertyPublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super(PropertyPublishedManager, self)
            .get_queryset()
            .filter(published_status=True)
        )

class Property(TimestampedUUIDModel):
    class AdvertType(models.TextChoices):
        FOR_SALE="For Sale", _("For Sale")
        FOR_RENT="For Rent", _("For Rent")
        AUCTION="Auction", _("Auction")
    
    class PropertyType(models.TextChoices):
        HOUSE="House", _("House")
        APARTMENT="Apartment", _("Apartment")
        OFFICE="Office", _("Office")
        WAREHOUSE="Warehouse", _("Warehouse")
        COMMERCIAL="Commercial", _("Commercial")
        OTHER="Other", _("Other")
    
    