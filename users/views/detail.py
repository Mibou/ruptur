from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView

from ..forms import ContributorForm
from ..models import Contributor, User

import base64
import hashlib

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

    @staticmethod
    def _email_to_username(email):
        # Emails should be case-insensitive unique
        email = email.lower()
        # Deal with internationalized email addresses
        converted = email.encode('utf8', 'ignore')
        return base64.urlsafe_b64encode(
            hashlib.sha256(converted).digest()
        )[:30]

    @staticmethod
    def update_contributor(request):
        contributor = request.user.contributor

        for fkattr in [
            'city',
            'position',
            'sector',
            'skill'
        ]:
            if request.POST.get(fkattr):
                setattr(contributor, fkattr + '_id', request.POST.get(fkattr))

        for attr in [
            'phonenumber',
            'description',
            'professional_profile'
        ]:
            if request.POST.get(attr):
                setattr(contributor, attr, request.POST.get(attr))

        contributor.save()

    @staticmethod
    def update_user(request):
        user = request.user

        for attr in [
            'first_name',
            'last_name'
        ]:
            if request.POST.get(attr):
                setattr(user, attr, request.POST.get(attr))

        user.save()

    @staticmethod
    def login(request):
        username = User.objects.get(email=request.POST['email']).username
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

    @classmethod
    def create_user_contributor(cls, request):
        user = User.objects.create_user(
            cls._email_to_username(request.POST.get('email')),
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
                self.update_user(request)
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
