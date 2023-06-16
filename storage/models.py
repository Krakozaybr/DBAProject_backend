import os
import uuid

from django.db.models import (
    Model,
    ImageField,
    FloatField,
    TextField,
    CharField,
    ForeignKey,
    CASCADE,
    DateTimeField,
    BooleanField,
)


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("uploads", filename)


class ProcessedImage(Model):
    name = CharField(max_length=300, default="Request")
    user = ForeignKey(
        "authentication.User",
        on_delete=CASCADE,
    )
    source = ImageField(upload_to=get_file_path, default="placeholder.png")
    date_creation = DateTimeField()
    rotated = BooleanField(default=False)
    selected = BooleanField(default=False)


class Shape(Model):
    source = ForeignKey(ProcessedImage, on_delete=CASCADE, related_name="shapes")
    label = CharField(max_length=400)
    score = FloatField()
    bbox = TextField()
    polygon = TextField()


class Defect(Model):
    name = CharField(max_length=100)
    score = FloatField()
    shape = ForeignKey(Shape, on_delete=CASCADE, related_name="defects")
