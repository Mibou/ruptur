from tastypie.resources import ModelResource
from geography.api import CityResource
from .models import Skill, User, Contributor
from tastypie import fields
from tastypie.exceptions import BadRequest


class SkillResource(ModelResource):
    class Meta:
        queryset = Skill.objects.all()
        resource_name = 'skills'
        allowed_methods = ['get']


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password']
        allowed_methods = ['get']
        filtering = {
            'email': ['exact'],
        }

    def build_filters(self, filters=None):
        if 'email__exact' not in filters:
            raise BadRequest("missing email param")
        return super(UserResource, self).build_filters(filters)


class ContributorResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)
    city = fields.ToOneField(CityResource, 'city', full=True)

    class Meta:
        queryset = Contributor.objects.all()
        resource_name = 'contributors'
        excludes = []
        allowed_methods = ['get']
