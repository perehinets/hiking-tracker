from django.shortcuts import render

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
        "index.html",
        context
    )
