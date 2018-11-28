from django.views.generic import TemplateView

__all__ = [
    'MapView'
]


class MapView(TemplateView):
    template_name = 'map/map.html'
