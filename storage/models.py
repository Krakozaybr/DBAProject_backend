import datetime

from django.db.models import (
    Model,
    ImageField,
    FloatField,
    TextField,
    ForeignKey,
    CASCADE,
    DateTimeField,
)
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("uploads", filename)


class ProcessedImage(Model):
    user = ForeignKey("authentication.User", on_delete=CASCADE)
    source = ImageField(upload_to=get_file_path, null=True)
    image_probability = FloatField()
    dirt_probability = FloatField()
    chip_probability = FloatField()
    bbox = TextField()
    points = TextField()
    created = DateTimeField(default=datetime.datetime.now)
