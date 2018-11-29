from django.urls import path
from django.conf.urls import url, include
from tastypie.api import Api
from .views import contribute, ProjectUpdate, ProjectDetailView
from .api import ProjectResource
from .autocomplete import TagAutocomplete

v1_api = Api(api_name='v1')
v1_api.register(ProjectResource())


urlpatterns = [
    url(
        r'^tag-autocomplete/$',
        TagAutocomplete.as_view(),
        name='tag-autocomplete',
    ),

    url('api/', include(v1_api.urls)),
    path('contribute', contribute, name='contribute'),
    path('project/new', ProjectUpdate.as_view(), name='project-form'),
    path(
        'project/<int:pk>/edit',
        ProjectUpdate.as_view(),
        name='project-form'
    ),
    path(
        'project/<int:pk>',
        ProjectDetailView.as_view(),
        name='project-detail'
    ),
]
