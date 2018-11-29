from django.db import models
from django.urls import reverse
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
        on_delete=models.CASCADE,
        related_name="projects"
    )
    contributors = models.ManyToManyField(
        'users.User',
        through='ProjectContributor',
        related_name='projects'
    )

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})

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

    def get_location(self) -> Optional[Point]:
        if self.latitude and self.longitude:
            return Point(self.get_longitude(), self.get_latitude())


POI.register(Project)


class ProjectContributor(models.Model):

    ACCEPTED = 'AX'
    REQUESTED = 'RQ'
    REFUSED = 'RF'
    STATUS_CHOICES = (
        (ACCEPTED, 'Accepté'),
        (REQUESTED, 'Demandé'),
        (REFUSED, 'Refusé'),
    )

    user = models.ForeignKey(
        'users.User',
        related_name='membership',
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        'projects.Project',
        related_name='membership',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=REQUESTED,
    )

    def __unicode__(self):
        return "%s is in group %s (as %s)" % (
            self.user,
            self.project,
            self.status
        )


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
