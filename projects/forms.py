from django.forms import ModelForm
from .models import (
    Project
)
from dal import autocomplete


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'nature',
            'maturity',
            'tags',
            'skills',
            'creator',
            'contributors'
        ]

        widgets = {
            'tags': autocomplete.TaggingSelect2(
                'tag-autocomplete'
            )
        }