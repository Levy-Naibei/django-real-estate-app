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

