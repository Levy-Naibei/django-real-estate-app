from django.db import models
from django.utils.translation import gettext_lazy as _

from real_estate.settings.base import AUTH_USER_MODEL
from apps.common.models import TimestampedUUIDModel
from apps.profiles.models import Profile

class Rating(TimestampedUUIDModel):
    class Range(models.IntegerChoices):
        RATING_1 = 1, _("1")
        RATING_2 = 2, _("2")
        RATING_3 = 3, _("3")
        RATING_4 = 4, _("4")
        RATING_5 = 5, _("5")

    rater = models.ForeignKey(
        AUTH_USER_MODEL, 
        verbose_name=_("User providng the rating"),
        null=True, 
        on_delete=models.SET_NULL
    )
    agent = models.ForeignKey(
        Profile,
        verbose_name=_("Agent being rated"),
        related_name="agent_reviewed",
        null=True, 
        on_delete=models.SET_NULL
    )
    rating = models.IntegerField(
        verbose_name=_("Rating"),
        choices=Range.choices,
        default=0,
        help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent"
    )
    comment = models.TextField(verbose_name=_("Comment"))

    class Meta:
        unique_together = ["rater", "agent"] # Sets of field names that, taken together, must be unique

    def __str__(self):
        return f"{self.agent} rated at {self.rating}"
    