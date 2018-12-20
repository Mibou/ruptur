from django.db import models
from ruptur.libs.virtual_delete import VirtualDelete
from ruptur.libs.datation import Datation
from django.utils.translation import gettext_lazy as _


__all__ = [
    'MemberCompany',
]


class MemberCompany(VirtualDelete, Datation):
    name = models.CharField(max_length=250)
    domain = models.CharField(max_length=250)

    def __str__(self):
        return "%s (%s)" % (self.name, self.domain)

    class Meta:
        verbose_name_plural = _('entreprises membres')
