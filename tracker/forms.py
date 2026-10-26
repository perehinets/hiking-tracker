from django import forms
from django.contrib.auth.forms import UserCreationForm

from tracker.models import Hike, Route, Difficulty, Hiker


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


class HikerCreationForm(UserCreationForm):
    password = None
    password2 = None
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "email@mail.com",
                "class": "form-control",
                "type": "email",
            }
        )
    )
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "placeholder": "YYYY-MM-DD",
            }
        )
    )
    class Meta:
        model = Hiker
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "gender",
        )