from tastypie.resources import ModelResource
from .models import Project, Tag
from users.api import ContributorResource, SkillResource
from tastypie import fields


class TagResource(ModelResource):

    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tags'
        excludes = []
        allowed_methods = ['get']


class ProjectResource(ModelResource):

    tags = fields.ToManyField(
        TagResource,
        'tags',
        related_name='project',
        full=True
    )
    skills = fields.ToManyField(
        SkillResource,
        'skills',
        related_name='project',
        full=True
    )
    creator = fields.ToOneField(ContributorResource, 'creator', full=True)

    class Meta:
        queryset = Project.objects.all()
        resource_name = 'projects'
        excludes = []
        allowed_methods = ['get']

    def dehydrate(self, bundle):
        bundle.data['type'] = 'rocket'
        return bundle
