from django.db import models
from ruptur.libs.virtual_delete import VirtualDelete
from ruptur.libs.datation import Datation
from ruptur.libs.poi import POI
from django.contrib.gis.geos import Point
from typing import Optional
from .users import User

__all__ = [
    'Contributor',
    'Sector',
    'Position',
    'Skill'
]


class Contributor(VirtualDelete, Datation):
    CLASS_ICON = 'user'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(
        'geography.City',
        on_delete=models.PROTECT
    )
    sector = models.ForeignKey(
        'users.Sector',
        on_delete=models.PROTECT
    )
    phonenumber = models.CharField(max_length=10, blank=True, null=True)
    company = models.CharField(max_length=120)
    position = models.ForeignKey(
        'users.Position',
        on_delete=models.PROTECT
    )
    skill = models.ForeignKey(
        'users.Skill',
        on_delete=models.PROTECT
    )
    professional_profile = models.CharField(
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

    def get_tags(self):
        return [str(self.skill)]

    def get_title(self):
        return " ".join([self.user.first_name, self.user.last_name])

    def get_subtitle(self):
        return str(self.sector)

    def get_latitude(self):
        return self.city.latitude

    def get_longitude(self):
        return self.city.longitude

    def get_icon(self):
        return self.CLASS_ICON

    def get_url(self):
        return ''

    def get_location(self) -> Optional[Point]:
        if self.latitude and self.longitude:
            return Point(self.longitude, self.latitude)


POI.register(Contributor)


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
