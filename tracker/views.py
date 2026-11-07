import datetime

from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST

from tracker.forms import (
    HikeCreationForm,
    RouteCreationForm,
    HikeSearchForm,
    HikerCreationForm
)

from tracker.models import Hike, Route, Hiker


def index(request):
    return render(request, "tracker/index.html")


@login_required
@require_POST
def hike_join_view(request, pk):
    hike = get_object_or_404(Hike, pk=pk)
    try:
        hike.add_hiker(request.user)
        messages.success(request, "You joined the hike.")
    except ValidationError as error:
        raise error.message[0]

    return redirect("tracker:hikes-list")


@login_required
@require_POST
def hike_remove_view(request, pk):
    hike = get_object_or_404(Hike, pk=pk)
    if hike.hikers.filter(pk=request.user.pk).exists():
        hike.remove_hiker(request.user)
        messages.success(request, "You have left the hike.")
    else:
        messages.warning(request, "You have not joined this hike.")

    return redirect("tracker:hikes-list")


class ProfileView(LoginRequiredMixin, generic.ListView):
    model = Hike
    template_name = "tracker/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_hikes = Hike.objects.filter(hikers=self.request.user)
        context["user_hikes"] = user_hikes
        context["all_hikes"] = user_hikes.count()
        context["all_distances"] = (
                user_hikes.aggregate(
                    total=Sum("route__distance"))["total"] or 0
        )
        context["all_elevations"] = (
                user_hikes.aggregate(
                    total=Sum("route__elevation"))["total"] or 0
        )
        return context


class HikeListView(LoginRequiredMixin, generic.ListView):
    model = Hike
    paginate_by = 6

    def get_queryset(self):
        queryset = Hike.objects.all()
        self.search_form = HikeSearchForm(self.request.GET or None)

        if self.search_form.is_valid():
            hike = self.search_form.cleaned_data["hike"]
            difficulty = self.search_form.cleaned_data["difficulty"]

            if hike:
                queryset = queryset.filter(name__icontains=hike)
            if difficulty:
                queryset = queryset.filter(route__difficulty=difficulty)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        totals = Hike.objects.aggregate(
            all_distances=Sum("route__distance"),
            all_elevations=Sum("route__elevation"),
        )

        context["today"] = datetime.date.today()
        context["all_hikes"] = Hike.objects.count()
        context["all_distances"] = totals["all_distances"] or 0
        context["all_elevations"] = totals["all_elevations"] or 0
        context["search_form"] = self.search_form
        return context


class HikeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Hike
    extra_context = {
        "today": datetime.date.today()
    }


class HikeCreationView(LoginRequiredMixin, generic.CreateView):
    model = Hike
    form_class = HikeCreationForm
    success_url = reverse_lazy("tracker:profile")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        self.object.hikers.add(self.request.user)
        return response


class HikeUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Hike
    form_class = HikeCreationForm
    success_url = reverse_lazy("tracker:profile")

    def test_func(self):
        return self.get_object().owner == self.request.user


class HikeDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = Hike
    success_url = reverse_lazy("tracker:profile")

    def test_func(self):
        return self.get_object().owner == self.request.user


class RouteCreationView(LoginRequiredMixin, generic.CreateView):
    model = Route
    form_class = RouteCreationForm
    success_url = reverse_lazy("tracker:profile")


class HikerCreationView(LoginRequiredMixin, generic.CreateView):
    model = Hiker
    form_class = HikerCreationForm
    success_url = reverse_lazy("tracker:profile")
