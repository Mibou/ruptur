from django.urls import path
from .views import IdeaCreate, IdeaUpdate, IdeaDelete, IdeaDetailView

from django.conf.urls import url, include
from tastypie.api import Api
from .api import IdeaResource, VoteResource, ContributionResource


v1_api = Api(api_name='v1')
v1_api.register(VoteResource())
v1_api.register(ContributionResource())
v1_api.register(IdeaResource())

urlpatterns = [
    url('api/', include(v1_api.urls)),
    path('idea/add/', IdeaCreate.as_view(), name='idea-add'),
    path('idea/new', IdeaUpdate.as_view(), name='idea-form'),
    path('idea/<int:pk>/edit', IdeaUpdate.as_view(), name='idea-form'),
    path('idea/<int:pk>/', IdeaDetailView.as_view(), name='idea-detail'),
    path('idea/<int:pk>/delete/', IdeaDelete.as_view(), name='idea-delete')
]
