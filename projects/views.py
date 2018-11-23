from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import ProjectForm
from .models import Project

__all__ = [
    'ProjectDetails'
]


def map(request):
    return render(request, 'projects/map.html')


def contribute(request):
    return render(request, 'projects/contribute.html')


class ProjectDetails(generic.CreateView):
    form_class = ProjectForm
    queryset = Project.objects
    success_url = reverse_lazy('contributor-details')
    template_name = 'contributors/details.html'
