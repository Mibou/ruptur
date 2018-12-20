from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IdeasConfig(AppConfig):
    name = 'ideas'
    verbose_name = _('idées')
