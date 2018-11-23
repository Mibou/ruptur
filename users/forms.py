
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import (
    Contributor,
    User
)
from django import forms
from dal import autocomplete


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class ContributorForm(ModelForm):
    class Meta:
        model = Contributor
        fields = ('city', 'sector', 'position', 'skill')

        widgets = {
            'city': autocomplete.ModelSelect2(
                url='city-autocomplete',
            ),
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'

        widgets = {
            'city': autocomplete.ModelSelect2(
                url='city-autocomplete',
            ),
        }
