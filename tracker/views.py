import datetime

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
    if hike.hikers.filter(pk=request.user.pk).exists():
        messages.warning(request, "You have already joined this hike")
    elif hike.hikers.count() >= hike.max_hikers:
        messages.error(request, "This hike is full.")
    else:
        hike.hikers.add(request.user)
        messages.success(request, "You joined the hike.")
    return redirect("tracker:hikes-list")


@login_required
@require_POST
def hike_remove_view(request, pk):
    hike = get_object_or_404(Hike, pk=pk)
    if hike.hikers.filter(pk=request.user.pk).exists():
        hike.hikers.remove(request.user)
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HikeListView, self).get_context_data(**kwargs)
        hike = self.request.GET.get("hike", "")

        all_hikes = Hike.objects.all().count()
        all_distances = Hike.objects.aggregate(
            total=Sum("route__distance")
        )["total"] or 0

        all_elevations = Hike.objects.aggregate(
            total=Sum("route__elevation")
        )["total"] or 0
        context["today"] = datetime.date.today()
        context["all_hikes"] = all_hikes
        context["all_distances"] = all_distances
        context["all_elevations"] = all_elevations
        context["search_form"] = HikeSearchForm(
            initial={"hike": hike}
        )
        return context

    def get_queryset(self):
        queryset = Hike.objects.all()
        form = HikeSearchForm(self.request.GET)
        if form.is_valid():
            hike = form.cleaned_data["hike"]
            difficulty = self.request.GET.get("difficulty", "")

            if hike:
                queryset = queryset.filter(
                    name__icontains=form.cleaned_data["hike"]
                )

            if difficulty:
                queryset = queryset.filter(
                    route__difficulty=difficulty
                )

        return queryset


class HikeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Hike
    extra_context = {
        "today": datetime.date.today()
    }


class HikeCreationView(LoginRequiredMixin, generic.CreateView):
    model = Hike
    form_class = HikeCreationForm
    success_url = reverse_lazy("tracker:profile")


class HikeUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Hike
    fields = "__all__"
    success_url = reverse_lazy("tracker:profile")

    def test_func(self):
        return self.get_object().leader == self.request.user


class HikeDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = Hike
    success_url = reverse_lazy("tracker:profile")

    def test_func(self):
        return self.get_object().leader == self.request.user


class RouteCreationView(LoginRequiredMixin, generic.CreateView):
    model = Route
    form_class = RouteCreationForm
    success_url = reverse_lazy("tracker:profile")


class HikerCreationView(LoginRequiredMixin, generic.CreateView):
    model = Hiker
    form_class = HikerCreationForm
    success_url = reverse_lazy("tracker:profile")
