import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class Hiker(AbstractUser):
    gender = models.CharField(choices=((1, "male"), (0, "female")))
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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
        return self.name


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

    def __str__(self):
        return self.name

    @property
    def leader(self):
        through_model = self.hikers.through
        first_hiker = through_model.objects.filter(
            hike_id=self.id
        ).order_by("id").first()
        return first_hiker.hiker if first_hiker else None
