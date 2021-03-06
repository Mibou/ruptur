from django.contrib import admin
from .models import (
    Nature,
    Maturity,
    Project,
    Invitation,
    ProjectContributor
)
from .forms import ProjectForm


@admin.register(Nature)
class NatureAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name']


@admin.register(Maturity)
class MaturityAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', )
    search_fields = ['name', 'level']


class ProjectContributorInline(admin.TabularInline):
    model = ProjectContributor
    extra = 2


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    list_display = ('title', 'creator')
    search_fields = ['title', 'creator']
    inlines = (ProjectContributorInline,)


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('project', 'contributor', )
    search_fields = ['project', 'contributor']
