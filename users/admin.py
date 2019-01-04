from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import (
    ContributorForm
)

from .models import (
    User,
    Contributor,
    Skill,
    Position,
    Sector
)

from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name']


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name']


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'city')
    search_fields = ['user']
    form = ContributorForm


class ContributorInline(admin.StackedInline):
    model = Contributor
    form = ContributorForm
    can_delete = False
    verbose_name_plural = 'contributors'


# Define a new User admin
class CustomUserAdmin(UserAdmin):

    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(CustomUserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = (ContributorInline, )
        return super(CustomUserAdmin, self).change_view(*args, **kwargs)

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username']


admin.site.register(User, CustomUserAdmin)
