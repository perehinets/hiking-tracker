from django.urls import path

from tracker.views import index, ProfileView, HikeCreationView, RouteCreationView

urlpatterns = [
    path("", index, name="index"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/hike/add/", HikeCreationView.as_view(), name="add-hike"),
    path("profile/route/add/", RouteCreationView.as_view(), name="add-route"),
]


app_name = "tracker"