from django.contrib.auth import get_user_model
from django.test import TestCase

from tracker.models import Route, Hike, Difficulty


class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.difficulty = Difficulty.objects.create(name="test")
        cls.route = Route.objects.create(
            name="test",
            location="test",
            difficulty=cls.difficulty
        )
        cls.hiker1 = get_user_model().objects.create(
            username="test1",
            first_name="Test1",
            last_name="Test2",
            gender="1"
        )
        cls.hiker2 = get_user_model().objects.create(
            username="test2",
            first_name="Test3",
            last_name="Test4",
            gender="0"
        )
        cls.hike = Hike.objects.create(
            name="test",
            route=cls.route,
        )
        cls.hike.hikers.set([cls.hiker2, cls.hiker1])

    def test_difficulty_str(self):
        self.assertEqual(str(self.difficulty), "test")

    def test_route_str(self):
        route = Route.objects.create(
            name="test",
            location="test",
            difficulty=self.difficulty
        )
        self.assertEqual(str(route), "test")

    def test_hike_str(self):
        self.assertEqual(str(self.hike), "test")

    def test_hiker_str(self):
        self.assertEqual(str(self.hiker1), "Test1 Test2")

    def test_hiker_leader(self):
        self.assertEqual(str(self.hiker2), "Test3 Test4")
