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
    template_name = "tracker/profile.html"


class HikeListView(LoginRequiredMixin, generic.ListView):
    model = Hike
    paginate_by = 6
    extra_context = {
        "today": datetime.date.today()
    }


class HikeCreationView(LoginRequiredMixin, generic.CreateView):
    model = Hike
    form_class = HikeCreationForm
    success_url = reverse_lazy("tracker:profile")


class RouteCreationView(LoginRequiredMixin, generic.CreateView):
    model = Route
    form_class = RouteCreationForm
    success_url = reverse_lazy("tracker:profile")
