from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic

from tracker.models import Hike, Route

def index(request):
    num_hikes = Hike.objects.all().count()
    num_hikers = Hike.objects.all().count()

    context = {
        "num_hikes": num_hikes,
        "num_hikers": num_hikers,
    }

    return render(
        request,
        "tracker/index.html",
        context
    )

class ProfileView(LoginRequiredMixin, generic.ListView):
    model = Hike
    template_name = "tracker/profile.html"
