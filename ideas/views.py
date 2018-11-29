from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic import (
    DetailView
)
from django.urls import reverse_lazy
from .models import Idea, Contribution

from .forms import IdeaForm

from users.models import User
from users.forms import ContributorForm
from users.views import ContributorUpdate
from django.http import HttpResponseRedirect


class IdeaCreate(CreateView):
    model = Idea
    fields = ['title', 'description']


class IdeaUpdate(UpdateView):
    form_class = IdeaForm
    contrib_form_class = ContributorForm
    queryset = Idea.objects
    template_name = 'ideas/idea_form.html'

    def get_object(self, queryset=None):
        try:
            return super(IdeaUpdate, self).get_object(queryset)
        except AttributeError:
            return None

    def get_success_url(self, **kwargs):
        if kwargs != None:
            return reverse_lazy('idea-form', kwargs={'pk': kwargs['pk']})
        else:
            return reverse_lazy('idea-form', args=(self.object.id,))

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
    def update_idea(idea, request):
        for attr in [
            'title',
            'description',
        ]:
            if request.POST.get(attr):
                setattr(idea, attr, request.POST.get(attr))

        idea.save()

    def create_idea(self, request):
        return Idea.objects.create(
            creator=request.user.contributor,
            title=request.POST.get('title'),
            description=request.POST.get('description')
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
            self.update_idea(self.get_object(), self.request)
        else:
            idea = self.create_idea(self.request)
            pk = idea.pk

        return HttpResponseRedirect(self.get_success_url(pk=pk))


class IdeaDelete(DeleteView):
    model = Idea
    success_url = reverse_lazy('idea-list')


class IdeaDetailView(DetailView):
    model = Idea

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, **kwargs):
        if request.POST.get('new_contribution', None):
            try:
                c = Contribution()
                c.text = request.POST['new_contribution']
                c.idea_id = kwargs['pk']
                c.user = request.user
                c.save()
            except Exception:
                pass
        return self.get(request, **kwargs)
