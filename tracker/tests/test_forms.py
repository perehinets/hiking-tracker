import datetime

from django.test import TestCase

from tracker.forms import (
    HikeCreationForm,
    HikeSearchForm,
    RouteCreationForm,
    HikerCreationForm
)
from tracker.models import Difficulty, Route, Hike, Hiker


class FormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.difficulty = Difficulty.objects.create(
            name="test",
            level=1,
        )
        cls.route = Route.objects.create(
            name="test",
            location="test",
            difficulty=cls.difficulty
        )

        cls.hike = Hike.objects.create(
            name="test",
            route=cls.route,
            date=datetime.date(2028, 1, 1),
            description="test",
            max_hikers=10

        )

        cls.hiker = Hiker.objects.create(
            username="test",
            email="test@test",
            first_name="test",
            last_name="test",
            gender="1",
            birth_date=datetime.date(1970, 1, 1),

        )

    def test_hiker_creation_form_is_valid(self):
        form_data = {
            "username": "test1",
            "email": "test1@test.com",
            "first_name": "test1",
            "last_name": "test1",
            "gender": "1",
            "birth_date": datetime.date(1970, 1, 1),
        }
        form = HikerCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors.as_json())
        self.assertEqual(form.cleaned_data, form_data)

    def test_hike_creation_form_is_valid(self):
        form_data = {
            "name": "test",
            "route": self.route,
            "date": datetime.date(2028, 1, 1),
            "description": "test",
            "max_hikers": 10,
            "hikers": [self.hiker],
        }
        form = HikeCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_hike_search_form_is_valid(self):
        form_data = {
            "hike": "test",
        }
        form = HikeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_route_creation_form_is_valid(self):
        form_data = {
            "name": "test",
            "location": "test",
            "difficulty": self.difficulty,
            "distance": 15.4,
            "elevation": 1800,
        }
        form = RouteCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
