from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Idea


class IdeaCreate(CreateView):
    model = Idea
    fields = ['title', 'description']


class IdeaUpdate(UpdateView):
    model = Idea
    fields = ['title', 'description']
    template_name_suffix = '_update_form'


class IdeaDelete(DeleteView):
    model = Idea
    success_url = reverse_lazy('idea-list')
