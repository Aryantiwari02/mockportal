from django.contrib import admin
from .models import Scheme


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "category",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "id",
        "title",
        "short_description",
        "description",
    )