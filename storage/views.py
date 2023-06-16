from rest_framework.generics import (
    CreateAPIView,
    RetrieveDestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    GenericAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .models import ProcessedImage
from .serializers import (
    ProcessedImageSerializer,
    ImageUploadSerializer,
    SelectSerializer,
    NameSerializer,
)


class UserQuerysetMixin(GenericAPIView):
    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).filter(user__pk=self.request.user.pk)


class AddDataAPI(CreateAPIView, UserQuerysetMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProcessedImageSerializer
    queryset = ProcessedImage.objects.all()


class StorageAPI(RetrieveDestroyAPIView, UserQuerysetMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProcessedImageSerializer
    lookup_url_kwarg = "pk"
    queryset = ProcessedImage.objects.all()


class UserStorageAPI(ListAPIView, UserQuerysetMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProcessedImageSerializer
    queryset = ProcessedImage.objects.all()


class ImageUploadAPI(UpdateAPIView, UserQuerysetMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageUploadSerializer
    lookup_url_kwarg = "pk"
    queryset = ProcessedImage.objects.all()


class SelectAPI(UpdateAPIView, UserQuerysetMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = SelectSerializer
    lookup_url_kwarg = "pk"
    queryset = ProcessedImage.objects.all()


class NameAPI(UpdateAPIView, UserQuerysetMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = NameSerializer
    lookup_url_kwarg = "pk"
    queryset = ProcessedImage.objects.all()
