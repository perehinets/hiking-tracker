import datetime

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
    return render(request,"tracker/index.html")


class ProfileView(LoginRequiredMixin, generic.ListView):
    model = Hike
    paginate_by = 6
    template_name = "tracker/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_hikes = Hike.objects.filter(hikers=self.request.user)
        context["user_hikes"] = user_hikes
        context["all_hikes"] = user_hikes.count()
        context["all_distances"] = (
                user_hikes.aggregate(total=Sum("route__distance"))["total"] or 0
        )
        context["all_elevations"] = (
                user_hikes.aggregate(total=Sum("route__elevation"))["total"] or 0
        )
        return context


class HikeListView(LoginRequiredMixin, generic.ListView):
    model = Hike
    paginate_by = 6
    all_hikes = Hike.objects.all().count()
    all_distances = Hike.objects.aggregate(
        total=Sum("route__distance")
    )["total"] or 0

    all_elevations = Hike.objects.aggregate(
        total=Sum("route__elevation")
    )["total"] or 0
    extra_context = {
        "today": datetime.date.today(),
        "all_hikes": all_hikes,
        "all_distances": all_distances,
        "all_elevations": all_elevations,
    }


class HikeCreationView(LoginRequiredMixin, generic.CreateView):
    model = Hike
    form_class = HikeCreationForm
    success_url = reverse_lazy("tracker:profile")


class RouteCreationView(LoginRequiredMixin, generic.CreateView):
    model = Route
    form_class = RouteCreationForm
    success_url = reverse_lazy("tracker:profile")
