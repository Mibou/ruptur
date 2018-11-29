from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from .forms import ProjectForm
from users.forms import ContributorForm
from users.views import ContributorUpdate
from .models import Project
from users.models import User
from django.http import HttpResponseRedirect
from django.views.generic import DetailView

__all__ = [
    'ProjectUpdate'
]


def contribute(request):
    return render(request, 'projects/contribute.html')


class ProjectUpdate(UpdateView):
    form_class = ProjectForm
    contrib_form_class = ContributorForm
    queryset = Project.objects
    template_name = 'projects/project_form.html'

    def get_object(self, queryset=None):
        try:
            return super(ProjectUpdate, self).get_object(queryset)
        except AttributeError:
            return None

    def get_success_url(self, **kwargs):
        if kwargs != None:
            return reverse_lazy('project-form', kwargs={'pk': kwargs['pk']})
        else:
            return reverse_lazy('project-form', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(initial=self.object)
        if 'contribform' not in context:
            city = None
            if (
                self.request.user.id and
                self.request.user.contributor and
                self.request.user.contributor.city
            ):
                city = self.request.user.contributor.city
            context['contribform'] = self.contrib_form_class(initial={
                'city': city
            })
        return context

    @staticmethod
    def update_project(project, request):
        for fkattr in [
            'nature'
        ]:
            if request.POST.get(fkattr):
                setattr(project, fkattr + '_id', request.POST.get(fkattr))

        for attr in [
            'title',
            'description',
        ]:
            if request.POST.get(attr):
                setattr(project, attr, request.POST.get(attr))

        for attr in [
            'tags'
        ]:
            if request.POST.getlist(attr):
                setattr(project, attr, ','.join(request.POST.getlist(attr)))

        project.save()

    def create_project(self, request):
        return Project.objects.create(
            creator=request.user.contributor,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            nature_id=request.POST.get('nature'),
            tags=','.join(request.POST.getlist('tags')),
        )

    def post(self, request, **kwargs):
        pk = None
        if request.user.id:
            if hasattr(request.user, 'contributor'):
                ContributorUpdate.update_contributor(request)
                ContributorUpdate.update_user(request)
        else:
            try:
                ContributorUpdate.login(request)
            except User.DoesNotExist:
                ContributorUpdate.create_user_contributor(request)

        if kwargs.get('pk'):
            pk = kwargs.get('pk')
            self.update_project(self.get_object(), self.request)
        else:
            project = self.create_project(self.request)
            pk = project.pk

        return HttpResponseRedirect(self.get_success_url(pk=pk))


class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
