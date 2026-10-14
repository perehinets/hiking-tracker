from django import forms

from tracker.models import Hike, Route, Difficulty


class HikeCreationForm(forms.ModelForm):
    class Meta:
        model = Hike
        fields = [
            "name",
            "description",
            "max_hikers",
            "route",
        ]


class RouteCreationForm(forms.ModelForm):
    difficulty = forms.ModelChoiceField(
        queryset=Difficulty.objects.all()
    )

    class Meta:
        model = Route
        fields = "__all__"
