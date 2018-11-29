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
