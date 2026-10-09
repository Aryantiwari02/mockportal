from rest_framework import serializers
from .models import Scheme


class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme

        fields = [
            "id",
            "category",
            "title",
            "short_description",
            "description",
            "eligibility",
            "eligibility_rules",
            "benefits",
            "documents",
            "application_process",
            "created_at",
            "updated_at",
            "application_fields",
            "translations",
        ]