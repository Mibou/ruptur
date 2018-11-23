from django.db import models


class VirtualDelete(models.Model):
    ACTIVE = 'AV'
    NOT_ACTIVE = 'NA'
    DELETED = 'DL'
    STATUS_CHOICES = (
        (ACTIVE, 'Actif'),
        (NOT_ACTIVE, 'Inactif'),
        (DELETED, 'Supprimé'),
    )

    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=NOT_ACTIVE,
    )

    class Meta:
        abstract = True
