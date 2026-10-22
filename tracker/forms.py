from django import forms

from tracker.models import Hike, Route, Difficulty


class HikeCreationForm(forms.ModelForm):
    class Meta:
        model = Hike
        fields = [
            "name",
            "route",
            "date",
            "description",
            "max_hikers",
            "hikers"
        ]


class RouteCreationForm(forms.ModelForm):
    difficulty = forms.ModelChoiceField(
        queryset=Difficulty.objects.all()
    )

    class Meta:
        model = Route
        fields = "__all__"


class HikeSearchForm(forms.Form):
    hike = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search hikes...",}
        ),
    )