from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import ProjectForm
from .models import Project

from django.views.generic import DetailView

__all__ = [
    'ProjectDetails'
]


def contribute(request):
    return render(request, 'projects/contribute.html')


class ProjectDetails(generic.CreateView):
    form_class = ProjectForm
    queryset = Project.objects
    success_url = reverse_lazy('contributor-form')
    template_name = 'projects/details.html'


class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
