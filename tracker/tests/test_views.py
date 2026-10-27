from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tracker.models import Hike, Hiker, Difficulty, Route

ALL_HIKES_URL = reverse("tracker:hikes-list")

class PublicTest(TestCase):
    def test_login_required(self):
        res = self.client.get(ALL_HIKES_URL)
        self.assertNotEqual(res.status_code, 200)



class PrivateTest(TestCase):
    def setUp(self):
        self.difficulty = Difficulty.objects.create(name="test", level=1)
        self.route = Route.objects.create(name="test", difficulty=self.difficulty)
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="1232test",
            gender="1",
        )
        self.client.force_login(self.user)



    def test_retrieve_hikes(self):
        Hike.objects.create(name="test1", route=self.route, date=date.today())
        Hike.objects.create(name="test2", route=self.route, date=date.today())
        response = self.client.get(ALL_HIKES_URL)
        self.assertEqual(response.status_code, 200)
        hikes = Hike.objects.all()
        self.assertEqual(len(hikes), 2)
        self.assertEqual(hikes[0].name, "test1")
        self.assertEqual(
            list(response.context["object_list"]),
            list(hikes)
        )
        self.assertTemplateUsed(response, "tracker/hike_list.html")