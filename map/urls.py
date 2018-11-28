from django.urls import path
from django.conf.urls import url, include
from tastypie.api import Api
from .views import MapView
from .api import POIResource


v1_api = Api(api_name='v1')
v1_api.register(POIResource())

urlpatterns = [
    url('api/', include(v1_api.urls)),
    path('', MapView.as_view(), name='map'),
]
