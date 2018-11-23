from django.urls import reverse_lazy
from django.views import generic
from ..forms import ContributorForm
from ..models import Contributor

__all__ = [
    'ContributorDetails'
]


class ContributorDetails(generic.UpdateView):
    form_class = ContributorForm
    queryset = Contributor.objects
    success_url = reverse_lazy('contributor-details')
    template_name = 'contributors/details.html'

    def get_object(self, queryset=None):
            return self.request.user.contributor
