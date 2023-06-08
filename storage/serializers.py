import json

from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import ProcessedImage


class ProcessedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedImage
        fields = "__all__"
        read_only_fields = ["pk", "user", "created"]

    def create(self, validated_data):
        validated_data["user"] = getattr(
            self.context.get("request", dict()), "user", None
        )
        return super().create(validated_data)
