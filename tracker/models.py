from django.contrib.auth.models import AbstractUser
from django.db import models


class Hiker(AbstractUser):
    gender = models.CharField(choices=((1, "male"), (0, "female")))
    birth_date = models.DateField(blank=True, null=True)


class Difficulty(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField(default=0)


class Route(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    difficulty = models.ForeignKey(
        Difficulty,
        on_delete=models.CASCADE,
        related_name='routes',
    )


class Hike(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    distance = models.FloatField(default=0.0)
    elevation = models.IntegerField(default=0)
    max_hikers = models.IntegerField(default=0)
    hikers = models.ManyToManyField(Hiker)
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name='hikes',
    )
