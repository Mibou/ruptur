from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView

from ..forms import ContributorForm
from ..models import Contributor, User

import base64
import hashlib
import os

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

__all__ = [
    'ContributorUpdate',
    'UserDetailView'
]


class ContributorUpdate(UpdateView):
    form_class = ContributorForm
    queryset = Contributor.objects
    success_url = reverse_lazy('contributor-form')
    template_name = 'users/contributor_form.html'

    def get_object(self, queryset=None):
        if hasattr(self.request.user, 'contributor'):
            return self.request.user.contributor
        else:
            return None

    def _email_to_username(self, email):
        # Emails should be case-insensitive unique
        email = email.lower()
        # Deal with internationalized email addresses
        converted = email.encode('utf8', 'ignore')
        return base64.urlsafe_b64encode(
            hashlib.sha256(converted).digest()
        )[:30]

    def update_contributor(self, request):
        contributor = request.user.contributor
        contributor.city_id = request.POST.get('city')
        contributor.phonenumber = request.POST.get('phonenumber')
        contributor.professional_profile = request.POST.get(
            'professional_profile'
        )
        contributor.position_id = request.POST.get('position')
        contributor.description = request.POST.get('description')
        contributor.sector_id = request.POST.get('sector')
        contributor.skill_id = request.POST.get('skill')

    def login(self, request):
        username = User.objects.get(email=request.POST['email']).username
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

    def create_user_contributor(self, request):
        user = User.objects.create_user(
            self._email_to_username(request.POST.get('email')),
            request.POST.get('email'),
            request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name')
        )
        Contributor.objects.create(
            user=user,
            city_id=request.POST.get('city'),
            phonenumber=request.POST.get('phonenumber'),
            professional_profile=request.POST.get('professional_profile'),
            position_id=request.POST.get('position'),
            description=request.POST.get('description'),
            sector_id=request.POST.get('sector'),
            skill_id=request.POST.get('skill')
        )
        login(request, user)

    def post(self, request, **kwargs):
        if request.user.id:
            if hasattr(request.user, 'contributor'):
                self.update_contributor(request)
        else:
            try:
                self.login(request)
            except User.DoesNotExist:
                self.create_user_contributor(request)

        return HttpResponseRedirect(self.success_url)


class UserDetailView(DetailView):

    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
