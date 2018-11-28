from django.urls import path
from django.conf.urls import url, include
from tastypie.api import Api
from .views import contribute, ProjectDetails
from .api import ProjectResource

v1_api = Api(api_name='v1')
v1_api.register(ProjectResource())


urlpatterns = [
    url('api/', include(v1_api.urls)),
    path('contribute', contribute, name='contribute'),
    path('details', ProjectDetails.as_view(), name='project-form'),
]
