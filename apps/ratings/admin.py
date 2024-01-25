from django.contrib import admin

from .models import Rating


class RatingAdmin(admin.ModelAdmin):
    list_display = ["rater", "agent", "rating"]
    list_display_links = ["rater", "agent"]
    list_filter = ["rating"]


admin.site.register(Rating, RatingAdmin)
