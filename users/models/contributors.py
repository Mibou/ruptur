from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.gis.geos import Point
from ruptur.libs.virtual_delete import VirtualDelete
from ruptur.libs.datation import Datation
from ruptur.libs.searchable import Searchable
from ruptur.libs.poi import POI
from typing import Optional
from .users import User

__all__ = [
    'Contributor',
    'Sector',
    'Position',
    'Skill'
]


class Contributor(VirtualDelete, Datation, Searchable):
    CLASS_ICON = 'user'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='contributor'
    )
    city = models.ForeignKey(
        'geography.City',
        on_delete=models.PROTECT,
        verbose_name=_('Code Postal')
    )
    sector = models.ForeignKey(
        'users.Sector',
        on_delete=models.PROTECT,
        verbose_name=_('Secteur'),
        blank=True,
        null=True
    )
    phonenumber = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name=_('Téléphone'),
    )
    company = models.CharField(
        max_length=120,
        verbose_name=_('Entreprise'),
        blank=True,
        null=True
    )
    position = models.ForeignKey(
        'users.Position',
        on_delete=models.PROTECT,
        verbose_name=_('Fonction'),
        blank=True,
        null=True
    )
    skill = models.ForeignKey(
        'users.Skill',
        on_delete=models.PROTECT,
        verbose_name=_('Une qualité'),
        blank=True,
        null=True
    )
    professional_profile = models.CharField(
        max_length=120,
        help_text=_('Copie/colle ici l\'URL de ton profil LinkedIn, Viadéo, ...'),
        verbose_name=_('Lien professionel'),
        blank=True,
        null=True
    )
    description = models.TextField(
        help_text=_('Ce que verront les autres membres en 1er sur ton profil'),
        verbose_name='',
        blank=True,
        null=True
    )

    def get_absolute_url(self):
        return reverse('contributor-details', kwargs={'pk': self.user.pk})

    def __str__(self):
        return "%s %s (%s)" % (
            self.user.first_name,
            self.user.last_name,
            self.city
        )

    @classmethod
    def search(cls, match):
        return cls.objects.filter(
            Q(user__first_name__icontains=match) |
            Q(user__last_name__icontains=match)
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

    def get_location(self) -> Optional[Point]:
        if self.get_latitude() and self.get_longitude():
            return Point(self.get_longitude(), self.get_latitude())

    class Meta:
        verbose_name = _('contributeur')


POI.register(Contributor)


class Sector(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('secteur')


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('poste')


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('competence')
