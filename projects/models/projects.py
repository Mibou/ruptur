from django.db import models

__all__ = [
    'Nature',
    'Project',
    'Tag',
    'Invitation'
]


class Nature(models.Model):
    name = models.CharField(max_length=100)
    contributor = models.ForeignKey('projects.Contributor')


class Tag(models.Model):
    name = models.CharField(max_length=100)
    contributor = models.ForeignKey('projects.Contributor')


class Project(models.Model):
    title = models.CharField()
    description = models.TextField()
    nature = models.ForeignKey('projects.Nature')
    tags = models.ManyToManyField('projects.Tag')
    skills = models.ManyToManyField('projects.Skill')


class Invitation(models.Model):
    project = models.ForeignKey('projects.Project')
