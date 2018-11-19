from django.db import models

__all__ = [
    'Contributor',
    'Skill'
]


class Contributor(models.Model):
    firstname = models.CharField()
    lastname = models.CharField()
    city = models.ForeignKey()
    skills = models.ManyToManyField('projects.Skill')


class Skill(models.Model):
    name = models.CharField(max_length=100)
