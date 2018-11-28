from tastypie.resources import ModelResource
from geography.api import CityResource
from .models import Skill, User, Contributor
from tastypie import fields


class SkillResource(ModelResource):
    class Meta:
        queryset = Skill.objects.all()
        resource_name = 'skills'
        allowed_methods = ['get']


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        excludes = ['password', 'email']
        allowed_methods = ['get']


class ContributorResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    city = fields.ToOneField(CityResource, 'city', full=True)

    class Meta:
        queryset = Contributor.objects.all()
        resource_name = 'contributors'
        excludes = []
        allowed_methods = ['get']
