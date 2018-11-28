from django.urls import path
from .views import SignUp, UserDetailView, ContributorUpdate
from django.views.generic import TemplateView


urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path(
        'login-signup/',
        TemplateView.as_view(template_name="registration/login_signup.html"),
        name='login-signup'
    ),
    path(
        'contributor/details/<int:pk>',
        UserDetailView.as_view(),
        name='contributor-details'
    ),
    path(
        'contributor/update',
        ContributorUpdate.as_view(),
        name='contributor-form'
    ),
]
