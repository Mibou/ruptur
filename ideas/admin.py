from django.contrib import admin
from .models import (
    Idea,
    Vote,
    Contribution
)


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ['title']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('idea', 'user', 'up')
    search_fields = ['idea', 'user']


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('idea', 'user', 'text')
    search_fields = ['idea', 'user']
