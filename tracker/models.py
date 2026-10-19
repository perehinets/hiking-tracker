import datetime
from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models


class Hiker(AbstractUser):
    gender = models.CharField(choices=((1, "male"), (0, "female")))
    birth_date = models.DateField(blank=True, null=True)


class Difficulty(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    distance = models.FloatField(default=0.0)
    elevation = models.IntegerField(default=0)
    difficulty = models.ForeignKey(
        Difficulty,
        on_delete=models.CASCADE,
        related_name='routes',
    )

    def __str__(self):
        return f"{self.name}, {self.location}, {self.distance}, {self.elevation}, {self.difficulty}"

class Hike(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(default=datetime.datetime.now)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    max_hikers = models.IntegerField(default=0)
    hikers = models.ManyToManyField(Hiker, related_name='hikes')
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name='hikes',
    )
