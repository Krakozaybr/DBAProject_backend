from rest_framework.generics import (
    CreateAPIView,
    RetrieveDestroyAPIView,
    ListAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

from .models import ProcessedImage
from .serializers import ProcessedImageSerializer, ImageUploadSerializer


class AddDataAPI(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProcessedImageSerializer
    queryset = ProcessedImage.objects.all()


class StorageAPI(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, DjangoObjectPermissions)
    serializer_class = ProcessedImageSerializer
    lookup_url_kwarg = "pk"
    queryset = ProcessedImage.objects.all()


class UserStorageAPI(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProcessedImageSerializer
    queryset = ProcessedImage.objects.all()

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).filter(user__pk=self.request.user.pk)


class ImageUploadAPI(UpdateAPIView):
    permission_classes = (IsAuthenticated, DjangoObjectPermissions)
    serializer_class = ImageUploadSerializer
    lookup_url_kwarg = "pk"
    queryset = ProcessedImage.objects.all()
