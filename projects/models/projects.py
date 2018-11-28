from django.db import models
from ruptur.libs.virtual_delete import VirtualDelete
from ruptur.libs.datation import Datation
from ruptur.libs.poi import POI
from django.contrib.gis.geos import Point
from typing import Optional


__all__ = [
    'Nature',
    'Project',
    'Tag',
    'Invitation'
]


class Nature(models.Model):
    name = models.CharField(max_length=100)
    contributor = models.ForeignKey(
        'users.Contributor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    contributor = models.ForeignKey(
        'users.Contributor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Project(VirtualDelete, Datation):
    CLASS_ICON = 'rocket'

    title = models.CharField(max_length=250)
    description = models.TextField()
    nature = models.ForeignKey(
        'projects.Nature',
        on_delete=models.PROTECT
    )
    tags = models.ManyToManyField('projects.Tag')
    skills = models.ManyToManyField('users.Skill')
    creator = models.ForeignKey(
        'users.Contributor',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    def get_tags(self):
        return [str(tag) for tag in self.tags.all()]

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

    def get_url(self):
        return ''

    def get_location(self) -> Optional[Point]:
        if self.latitude and self.longitude:
            return Point(self.longitude, self.latitude)


POI.register(Project)


class Invitation(models.Model):
    contributor = models.ForeignKey(
        'users.Contributor',
        on_delete=models.CASCADE
    )

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s %s" % (self.contributor, self.project)
