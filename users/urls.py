from django.urls import path
from .views import SignUp, UserDetailView, ContributorUpdate
from django.views.generic import TemplateView

from django.conf.urls import url, include
from tastypie.api import Api
from .api import ContributorResource, UserResource


v1_api = Api(api_name='v1')
v1_api.register(ContributorResource())
v1_api.register(UserResource())

urlpatterns = [
    url('api/', include(v1_api.urls)),

    path('signup/', SignUp.as_view(), name='signup'),
    path(
        'login-signup/',
        TemplateView.as_view(template_name="registration/login_signup.html"),
        name='login-signup'
    ),
    path(
        'contributor/<int:pk>',
        UserDetailView.as_view(),
        name='contributor-details'
    ),
    path(
        'contributor/update',
        ContributorUpdate.as_view(),
        name='contributor-form'
    ),
]
