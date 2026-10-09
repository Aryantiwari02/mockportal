from rest_framework import serializers

from .models import Citizen


class CitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = [
            "id",
            "mobile",
            "full_name",
            "email",
            "address",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "mobile",
            "is_verified",
            "created_at",
            "updated_at",
        ]