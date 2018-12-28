from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ruptur.libs.virtual_delete import VirtualDelete
from ruptur.libs.datation import Datation
from ruptur.libs.searchable import Searchable
from django.contrib.gis.geos import Point
from ruptur.libs.poi import POI
from typing import Optional


__all__ = [
    'Idea',
    'Vote',
    'Contribution'
]


class Idea(VirtualDelete, Datation, Searchable):
    CLASS_ICON = 'lightbulb'

    title = models.CharField(max_length=250)
    description = models.TextField()

    creator = models.ForeignKey(
        'users.Contributor',
        on_delete=models.CASCADE,
        related_name='ideas'
    )

    def __str__(self):
        return "%s (%s)" % (self.title, self.creator.user.get_full_name())

    @classmethod
    def search(cls, match):
        return cls.objects.filter(
            Q(title__icontains=match) | Q(description__icontains=match)
        )

    def get_absolute_url(self):
        return reverse('idea-detail', kwargs={'pk': self.pk})

    def get_tags(self):
        return []

    def get_title(self):
        return self.title

    def get_subtitle(self):
        return self.description

    def get_latitude(self):
        return self.creator.city.latitude

    def get_longitude(self):
        return self.creator.city.longitude

    def get_icon(self):
        return self.CLASS_ICON

    def get_location(self) -> Optional[Point]:
        if self.get_latitude() and self.get_longitude():
            return Point(self.get_longitude(), self.get_latitude())

    def get_votes_up(self):
        return self.votes.filter(up=True)

    def get_votes_down(self):
        return self.votes.filter(up=False)

    class Meta:
        verbose_name = _('idée')


POI.register(Idea)


class Vote(models.Model):
    idea = models.ForeignKey(
        'ideas.Idea',
        on_delete=models.CASCADE,
        related_name='votes'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    up = models.BooleanField()

    class Meta:
        unique_together = ('user', 'idea')

    def save(self, *args, **kwargs):

        if self.pk is None:
            Vote.objects.update_or_create(
                user=self.user,
                idea=self.idea,
                defaults={'up': self.up}
            )[0]
        else:
            super(Vote, self).save(*args, **kwargs)


class Contribution(Datation, models.Model):
    idea = models.ForeignKey(
        'ideas.Idea',
        on_delete=models.CASCADE,
        related_name='contributions'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    text = models.TextField()

    class Meta:
        unique_together = ('user', 'idea', 'text')
