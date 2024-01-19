import random
import string

from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator
from django.utils import timezone

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
    
    user = models.ForeignKey(
        User,
        verbose_name=_("Agent, Buyer or Seller"),
        related_name="agent_buyer", 
        on_delete=models.DO_NOTHING
    )
    title = models.CharField(verbose_name=_("Property title"), max_length=250)
    slug= AutoSlugField(populate_from="title", unique=True, always_update=True)
    description= models.TextField(verbose_name=_("Property description"), default="describe property....")
    ref_code = models.CharField(verbose_name=_("Reference Code"), max_length=255, unique=True, blank=True)
    country = CountryField(verbose_name=_("Country"), default="KE", blank_label="(select country)")
    city=models.CharField(verbose_name=_("City"),  default="Eldoret", max_length=180)
    postal_code = models.CharField(verbose_name=_("Postal code"), max_length=150, default="72")
    street_address=models.CharField(verbose_name=_("Street Address"), max_length=150, default="barng'etuny")
    property_number = models.IntegerField(
        verbose_name=_("Property number"), default=121, validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=8, decimal_places=2, default=0.0
    )
    tax = models.DecimalField(
        verbose_name=_("Property Tax"),
        max_digits=6,
        decimal_places=2,
        default=0.15,
        help_text="15% property tax charged",
    )
    plot_area = models.DecimalField(
        verbose_name=_("Plot Area(m^2)"), max_digits=8, decimal_places=2, default=0.0
    )
    total_floors = models.IntegerField(verbose_name=_("Number of floors"), default=0)
    bedrooms = models.IntegerField(verbose_name=_("Bedrooms"), default=1)
    bathrooms = models.DecimalField(verbose_name=_("Bathrooms"), max_digits=4, decimal_places=2, default=1.0)
    advert_type = models.CharField(
        verbose_name=_("Advert Type"),
        max_length=50,
        choices=AdvertType.choices,
        default=AdvertType.FOR_SALE,
    )
    
    property_type = models.CharField(
        verbose_name=_("Property Type"),
        max_length=50,
        choices=PropertyType.choices,
        default=PropertyType.OTHER,
    )

    cover_photo = models.ImageField(
        verbose_name=_("Main Photo"), default="/house_sample.jpg", null=True, blank=True
    )
    photo1 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    photo2 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    photo3 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    photo4 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    published_status = models.BooleanField(
        verbose_name=_("Published Status"), default=False
    )
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)
    date_created = models.DateTimeField(default=timezone.now)

    objects = models.Manager()
    published = PropertyPublishedManager()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
    
    # on every model save, automatically create ref_code
    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return super(Property, self).save(*args, **kwargs)

    @property
    def final_property_price(self):
        tax_in_percent = self.tax
        property_price = self.price
        tax_amount = round(tax_in_percent * property_price, 2)
        price_with_tax = float(round(tax_amount + property_price, 2))
        return price_with_tax
    

class PropertyViews(TimestampedUUIDModel):
    """tracks property views using ip address"""
    ip_address = models.CharField(verbose_name=_("IP Address"), max_length=255)
    property = models.ForeignKey(Property, related_name="property_views", on_delete=models.CASCADE)

    def __str__(self):
        return (f"Total views on - {self.property.title} is - {self.property.views}")
    
    class Meta:
        verbose_name="Total views on property"
        verbose_name_plural="Total property views"
        