from django import forms

from tracker.models import Hike, Route, Difficulty


class HikeCreationForm(forms.ModelForm):
    class Meta:
        model = Hike
        fields = [
            "name",
            "description",
            "distance",
            "elevation",
            "max_hikers",
            "route",
        ]


class RouteCreationForm(forms.ModelForm):
    difficulty = forms.ModelMultipleChoiceField(
        queryset=Difficulty.objects.all(),
        widget=forms.SelectMultiple,
        required=False,
    )

    class Meta:
        model = Route
        fields = "__all__"
