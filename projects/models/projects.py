from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.geos import Point
from ruptur.libs.virtual_delete import VirtualDelete
from ruptur.libs.datation import Datation
from ruptur.libs.searchable import Searchable
from ruptur.libs.poi import POI
from typing import Optional
from tagging.fields import TagField


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


class Project(VirtualDelete, Datation, Searchable):
    CLASS_ICON = 'rocket'

    title = models.CharField(
        max_length=250,
        verbose_name=_('Titre du projet')
    )
    description = models.TextField(
        verbose_name=_('Description du projet')
    )
    nature = models.ForeignKey(
        'projects.Nature',
        on_delete=models.PROTECT,
        verbose_name=_('Nature du chantier')
    )
    tags = TagField()
    skills = models.ManyToManyField(
        'users.Skill',
        verbose_name=_('Compétences recherchées')
    )
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

    @classmethod
    def search(cls, match):
        return cls.objects.filter(
            Q(title__icontains=match) | Q(description__icontains=match)
        )

    def get_tags(self):
        return [str(tag) for tag in self.tags.split(',')]

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

    class Meta:
        verbose_name = _('projet')


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
        return _("%s contribue au projet %s (en tant que %s)") % (
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
