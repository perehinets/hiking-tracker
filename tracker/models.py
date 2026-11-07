import datetime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction


class Hiker(AbstractUser):
    gender = models.CharField(
        choices=(("1", "male"), ("0", "female")),
        default=None,
        null=True,
        blank=True,
    )
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
    max_hikers = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    hikers = models.ManyToManyField(Hiker, related_name='hikes')
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name='hikes',
    )
    owner = models.ForeignKey(
        Hiker,
        on_delete=models.CASCADE,
        related_name='owned_hikes',
        blank=True,
        null=True,
    )

    def add_hiker(self, hiker):
        with transaction.atomic():
            hike = Hike.objects.select_for_update().get(pk=self.pk)
            if hike.hikers.filter(pk=hiker.pk).exists():
                return
            if hike.hikers.count() >= hike.max_hikers:
                raise ValidationError(
                    "This hike has reached its maximum capacity."
                )
            hike.hikers.add(hiker)

    def remove_hiker(self, hiker):
        self.hikers.remove(hiker)

    def __str__(self):
        return self.name
