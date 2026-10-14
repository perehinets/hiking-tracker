from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic
from tracker.forms import HikeCreationForm, RouteCreationForm

from tracker.models import Hike, Route, Hiker


@login_required
def index(request):
    num_hikes = Hike.objects.all().count()
    num_hikers = Hiker.objects.all().count()
    # sum_distance = Hike.objects.all().aggregate(Sum('distance'))
    # sum_elevation = Hike.objects.all().aggregate(Sum('elevation'))

    context = {
        "num_hikes": num_hikes,
        "num_hikers": num_hikers,
        # "sum_distance": sum_distance,
        # "sum_elevation": sum_elevation
    }

    return render(
        request,
        "tracker/index.html",
        context
    )

class ProfileView(LoginRequiredMixin, generic.ListView):
    model = Hike
    template_name = "tracker/profile.html"

class HikeCreationView(LoginRequiredMixin, generic.CreateView):
    model = Hike
    form_class = HikeCreationForm
    success_url = reverse_lazy("tracker:profile")

class RouteCreationView(LoginRequiredMixin, generic.CreateView):
    model = Route
    form_class = RouteCreationForm
    success_url = reverse_lazy("tracker:profile")
