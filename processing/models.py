from django.db.models import (
    Model,
    ForeignKey,
    CASCADE,
    BooleanField,
    CharField,
    OneToOneField,
    FloatField,
)


class Image(Model):
    name = CharField(max_length=300, verbose_name="path")
    request = ForeignKey("processing.Request", on_delete=CASCADE, related_name="images")


class Request(Model):
    user = ForeignKey("authentication.User", on_delete=CASCADE)
    is_cancelled = BooleanField("Cancelled")


class Response(Model):
    request = OneToOneField(Request, on_delete=CASCADE, related_name="response")
    image = OneToOneField(Image, on_delete=CASCADE, related_name="response")
    image_probability = FloatField()
    dirt_probability = FloatField()
    chip_probability = FloatField()
