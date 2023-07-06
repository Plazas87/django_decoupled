"""URLs module."""
from django.urls import path

from .views import (
    FileUploadView,
    WorkspaceCreateView,
    WorkspaceDetailView,
    WorkspaceListView,
    WorkspaceTrainView,
)

app_name = "workspaces"
urlpatterns = [
    path("", WorkspaceListView.as_view(), name="list"),
    path("create/", WorkspaceCreateView.as_view(), name="create"),
    path("train/<uuid:pk>/", WorkspaceTrainView.as_view(), name="train"),
    path("detail/<uuid:pk>/", WorkspaceDetailView.as_view(), name="detail"),
    path("upload_file/", FileUploadView.as_view(), name="file-upload"),
]
