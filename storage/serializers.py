import json

from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework_guardian.serializers import ObjectPermissionsAssignmentMixin

from core.mixins import EditPermissionsMixin
from .models import ProcessedImage, Shape, Defect


class DefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defect
        fields = [
            "name",
            "score",
        ]


class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_internal_value(self, data):
        return str(data)

    def to_representation(self, value):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value


class ShapeSerializer(WritableNestedModelSerializer):

    defects = DefectSerializer(many=True)
    bbox = JSONSerializerField()
    polygon = JSONSerializerField()

    class Meta:
        model = Shape
        fields = ["label", "score", "bbox", "polygon", "defects"]


class ProcessedImageSerializer(
    WritableNestedModelSerializer,
    EditPermissionsMixin,
    ObjectPermissionsAssignmentMixin,
):

    shapes = ShapeSerializer(many=True)
    dateCreation = serializers.DateTimeField(source="date_creation")

    class Meta:
        model = ProcessedImage
        fields = ["id", "dateCreation", "shapes"]
        read_only_fields = ["id", "source"]

    def create(self, validated_data):
        validated_data["user"] = getattr(
            self.context.get("request", dict()), "user", None
        )
        return super().create(validated_data)


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedImage
        fields = ["source"]
