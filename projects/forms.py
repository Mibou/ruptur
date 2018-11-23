from django.forms import ModelForm
from .models import (
    Project
)
from django import forms
from dal import autocomplete
from django.forms import inlineformset_factory


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'nature', 'tags', 'skills']
