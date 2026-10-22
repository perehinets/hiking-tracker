from django.urls import path

from tracker.views import index, ProfileView, HikeCreationView, RouteCreationView, HikeListView, HikeUpdateView, \
    HikeDeleteView, hike_join_view, hike_remove_view, HikeDetailView

urlpatterns = [
    path("", index, name="index"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/hike/add/", HikeCreationView.as_view(), name="add-hike"),
    path("profile/route/add/", RouteCreationView.as_view(), name="add-route"),
    path("hikes/", HikeListView.as_view(), name="hikes-list"),
    path("hike/<int:pk>/", HikeDetailView.as_view(), name="hike-detail"),
    path("hike/<int:pk>/update/", HikeUpdateView.as_view(), name="hike-update"),
    path("hike/<int:pk>/delete/", HikeDeleteView.as_view(), name="hike-delete"),
    path(
        "hike/<int:pk>/join/",
        hike_join_view,
        name="hike-join-hiker"
    ),
    path(
        "hike/<int:pk>/remove/",
        hike_remove_view,
        name="hike-remove-hiker"
    ),
]

app_name = "tracker"
