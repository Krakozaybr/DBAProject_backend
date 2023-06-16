from django.urls import path

from .views import StorageAPI, AddDataAPI, UserStorageAPI, ImageUploadAPI, SelectAPI

app_name = "storage"
urlpatterns = [
    path("<int:pk>/", StorageAPI.as_view()),
    path("<int:pk>/upload/", ImageUploadAPI.as_view()),
    path("<int:pk>/select/", SelectAPI.as_view()),
    path("create/", AddDataAPI.as_view()),
    path("list/", UserStorageAPI.as_view()),
]
