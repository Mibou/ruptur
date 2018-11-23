from django.db import models
from ruptur.libs.virtual_delete import VirtualDelete
from ruptur.libs.datation import Datation

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
