from django.urls import path
from lean_canvas.views import (
    LeanCanvasListView,
    LeanCanvasDetailView,
    LeanCanvasCreateView,
    LeanCanvasUpdateView,
    LeanCanvasDeleteView,
)
from lean_canvas.views import (
    ChannelListView,
    ChannelDetailView,
    ChannelCreateView,
    ChannelUpdateView,
    ChannelDeleteView,
)


urlpatterns = [
    path("", LeanCanvasListView.as_view(), name="canvas_list"),
    path("<int:pk>/", LeanCanvasDetailView.as_view(), name="canvas_detail"),
    path("new/", LeanCanvasCreateView.as_view(), name="canvas_new"),
    path("<int:pk>/edit/", LeanCanvasUpdateView.as_view(), name="canvas_edit"),
    path(
        "<int:pk>/delete/",
        LeanCanvasDeleteView.as_view(),
        name="canvas_delete",
    ),
    # channels
    path(
        "<int:lean_canvas_id>/channels/",
        ChannelListView.as_view(),
        name="channel_list",
    ),
    path("channels/<int:id>/", ChannelDetailView.as_view(), name="channel_detail"),
    path(
        "<int:lean_canvas_id>/channels/new/",
        ChannelCreateView.as_view(),
        name="channel_create",
    ),
    path("channels/<int:id>/edit/", ChannelUpdateView.as_view(), name="channel_update"),
    path(
        "channels/<int:id>/delete/", ChannelDeleteView.as_view(), name="channel_delete"
    ),
]
