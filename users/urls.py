from django.urls import path
from .views import SignUp, ContributorDetails
from django.views.generic import TemplateView


urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path(
        'login-signup/',
        TemplateView.as_view(template_name="registration/login_signup.html"),
        name='login-signup'
    ),
    path(
        'contributor/details',
        ContributorDetails.as_view(),
        name='contributor-details'
    ),
]
