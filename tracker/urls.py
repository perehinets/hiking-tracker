from django.urls import path

from tracker.views import index, ProfileView, HikeCreationView, RouteCreationView, HikeListView

urlpatterns = [
    path("", index, name="index"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/hike/add/", HikeCreationView.as_view(), name="add-hike"),
    path("profile/route/add/", RouteCreationView.as_view(), name="add-route"),
    path("hikes/", HikeListView.as_view(), name="hikes-list"),
]


app_name = "tracker"