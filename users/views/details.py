from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView

from ..forms import ContributorForm
from ..models import Contributor, User


__all__ = [
    'ContributorUpdate',
    'UserDetailView'
]


class ContributorUpdate(UpdateView):
    form_class = ContributorForm
    queryset = Contributor.objects
    success_url = reverse_lazy('contributor-details')
    template_name = 'contributors/details.html'

    def get_object(self, queryset=None):
            return self.request.user.contributor


class UserDetailView(DetailView):

    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
