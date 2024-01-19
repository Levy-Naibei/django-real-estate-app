from django.contrib import admin

from .models import Property, PropertyViews

class PropertyAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    list_display = ["user", "title", "country", "advert_type", "property_type", "views"]
    list_filter = ["advert_type", "property_type", "country"]

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyViews)

