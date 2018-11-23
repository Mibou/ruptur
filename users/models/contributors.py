from django.db import models
from ruptur.libs.virtual_delete import VirtualDelete
from ruptur.libs.datation import Datation
from .users import User

__all__ = [
    'Contributor',
    'Sector',
    'Position',
    'Skill'
]


class Contributor(VirtualDelete, Datation):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(
        'geography.City',
        on_delete=models.PROTECT
    )
    sector = models.ForeignKey(
        'users.Sector',
        on_delete=models.PROTECT
    )
    company = models.CharField(max_length=120)
    position = models.ForeignKey(
        'users.Position',
        on_delete=models.PROTECT
    )
    skill = models.ForeignKey(
        'users.Skill',
        on_delete=models.PROTECT
    )
    professional_profil = models.CharField(
        max_length=120,
        help_text='Copie/colle ici l\'URL de ton profil LinkedIn, Viadéo, ...'
    )
    description = models.TextField(
        help_text='Ce que verront les autres membres en 1er sur ton profil'
    )

    def __str__(self):
        return "%s %s (%s)" % (
            self.user.first_name,
            self.user.last_name,
            self.city
        )


class Sector(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
