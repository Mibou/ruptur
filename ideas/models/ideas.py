from django.db import models
from django.urls import reverse
from ruptur.libs.virtual_delete import VirtualDelete
from ruptur.libs.datation import Datation
from django.contrib.gis.geos import Point
from typing import Optional


__all__ = [
    'Idea',
    'Vote',
    'Contribution'
]


class Idea(VirtualDelete, Datation):
    title = models.CharField(max_length=250)
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('idea-detail', kwargs={'pk': self.pk})

    def get_location(self) -> Optional[Point]:
        if self.latitude and self.longitude:
            return Point(self.longitude, self.latitude)


class Vote(models.Model):
    idea = models.ForeignKey(
        'ideas.Idea',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    up = models.BooleanField()


class Contribution(models.Model):
    idea = models.ForeignKey(
        'ideas.Idea',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    text = models.TextField()
